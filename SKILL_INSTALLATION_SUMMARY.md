# GitHub Trending Peek Skill - Installation Summary

## 🎉 Skill Successfully Created!

Your new skill **"github-trending-peek"** has been installed and is ready to use.

---

## 📁 Skill Location

```
/mnt/skills/user/github-trending-peek/
├── SKILL.md              # Skill definition (read by Claude)
├── README.md             # Full documentation
├── QUICKSTART.md         # Quick reference guide
├── requirements.txt      # Python dependencies
└── scripts/
    ├── crawl_trending.py # Main crawler (Step 1)
    ├── send_email.py     # Email sender (Step 2)
    └── test_skill.py     # Demo/test script
```

---

## 🚀 How It Works

### Step 1: Crawl GitHub Trending
- Fetches top 5 repositories from https://github.com/trending
- Ranks by stars and forks
- Retrieves README files for each project
- Generates JSON and HTML summary files

### Step 2: Analyze & Summarize
- Extracts project information
- Identifies tech stacks used
- Finds common patterns
- Calculates statistics

### Step 3: Generate Reports
- Creates `trending_summary.json` (structured data)
- Creates `trending_summary.html` (beautiful report)

### Step 4: Email Delivery (Optional)
- Sends reports to **yqing999@gmail.com**
- Attaches JSON and HTML files
- Includes inline summary in email body

---

## 💬 Usage Examples

### Ask Claude:
```
"Show me what's trending on GitHub"
"Check the top GitHub projects today"
"Send me a GitHub trending report"
"What are the hottest repos right now?"
```

### Manual Execution:
```bash
cd /mnt/skills/user/github-trending-peek/scripts

# Fetch trending repos and create reports
python3 crawl_trending.py

# Send via email (optional)
python3 send_email.py
```

---

## 📧 Email Configuration

The email feature is **optional**. Without SMTP credentials, the script will save an `.eml` file you can open with any email client.

### To Enable Email Sending:

#### For Gmail Users:
1. Enable 2-factor authentication in your Google Account
2. Generate an App Password:
   - Go to: Google Account → Security → App passwords
   - Create a new app password
3. Set environment variables:

```bash
export SMTP_SERVER='smtp.gmail.com'
export SMTP_EMAIL='your-email@gmail.com'
export SMTP_PASSWORD='your-app-password'
```

#### For Other Email Providers:
```bash
export SMTP_SERVER='smtp.yourdomain.com'
export SMTP_PORT='587'  # Optional, defaults to 587
export SMTP_EMAIL='your-email@example.com'
export SMTP_PASSWORD='your-password'
```

---

## 🎨 Sample Output

### Console Output:
```
Fetching GitHub trending repositories...

Found 5 repositories. Fetching READMEs...
  - owner/awesome-project
  - team/cool-library
  - dev/useful-tool
  - org/innovative-framework
  - user/popular-app

Generating summary...

✅ Complete! Files saved:
  - trending_summary.json
  - trending_summary.html
```

### JSON Output Structure:
```json
{
  "generated_at": "2026-02-07T15:30:00",
  "total_repos": 5,
  "repositories": [
    {
      "name": "owner/project",
      "url": "https://github.com/owner/project",
      "description": "An amazing project",
      "language": "Python",
      "stars_today": 250,
      "total_stars": 15000,
      "forks": 2500,
      "readme_preview": "..."
    }
  ],
  "insights": {
    "most_common_language": "Python",
    "total_stars": 75000,
    "total_forks": 12000
  }
}
```

### HTML Report Features:
- ✅ Clean, professional design
- ✅ Color-coded stats
- ✅ Language tags
- ✅ Clickable repository links
- ✅ Responsive layout
- ✅ Insights summary section

---

## 🛠️ Customization Options

### Change Number of Repositories
Edit `crawl_trending.py`, line ~110:
```python
repos = fetch_trending_repos(limit=10)  # Change from 5
```

