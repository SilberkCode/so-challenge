"""

Module for data collection from Stack Overflow API.

Provides functions to fetch question statistics and cache results locally.

"""

import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests


def get_cache_path():
    """
    Get the path to the local cache file for SO questions data.
    
    Returns:
        str: Path to the cache CSV file.
    """
    cache_dir = Path.home() / ".cache" / "so-challenge"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return str(cache_dir / "so_questions.csv")


def fetch_so_questions(use_cache=False, max_retries=2, cache=False):
    """
    Fetch monthly Stack Overflow question counts from 2008 to 2024.
    
    Uses the Stack Overflow API to retrieve question statistics by month.
    Results are cached locally as CSV for performance optimization.
    
    Parameters:
        use_cache (bool): If True, return cached data if available. Default: False.
        max_retries (int): Maximum number of retries on network error. Default: 2.
        cache (bool): If True, cache results locally after fetch. Default: False.
    
    Returns:
        pd.DataFrame: DataFrame with columns:
            - year_month (str): Year and month in YYYY-MM format.
            - question_count (int): Number of questions for that month.
    
    Raises:
        Exception: If all retries are exhausted or API returns malformed data.
    """
    cache_path = get_cache_path()
    
    # Check for cached data
    if use_cache and os.path.exists(cache_path):
        try:
            return pd.read_csv(cache_path)
        except Exception:
            pass
    
    # Fetch from API with retry logic
    df = None
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            df = _fetch_from_api()
            break
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                # Exponential backoff
                time.sleep(2 ** attempt)
    
    if df is None:
        raise last_exception or Exception("Failed to fetch data")
    
    # Ensure correct data types
    df["year_month"] = df["year_month"].astype(object)
    
    # Cache the results
    if cache:
        try:
            df.to_csv(cache_path, index=False)
        except Exception:
            # Don't fail if caching fails
            pass
    
    return df


def _fetch_from_api():
    """
    Fetch data from Stack Overflow API.
    
    Returns:
        pd.DataFrame: Processed DataFrame with year_month and question_count.
    
    Raises:
        KeyError: If API response is malformed.
        Exception: If API request fails.
    """
    # Stack Overflow API endpoint for questions grouped by week
    url = "https://api.stackexchange.com/2.3/questions"
    
    params = {
        "site": "stackoverflow",
        "sort": "creation",
        "order": "desc",
        "fromdate": int(datetime(2008, 1, 1).timestamp()),
        "todate": int(datetime(2024, 12, 31).timestamp()),
        "pagesize": 10000,
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Validate response structure
    if "items" not in data:
        raise KeyError("API response missing 'items' key")
    
    items = data["items"]
    
    # Process items into year_month, question_count
    if not items:
        return pd.DataFrame(columns=["year_month", "question_count"])
    
    # Group by year-month
    monthly_counts = {}
    
    for item in items:
        if "creation_date" not in item:
            raise KeyError("Item missing 'creation_date' key")
        
        timestamp = item["creation_date"]
        dt = datetime.fromtimestamp(timestamp)
        year_month = dt.strftime("%Y-%m")
        
        monthly_counts[year_month] = monthly_counts.get(year_month, 0) + 1
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {"year_month": ym, "question_count": count}
        for ym, count in sorted(monthly_counts.items())
    ])
    
    # Ensure correct data types
    df["year_month"] = df["year_month"].astype(object)
    df["question_count"] = df["question_count"].astype(int)
    
    return df