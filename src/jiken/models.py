from dataclasses import dataclass


@dataclass
class TradePrice:
    """Trade price with JPY/USD currency conversion support.

    Args:
        amount_jpy: Transaction price in Japanese Yen (JPY)
    """

    amount_jpy: int

    def as_jpy(self) -> str:
        """Format price in Japanese Yen.

        Returns:
            Price string with yen symbol (e.g., "¥50,000,000")
        """
        return f"¥{self.amount_jpy:,}"

    def as_usd(self, exchange_rate: float) -> str:
        """Convert and format price in US Dollars.

        Args:
            exchange_rate: JPY per 1 USD (e.g., 150.0 means 150 JPY = 1 USD)

        Returns:
            Price string with dollar symbol (e.g., "$333,333")
        """
        amount_usd = round(self.amount_jpy / exchange_rate)
        return f"${amount_usd:,}"

    def format(self, language: str, exchange_rate: float = 150.0) -> str:
        """Format price based on language setting.

        Args:
            language: Language code ("ja" returns JPY, "en" returns USD)
            exchange_rate: JPY per 1 USD used for conversion (default: 150.0)

        Returns:
            Formatted price string in JPY for "ja", USD for "en"
        """
        if language == "ja":
            return self.as_jpy()
        return self.as_usd(exchange_rate)


@dataclass
class SearchCondition:
    """Search condition for real estate transaction API.

    At least one of area, city must be specified.

    Args:
        year: Transaction year (required)
        area: Prefecture code (2 digits, optional)
        city: City code (5 digits, optional)
        quarter: Quarter 1-4 (optional)
        language: Response language "ja" or "en" (default: "en")
    """

    year: int
    area: str | None = None
    city: str | None = None
    quarter: int | None = None
    language: str = "en"

    def __post_init__(self) -> None:
        if self.area is None and self.city is None:
            raise ValueError("At least one of 'area' or 'city' must be specified")

        if self.quarter is not None and not 1 <= self.quarter <= 4:
            raise ValueError("Quarter must be between 1 and 4")

        if self.language not in ("ja", "en"):
            raise ValueError("Language must be 'ja' or 'en'")


@dataclass
class Transaction:
    """Real estate transaction data.

    Core fields for identifying undervalued properties.
    Field names are in English, but values are in the language specified by SearchCondition.
    """

    # Price information (core for valuation)
    transaction_price: TradePrice
    """Total transaction price"""

    area: float
    """Area (square meters)"""

    unit_price: float | None
    """Unit price per tsubo"""

    # Location information (for regional comparison)
    prefecture: str
    """Prefecture name"""

    city: str
    """City/ward name"""

    district: str | None
    """District name"""

    # Property attributes (for value assessment)
    building_year: int | None
    """Year of construction"""

    property_type: str
    """Type: residential land, apartment, etc."""

    structure: str | None
    """Building structure (RC, Wood, Steel, etc.)"""

    # Regulatory information (affects property value)
    floor_area_ratio: float | None
    """Floor area ratio (%)"""

    building_coverage: float | None
    """Building coverage ratio (%)"""

    frontage_road_width: float | None
    """Width of frontage road (meters)"""

    # Metadata
    transaction_period: str
    """Transaction period (e.g., "2024Q1")"""
