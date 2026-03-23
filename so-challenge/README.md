# SO Challenge

A Python project for analyzing Stack Overflow question trends (2008-2024), identifying key milestones, and creating visualizations.

## Project Description

This project demonstrates test-driven development (TDD) practices by:
- Fetching monthly Stack Overflow question counts via the SO API
- Identifying key milestones (peak months, minimum months, growth periods)
- Creating matplotlib visualizations of question trends
- Caching data locally for improved performance
- Handling network errors with retry logic

## Project Structure

```
so-challenge/
├── main.py                 # Main entry point
├── data_fetcher.py         # SO API data collection module
├── plotter.py              # Matplotlib visualization module
├── milestones.py           # Milestone analysis module
├── tests/                  # Test suite
│   ├── test_data_fetcher.py
│   ├── test_plotter.py
│   └── test_milestones.py
├── docs/
│   └── requirements.md      # Project requirements specification
├── diary/                   # AI interaction records
│   ├── 001-project-setup.md
│   ├── 002-requirements-specification.md
│   ├── 003-data-fetcher-tests.md
│   ├── 004-data-fetcher-implementation.md
│   ├── 005-plotter-tests.md
│   ├── 006-plotter-implementation.md
│   ├── 007-milestones-tests.md
│   └── 008-milestones-implementation.md
├── pyproject.toml           # uv project configuration
└── README.md                # This file
```

## Requirements

- Python 3.12+
- Dependencies (managed via uv):
  - pandas
  - matplotlib
  - requests
  - pytest (dev)

## Setup

### Installation with uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

## Usage

### Running the Main Analysis

```bash
# Run the complete analysis pipeline
python main.py
```

This will:
1. Fetch Stack Overflow question data (2008-2024)
2. Identify key milestones in question activity
3. Create a visualization and save as PNG
4. Save milestone details as JSON
5. Log all activities to so_challenge.log

### Using Individual Modules

#### Data Fetcher

```python
from data_fetcher import fetch_so_questions

# Fetch data with caching
df = fetch_so_questions(use_cache=True, max_retries=3, cache=True)
print(df.head())
```

#### Milestone Analysis

```python
from milestones import identify_milestones

milestones = identify_milestones(df, save_path="milestones.json")
print(f"Peak: {milestones['peak_month']} with {milestones['peak_count']} questions")
```

#### Visualization

```python
from plotter import plot_question_counts

plot_question_counts(df, filename="so_trends.png")
```

## Testing

The project uses pytest with comprehensive test coverage including mocked API calls and file I/O operations.

### Run All Tests

```bash
python -m pytest tests/
```

### Run Specific Test Module

```bash
# Test data fetching module
python -m pytest tests/test_data_fetcher.py -v

# Test plotter module
python -m pytest tests/test_plotter.py -v

# Test milestones module
python -m pytest tests/test_milestones.py -v
```

### Test Coverage

- **data_fetcher.py** (9 tests)
  - API data fetching with mocked requests
  - Local caching functionality
  - Retry logic with exponential backoff
  - Error handling for network failures
  - Empty and malformed response handling

- **plotter.py** (11 tests)
  - DataFrame validation and type checking
  - matplotlib function calls and data verification
  - PNG file saving
  - Axis labels and title validation
  - Empty DataFrame handling
  - Custom filename support

- **milestones.py** (14 tests)
  - Peak/minimum month identification
  - Growth period detection
  - JSON/CSV export
  - Input validation and error handling
  - Edge cases (single month, empty DataFrames)

## API and Data

### Stack Overflow API

Uses the [Stack Exchange API](https://api.stackexchange.com/docs) to retrieve question statistics.

**Endpoint**: `https://api.stackexchange.com/2.3/questions`

**Parameters**:
- site: `stackoverflow`
- sort: `creation`
- order: `desc`
- fromdate: `2008-01-01` (Unix timestamp)
- todate: `2024-12-31` (Unix timestamp)

### Data Format

The project works with DataFrames containing:
- `year_month` (str): Month in YYYY-MM format (e.g., "2008-09")
- `question_count` (int): Number of questions for that month

## Development

### Test-Driven Development Approach

This project was developed using TDD:
1. Comprehensive test suites written first
2. Implementation guided by test requirements
3. All tests passing before feature completion

### Diary System

Every major development cycle is documented in the `diary/` folder with:
- Prompts and specifications
- Tools and models used
- Iteration count

See `diary/` folder for detailed interaction history.

## Output Files

When running the analysis, the project generates:

- `so_question_counts.png` - Line plot of monthly question counts
- `milestones.json` - Identified milestones in JSON format
- `so_challenge.log` - Application activity log
- Local cache at `~/.cache/so-challenge/so_questions.csv` - Cached API data

## Error Handling

The project includes robust error handling:
- Network error retries with exponential backoff
- Clear exception messages for invalid inputs
- Graceful handling of empty datasets
- Comprehensive logging for debugging

## Performance Considerations

- **Caching**: Local CSV caching reduces repeated API calls
- **Retry Logic**: Exponential backoff prevents overwhelming the API
- **Memory Management**: matplotlib figures are properly closed after use
- **Batch Operations**: Efficient pandas operations for data processing

## License

Educational project for software engineering practices.

## Contributing

This is an educational project demonstrating software engineering best practices including:
- Test-driven development
- Modular design
- Comprehensive error handling
- Clear documentation