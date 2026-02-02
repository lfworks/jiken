import gzip
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from jiken.exceptions import ReinfoLibAPIError, ReinfoLibAuthError, ReinfoLibRequestError
from jiken.models import SearchCondition, Transaction


class ReinfoLibClient:
    _API_BASE_URL = "https://www.reinfolib.mlit.go.jp/ex-api/external/XIT001"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def search_transactions(self, condition: SearchCondition) -> list[Transaction]:
        """Search real estate transactions based on conditions.

        Args:
            condition: Search condition specifying year, area, quarter, etc.

        Returns:
            List of transaction records
        """
        params = self._build_params(condition)
        response_data = self._fetch_data(params)
        return self._parse_transactions(response_data)

    def _build_params(self, condition: SearchCondition) -> dict[str, str]:
        """Build query parameters from search condition.

        Args:
            condition: Search condition

        Returns:
            Dictionary of query parameters
        """
        params: dict[str, str] = {"year": str(condition.year)}

        if condition.area is not None:
            params["area"] = condition.area

        if condition.city is not None:
            params["city"] = condition.city

        if condition.quarter is not None:
            params["quarter"] = str(condition.quarter)

        params["language"] = condition.language

        return params

    def _fetch_data(self, params: dict[str, str]) -> dict[str, Any]:
        """Fetch and decode gzip-compressed JSON from API.

        Args:
            params: Query parameters

        Returns:
            Parsed JSON response data

        Raises:
            ReinfoLibAuthError: Authentication failed (401)
            ReinfoLibRequestError: Invalid request parameters (400)
            ReinfoLibAPIError: API error occurred
        """
        url = f"{self._API_BASE_URL}?{urlencode(params)}"

        request = Request(url)
        request.add_header("Ocp-Apim-Subscription-Key", self._api_key)

        try:
            with urlopen(request) as response:
                data = response.read()

                if response.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)

                return json.loads(data.decode("utf-8"))

        except HTTPError as e:
            if e.code == 401:
                raise ReinfoLibAuthError("Authentication failed. Check your API key.") from e
            elif e.code == 400:
                raise ReinfoLibRequestError(f"Invalid request parameters: {e.reason}") from e
            else:
                raise ReinfoLibAPIError(f"API error occurred (status {e.code}): {e.reason}") from e
        except URLError as e:
            raise ReinfoLibAPIError(f"Failed to connect to API: {e.reason}") from e
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise ReinfoLibAPIError("Failed to parse API response") from e

    def _parse_transactions(self, data: dict[str, Any]) -> list[Transaction]:
        """Parse API response data to Transaction objects.

        Args:
            data: API response data

        Returns:
            List of Transaction objects
        """
        transactions: list[Transaction] = []

        if "data" not in data:
            return transactions

        for item in data["data"]:
            transaction = self._parse_transaction_item(item)
            transactions.append(transaction)

        return transactions

    def _parse_transaction_item(self, item: dict[str, Any]) -> Transaction:
        """Parse a single transaction item from API response.

        Args:
            item: Transaction item from API response

        Returns:
            Transaction object
        """

        def to_int(value: Any) -> int | None:
            if value is None or value == "":
                return None
            try:
                return int(value)
            except (ValueError, TypeError):
                return None

        def to_float(value: Any) -> float | None:
            if value is None or value == "":
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None

        return Transaction(
            transaction_price=to_int(item.get("TradePrice")) or 0,
            area=to_float(item.get("Area")) or 0.0,
            unit_price=to_float(item.get("UnitPrice")),
            prefecture=item.get("Prefecture", ""),
            city=item.get("Municipality", ""),
            district=item.get("DistrictName"),
            building_year=to_int(item.get("BuildingYear")),
            property_type=item.get("Type", ""),
            structure=item.get("Structure"),
            floor_area_ratio=to_float(item.get("FloorAreaRatio")),
            building_coverage=to_float(item.get("CoverageRatio")),
            frontage_road_width=to_float(item.get("Frontage")),
            transaction_period=item.get("Period", ""),
        )
