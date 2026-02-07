# GitHub Trending Peek - Quick Reference

## Installation Complete! ✅

Your skill is now available at:
`/mnt/skills/user/github-trending-peek/`

## Usage

### Via Claude (Recommended)
Just ask Claude any of these:
- "Show me what's trending on GitHub"
- "What are the top GitHub projects today?"
- "Check GitHub trending repositories"
- "Send me a GitHub trending report"

### Manual Execution
```bash
cd /mnt/skills/user/github-trending-peek/scripts

# Step 1: Fetch and analyze trending repos
python3 crawl_trending.py

# Step 2: Send via email (optional)
python3 send_email.py
```

## Output Files

After running, you'll get:
- `trending_summary.json` - Structured data
- `trending_summary.html` - Beautiful visual report
- `email_draft_*.eml` - Email file (if no SMTP configured)

## Email Configuration (Optional)

### For Gmail:
1. Enable 2-factor authentication
2. Go to: Google Account → Security → App passwords
3. Generate an app password
4. Set environment variables:

```bash
export SMTP_SERVER='smtp.gmail.com'
export SMTP_EMAIL='your-email@gmail.com'
export SMTP_PASSWORD='your-app-password'
```

### Default Recipient
The default email recipient is: **yqing999@gmail.com**

To change it, edit `send_email.py` or pass as argument:
```bash
python3 send_email.py different-email@example.com
```

## Customization

### Change number of repos
Edit `crawl_trending.py`, line 110:
```python
repos = fetch_trending_repos(limit=10)  # Change from 5 to 10
```

### Change HTML styling
Edit `crawl_trending.py`, function `save_to_html()` around line 226

### Change email template
Edit `send_email.py`, function `create_email_body()` around line 128

## Dependencies

Required packages (already installed):
- requests
- beautifulsoup4

To reinstall:
```bash
pip install -r requirements.txt --break-system-packages
```

## Troubleshooting

### Email not sending?
- Check SMTP credentials are set correctly
- For Gmail, use App Password (not regular password)
- Without credentials, an .eml file will be saved instead

### GitHub rate limiting?
- The script includes delays to be respectful
- If still limited, increase delays in `crawl_trending.py`

### No README found?
- Some repos may not have README files
- Script will show "README not available"

## What Gets Analyzed?

For each repository:
- ✅ Project name and GitHub URL
- ✅ Description
- ✅ Programming language
- ✅ Total stars count
- ✅ Today's star growth
- ✅ Fork count
- ✅ README content (first 500 chars in summary)

Plus overall insights:
- Most common programming language
- Total stars across all repos
- Total forks across all repos

## Next Steps

1. Try it out: Ask Claude to check trending repos
2. Configure email (optional)
3. Customize the number of repos or styling
4. Set up a daily cron job to get automatic reports

Enjoy discovering trending projects! 🚀
