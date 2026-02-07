#!/usr/bin/env python3
"""
GitHub Trending Crawler
Fetches the top 5 trending repositories from GitHub and their README files.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time


def fetch_trending_repos(limit=5):
    """
    Fetch trending repositories from GitHub.
    Returns a list of repository information.
    """
    url = "https://github.com/trending"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching trending page: {e}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = []
    
    # Find all repository articles
    repo_articles = soup.find_all('article', class_='Box-row')
    
    for article in repo_articles[:limit]:
        try:
            # Extract repository name and URL
            h2 = article.find('h2')
            if not h2:
                continue
                
            repo_link = h2.find('a')
            if not repo_link:
                continue
                
            repo_path = repo_link.get('href', '').strip()
            repo_full_name = repo_path.lstrip('/')
            repo_url = f"https://github.com{repo_path}"
            
            # Extract stars (today's stars)
            stars_today = 0
            stars_span = article.find('span', class_='d-inline-block float-sm-right')
            if stars_span:
                stars_text = stars_span.get_text(strip=True)
                stars_match = re.search(r'([\d,]+)', stars_text)
                if stars_match:
                    stars_today = int(stars_match.group(1).replace(',', ''))
            
            # Extract description
            description = ""
            desc_p = article.find('p', class_='col-9')
            if desc_p:
                description = desc_p.get_text(strip=True)
            
            # Extract language
            language = ""
            lang_span = article.find('span', itemprop='programmingLanguage')
            if lang_span:
                language = lang_span.get_text(strip=True)
            
            # Extract total stars and forks from the repo page
            total_stars, forks = fetch_repo_stats(repo_full_name)
            
            repo_info = {
                'name': repo_full_name,
                'url': repo_url,
                'description': description,
                'language': language,
                'stars_today': stars_today,
                'total_stars': total_stars,
                'forks': forks,
                'readme': ''
            }
            
            repos.append(repo_info)
            time.sleep(1)  # Be respectful with requests
            
        except Exception as e:
            print(f"Error parsing repository: {e}")
            continue
    
    return repos


def fetch_repo_stats(repo_full_name):
    """
    Fetch total stars and forks count from repository page.
    """
    url = f"https://github.com/{repo_full_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find stars count
        stars = 0
        stars_link = soup.find('a', href=lambda x: x and '/stargazers' in x)
        if stars_link:
            stars_text = stars_link.get_text(strip=True)
            stars_match = re.search(r'([\d.]+)([kKmM])?', stars_text)
            if stars_match:
                num = float(stars_match.group(1))
                suffix = stars_match.group(2)
                if suffix:
                    if suffix.lower() == 'k':
                        num *= 1000
                    elif suffix.lower() == 'm':
                        num *= 1000000
                stars = int(num)
        
        # Find forks count
        forks = 0
        forks_link = soup.find('a', href=lambda x: x and '/forks' in x)
        if forks_link:
            forks_text = forks_link.get_text(strip=True)
            forks_match = re.search(r'([\d.]+)([kKmM])?', forks_text)
            if forks_match:
                num = float(forks_match.group(1))
                suffix = forks_match.group(2)
                if suffix:
                    if suffix.lower() == 'k':
                        num *= 1000
                    elif suffix.lower() == 'm':
                        num *= 1000000
                forks = int(num)
        
        return stars, forks
        
    except Exception as e:
        print(f"Error fetching repo stats for {repo_full_name}: {e}")
        return 0, 0


def fetch_readme(repo_full_name):
    """
    Fetch README content from a GitHub repository.
    Tries both README.md and README files.
    """
    readme_urls = [
        f"https://raw.githubusercontent.com/{repo_full_name}/main/README.md",
        f"https://raw.githubusercontent.com/{repo_full_name}/master/README.md",
        f"https://raw.githubusercontent.com/{repo_full_name}/main/README",
        f"https://raw.githubusercontent.com/{repo_full_name}/master/README",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url in readme_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            continue
    
    return "README not available"


def generate_summary(repos):
    """
    Generate a summary of the trending repositories.
    """
    if not repos:
        return "No trending repositories found."
    
    summary = {
        'generated_at': datetime.now().isoformat(),
        'total_repos': len(repos),
        'repositories': []
    }
    
    for repo in repos:
        repo_summary = {
            'name': repo['name'],
            'url': repo['url'],
            'description': repo['description'],
            'language': repo['language'],
            'stars_today': repo['stars_today'],
            'total_stars': repo['total_stars'],
            'forks': repo['forks'],
            'readme_preview': repo['readme'][:500] if repo['readme'] else ''
        }
        summary['repositories'].append(repo_summary)
    
    # Find common patterns
    languages = [r['language'] for r in repos if r['language']]
    if languages:
        most_common_lang = max(set(languages), key=languages.count)
        summary['insights'] = {
            'most_common_language': most_common_lang,
            'total_stars': sum(r['total_stars'] for r in repos),
            'total_forks': sum(r['forks'] for r in repos)
        }
    
    return summary


def save_to_json(data, filename='trending_summary.json'):
    """Save summary data to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to {filename}")


