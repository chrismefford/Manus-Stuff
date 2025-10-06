# Multi-Subreddit Reddit Leadership Automation

Automated system that monitors **7 leadership and management subreddits** every 3 hours, generates thought-provoking questions and high-quality responses based on "Leadership Is Overrated" by Chris Mefford and Kyle Buckett, and automatically posts content to Google Docs with bold formatting and clear visual separators.

## Monitored Subreddits

1. **r/Leadership** - Leadership philosophy, team dynamics, empowerment
2. **r/managers** - Practical management advice for supervisors and team leads
3. **r/AskManagers** - Q&A about workplace dynamics and management challenges
4. **r/Work** - General workplace culture and job issues across industries
5. **r/Executives** - Strategic thinking and decision-making for senior leaders
6. **r/BadBosses** - Constructive reframing of negative leadership experiences
7. **r/antiwork** - Systemic workplace issues and employee empowerment

## Features

- ✅ Monitors 7 subreddits for new discussions
- ✅ Generates 1 thought-provoking question per subreddit (7 total per run)
- ✅ Creates 3 high-quality responses per subreddit (21 total per run)
- ✅ Tailors tone and focus for each community
- ✅ Automatically posts to Google Docs with bold formatting
- ✅ Clear visual separators (block characters) for each subreddit
- ✅ Runs every 3 hours via GitHub Actions
- ✅ No server or infrastructure required

## Setup Instructions

### 1. Create a GitHub Repository

1. Go to https://github.com/new
2. Name your repository (e.g., `reddit-leadership-automation`)
3. Set it to **Private** (recommended to keep your credentials secure)
4. Click "Create repository"

### 2. Upload Files

Upload all files from this directory to your GitHub repository:
- `.github/workflows/reddit-automation.yml`
- `reddit_automation.py`
- `update_and_format_docs.py`
- `book_summary.md`
- `requirements.txt`
- `README.md`

### 3. Set Up GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

#### OPENAI_API_KEY
Your OpenAI API key (already configured in your environment)

#### GOOGLE_CREDENTIALS
The contents of your `credentials.json` file. To get this:
```bash
cat /home/ubuntu/credentials.json
```
Copy the entire JSON output and paste it as the secret value.

#### GOOGLE_TOKEN
The contents of your `token.json` file. To get this:
```bash
cat /home/ubuntu/token.json
```
Copy the entire JSON output and paste it as the secret value.

### 4. Enable GitHub Actions

1. Go to your repository → Actions tab
2. Click "I understand my workflows, go ahead and enable them"
3. The automation will now run every 3 hours automatically

### 5. Manual Trigger (Optional)

You can manually trigger a run anytime:
1. Go to Actions tab
2. Click "Reddit Leadership Automation"
3. Click "Run workflow"
4. Click the green "Run workflow" button

## How It Works

### Schedule
- Runs every 3 hours automatically (00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 UTC)
- **PST times:** 1 AM, 4 AM, 7 AM, 10 AM, 1 PM, 4 PM, 7 PM, 10 PM
- Approximately 8 runs per day
- Generates ~56 questions and ~168 responses daily (across all subreddits)

### Content Generation
1. Fetches latest posts from all 7 subreddits
2. Uses OpenAI API to generate content tailored to each community's tone
3. Creates thought-provoking questions with detailed post bodies
4. Generates helpful, empathetic responses to existing discussions

### Subreddit-Specific Tones

Each subreddit gets content tailored to its community:

- **r/Leadership**: Thought-provoking, challenges conventional wisdom
- **r/managers**: Practical, actionable day-to-day advice
- **r/AskManagers**: Helpful, direct answers to specific questions
- **r/Work**: Broad, relatable insights across industries
- **r/Executives**: Strategic, high-level thinking
- **r/BadBosses**: Empathetic, constructive reframing (not defensive)
- **r/antiwork**: Constructive, validates concerns, systemic insights

### Google Docs Integration
Content is automatically posted to two Google Docs:
- **Questions Doc**: Thought-provoking questions you can post
- **Comments Doc**: Responses to existing discussions

