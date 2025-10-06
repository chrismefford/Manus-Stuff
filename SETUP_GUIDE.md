# Quick Setup Guide - Multi-Subreddit Automation

Follow these steps to get your automation running on GitHub Actions.

## What This Does

Monitors **7 subreddits** every 3 hours:
- r/Leadership
- r/managers  
- r/AskManagers
- r/Work
- r/Executives
- r/BadBosses
- r/antiwork

Generates:
- **7 questions per run** (1 per subreddit)
- **21 responses per run** (3 per subreddit)
- **~56 questions + ~168 responses per day**

Posts everything to your Google Docs with clear visual separators for each subreddit.

---

## Step 1: Get Your Credentials

Run this command to get the values you'll need:

```bash
/home/ubuntu/reddit-leadership-automation/GET_SECRETS.sh
```

This displays:
- **OPENAI_API_KEY**
- **GOOGLE_CREDENTIALS** (JSON)
- **GOOGLE_TOKEN** (JSON)

**Copy these - you'll need them in Step 4!**

---

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `reddit-leadership-automation` (or any name you prefer)
3. **Important**: Set to **Private** (to keep your credentials secure)
4. Click "Create repository"

---

## Step 3: Upload Files

### Option A: Using GitHub Web Interface

1. On your new repository page, click "uploading an existing file"
2. Drag and drop all files from the `reddit-leadership-automation` folder
3. Commit the files

### Option B: Using Git Command Line

```bash
cd /home/ubuntu/reddit-leadership-automation
git init
git add .
git commit -m "Initial commit - Multi-subreddit automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/reddit-leadership-automation.git
git push -u origin main
```

---

## Step 4: Add GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. In left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Add these 3 secrets:

#### Secret 1: OPENAI_API_KEY
- Name: `OPENAI_API_KEY`
- Value: Paste the output from Step 1 (OPENAI_API_KEY)
- Click "Add secret"

#### Secret 2: GOOGLE_CREDENTIALS
- Click "New repository secret" again
- Name: `GOOGLE_CREDENTIALS`
- Value: Paste the entire JSON from Step 1 (GOOGLE_CREDENTIALS)
- Click "Add secret"

#### Secret 3: GOOGLE_TOKEN
- Click "New repository secret" again
- Name: `GOOGLE_TOKEN`
- Value: Paste the entire JSON from Step 1 (GOOGLE_TOKEN)
- Click "Add secret"

---

## Step 5: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. Done! The automation will now run every 3 hours

---

## Step 6: Test It (Optional)

To test immediately without waiting 3 hours:

1. Go to **Actions** tab
2. Click "Reddit Leadership Automation" in the left sidebar
3. Click "Run workflow" button (top right)
4. Click the green "Run workflow" button
5. Wait 3-5 minutes (processing 7 subreddits takes time)
6. Check your Google Docs for new content!

---

## Verification

### Check if it's running:
1. Go to **Actions** tab
2. You'll see workflow runs listed with timestamps
3. Green checkmark ✅ = Success
4. Red X ❌ = Failed (click to see error logs)
5. Each run takes ~3-5 minutes

### Check Google Docs:
- Questions: https://docs.google.com/document/d/1CYECMcw8pPu-a7H27ChbKcRWVnV7PQJKy5QHsSvJElw/edit
- Comments: https://docs.google.com/document/d/1trD4JzyBQtHEKXt0lVWPfayGo89kM182T_HXAupYP3A/edit

Look for content with **block separators** (████) showing each subreddit name.

---

## Schedule - PST Times

The automation runs **8 times per day** at:

1. **1:00 AM** PST
2. **4:00 AM** PST
3. **7:00 AM** PST
4. **10:00 AM** PST
5. **1:00 PM** PST
6. **4:00 PM** PST
7. **7:00 PM** PST
8. **10:00 PM** PST

---

## Understanding Your Google Docs

Content is organized by subreddit with clear visual separators:

```
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
SUBREDDIT: r/managers
GENERATED: 2025-10-05 21:04:18
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████

QUESTION 1 — r/managers
--------------------------------------------------------------------------------
TITLE: [Question title]

POST BODY:
[Question content]
```

This makes it **super easy to scan** and find content for specific subreddits!

---

## Daily Workflow

1. **Check Google Docs** once or twice daily
2. **Scan by subreddit** using the block separators
3. **Select 1-2 questions** to post (across all subreddits)
4. **Select 3-5 responses** to post (across all subreddits)
5. **Match content to subreddit** - post to the right community
6. **Engage with replies**

**Important**: Don't post everything! Be selective and space out your posts.

---

## Output Per Run

- 7 questions (1 per subreddit)
- 21 responses (3 per subreddit)
- Takes ~3-5 minutes to complete

## Daily Output

- ~56 questions total
- ~168 responses total
- **You should post:** 1-2 questions + 3-5 responses per day

---

## Troubleshooting

### "Workflow not found" error
- Make sure you uploaded the `.github/workflows/reddit-automation.yml` file
- The folder structure must be exactly: `.github/workflows/`

### "Secret not found" error
- Double-check all 3 secrets are added with exact names (case-sensitive)
- Make sure you pasted the complete JSON for credentials and token

### Google Docs not updating
- Check Actions logs for errors
- Verify document IDs in the scripts match your Google Docs

### Automation taking too long
- Normal! Processing 7 subreddits takes 3-5 minutes
- Check the Actions logs to see progress

### Still having issues?
- Check the Actions tab for detailed error logs
- Each workflow run shows step-by-step what happened

---

## Best Practices

### Posting Strategy
- ✅ Post max 1-2 items per subreddit per day
- ✅ Space out posts throughout the day
- ✅ Match content tone to each community
- ✅ Edit to match your voice
- ❌ Don't flood any single subreddit
- ❌ Don't cross-post the same content

### Subreddit-Specific Tips
- **r/antiwork**: Be constructive, validate concerns
- **r/BadBosses**: Show empathy, avoid being defensive
- **r/Executives**: Keep it strategic
- **r/managers**: Be practical and actionable

---

## You're Done!

Your automation is now running on GitHub Actions. It will:
- ✅ Run every 3 hours automatically
- ✅ Generate fresh content from 7 subreddits
- ✅ Post to your Google Docs with clear organization
- ✅ Require no maintenance or manual intervention

Just check your Google Docs daily, select the best content, and post to Reddit!
