# MADIO Google Docs Sync - Setup Guide (New Registry System)

> **🎯 Goal**: Enable your MADIO project to sync with Google Docs using the new `.madio/document_registry.json` system.

This guide provides **step-by-step instructions** for setting up Google Docs synchronization in your MADIO project. This version assumes you are using the MADIO framework with the `.madio/document_registry.json` system (introduced around Phase 1/2 of the iterative development PRD).

**If you have an older project using `sync_config.json` or `.synced_docs_mapping.json`, first run `/madio-migrate-config` to upgrade your project structure.**

---

## 📋 Quick Overview

**What you'll accomplish:**
1. ✅ Configure Google Cloud APIs and credentials (one-time).
2. ✅ Install Python dependencies for the sync scripts (one-time).
3. ✅ Understand how the `.madio/document_registry.json` controls sync.
4. ✅ Perform your first sync using `/push-to-docs`.

**Time Required:** ~10-15 minutes for initial Google Cloud setup. Subsequent project syncs are quick.
**Prerequisites:**
- A MADIO project initialized (`/madio-setup`).
- Python 3.x installed.
- Access to a Google Cloud Platform project.

---

## 🚨 Security Notice

> **⚠️ CRITICAL SECURITY REQUIREMENTS:**
> - **NEVER commit** `credentials.json` or `token.pickle` (or `token.json`) files to Git. The `.gitignore` file should already list `token.pickle`. Ensure `credentials.json` is also covered if you place it directly in `.claude/scripts/`.
> - **Set proper permissions for `credentials.json`**: `chmod 600 .claude/scripts/credentials.json` after downloading.
> - **Keep credentials private:** These files grant access to your Google account's Docs and Drive.
> - **Consider a dedicated Google account** for MADIO projects if working in a team or for sensitive data.

---

## 🔧 Step 1: Google Cloud Setup (One-Time)

If you've already done this for another MADIO project using the same Google Account, you might be able to reuse `credentials.json`, but it's often cleaner to have project-specific OAuth clients if you manage multiple distinct systems.

### 1.1 Create/Select Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. **Create a new project** or select an existing one.
3. Note your **Project ID**.

### 1.2 Enable Required APIs
Enable **BOTH** of these APIs for your project:
1.  **Google Docs API:** Search for "Google Docs API" in the console's search bar and click **Enable**.
2.  **Google Drive API:** Search for "Google Drive API" and click **Enable**. (Needed for creating documents, managing folders, and fetching metadata like versions).

### 1.3 Configure OAuth Consent Screen
1.  In Google Cloud Console, navigate to **APIs & Services → OAuth consent screen**.
2.  Choose **User Type**:
    *   **Internal:** If your organization uses Google Workspace and the app is only for internal users.
    *   **External:** For most other cases (e.g., using a personal Gmail account).
3.  Fill in required app information (App name, User support email, Developer contact). For a personal tool, these can be straightforward (e.g., App name: "MADIO Sync Utility").
4.  **Scopes:** You don't need to add scopes here; the application will request them.
5.  **Test users:** If your app is "External" and in "Testing" publishing status, **add your Google account email address as a test user**. Otherwise, you won't be able to authenticate.

### 1.4 Create OAuth 2.0 Client ID
1.  Navigate to **APIs & Services → Credentials**.
2.  Click **+ Create Credentials** → **OAuth client ID**.
3.  **Application type:** Choose **Desktop app**.
4.  **Name:** Give it a name (e.g., "MADIO Desktop Sync Client").
5.  Click **Create**.
6.  A dialog will show your Client ID and Client Secret. Click **DOWNLOAD JSON**. This file contains your client secret.
7.  **Rename** the downloaded JSON file to `credentials.json`.

### 1.5 Install Credentials File
1.  Move the renamed `credentials.json` file into the `.claude/scripts/` directory within your MADIO project.
    So the path should be: `YOUR_PROJECT_ROOT/.claude/scripts/credentials.json`.
2.  **Secure the file** (on Linux/macOS):
    ```bash
    chmod 600 .claude/scripts/credentials.json
    ```

✅ **Verification:** The file `.claude/scripts/credentials.json` exists and is secured.

---

## 📦 Step 2: Install Python Dependencies (Per Project or Globally)

The sync scripts require some Python libraries.

### Option A: Automatic Setup via MADIO command (Recommended)
Run the following command from your project root:
```bash
/madio-enable-sync
```
This command typically:
- Checks for Python.
- May guide you to set up a virtual environment within `.claude/scripts/venv/`.
- Installs dependencies from `.claude/scripts/requirements.txt`.

### Option B: Manual Setup
If `/madio-enable-sync` is not available or you prefer manual setup:
```bash
# Navigate to the scripts directory
cd .claude/scripts

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# When done, you can deactivate (if you used a venv)
# deactivate
```
The key dependencies usually include `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`.

✅ **Verification:** You can run `python3 .claude/scripts/sync_to_docs.py --help` without import errors.

---

##  🛠️ Step 3: Understanding `.madio/document_registry.json`

MADIO now uses a central file `.madio/document_registry.json` to manage all aspects of your documents. You generally don't need to edit this file manually; commands like `/madio-import-docs`, `/madio-update-docs`, and `/push-to-docs` will manage it for you.

