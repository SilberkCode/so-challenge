"""

Tests for milestones module.

"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
import json
import os

from milestones import identify_milestones


class TestIdentifyMilestones:
    """Test suite for Stack Overflow milestones identification."""

    @pytest.fixture
    def sample_dataframe(self):
        """Fixture providing a sample DataFrame for testing."""
        return pd.DataFrame({
            "year_month": ["2008-09", "2008-10", "2008-11", "2008-12", "2009-01"],
            "question_count": [100, 200, 150, 300, 250]  # Peak at 2008-12, min at 2008-09
        })

    @pytest.fixture
    def empty_dataframe(self):
        """Fixture providing an empty DataFrame."""
        return pd.DataFrame(columns=["year_month", "question_count"])

    @pytest.fixture
    def invalid_dataframe_missing_columns(self):
        """Fixture providing a DataFrame missing required columns."""
        return pd.DataFrame({
            "year": ["2008", "2009"],
            "count": [100, 150]
        })

    @pytest.fixture
    def invalid_dataframe_wrong_types(self):
        """Fixture providing a DataFrame with wrong column types."""
        return pd.DataFrame({
            "year_month": [200809, 200810],  # int instead of str
            "question_count": ["100", "150"]  # str instead of int
        })

    def test_identify_milestones_valid_input(self, sample_dataframe):
        """Test that valid input returns correct milestone structure."""
        result = identify_milestones(sample_dataframe)

        assert isinstance(result, dict)
        assert "peak_month" in result
        assert "min_month" in result
        assert "peak_count" in result
        assert "min_count" in result
        assert "growth_periods" in result

    def test_identify_milestones_peak_month_correct(self, sample_dataframe):
        """Test that peak month is correctly identified."""
        result = identify_milestones(sample_dataframe)

        assert result["peak_month"] == "2008-12"
        assert result["peak_count"] == 300

    def test_identify_milestones_min_month_correct(self, sample_dataframe):
        """Test that minimum month is correctly identified."""
        result = identify_milestones(sample_dataframe)

        assert result["min_month"] == "2008-09"
        assert result["min_count"] == 100

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_identify_milestones_save_json(self, mock_json_dump, mock_file, sample_dataframe):
        """Test that milestones are saved to JSON file."""
        save_path = "milestones.json"
        result = identify_milestones(sample_dataframe, save_path=save_path)

        mock_file.assert_called_once_with(save_path, 'w')
        mock_json_dump.assert_called_once_with(result, mock_file())

    @patch("pandas.DataFrame.to_csv")
    def test_identify_milestones_save_csv(self, mock_to_csv, sample_dataframe):
        """Test that milestones are saved to CSV file."""
        save_path = "milestones.csv"
        result = identify_milestones(sample_dataframe, save_path=save_path)

        mock_to_csv.assert_called_once()

    def test_identify_milestones_missing_columns_raises_exception(self, invalid_dataframe_missing_columns):
        """Test that missing required columns raises a clear exception."""
        with pytest.raises(ValueError, match="DataFrame must contain 'year_month' and 'question_count' columns"):
            identify_milestones(invalid_dataframe_missing_columns)

    def test_identify_milestones_empty_dataframe(self, empty_dataframe):
        """Test that empty DataFrame is handled gracefully."""
        result = identify_milestones(empty_dataframe)

        assert isinstance(result, dict)
        # For empty DataFrame, milestones might be None or empty
        assert result["peak_month"] is None or "peak_month" in result

    def test_identify_milestones_invalid_data_types(self, invalid_dataframe_wrong_types):
        """Test that invalid data types are handled gracefully."""
        with pytest.raises(ValueError):
            identify_milestones(invalid_dataframe_wrong_types)

    def test_identify_milestones_growth_periods_identified(self, sample_dataframe):
        """Test that growth periods are identified."""
        result = identify_milestones(sample_dataframe)

        assert "growth_periods" in result
        # Assuming growth periods are identified, check structure
        growth_periods = result["growth_periods"]
        assert isinstance(growth_periods, list)

    @patch("builtins.open", new_callable=mock_open)
    def test_identify_milestones_no_save_when_no_path(self, mock_file, sample_dataframe):
        """Test that no file operations occur when save_path is not provided."""
        result = identify_milestones(sample_dataframe)

        mock_file.assert_not_called()

    def test_identify_milestones_handles_single_month(self):
        """Test handling of DataFrame with single month."""
        single_df = pd.DataFrame({
            "year_month": ["2008-09"],
            "question_count": [100]
        })
        result = identify_milestones(single_df)

        assert result["peak_month"] == "2008-09"
        assert result["min_month"] == "2008-09"
        assert result["peak_count"] == 100
        assert result["min_count"] == 100

    def test_identify_milestones_non_dataframe_input(self):
        """Test that non-DataFrame input raises TypeError."""
        with pytest.raises(TypeError):
            identify_milestones([1, 2, 3])

    def test_identify_milestones_none_input(self):
        """Test that None input raises TypeError."""
        with pytest.raises(TypeError):
            identify_milestones(None)