### Change Email Recipient
Option 1 - Edit default in `send_email.py`, line ~106:
```python
to_email = 'new-email@example.com'
```

Option 2 - Pass as command line argument:
```bash
python3 send_email.py different-email@example.com
```

### Customize HTML Styling
Edit the CSS in `crawl_trending.py`, function `save_to_html()` around line 226

### Customize Email Template
Edit `send_email.py`, function `create_email_body()` around line 128

---

## 📦 Dependencies

The skill requires these Python packages:
- **requests** - For HTTP requests
- **beautifulsoup4** - For HTML parsing
- **smtplib** - For email (built-in)
- **email** - For email formatting (built-in)

Already installed! To reinstall:
```bash
pip install -r requirements.txt --break-system-packages
```

---

## 🔧 Testing the Skill

Run the test script to see a demo:
```bash
cd /mnt/skills/user/github-trending-peek/scripts
python3 test_skill.py
```

This will show:
- Skill structure
- Mock data example
- Usage instructions

---

## ⚡ Automation Ideas

### Daily Reports via Cron
Add to your crontab:
```bash
# Run every day at 9 AM
0 9 * * * cd /mnt/skills/user/github-trending-peek/scripts && python3 crawl_trending.py && python3 send_email.py
```

### Weekly Digest
```bash
# Run every Monday at 8 AM
0 8 * * 1 cd /mnt/skills/user/github-trending-peek/scripts && python3 crawl_trending.py && python3 send_email.py
```

---

## 🐛 Troubleshooting

### Issue: "No repositories found"
- **Cause**: GitHub may have changed their HTML structure
- **Solution**: Check if trending page is accessible, update parsing logic

### Issue: "Email sending failed"
- **Cause**: Invalid SMTP credentials
- **Solution**: 
  - Check environment variables are set correctly
  - For Gmail, use App Password (not regular password)
  - Script will save .eml file as fallback

### Issue: "README not available"
- **Cause**: Repository doesn't have a README file
- **Solution**: This is normal, script handles gracefully

### Issue: GitHub rate limiting
- **Cause**: Too many requests too quickly
- **Solution**: Script includes delays, but you can increase them in `crawl_trending.py`

---

## 📚 Documentation Files

1. **SKILL.md** - Main skill definition (for Claude)
2. **README.md** - Comprehensive documentation
3. **QUICKSTART.md** - Quick reference guide
4. **requirements.txt** - Python dependencies
5. **This file** - Installation summary

---

## 🎯 What Gets Analyzed

For each trending repository, the skill collects:

- ✅ Repository name
- ✅ GitHub URL
- ✅ Project description
- ✅ Programming language/tech stack
- ✅ Total star count
- ✅ Stars gained today
- ✅ Fork count
- ✅ README content

Plus aggregate insights:
- ✅ Most common programming language
- ✅ Total stars across all repos
- ✅ Total forks across all repos
- ✅ Common themes or patterns

---

## 🎊 Next Steps

1. **Test it out**: Ask Claude "Show me what's trending on GitHub"
2. **Configure email** (optional): Set up SMTP credentials
3. **Customize**: Adjust number of repos, styling, etc.
4. **Automate**: Set up cron jobs for regular reports
5. **Share**: Use the reports to stay updated on trending tech!

---

## 💡 Pro Tips

- Run the skill in the morning to catch overnight trending projects
- Compare reports over time to see trends
- Use the JSON output for data analysis or integrations
- Share the HTML report with your team
- Filter trending by language (edit the URL in script)

---

## 📝 License & Credits

This skill is part of your Claude skills ecosystem. Feel free to modify and customize it for your needs!

**Created**: February 7, 2026
**Version**: 1.0.0
**Default Email**: yqing999@gmail.com

---

## 🙏 Support

If you need help:
1. Read the QUICKSTART.md for quick reference
2. Check the README.md for detailed docs
3. Review the test_skill.py for examples
4. Ask Claude for assistance!

**Enjoy discovering trending GitHub projects! 🚀**
