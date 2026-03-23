# 006 — Plotter Implementation

**Date**: 2026-03-23
**Tool**: GitHub Copilot
**Model**: Grok Code Fast 1
**Iterations**: 1

## Prompt

**2026-03-23**

Now implement `plotter.py` to pass the tests in `test_plotter.py`. The implementation should pass all tests. Do not modify the tests.

The module should:

- Accept a pandas DataFrame with columns: year_month, question_count
- Use matplotlib to create a line plot
- Label axes and include a descriptive title
- Save the plot as a PNG file to the specified path
- Avoid displaying the plot (no plt.show())
- Validate input data and handle errors gracefully

Run the tests to confirm they pass. If they do, save the diary entry and commit everything with a proper commit message that describes what was implemented and why.