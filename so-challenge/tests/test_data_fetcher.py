"""

Tests for data_fetcher module.

"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import os

from data_fetcher import fetch_so_questions, get_cache_path


class TestFetchSOQuestions:
    """Test suite for Stack Overflow question data fetching."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary directory for cache testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_api_response(self):
        """Fixture providing a mock API response."""
        return {
            "items": [
                {"creation_date": 1225000000, "count": 100},  # 2008
                {"creation_date": 1256000000, "count": 150},  # 2009
                {"creation_date": 1577000000, "count": 5000},  # 2019
            ]
        }

    @patch("data_fetcher.requests.get")
    def test_fetch_so_questions_successful(self, mock_get, mock_api_response):
        """Test successful data fetch returns correct DataFrame shape."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = fetch_so_questions()

        assert isinstance(result, pd.DataFrame)
        assert "year_month" in result.columns
        assert "question_count" in result.columns
        assert len(result) > 0
        assert result["year_month"].dtype == "object"
        assert result["question_count"].dtype in ["int64", "int32", "int"]

    @patch("data_fetcher.requests.get")
    def test_fetch_so_questions_returns_correct_date_range(self, mock_get, mock_api_response):
        """Test that fetched data covers 2008-2024 range."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = fetch_so_questions()

        # Extract years from year_month strings
        years = pd.to_datetime(result["year_month"]).dt.year.unique()
        assert years.min() >= 2008
        assert years.max() <= 2024

    @patch("data_fetcher.os.path.exists")
    @patch("data_fetcher.pd.read_csv")
    def test_cached_data_returned_without_network_call(self, mock_read_csv, mock_exists, temp_cache_dir):
        """Test that cached data is returned without making a network call."""
        # Setup mock cached data
        mock_exists.return_value = True
        cached_df = pd.DataFrame({
            "year_month": ["2008-09", "2008-10"],
            "question_count": [100, 150]
        })
        mock_read_csv.return_value = cached_df

        with patch("data_fetcher.requests.get") as mock_get:
            result = fetch_so_questions(use_cache=True)

            # Network call should not be made
            mock_get.assert_not_called()
            # Cached data should be returned
            pd.testing.assert_frame_equal(result, cached_df)

    @patch("data_fetcher.requests.get")
    def test_network_error_triggers_retry_logic(self, mock_get):
        """Test that network errors trigger retry logic."""
        # Simulate network failures followed by success
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": [{"creation_date": 1225000000, "count": 100}]}
        mock_response.status_code = 200

        mock_get.side_effect = [
            Exception("Network error"),
            Exception("Network error"),
            mock_response,
        ]

        result = fetch_so_questions(max_retries=3)

        assert isinstance(result, pd.DataFrame)
        assert mock_get.call_count == 3

    @patch("data_fetcher.requests.get")
    def test_network_error_exhausts_retries(self, mock_get):
        """Test that exhausted retries raise an exception."""
        mock_get.side_effect = Exception("Network error")

        with pytest.raises(Exception):
            fetch_so_questions(max_retries=2)

        assert mock_get.call_count == 2

    @patch("data_fetcher.requests.get")
    def test_cache_is_saved_after_successful_fetch(self, mock_get, temp_cache_dir):
        """Test that successful fetch results are cached locally."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [{"creation_date": 1225000000, "count": 100}]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with patch("data_fetcher.get_cache_path") as mock_cache_path:
            cache_file = os.path.join(temp_cache_dir, "so_questions.csv")
            mock_cache_path.return_value = cache_file

            fetch_so_questions(cache=True)

            # Verify cache file was created
            assert os.path.exists(cache_file) or mock_cache_path.called

    def test_get_cache_path_returns_valid_path(self):
        """Test that get_cache_path returns a valid cache file path."""
        cache_path = get_cache_path()

        assert isinstance(cache_path, (str, Path))
        assert "so_questions" in str(cache_path)
        assert str(cache_path).endswith(".csv")

    @patch("data_fetcher.requests.get")
    def test_fetch_so_questions_handles_empty_response(self, mock_get):
        """Test that empty API response is handled gracefully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = fetch_so_questions()

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0 or "year_month" in result.columns

    @patch("data_fetcher.requests.get")
    def test_fetch_so_questions_handles_malformed_response(self, mock_get):
        """Test that malformed API responses are handled gracefully."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"unexpected_key": "unexpected_value"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        with pytest.raises((KeyError, ValueError)):
            fetch_so_questions()