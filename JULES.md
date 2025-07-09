# JULES.md

[jules.google]
Jules is a skilled software engineer, and can:

- Understand Code: I can read and analyze code to explain how it works, identify potential issues, or describe its overall architecture.
- Write Code: I can implement new features, write functions, classes, or entire modules based on your requirements.
- Fix Bugs: If you have code that's not working as expected, I can help you debug it and find a solution.
- Write Tests: I can write unit tests, integration tests, or other types of tests to ensure your code is robust and reliable.
- Refactor Code: I can help you improve the structure, readability, and maintainability of your existing code.
- Work with Tools: I can use common development tools like git, run shell commands, and interact with web resources.
- Plan Tasks: I can create detailed plans for how to approach a coding task.
- Answer Questions: I can answer your questions about programming concepts, specific technologies, or the codebase we are working on.
- Essentially, if it's a task a software engineer would do, I can likely help with it.

---

## Recommendations
1. Ensure valid credentials.json is in .claude/scripts/.
2. Create a test markdown file, e.g., test_new_doc.md in the project root, with some simple content like:

    `# My New Test Document
    This is a test document created automatically. `

3. Create/update a test configuration file, e.g., .claude/scripts/test_sync_config_create.json, with content like this (ensure the path to test_new_doc.md is relative to the project root, which is test_new_doc.md if the file is in the project root):
    `{
    "_comment": "Test creation & sync",
    "test_new_doc.md": "CREATE_NEW_DOCUMENT",
    "docs/development-history/google-docs-sync/test_orchestrator.md": "1RdDNthNa0ayZu31MnKNo6RE20b_RBVzGqIDrKHkzIYc" 
    }`
Execution: 

4. From the .claude/scripts/ directory, run: python sync_to_docs.py --config test_sync_config_create.json

Verification: 

5. Script Output: Check for messages indicating document creation, config update, and successful sync. 
6. Google Docs: Verify a new Google Doc titled "test_new_doc" (or similar, based on filename) exists with the correct content. 
7. Config File: Check that test_sync_config_create.json now has the actual Google Doc ID for test_new_doc.md.




1. Create a test markdown file (e.g., docs/new_test_doc.md).
2. Update the sync_config.json (or a test copy) to include this new file with the CREATE_NEW_DOCUMENT placeholder.
3. Run the script: python .claude/scripts/sync_to_docs.py --config path/to/your/test_sync_config.json.
Verify:
4. A new Google Doc is created with the correct title.
5. The sync_config.json is updated with the new Google Doc ID.
6. The content of new_test_doc.md is synced to the newly created Google Doc.
7. Existing documents in the config are still synced correctly.
8. Ensure comments in the JSON config are handled (they will be removed by json.dump, which is acceptable based on prior assumption).


