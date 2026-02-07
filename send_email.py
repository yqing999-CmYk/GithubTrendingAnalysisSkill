#!/usr/bin/env python3
"""
Email Sender for GitHub Trending Summary
Sends the generated JSON and HTML files to a specified email address.
"""

import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def send_email(
    to_email,
    json_file='trending_summary.json',
    html_file='trending_summary.html',
    smtp_server=None,
    smtp_port=587,
    sender_email=None,
    sender_password=None
):
    """
    Send email with attachments.
    
    Args:
        to_email: Recipient email address
        json_file: Path to JSON summary file
        html_file: Path to HTML summary file
        smtp_server: SMTP server address (e.g., 'smtp.gmail.com')
        smtp_port: SMTP port (default: 587 for TLS)
        sender_email: Sender's email address
        sender_password: Sender's email password or app password
    """
    
    # Check if files exist
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return False
    
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found")
        return False
    
    # Load summary for email body
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            summary_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return False
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email or 'github-trending@noreply.com'
    msg['To'] = to_email
    msg['Subject'] = f"GitHub Trending Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    # Create email body
    email_body = create_email_body(summary_data)
    
    # Attach plain text version
    text_part = MIMEText(email_body['text'], 'plain')
    msg.attach(text_part)
    
    # Attach HTML version
    html_part = MIMEText(email_body['html'], 'html')
    msg.attach(html_part)
    
    # Attach JSON file
    try:
        with open(json_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(json_file)}'
            )
            msg.attach(part)
    except Exception as e:
        print(f"Error attaching JSON file: {e}")
    
    # Attach HTML file
    try:
        with open(html_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(html_file)}'
            )
            msg.attach(part)
    except Exception as e:
        print(f"Error attaching HTML file: {e}")
    
    # Send email
    try:
        # If SMTP credentials provided, use them
        if smtp_server and sender_email and sender_password:
            print(f"Connecting to {smtp_server}:{smtp_port}...")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent successfully to {to_email}")
            return True
        else:
            # No SMTP credentials - save email to file for manual sending
            email_file = f"email_draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.eml"
            with open(email_file, 'w', encoding='utf-8') as f:
                f.write(msg.as_string())
            print(f"⚠️  SMTP credentials not provided.")
            print(f"📧 Email draft saved to: {email_file}")
            print(f"   You can open this file with your email client to send.")
            return True
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        print("\nNote: If using Gmail, you may need to:")
        print("  1. Enable 2-factor authentication")
        print("  2. Generate an 'App Password' in your Google Account settings")
        print("  3. Use the app password instead of your regular password")
        return False


def create_email_body(summary_data):
    """Create email body in both plain text and HTML formats."""
    
    repos = summary_data.get('repositories', [])
    generated_at = summary_data.get('generated_at', 'N/A')
    
    # Plain text version
    text_body = f"""GitHub Trending Report
Generated: {generated_at}

Top {len(repos)} Trending Repositories:

"""
    
    for idx, repo in enumerate(repos, 1):
        text_body += f"""
{idx}. {repo['name']}
   ⭐ Stars: {repo['total_stars']:,} (↑{repo['stars_today']:,} today)
   🍴 Forks: {repo['forks']:,}
   🔧 Language: {repo.get('language', 'N/A')}
   📝 {repo['description']}
   🔗 {repo['url']}

"""
    
    if 'insights' in summary_data:
        insights = summary_data['insights']
        text_body += f"""
Insights:
- Most Common Language: {insights.get('most_common_language', 'N/A')}
- Total Stars: {insights.get('total_stars', 0):,}
- Total Forks: {insights.get('total_forks', 0):,}
"""
    
    text_body += "\n---\nSee attached files for full details."
    
    # HTML version
    html_body = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #0366d6; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .repo {{ background: #f6f8fa; border-left: 4px solid #0366d6; padding: 15px; margin: 15px 0; }}
        .repo-title {{ font-size: 18px; font-weight: bold; color: #0366d6; }}
        .stats {{ color: #666; margin: 10px 0; }}
        .insights {{ background: #fffbdd; padding: 15px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 GitHub Trending Report</h1>
        <p>Generated: {generated_at}</p>
    </div>
    <div class="content">
        <h2>Top {len(repos)} Trending Repositories</h2>
"""
    
    for idx, repo in enumerate(repos, 1):
        html_body += f"""
        <div class="repo">
            <div class="repo-title">{idx}. {repo['name']}</div>
            <p>{repo['description']}</p>
            <div class="stats">
                ⭐ <strong>{repo['total_stars']:,}</strong> stars (↑{repo['stars_today']:,} today) | 
                🍴 <strong>{repo['forks']:,}</strong> forks | 
                🔧 {repo.get('language', 'N/A')}
            </div>
            <a href="{repo['url']}" target="_blank">View on GitHub →</a>
        </div>
"""
    
    if 'insights' in summary_data:
        insights = summary_data['insights']
        html_body += f"""
        <div class="insights">
            <h3>📊 Insights</h3>
            <p><strong>Most Common Language:</strong> {insights.get('most_common_language', 'N/A')}</p>
            <p><strong>Total Stars:</strong> {insights.get('total_stars', 0):,}</p>
            <p><strong>Total Forks:</strong> {insights.get('total_forks', 0):,}</p>
        </div>
"""
    
    html_body += """
        <p style="color: #666; margin-top: 30px;">See attached files for full details including README previews.</p>
    </div>
</body>
</html>"""
    
    return {'text': text_body, 'html': html_body}


def main():
    """Main execution function."""
    import sys
    
    # Default recipient
    to_email = 'yqing999@gmail.com'
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        to_email = sys.argv[1]
    
    print(f"Preparing to send email to: {to_email}")
    print("\nNote: This script requires SMTP credentials to send emails.")
    print("You can either:")
    print("  1. Set environment variables: SMTP_SERVER, SMTP_EMAIL, SMTP_PASSWORD")
    print("  2. Or the script will save an .eml file you can send manually\n")
    
    # Get SMTP settings from environment variables
    smtp_server = os.getenv('SMTP_SERVER')  # e.g., 'smtp.gmail.com'
    sender_email = os.getenv('SMTP_EMAIL')
    sender_password = os.getenv('SMTP_PASSWORD')
    
    success = send_email(
        to_email=to_email,
        smtp_server=smtp_server,
        sender_email=sender_email,
        sender_password=sender_password
    )
    
    if success:
        print("\n✅ Email process completed!")
    else:
        print("\n❌ Email sending failed!")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
