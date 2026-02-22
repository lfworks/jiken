import gzip
import json
import urllib.error
import urllib.request
from email.message import Message
from unittest.mock import MagicMock, Mock, patch

import pytest
from parameterized import parameterized

from jiken.client import JikenClient
from jiken.exceptions import JikenAPIError, JikenAuthError, JikenRequestError
from jiken.models import SearchCondition


class TestJikenClient:
    """Tests for JikenClient."""

    def test_init(self) -> None:
        client = JikenClient(api_key="test-api-key")
        assert client._api_key == "test-api-key"

    def test_build_params_with_area_only(self) -> None:
        client = JikenClient(api_key="test-key")
        condition = SearchCondition(year=2024, area="13")

        params = client._build_params(condition)

        assert params["year"] == "2024"
        assert params["area"] == "13"
        assert params["language"] == "en"
        assert "city" not in params
        assert "quarter" not in params

    def test_build_params_with_all_fields(self) -> None:
        client = JikenClient(api_key="test-key")
        condition = SearchCondition(year=2024, area="13", city="13101", quarter=1, language="ja")

        params = client._build_params(condition)

        assert params["year"] == "2024"
        assert params["area"] == "13"
        assert params["city"] == "13101"
        assert params["quarter"] == "1"
        assert params["language"] == "ja"

    @patch("jiken.client.urlopen")
    def test_fetch_data_success(self, mock_urlopen: Mock) -> None:
        response_data = {"data": [{"TradePrice": "50000000"}]}
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(response_data).encode("utf-8")
        mock_response.headers.get.return_value = None
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        client = JikenClient(api_key="test-key")
        params = {"year": "2024", "area": "13"}

        result = client._fetch_data(params)

        assert result == response_data
        mock_urlopen.assert_called_once()

    @patch("jiken.client.urlopen")
    def test_fetch_data_with_gzip(self, mock_urlopen: Mock) -> None:
        response_data = {"data": [{"TradePrice": "50000000"}]}
        compressed_data = gzip.compress(json.dumps(response_data).encode("utf-8"))

        mock_response = MagicMock()
        mock_response.read.return_value = compressed_data
        mock_response.headers.get.return_value = "gzip"
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        client = JikenClient(api_key="test-key")
        params = {"year": "2024", "area": "13"}

        result = client._fetch_data(params)

        assert result == response_data

    @patch("jiken.client.urlopen")
    def test_fetch_data_auth_error(self, mock_urlopen: Mock) -> None:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com", code=401, msg="Unauthorized", hdrs=Message(), fp=None
        )

        client = JikenClient(api_key="invalid-key")
        params = {"year": "2024", "area": "13"}

        with pytest.raises(JikenAuthError) as exc_info:
            client._fetch_data(params)

        assert "Authentication failed" in str(exc_info.value)

    @patch("jiken.client.urlopen")
    def test_fetch_data_request_error(self, mock_urlopen: Mock) -> None:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com", code=400, msg="Bad Request", hdrs=Message(), fp=None
        )

        client = JikenClient(api_key="test-key")
        params = {"year": "invalid"}

        with pytest.raises(JikenRequestError) as exc_info:
            client._fetch_data(params)

        assert "Invalid request parameters" in str(exc_info.value)

    @parameterized.expand(
        [
            (500, "Internal Server Error"),
            (502, "Bad Gateway"),
            (503, "Service Unavailable"),
        ]
    )
    @patch("jiken.client.urlopen")
    def test_fetch_data_server_error(self, status_code: int, msg: str, mock_urlopen: Mock) -> None:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://test.com", code=status_code, msg=msg, hdrs=Message(), fp=None
        )

        client = JikenClient(api_key="test-key")
        params = {"year": "2024", "area": "13"}

        with pytest.raises(JikenAPIError) as exc_info:
            client._fetch_data(params)

        assert f"status {status_code}" in str(exc_info.value)

    @patch("jiken.client.urlopen")
    def test_fetch_data_url_error(self, mock_urlopen: Mock) -> None:
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        client = JikenClient(api_key="test-key")
        params = {"year": "2024", "area": "13"}

        with pytest.raises(JikenAPIError) as exc_info:
            client._fetch_data(params)

        assert "Failed to connect to API" in str(exc_info.value)

    @patch("jiken.client.urlopen")
    def test_fetch_data_invalid_json(self, mock_urlopen: Mock) -> None:
        mock_response = MagicMock()
        mock_response.read.return_value = b"invalid json"
        mock_response.headers.get.return_value = None
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        client = JikenClient(api_key="test-key")
        params = {"year": "2024", "area": "13"}

        with pytest.raises(JikenAPIError) as exc_info:
            client._fetch_data(params)

        assert "Failed to parse API response" in str(exc_info.value)

    def test_parse_transaction_item(self) -> None:
        client = JikenClient(api_key="test-key")

        item = {
            "TradePrice": "50000000",
            "Area": "100.5",
            "UnitPrice": "1500000",
            "Prefecture": "Tokyo",
            "Municipality": "Chiyoda-ku",
            "DistrictName": "Marunouchi",
            "BuildingYear": "2020",
            "Type": "Residential Land",
            "Structure": "RC",
            "FloorAreaRatio": "200",
            "CoverageRatio": "60",
            "Frontage": "6.0",
            "Period": "2024Q1",
        }

        transaction = client._parse_transaction_item(item)

        assert transaction.transaction_price == 50000000
        assert transaction.area == 100.5
        assert transaction.unit_price == 1500000.0
        assert transaction.prefecture == "Tokyo"
        assert transaction.city == "Chiyoda-ku"
        assert transaction.district == "Marunouchi"
        assert transaction.building_year == 2020
        assert transaction.property_type == "Residential Land"
        assert transaction.structure == "RC"
        assert transaction.floor_area_ratio == 200.0
        assert transaction.building_coverage == 60.0
        assert transaction.frontage_road_width == 6.0
        assert transaction.transaction_period == "2024Q1"

    def test_parse_transaction_item_with_none_values(self) -> None:
        client = JikenClient(api_key="test-key")

        item = {
            "TradePrice": "30000000",
            "Area": "80",
            "UnitPrice": None,
            "Prefecture": "Osaka",
            "Municipality": "Osaka-shi",
            "DistrictName": None,
            "BuildingYear": "",
            "Type": "Apartment",
            "Structure": None,
            "FloorAreaRatio": "",
            "CoverageRatio": None,
            "Frontage": "",
            "Period": "2024Q2",
        }

        transaction = client._parse_transaction_item(item)

        assert transaction.transaction_price == 30000000
        assert transaction.area == 80.0
        assert transaction.unit_price is None
        assert transaction.prefecture == "Osaka"
        assert transaction.city == "Osaka-shi"
        assert transaction.district is None
        assert transaction.building_year is None
        assert transaction.property_type == "Apartment"
        assert transaction.structure is None
        assert transaction.floor_area_ratio is None
        assert transaction.building_coverage is None
        assert transaction.frontage_road_width is None
        assert transaction.transaction_period == "2024Q2"

    def test_parse_transactions_empty_data(self) -> None:
        client = JikenClient(api_key="test-key")

        result = client._parse_transactions({})

        assert result == []

    def test_parse_transactions_with_data(self) -> None:
        client = JikenClient(api_key="test-key")

        data = {
            "data": [
                {
                    "TradePrice": "50000000",
                    "Area": "100",
                    "UnitPrice": None,
                    "Prefecture": "Tokyo",
                    "Municipality": "Shibuya-ku",
                    "DistrictName": None,
                    "BuildingYear": "2020",
                    "Type": "Residential Land",
                    "Structure": None,
                    "FloorAreaRatio": None,
                    "CoverageRatio": None,
                    "Frontage": None,
                    "Period": "2024Q1",
                },
                {
                    "TradePrice": "30000000",
                    "Area": "60",
                    "UnitPrice": None,
                    "Prefecture": "Osaka",
                    "Municipality": "Osaka-shi",
                    "DistrictName": None,
                    "BuildingYear": "2018",
                    "Type": "Apartment",
                    "Structure": "RC",
                    "FloorAreaRatio": "200",
                    "CoverageRatio": "60",
                    "Frontage": "5",
                    "Period": "2024Q1",
                },
            ]
        }

        transactions = client._parse_transactions(data)

        assert len(transactions) == 2
        assert transactions[0].transaction_price == 50000000
        assert transactions[1].transaction_price == 30000000

    @patch("jiken.client.urlopen")
    def test_search_transactions_integration(self, mock_urlopen: Mock) -> None:
        response_data = {
            "data": [
                {
                    "TradePrice": "50000000",
                    "Area": "100",
                    "UnitPrice": "1500000",
                    "Prefecture": "Tokyo",
                    "Municipality": "Shibuya-ku",
                    "DistrictName": "Test District",
                    "BuildingYear": "2020",
                    "Type": "Residential Land",
                    "Structure": "RC",
                    "FloorAreaRatio": "200",
                    "CoverageRatio": "60",
                    "Frontage": "6",
                    "Period": "2024Q1",
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(response_data).encode("utf-8")
        mock_response.headers.get.return_value = None
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        mock_urlopen.return_value = mock_response

        client = JikenClient(api_key="test-key")
        condition = SearchCondition(year=2024, area="13", quarter=1)

        transactions = client.search_transactions(condition)

        assert len(transactions) == 1
        assert transactions[0].transaction_price == 50000000
        assert transactions[0].prefecture == "Tokyo"
