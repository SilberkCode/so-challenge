"""

Module for visualization of Stack Overflow question data.

Provides functions to create and save plots from question count data.

"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_question_counts(df, filename="so_question_counts.png"):
    """
    Create a line plot of monthly Stack Overflow question counts and save as PNG.
    
    Parameters:
        df (pd.DataFrame): DataFrame with columns 'year_month' (str) and 'question_count' (numeric).
        filename (str): Path to save the PNG file. Default: "so_question_counts.png".
    
    Raises:
        TypeError: If input is not a pandas DataFrame.
        ValueError: If required columns are missing or data types are invalid.
    
    Note:
        This function does not display the plot (no plt.show() call).
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
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    if not df.empty:
        plt.plot(df["year_month"], df["question_count"], marker='o', linestyle='-')
    # For empty DataFrame, just create the figure without plotting
    
    # Add labels and title
    plt.xlabel("Year-Month")
    plt.ylabel("Question Count")
    plt.title("Monthly Stack Overflow Question Counts")
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Save the plot
    plt.savefig(filename)
    
    # Close the figure to free memory
    plt.close()