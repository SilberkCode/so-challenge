# 007 — Test-Driven Development for Milestones

**Date**: 2026-03-23
**Tool**: GitHub Copilot
**Model**: Grok Code Fast 1
**Iterations**: 1

## Prompt

**2026-03-23**

Write pytest tests for `milestones.py`. The module should:

- Take a pandas DataFrame with columns: year_month, question_count
- Identify key milestones in Stack Overflow question activity (e.g. peak month, lowest month, significant growth periods)
- Return results in a structured format (e.g. dict or DataFrame with milestone descriptions and dates)
- Optionally save milestones locally as a JSON or CSV file
- Handle missing or invalid input data gracefully

Write the tests BEFORE the implementation. Use unittest.mock to mock file saving and any external dependencies in tests. Include tests for:

- Valid input returns correct milestone structure
- Peak and minimum months are correctly identified
- Output file is saved to the expected path
- Missing required columns raises a clear exception
- Empty DataFrame is handled gracefully

Save the diary entry and commit everything with a proper commit message describing what was added.