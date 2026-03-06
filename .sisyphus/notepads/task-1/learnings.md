## Learnings from task-1: YAML indentation fix in daily-email workflow
- Indentation in YAML blocks under env is critical. Mis-indented keys can cause GitHub Actions to error or misread environment variables.
- Always align subsequent keys after a multi-line key block to the same indentation level as existing keys.
- After making a patch, verify syntax with a YAML validator and save evidence of validation for traceability.
