---
name: github-trending-peek
description: Automatically fetch and analyze the top 5 trending GitHub repositories, including their README files, and generate a comprehensive summary with project details, tech stacks, and insights. Optionally sends the report via email. Use when users want to discover trending GitHub projects, get summaries of popular repositories, track GitHub trending topics, or receive automated GitHub trend reports.
---

# GitHub Trending Peek

This skill automatically discovers and analyzes trending GitHub repositories, providing comprehensive summaries and insights about the hottest projects on GitHub.

## What This Skill Does

1. **Crawls GitHub Trending**: Fetches the top 5 trending repositories from https://github.com/trending
2. **Analyzes Projects**: Collects detailed information including:
   - Project name and URL
   - Description
   - Star count (total and today's growth)
   - Fork count
   - Programming language/tech stack
   - README content
3. **Generates Summary**: Creates a comprehensive report with:
   - Individual project summaries
   - Common patterns and insights
   - Tech stack analysis
4. **Multiple Output Formats**: 
   - JSON file (structured data)
   - HTML file (beautifully formatted report)
   - Optional email delivery

## When to Use This Skill

Trigger this skill when the user:
- Asks about "trending GitHub projects" or "popular GitHub repos"
- Wants to "discover what's hot on GitHub"
- Requests "top GitHub repositories"
- Asks to "check GitHub trending"
- Wants a "summary of trending open source projects"
- Requests automated GitHub trend reports
- Wants to stay updated on popular development projects

## Implementation

### Step 1: Crawl and Analyze

Run the crawler script to fetch trending repositories:

```bash
cd /mnt/skills/user/github-trending-peek/scripts
python3 crawl_trending.py
```

This script:
- Fetches the top 5 repositories by stars and forks
- Retrieves each repository's README file
- Generates `trending_summary.json` and `trending_summary.html`

### Step 2: Send Email (Optional)

If the user wants the report sent via email:

```bash
python3 send_email.py
```

By default, this sends to: yqing999@gmail.com

**Note**: Email sending requires SMTP credentials. Without them, the script will save an `.eml` file that can be opened with any email client.

To configure email sending, set these environment variables:
```bash
export SMTP_SERVER='smtp.gmail.com'
export SMTP_EMAIL='your-email@gmail.com'
export SMTP_PASSWORD='your-app-password'
```

## Output Format

### JSON Output
Structured data including:
- Generated timestamp
- Repository details (name, URL, description, language)
- Statistics (stars, forks, today's growth)
- README preview
- Insights (common languages, totals)

### HTML Output
Beautifully formatted report with:
- Visual card layout for each repository
- Color-coded stats and language tags
- Clickable links to repositories
- Summary insights section

## Dependencies

Required Python packages:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- Standard library: `smtplib`, `email`, `json`, `datetime`

Install with:
```bash
pip install requests beautifulsoup4 --break-system-packages
```

## Example Usage

**User**: "Show me what's trending on GitHub today"

**Claude**: 
1. Runs `crawl_trending.py` to fetch and analyze top 5 repos
2. Presents summary with key insights
3. Offers to send the full report via email
4. Provides download links to JSON and HTML files

## Best Practices

- **Be Respectful**: Script includes delays between requests to avoid overwhelming GitHub
- **Error Handling**: Gracefully handles missing READMEs or connection issues
- **Flexibility**: Works even without email credentials (saves .eml file instead)
- **Clear Communication**: Explains what it's doing at each step
- **Multiple Formats**: Provides both machine-readable (JSON) and human-readable (HTML) outputs

## Workflow

```
User Request
    ↓
Fetch GitHub Trending Page
    ↓
Parse Top 5 Repositories
    ↓
Fetch README for Each Repo
    ↓
Analyze & Generate Summary
    ↓
Save JSON & HTML Files
    ↓
Optional: Send via Email
    ↓
Present Results to User
```

## Customization

Users can customize:
- Number of repositories (modify `limit=5` in script)
- Email recipient (pass as command line argument)
- Output filenames
- SMTP server settings
- Report styling (edit HTML template in script)

## Important Notes

- GitHub may rate-limit requests - the script includes delays to be respectful
- For Gmail users: Use "App Passwords" instead of regular passwords
- README files are fetched from raw.githubusercontent.com
- The skill works even without email credentials (will save .eml file)
- All files are saved to the current working directory
