"""

Tests for plotter module.

"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import tempfile
import os

from plotter import plot_question_counts


class TestPlotQuestionCounts:
    """Test suite for Stack Overflow question count plotting."""

    @pytest.fixture
    def sample_dataframe(self):
        """Fixture providing a sample DataFrame for testing."""
        return pd.DataFrame({
            "year_month": ["2008-09", "2008-10", "2009-01", "2009-02"],
            "question_count": [100, 150, 200, 250]
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

    @patch("plotter.plt")
    def test_plot_question_counts_valid_input(self, mock_plt, sample_dataframe):
        """Test that valid input DataFrame produces a plot without raising exceptions."""
        # Setup mock
        mock_plt.figure.return_value = MagicMock()
        mock_plt.savefig.return_value = None

        # Call function
        plot_question_counts(sample_dataframe)

        # Verify no exceptions raised and basic calls made
        mock_plt.figure.assert_called_once()
        mock_plt.plot.assert_called_once()
        mock_plt.xlabel.assert_called_once_with("Year-Month")
        mock_plt.ylabel.assert_called_once_with("Question Count")
        mock_plt.title.assert_called_once()
        mock_plt.savefig.assert_called_once()
        mock_plt.show.assert_not_called()

    @patch("plotter.plt")
    def test_plot_question_counts_calls_plot_with_correct_data(self, mock_plt, sample_dataframe):
        """Test that matplotlib plotting functions are called with correct data."""
        mock_plt.figure.return_value = MagicMock()

        plot_question_counts(sample_dataframe)

        # Verify plot was called with the correct x and y data
        mock_plt.plot.assert_called_once()
        args, kwargs = mock_plt.plot.call_args
        x_data, y_data = args
        assert list(x_data) == sample_dataframe["year_month"].tolist()
        assert list(y_data) == sample_dataframe["question_count"].tolist()

    @patch("plotter.plt")
    def test_plot_question_counts_saves_to_correct_path(self, mock_plt, sample_dataframe):
        """Test that the plot is saved to the correct file path."""
        mock_plt.figure.return_value = MagicMock()
        expected_path = "so_question_counts.png"

        plot_question_counts(sample_dataframe)

        mock_plt.savefig.assert_called_once_with(expected_path)

    @patch("plotter.plt")
    def test_plot_question_counts_no_show_call(self, mock_plt, sample_dataframe):
        """Test that no call to plt.show() is made."""
        mock_plt.figure.return_value = MagicMock()

        plot_question_counts(sample_dataframe)

        mock_plt.show.assert_not_called()

    @patch("plotter.plt")
    def test_plot_question_counts_missing_columns_raises_exception(self, mock_plt, invalid_dataframe_missing_columns):
        """Test that missing required columns raises a clear exception."""
        with pytest.raises(ValueError, match="DataFrame must contain 'year_month' and 'question_count' columns"):
            plot_question_counts(invalid_dataframe_missing_columns)

    @patch("plotter.plt")
    def test_plot_question_counts_empty_dataframe(self, mock_plt, empty_dataframe):
        """Test that empty DataFrame does not crash and is handled appropriately."""
        mock_plt.figure.return_value = MagicMock()

        # Should not raise exception, but may not plot anything
        plot_question_counts(empty_dataframe)

        # Verify figure was created but plot may not be called
        mock_plt.figure.assert_called_once()
        # For empty data, plot might not be called, but savefig should still be called
        mock_plt.savefig.assert_called_once()

    @patch("plotter.plt")
    def test_plot_question_counts_invalid_data_types(self, mock_plt, invalid_dataframe_wrong_types):
        """Test that invalid data types are handled gracefully."""
        mock_plt.figure.return_value = MagicMock()

        # Should handle type conversion or raise appropriate error
        with pytest.raises((ValueError, TypeError)):
            plot_question_counts(invalid_dataframe_wrong_types)

    @patch("plotter.plt")
    def test_plot_question_counts_custom_filename(self, mock_plt, sample_dataframe):
        """Test that custom filename can be specified."""
        mock_plt.figure.return_value = MagicMock()
        custom_filename = "custom_plot.png"

        plot_question_counts(sample_dataframe, filename=custom_filename)

        mock_plt.savefig.assert_called_once_with(custom_filename)

    @patch("plotter.plt")
    def test_plot_question_counts_title_contains_descriptive_text(self, mock_plt, sample_dataframe):
        """Test that the plot title is descriptive."""
        mock_plt.figure.return_value = MagicMock()

        plot_question_counts(sample_dataframe)

        mock_plt.title.assert_called_once()
        args, kwargs = mock_plt.title.call_args
        title = args[0]
        assert "Stack Overflow" in title
        assert "Question" in title

    @patch("plotter.plt")
    def test_plot_question_counts_handles_none_input(self, mock_plt):
        """Test that None input raises appropriate exception."""
        with pytest.raises((TypeError, ValueError)):
            plot_question_counts(None)

    @patch("plotter.plt")
    def test_plot_question_counts_handles_non_dataframe_input(self, mock_plt):
        """Test that non-DataFrame input raises appropriate exception."""
        with pytest.raises(TypeError):
            plot_question_counts([1, 2, 3])