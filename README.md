# GitHub Trending Peek

A skill for Claude that automatically discovers and analyzes trending GitHub repositories.

## Features

- 🔥 Fetches top 5 trending repositories from GitHub
- 📊 Analyzes stars, forks, and growth metrics
- 📝 Retrieves and processes README files
- 🎨 Generates beautiful HTML reports
- 📧 Optional email delivery
- 💾 Exports to JSON and HTML formats

## Quick Start

### Prerequisites

```bash
pip install requests beautifulsoup4 --break-system-packages
```

### Usage

Just ask Claude:
- "Show me what's trending on GitHub"
- "What are the top GitHub projects today?"
- "Send me a report of trending repositories"

### Manual Execution

```bash
# Fetch and analyze trending repos
cd scripts
python3 crawl_trending.py

# Send report via email (optional)
python3 send_email.py
```

## Configuration

### Email Setup (Optional)

To enable email sending, set environment variables:

```bash
export SMTP_SERVER='smtp.gmail.com'
export SMTP_EMAIL='your-email@gmail.com'
export SMTP_PASSWORD='your-app-password'
```

**Note**: Without SMTP credentials, the script will save an `.eml` file you can send manually.

### Gmail Users

1. Enable 2-factor authentication
2. Generate an "App Password" in Google Account settings
3. Use the app password (not your regular password)

## Output Files

- `trending_summary.json` - Structured data for processing
- `trending_summary.html` - Beautiful visual report
- `email_draft_*.eml` - Email draft (if SMTP not configured)

## Customization

Edit `crawl_trending.py` to:
- Change number of repos: `fetch_trending_repos(limit=10)`
- Modify output filenames
- Customize HTML styling

Edit `send_email.py` to:
- Change default recipient email
- Customize email template
- Adjust SMTP settings

## Structure

```
github-trending-peek/
├── SKILL.md                    # Skill definition
├── README.md                   # This file
└── scripts/
    ├── crawl_trending.py       # Main crawler
    └── send_email.py           # Email sender
```

## Example Output

The HTML report includes:
- Repository name with clickable link
- Project description
- Star count (total + today's growth)
- Fork count
- Programming language
- Insights section with common patterns

## License

This skill is part of the Claude skills ecosystem.
