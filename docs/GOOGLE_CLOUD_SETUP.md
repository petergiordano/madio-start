# Google Cloud Setup Guide for MADIO Docs Sync

This guide walks you through setting up Google Cloud credentials required for the optional MADIO Google Docs synchronization feature. This allows the script to access your Google Docs on your behalf.

**Estimated time: 10-15 minutes**

**Prerequisites:**
*   A Google account (e.g., Gmail, Google Workspace).
*   Access to the internet and a web browser.

**Important Note on Account Selection:**
Ensure you are logged into the Google account you intend to use for this project. This account will be associated with the Google Cloud Project you create/use, and the credentials will allow access to Google Docs owned by or shared with this account.

---

## Steps to Configure Google Cloud and Get Credentials:

1.  **Navigate to Google Cloud Console:**
    *   Open your web browser and go to [https://console.cloud.google.com/](https://console.cloud.google.com/).
    *   Sign in with your chosen Google account if prompted.

2.  **Create or Select a Google Cloud Project:**
    *   **If you don't have a project or want a new one:**
        *   Click the project selector dropdown at the top of the page (it might say "Select a project" or show an existing project name).
        *   Click **"NEW PROJECT"**.
        *   Enter a **Project name** (e.g., "My MADIO Sync", "Docs Sync Project"). The Project ID will be auto-generated.
        *   Select a Billing account if prompted (many services, including basic API access needed here, have a free tier, but a billing account might be required by Google Cloud for project creation).
        *   Select an Organization or Location if applicable (usually "No organization" is fine for personal projects).
        *   Click **"CREATE"**.
    *   **If you have an existing project you want to use:**
        *   Click the project selector dropdown and choose your desired project.
    *   <!-- Consider adding screenshot of project creation/selection -->

3.  **Enable the Google Docs API:**
    *   Once your project is selected, use the search bar at the top of the Google Cloud Console (or navigate via the menu ☰ to "APIs & Services" > "Library").
    *   Search for **"Google Docs API"**.
    *   Click on "Google Docs API" in the search results.
    *   Click the **"ENABLE"** button. If it's already enabled, you'll see "MANAGE".
    *   <!-- Consider adding screenshot of API Library search and enabling Google Docs API -->

4.  **Configure the OAuth Consent Screen:**
    *   Before creating credentials, you might need to configure the OAuth consent screen.
    *   In the navigation menu (☰), go to **"APIs & Services" > "OAuth consent screen"**.
    *   **User Type:** Choose **"External"** if you are using a standard Gmail account. If you are using a Google Workspace account and only users within your organization will use this, you might choose "Internal". For most individual users, "External" is appropriate. Click **"CREATE"**.
    *   **App information:**
        *   **App name:** Enter a name for the application (e.g., "MADIO Docs Sync Tool", "My Local Docs Script"). This is what you'll see during the consent flow.
        *   **User support email:** Select your email address.
        *   **App logo:** Optional.
    *   **Developer contact information:** Enter your email address.
    *   Click **"SAVE AND CONTINUE"** through the "Scopes" and "Test users" sections. For this type of script (Desktop app), you don't need to add scopes or test users here; the script will request scopes locally. If you are in "testing" mode for an "External" app, Google might later require you to add test users or publish the app if it's used broadly, but for personal use, this is usually not an immediate issue.
    *   Review the summary and click **"BACK TO DASHBOARD"**.
    *   <!-- Consider adding screenshot of OAuth consent screen setup -->

5.  **Create OAuth 2.0 Credentials:**
    *   In the navigation menu (☰), go to **"APIs & Services" > "Credentials"**.
    *   Click **"+ CREATE CREDENTIALS"** at the top of the page.
    *   Select **"OAuth client ID"** from the dropdown menu.
    *   **Application type:** Choose **"Desktop app"** from the dropdown. This is crucial.
    *   **Name:** You can leave the default name (e.g., "Desktop client 1") or give it a more descriptive name like "MADIO Sync Desktop Client".
    *   Click **"CREATE"**.
    *   <!-- Consider adding screenshot of OAuth Client ID creation for Desktop app -->

6.  **Download Credentials File:**
    *   A dialog box "OAuth client created" will appear, showing your Client ID and Client secret. You don't need to copy these directly.
    *   Click the **"DOWNLOAD JSON"** button (or a download icon 📥 next to your newly created Desktop app client ID in the credentials list).
    *   The file will be downloaded by your browser. It will likely be named something like `client_secret_[long_ID_here].json`.
    *   **Important:** Rename this downloaded file to exactly `credentials.json`.

7.  **Place `credentials.json` File:**
    *   Move the renamed `credentials.json` file into the `.claude/scripts/` directory within your MADIO project.
    *   The full path should be `[Your_MADIO_Project_Root]/.claude/scripts/credentials.json`.

---

## Verification and Next Steps

Once you have placed `credentials.json` in the correct location:

*   You can proceed with the `/madio-enable-sync` command in the Claude Code CLI if you haven't already. It will guide you through the rest of the sync setup.
*   The first time the sync script runs (usually triggered by `/madio-enable-sync` or `/push-to-docs`), it will open a browser window asking you to authorize the "app" (which you named in the OAuth consent screen) to access your Google Docs. You must grant this permission.
*   After granting permission, a `token.pickle` file will be created in `.claude/scripts/` to store your authorization, so you don't have to re-authorize every time.

## Security Reminders:
*   The `credentials.json` file contains sensitive information. **Do not commit it to Git or share it publicly.** The `.gitignore` file in this project should already be configured to ignore it.
*   The `token.pickle` file also contains sensitive access tokens and should also be ignored by Git.
*   This setup grants the script permission to manage your Google Docs files. Ensure you understand the script's functionality.

## Troubleshooting Common Issues:

*   **`Error 400: redirect_uri_mismatch` during authorization:** You likely did not select "Desktop app" as the Application type when creating OAuth Client ID (Step 5). Delete the incorrect credential, create a new one ensuring "Desktop app" is selected, and re-download/rename `credentials.json`.
*   **`Error 403: access_denied` or similar permission errors:**
    *   Ensure the Google Docs API is enabled for your project (Step 3).
    *   If your OAuth consent screen is in "testing" mode and your Google account is not listed as a "Test user", you might encounter this. For personal use with your own account, this usually isn't an issue.
*   **`FileNotFoundError: [Errno 2] No such file or directory: 'credentials.json'` when running the script:** Ensure you have placed the renamed `credentials.json` file in the correct location: `.claude/scripts/credentials.json`.
*   **Script hangs or browser doesn't open for authorization:** Check your system's default browser settings and any pop-up blockers.

If you encounter other issues, refer to the official Google Cloud and Google APIs documentation.