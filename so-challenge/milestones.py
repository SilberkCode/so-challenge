"""

Module for identifying milestones in Stack Overflow question data.

Provides functions to analyze question count data and identify key milestones.

"""

import json
import pandas as pd


def identify_milestones(df, save_path=None):
    """
    Identify key milestones in Stack Overflow question activity.
    
    Parameters:
        df (pd.DataFrame): DataFrame with columns 'year_month' (str) and 'question_count' (numeric).
        save_path (str, optional): Path to save milestones. If ends with .json, saves as JSON; otherwise as CSV.
    
    Returns:
        dict: Dictionary containing identified milestones with keys:
            - peak_month: Month with highest question count
            - min_month: Month with lowest question count
            - peak_count: Highest question count
            - min_count: Lowest question count
            - growth_periods: List of significant growth periods
    
    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If required columns are missing or data types are invalid.
    """
    # Validate input type
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    
    # Validate required columns
    required_columns = ["year_month", "question_count"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame must contain 'year_month' and 'question_count' columns. Missing: {missing_columns}")
    
    # Validate data types (skip for empty DataFrame)
    if not df.empty:
        if not pd.api.types.is_string_dtype(df["year_month"]):
            raise ValueError("Column 'year_month' must contain string values")
        
        if not pd.api.types.is_numeric_dtype(df["question_count"]):
            raise ValueError("Column 'question_count' must contain numeric values")
    
    # Initialize result
    result = {
        "peak_month": None,
        "min_month": None,
        "peak_count": None,
        "min_count": None,
        "growth_periods": []
    }
    
    if df.empty:
        return result
    
    # Find peak and minimum
    peak_idx = df["question_count"].idxmax()
    min_idx = df["question_count"].idxmin()
    
    result["peak_month"] = df.loc[peak_idx, "year_month"]
    result["min_month"] = df.loc[min_idx, "year_month"]
    result["peak_count"] = int(df.loc[peak_idx, "question_count"])
    result["min_count"] = int(df.loc[min_idx, "question_count"])
    
    # Identify significant growth periods
    if len(df) > 1:
        # Calculate month-to-month growth
        df_sorted = df.sort_values("year_month").reset_index(drop=True)
        growth = df_sorted["question_count"].diff()
        
        # Find periods with significant growth (e.g., top 3 largest increases)
        significant_growth = growth.nlargest(3)  # Get top 3 growth periods
        
        for idx in significant_growth.index:
            if idx > 0:  # Skip first row (NaN)
                growth_period = {
                    "start_month": df_sorted.loc[idx-1, "year_month"],
                    "end_month": df_sorted.loc[idx, "year_month"],
                    "growth": int(growth.loc[idx])
                }
                result["growth_periods"].append(growth_period)
    
    # Save to file if path provided
    if save_path:
        if save_path.endswith('.json'):
            with open(save_path, 'w') as f:
                json.dump(result, f, indent=2)
        else:
            # Save as CSV
            milestones_df = pd.DataFrame([result])
            milestones_df.to_csv(save_path, index=False)
    
    return result