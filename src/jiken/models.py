from dataclasses import dataclass


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
    transaction_price: int
    """Total transaction price (JPY)"""

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
