import pytest
from parameterized import parameterized

from jiken.models import SearchCondition, TradePrice, Transaction


class TestSearchCondition:
    def test_create_with_area(self) -> None:
        condition = SearchCondition(year=2024, area="13")

        assert condition.year == 2024
        assert condition.area == "13"
        assert condition.city is None
        assert condition.quarter is None
        assert condition.language == "en"

    def test_create_with_city(self) -> None:
        condition = SearchCondition(year=2024, city="13101")

        assert condition.year == 2024
        assert condition.area is None
        assert condition.city == "13101"
        assert condition.quarter is None
        assert condition.language == "en"

    def test_create_with_all_params(self) -> None:
        condition = SearchCondition(year=2024, area="13", city="13101", quarter=1, language="ja")

        assert condition.year == 2024
        assert condition.area == "13"
        assert condition.city == "13101"
        assert condition.quarter == 1
        assert condition.language == "ja"

    def test_missing_area_and_city_raises_error(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            SearchCondition(year=2024)

        assert "At least one of 'area' or 'city' must be specified" in str(exc_info.value)

    @parameterized.expand(
        [
            (0,),
            (5,),
            (-1,),
            (10,),
        ]
    )
    def test_invalid_quarter_raises_error(self, quarter: int) -> None:
        with pytest.raises(ValueError) as exc_info:
            SearchCondition(year=2024, area="13", quarter=quarter)

        assert "Quarter must be between 1 and 4" in str(exc_info.value)

    @parameterized.expand(
        [
            ("fr",),
            ("de",),
            ("zh",),
            ("",),
        ]
    )
    def test_invalid_language_raises_error(self, language: str) -> None:
        with pytest.raises(ValueError) as exc_info:
            SearchCondition(year=2024, area="13", language=language)

        assert "Language must be 'ja' or 'en'" in str(exc_info.value)

    @parameterized.expand(
        [
            (1,),
            (2,),
            (3,),
            (4,),
        ]
    )
    def test_valid_quarter(self, quarter: int) -> None:
        condition = SearchCondition(year=2024, area="13", quarter=quarter)
        assert condition.quarter == quarter

    @parameterized.expand(
        [
            ("ja",),
            ("en",),
        ]
    )
    def test_valid_language(self, language: str) -> None:
        condition = SearchCondition(year=2024, area="13", language=language)
        assert condition.language == language


class TestTradePrice:
    def test_as_jpy_formats_with_yen_symbol(self) -> None:
        price = TradePrice(amount_jpy=50000000)

        assert price.as_jpy() == "¥50,000,000"

    def test_as_jpy_zero(self) -> None:
        price = TradePrice(amount_jpy=0)

        assert price.as_jpy() == "¥0"

    @parameterized.expand(
        [
            # (amount_jpy, exchange_rate, expected)
            (50000000, 150.0, "$333,333"),
            (15000000, 150.0, "$100,000"),
            (300000, 150.0, "$2,000"),
            (50000000, 100.0, "$500,000"),
        ]
    )
    def test_as_usd_converts_correctly(
        self, amount_jpy: int, exchange_rate: float, expected: str
    ) -> None:
        price = TradePrice(amount_jpy=amount_jpy)

        assert price.as_usd(exchange_rate) == expected

    def test_format_ja_returns_jpy(self) -> None:
        price = TradePrice(amount_jpy=50000000)

        assert price.format(language="ja") == "¥50,000,000"

    def test_format_en_returns_usd_with_default_rate(self) -> None:
        price = TradePrice(amount_jpy=15000000)

        assert price.format(language="en") == "$100,000"

    def test_format_en_returns_usd_with_custom_rate(self) -> None:
        price = TradePrice(amount_jpy=50000000)

        assert price.format(language="en", exchange_rate=100.0) == "$500,000"


class TestTransaction:
    def test_create_transaction_with_all_fields(self) -> None:
        transaction = Transaction(
            transaction_price=TradePrice(amount_jpy=50000000),
            area=100.5,
            unit_price=1500000.0,
            prefecture="Tokyo",
            city="Chiyoda-ku",
            district="Marunouchi",
            building_year=2020,
            property_type="Residential Land",
            structure="RC",
            floor_area_ratio=200.0,
            building_coverage=60.0,
            frontage_road_width=6.0,
            transaction_period="2024Q1",
        )

        assert transaction.transaction_price == TradePrice(amount_jpy=50000000)
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

    def test_create_transaction_with_optional_none(self) -> None:
        transaction = Transaction(
            transaction_price=TradePrice(amount_jpy=30000000),
            area=80.0,
            unit_price=None,
            prefecture="Osaka",
            city="Osaka-shi",
            district=None,
            building_year=None,
            property_type="Apartment",
            structure=None,
            floor_area_ratio=None,
            building_coverage=None,
            frontage_road_width=None,
            transaction_period="2024Q2",
        )

        assert transaction.transaction_price == TradePrice(amount_jpy=30000000)
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

    def test_transaction_price_per_area_calculation(self) -> None:
        transaction = Transaction(
            transaction_price=TradePrice(amount_jpy=50000000),
            area=100.0,
            unit_price=None,
            prefecture="Tokyo",
            city="Shibuya-ku",
            district=None,
            building_year=2021,
            property_type="Residential Land",
            structure=None,
            floor_area_ratio=None,
            building_coverage=None,
            frontage_road_width=None,
            transaction_period="2024Q1",
        )

        price_per_sqm = transaction.transaction_price.amount_jpy / transaction.area
        assert price_per_sqm == 500000.0