Key parts of this registry include:
-   **`document_registry` (object):** A dictionary where each key is a project-relative path to a local markdown file. The value contains:
    -   `local_path`: The path itself.
    -   `google_doc_id`: The ID of the linked Google Doc.
    -   `local_sha256_hash`: Hash of the local file content.
    -   `google_doc_version`: Version of the Google Doc content.
    -   `status`: Sync status (e.g., "active", "local_only", "conflict").
    -   Other timestamps and metadata.
-   **`sync_preferences` (object):**
    -   `google_drive_folder`: Stores the `name` and `id` of the Google Drive folder where your MADIO documents are synced.
    -   `interaction_mode`: Controls interactivity of scripts.

**How documents get into the registry for syncing:**
-   Using `/madio-import-docs` to import existing markdown files.
-   Using `/madio-update-docs --add path/to/file.md` to add a specific file.
-   If you have an old project, using `/madio-migrate-config` to convert old configs.

---

## 🚀 Step 4: Your First Sync with `/push-to-docs`

Once you have:
1.  `credentials.json` in place.
2.  Python dependencies installed.
3.  Documents listed in your `.madio/document_registry.json` (e.g., after import or add).

You can perform your first sync:

```bash
/push-to-docs
```

**What to expect on the very first run:**
1.  🔐 **Authentication:** Your web browser should open, asking you to log in to your Google account and grant permission for the application ("MADIO Desktop Sync Client" or whatever you named it) to access your Google Docs and Google Drive. Review the permissions and accept. After authorization, you might be shown a message like "Authentication successful, you can close this tab." The script will store an access token (e.g., `token.pickle` or `token.json`) in `.claude/scripts/` for future use.
2.  📁 **Folder Setup:** If no Google Drive folder is configured in `sync_preferences` (which is true for a brand new setup), `sync_to_docs.py` (called by `/push-to-docs`) will prompt you:
    ```
    📁 Google Drive Folder Configuration
       Choose a Google Drive folder for your MADIO documents.
       - Press Enter to use the root 'My Drive' folder.
       - Type a folder name (e.g., 'My AI Project Docs').
       - If the folder doesn't exist, you'll be asked to create it.
    Enter folder name (or press Enter for root 'My Drive'):
    ```
    Enter your desired folder name. If it doesn't exist, it will ask to create it. This preference will be saved in `.madio/document_registry.json`.
3.  📄 **Document Creation/Update:** For each document in the registry:
    *   If it doesn't have a `google_doc_id` (or it's marked for creation), a new Google Doc will be created in the chosen folder.
    *   Its content will be set from your local markdown file.
    *   The new `google_doc_id`, `google_doc_version`, `local_sha256_hash`, and timestamps will be saved in the registry.
4.  ✅ **Success:** You'll see output indicating which files were processed and their new Google Doc URLs. A `google_docs_urls.txt` file might also be created in your project root for easy reference.

**Subsequent Syncs:**
Running `/push-to-docs` again will:
- Use the saved folder preference.
- Update existing Google Docs if local files have changed (based on hash comparison).
- Create new Google Docs for any newly added files in the registry marked as `local_only` or similar.
- Handle potential stale mappings or conflicts (possibly with prompts, based on Phase 2/3 implementations).

---

## ✅ Step 5: Verification & Usage

-   **Check Google Drive:** Open Google Drive and find the folder you specified. Your documents should be there.
-   **Verify Content:** Open a synced Google Doc and compare its content with your local markdown file.
-   **Edit Locally & Re-sync:** Make a change to a local markdown file and run `/push-to-docs` again. Verify the Google Doc updates.
-   **Check Status:** Use `/sync-status` to see the health of your sync setup. Use `/sync-status --repair` if it reports fixable issues.
-   **Manage Documents:** Use `/madio-update-docs` to add or remove documents from the sync process.

---

## 🔧 Troubleshooting Common Issues

-   **`credentials.json` not found:** Ensure it's correctly named and placed in `.claude/scripts/`.
-   **Authentication errors (401/403):**
    -   Delete `.claude/scripts/token.pickle` (or `token.json`) and re-run `/push-to-docs` to re-authenticate.
    -   Ensure Google Docs and Drive APIs are enabled in your Cloud Project.
    -   Verify your OAuth Consent Screen is correctly configured (especially test users if app is in testing).
    -   Check that `credentials.json` has the correct OAuth scopes (though `sync_to_docs.py` requests them).
-   **Folder prompt skipped in Claude Code CLI:** This was BUG-001. Recent versions (post-Phase 1 fix) should handle this better by attempting direct TTY access or guiding you to use `/push-to-docs --folder "Your Folder Name"` if interaction fails.
-   **Python Import Errors:** Ensure you've installed dependencies from `requirements.txt` (Step 2). If using a virtual environment, make sure it's activated when running scripts manually.

For further issues, consult the main `README.md` or specific command documentation.
The `/madio-doctor` command (if available and updated for the new registry system) can also help diagnose setup problems.

---

*✅ **Setup Complete!** Your MADIO project should now be configured to sync with Google Docs using the `.madio/document_registry.json` system.*