**Visual Organization:**
- Each subreddit section has distinctive block separators (████)
- Headers and titles are automatically formatted in bold
- Easy to scan and find content for specific subreddits

## Your Workflow

1. **Check Google Docs** once or twice daily
2. **Scan by subreddit** using the visual separators
3. **Select best content** - Choose 1-2 questions and 3-5 responses per day
4. **Post to appropriate subreddit** - Match content to the right community
5. **Engage** - Respond to replies and build relationships

## Google Docs Links

- Questions: https://docs.google.com/document/d/1CYECMcw8pPu-a7H27ChbKcRWVnV7PQJKy5QHsSvJElw/edit
- Comments: https://docs.google.com/document/d/1trD4JzyBQtHEKXt0lVWPfayGo89kM182T_HXAupYP3A/edit

## Monitoring

### Check if it's working:
1. Go to your repository → Actions tab
2. You'll see a list of workflow runs with timestamps
3. Click on any run to see detailed logs
4. Green checkmark = successful run
5. Red X = failed run (check logs for errors)

### Verify in Google Docs:
- New content should appear every 3 hours
- Look for block separators (████) with subreddit names
- Each section has a timestamp in the format "GENERATED: YYYY-MM-DD HH:MM:SS"

## Output Per Run

- **7 questions** (1 per subreddit)
- **21 responses** (3 per subreddit)
- **Runtime:** ~3-5 minutes per run

## Daily Output

- **~56 questions** across all subreddits
- **~168 responses** across all subreddits
- **Your action:** Post 1-2 questions + 3-5 responses daily (be selective!)

## Troubleshooting

### Automation not running
- Check Actions tab for error messages
- Verify all three secrets are set correctly
- Make sure GitHub Actions is enabled

### Google Docs not updating
- Check that GOOGLE_TOKEN hasn't expired
- Verify document IDs are correct in the scripts
- Check workflow logs for API errors

### Content quality issues
- Review `book_summary.md` to ensure key themes are captured
- Adjust prompts in `reddit_automation.py` if needed
- Check that subreddit-specific tones are appropriate

## File Descriptions

- **reddit_automation.py**: Main multi-subreddit automation script
- **update_and_format_docs.py**: Google Docs integration with formatting
- **book_summary.md**: Key themes and concepts from the book
- **requirements.txt**: Python dependencies
- **.github/workflows/reddit-automation.yml**: GitHub Actions workflow configuration

## Best Practices

### Posting to Reddit
- ✅ Be selective - don't post everything generated
- ✅ Match content to the right subreddit
- ✅ Space out posts throughout the day (max 1-2 per subreddit per day)
- ✅ Edit content to match your voice
- ✅ Engage with replies authentically
- ❌ Don't flood any single subreddit
- ❌ Don't mention your book (no self-promotion)
- ❌ Don't be defensive in r/BadBosses or r/antiwork

### Content Quality
- Review before posting
- Choose pieces that feel genuine and helpful
- Skip anything that doesn't resonate
- Quality over quantity
- Respect each community's culture

### Subreddit-Specific Tips
- **r/antiwork**: Be constructive, validate concerns, avoid defending management
- **r/BadBosses**: Show empathy, focus on learning from negative examples
- **r/Executives**: Keep it strategic and high-level
- **r/managers**: Be practical and actionable
- **r/AskManagers**: Answer the specific question directly

## Cost Estimate

- **GitHub Actions**: Free (2,000 minutes/month on free tier, this uses ~40 minutes/day)
- **OpenAI API**: ~$3-5 per day (7 subreddits × 8 runs/day)
- **Google Docs API**: Free

## Security Notes

- Repository should be set to **Private** to protect your credentials
- Never commit `credentials.json` or `token.json` directly to the repository
- All sensitive data is stored in GitHub Secrets (encrypted)
- Credentials are only created temporarily during workflow runs and deleted after

## Support

If you encounter issues:
1. Check the Actions tab for error logs
2. Verify all secrets are set correctly
3. Ensure Google OAuth token hasn't expired
4. Check that document IDs are correct

## License

Private use only.