def save_to_html(data, filename='trending_summary.html'):
    """Save summary data to HTML file."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Trending - {data.get('generated_at', 'N/A')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f6f8fa;
        }}
        h1 {{
            color: #24292e;
            border-bottom: 2px solid #0366d6;
            padding-bottom: 10px;
        }}
        .repo-card {{
            background: white;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .repo-title {{
            color: #0366d6;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .repo-title a {{
            color: #0366d6;
            text-decoration: none;
        }}
        .repo-title a:hover {{
            text-decoration: underline;
        }}
        .repo-stats {{
            display: flex;
            gap: 20px;
            margin: 10px 0;
            color: #586069;
        }}
        .stat {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .description {{
            color: #586069;
            margin: 15px 0;
            line-height: 1.6;
        }}
        .language {{
            display: inline-block;
            padding: 4px 12px;
            background: #0366d6;
            color: white;
            border-radius: 12px;
            font-size: 14px;
        }}
        .insights {{
            background: #fffbdd;
            border: 1px solid #d1d5da;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
        }}
        .timestamp {{
            color: #586069;
            font-size: 14px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>🔥 GitHub Trending Repositories</h1>
    <p class="timestamp">Generated at: {data.get('generated_at', 'N/A')}</p>
"""
    
    if 'insights' in data:
        insights = data['insights']
        html_content += f"""
    <div class="insights">
        <h2>📊 Insights</h2>
        <p><strong>Most Common Language:</strong> {insights.get('most_common_language', 'N/A')}</p>
        <p><strong>Total Stars:</strong> {insights.get('total_stars', 0):,}</p>
        <p><strong>Total Forks:</strong> {insights.get('total_forks', 0):,}</p>
    </div>
"""
    
    for idx, repo in enumerate(data.get('repositories', []), 1):
        html_content += f"""
    <div class="repo-card">
        <div class="repo-title">
            {idx}. <a href="{repo['url']}" target="_blank">{repo['name']}</a>
        </div>
        <div class="description">{repo['description']}</div>
        <div class="repo-stats">
            <div class="stat">⭐ <strong>{repo['total_stars']:,}</strong> stars</div>
            <div class="stat">🍴 <strong>{repo['forks']:,}</strong> forks</div>
            <div class="stat">📈 <strong>{repo['stars_today']:,}</strong> stars today</div>
        </div>
        {f'<span class="language">{repo["language"]}</span>' if repo.get('language') else ''}
    </div>
"""
    
    html_content += """
</body>
</html>"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved HTML to {filename}")


def main():
    """Main execution function."""
    print("Fetching GitHub trending repositories...")
    repos = fetch_trending_repos(limit=5)
    
    if not repos:
        print("No repositories found.")
        return
    
    print(f"\nFound {len(repos)} repositories. Fetching READMEs...")
    
    for repo in repos:
        print(f"  - {repo['name']}")
        repo['readme'] = fetch_readme(repo['name'])
        time.sleep(1)  # Be respectful with requests
    
    print("\nGenerating summary...")
    summary = generate_summary(repos)
    
    # Save to files
    save_to_json(summary, 'trending_summary.json')
    save_to_html(summary, 'trending_summary.html')
    
    print("\n✅ Complete! Files saved:")
    print("  - trending_summary.json")
    print("  - trending_summary.html")
    
    return summary


if __name__ == '__main__':
    main()
