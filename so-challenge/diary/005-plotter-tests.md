# 005 — Test-Driven Development for Plotter

**Date**: 2026-03-23
**Tool**: GitHub Copilot
**Model**: Grok Code Fast 1
**Iterations**: 1

## Prompt

**2026-03-23**

Write pytest tests for `plotter.py`. The module should:

- Take a pandas DataFrame with columns: year_month, question_count
- Use matplotlib to create a line plot of monthly Stack Overflow question counts
- Ensure the x-axis shows time (year_month) and the y-axis shows question_count
- Add axis labels and a descriptive title
- Save the plot locally as a PNG file
- Not display the plot (no GUI popups)
- Handle missing or invalid input data gracefully

Write the tests BEFORE the implementation. Use unittest.mock to mock matplotlib and file system interactions. Include tests for:

- Valid input DataFrame produces a plot without raising exceptions
- matplotlib plotting functions are called with correct data
- The plot is saved to the correct file path
- No call to plt.show() is made
- Missing required columns raises a clear exception
- Empty DataFrame does not crash and is handled appropriately

Save the diary entry and commit everything with a proper commit message describing what was added.