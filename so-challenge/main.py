"""

Main entry point for SO Challenge project.

Orchestrates data fetching, analysis, and visualization of Stack Overflow metrics.

"""

import sys
import logging
from data_fetcher import fetch_so_questions
from milestones import identify_milestones
from plotter import plot_question_counts


def setup_logging(level=logging.INFO):
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('so_challenge.log')
        ]
    )
    return logging.getLogger(__name__)


def main():
    """
    Main workflow: Fetch data, identify milestones, and create visualizations.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    logger = setup_logging()
    
    try:
        logger.info("Starting SO Challenge analysis...")
        
        # Step 1: Fetch data from Stack Overflow API
        logger.info("Fetching Stack Overflow question data (2008-2024)...")
        df = fetch_so_questions(use_cache=True, max_retries=3, cache=True)
        logger.info(f"Successfully fetched data: {len(df)} months of data")
        
        # Step 2: Identify milestones
        logger.info("Identifying milestones in question activity...")
        milestones = identify_milestones(df, save_path="milestones.json")
        
        logger.info(f"Peak month: {milestones['peak_month']} with {milestones['peak_count']} questions")
        logger.info(f"Minimum month: {milestones['min_month']} with {milestones['min_count']} questions")
        logger.info(f"Identified {len(milestones['growth_periods'])} significant growth periods")
        
        # Step 3: Create visualization
        logger.info("Creating visualization...")
        plot_question_counts(df, filename="so_question_counts.png")
        logger.info("Plot saved as 'so_question_counts.png'")
        
        logger.info("Analysis complete!")
        return 0
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
