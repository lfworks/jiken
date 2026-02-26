# jiken

[![CI](https://github.com/lfworks/jiken/actions/workflows/ci.yml/badge.svg)](https://github.com/lfworks/jiken/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

**jiken** - Where 地 (ji/land) meets 検証 (kensho/verification).

Verify land values with official data from Japan's MLIT (Ministry of Land, Infrastructure, Transport and Tourism). Python library for accessing MLIT Real Estate Transaction Price Information API.

## Features

- **Simple API**: Clean, intuitive interface for querying real estate transaction data
- **Zero external dependencies**: Built using Python standard library only
- **Type-safe**: Full type hints for better IDE support and code quality
- **Bilingual support**: Retrieve data in English or Japanese
- **Well-tested**: Comprehensive test coverage with unit tests

## Installation

```bash
pip install jiken
```

Or using [uv](https://github.com/astral-sh/uv):

```bash
uv pip install jiken
```

## Quick Start

### Prerequisites

You need an API key from MLIT to use this library. Visit [MLIT Real Estate Information Library](https://www.reinfolib.mlit.go.jp/) to obtain your API key.

### Basic Usage

```python
from jiken import JikenClient, SearchCondition

# Initialize client with your API key
client = JikenClient(api_key="your-api-key-here")

# Search for transactions in Tokyo (area code: 13) in 2024 Q1
condition = SearchCondition(
    year=2024,
    area="13",      # Tokyo prefecture code
    quarter=1,      # First quarter
    language="en"   # English response (default)
)

# Fetch transaction data
transactions = client.search_transactions(condition)

# Analyze the data
for tx in transactions:
    print(f"Price: ¥{tx.transaction_price:,}")
    print(f"Area: {tx.area} m²")
    print(f"Location: {tx.prefecture}, {tx.city}")
    print(f"Type: {tx.property_type}")
    print("---")
```

### Search with City Code

```python
# Search for transactions in Chiyoda-ku, Tokyo (city code: 13101)
condition = SearchCondition(
    year=2024,
    city="13101",
    language="ja"   # Japanese response
)

transactions = client.search_transactions(condition)
```

## Examples

| Notebook | Description |
|----------|-------------|
| [Map Visualization](examples/map_visualization.ipynb) | Plot real estate transactions on an interactive map using pandas, geopy, and plotly |

## API Reference

### `JikenClient`

Main client for accessing the API.

#### Methods

- `search_transactions(condition: SearchCondition) -> list[Transaction]`
  - Search real estate transactions based on conditions
  - Returns a list of `Transaction` objects

### `SearchCondition`

Search parameters for querying transaction data.

#### Parameters

- `year` (int, required): Transaction year
- `area` (str, optional): Prefecture code (2 digits)
- `city` (str, optional): City/municipality code (5 digits)
- `quarter` (int, optional): Quarter (1-4)
- `language` (str, optional): Response language "ja" or "en" (default: "en")

**Note:** At least one of `area` or `city` must be specified.

### `Transaction`

Real estate transaction data.

#### Attributes

**Price Information:**
- `transaction_price` (int): Total transaction price in JPY
- `area` (float): Area in square meters
- `unit_price` (float | None): Unit price per tsubo

**Location:**
- `prefecture` (str): Prefecture name
- `city` (str): City/ward name
- `district` (str | None): District name

**Property Details:**
- `building_year` (int | None): Year of construction
- `property_type` (str): Property type (e.g., "Residential Land", "Apartment")
- `structure` (str | None): Building structure (e.g., "RC", "Wood", "Steel")

**Regulatory Information:**
- `floor_area_ratio` (float | None): Floor area ratio (%)
- `building_coverage` (float | None): Building coverage ratio (%)
- `frontage_road_width` (float | None): Width of frontage road in meters

**Metadata:**
- `transaction_period` (str): Transaction period (e.g., "2024Q1")

### Exceptions

All exceptions inherit from `JikenError`:

- `JikenAuthError`: Authentication failed (401)
- `JikenRequestError`: Invalid request parameters (400)
- `JikenAPIError`: General API error

## Use Cases

This library is ideal for:

- **Real estate market analysis**: Analyze transaction trends and pricing patterns
- **Investment research**: Identify undervalued properties in specific areas
- **Academic research**: Study real estate market dynamics in Japan
- **Data science projects**: Build machine learning models for price prediction

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/lfworks/jiken.git
cd jiken

# Install dependencies with uv
uv sync --all-extras
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
uv run pytest --cov=src/jiken
```

### Code Quality

```bash
# Format code
make format

# Lint
make lint

# Type check
make type-check

# Dead code detection
make deadcode

# Run all checks
make check
```

## Prefecture and City Codes

Common prefecture codes:
- `13`: Tokyo
- `27`: Osaka
- `14`: Kanagawa
- `23`: Aichi
- `40`: Fukuoka

For a complete list of codes, refer to the [MLIT documentation](https://www.reinfolib.mlit.go.jp/help/apiManual/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Links

- [MLIT Real Estate Information Library](https://www.reinfolib.mlit.go.jp/)
- [API Documentation](https://www.reinfolib.mlit.go.jp/help/apiManual/)
- [GitHub Repository](https://github.com/lfworks/jiken)
- [Issue Tracker](https://github.com/lfworks/jiken/issues)

## Acknowledgments

This library provides access to data from the Ministry of Land, Infrastructure, Transport and Tourism (MLIT) of Japan.
