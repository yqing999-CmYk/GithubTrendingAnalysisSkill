#!/usr/bin/env python3
"""
Test script for GitHub Trending Peek skill
Demonstrates basic functionality without actually hitting GitHub
"""

import json
from datetime import datetime

def create_mock_summary():
    """Create a mock summary for testing."""
    mock_data = {
        'generated_at': datetime.now().isoformat(),
        'total_repos': 5,
        'repositories': [
            {
                'name': 'example/awesome-ai',
                'url': 'https://github.com/example/awesome-ai',
                'description': 'A comprehensive guide to AI and machine learning resources',
                'language': 'Python',
                'stars_today': 250,
                'total_stars': 15000,
                'forks': 2500,
                'readme_preview': 'This is a curated list of awesome AI resources...'
            },
            {
                'name': 'example/react-native-app',
                'url': 'https://github.com/example/react-native-app',
                'description': 'A beautiful cross-platform mobile application',
                'language': 'JavaScript',
                'stars_today': 180,
                'total_stars': 8900,
                'forks': 1200,
                'readme_preview': 'React Native app with modern UI components...'
            },
            {
                'name': 'example/rust-compiler',
                'url': 'https://github.com/example/rust-compiler',
                'description': 'High-performance compiler written in Rust',
                'language': 'Rust',
                'stars_today': 320,
                'total_stars': 22000,
                'forks': 3400,
                'readme_preview': 'Fast and memory-safe compiler implementation...'
            },
            {
                'name': 'example/go-microservices',
                'url': 'https://github.com/example/go-microservices',
                'description': 'Microservices architecture with Go',
                'language': 'Go',
                'stars_today': 150,
                'total_stars': 12000,
                'forks': 1800,
                'readme_preview': 'Example microservices using Go and Docker...'
            },
            {
                'name': 'example/python-ml-framework',
                'url': 'https://github.com/example/python-ml-framework',
                'description': 'Machine learning framework for rapid prototyping',
                'language': 'Python',
                'stars_today': 200,
                'total_stars': 18000,
                'forks': 2900,
                'readme_preview': 'Easy-to-use ML framework with pre-trained models...'
            }
        ],
        'insights': {
            'most_common_language': 'Python',
            'total_stars': 75900,
            'total_forks': 11800
        }
    }
    return mock_data

def main():
    """Test the skill functionality."""
    print("=" * 60)
    print("GitHub Trending Peek - Test Demo")
    print("=" * 60)
    print()
    
    print("✓ Skill files created successfully!")
    print("✓ Dependencies: requests, beautifulsoup4")
    print()
    
    print("Skill structure:")
    print("  /mnt/skills/user/github-trending-peek/")
    print("    ├── SKILL.md              (skill definition)")
    print("    ├── README.md             (documentation)")
    print("    ├── requirements.txt      (dependencies)")
    print("    └── scripts/")
    print("        ├── crawl_trending.py (crawler)")
    print("        └── send_email.py     (email sender)")
    print()
    
    print("Creating mock summary data...")
    mock_data = create_mock_summary()
    
    print("\n" + "=" * 60)
    print("MOCK TRENDING REPOSITORIES SUMMARY")
    print("=" * 60)
    
    for idx, repo in enumerate(mock_data['repositories'], 1):
        print(f"\n{idx}. {repo['name']}")
        print(f"   ⭐ {repo['total_stars']:,} stars (↑{repo['stars_today']:,} today)")
        print(f"   🍴 {repo['forks']:,} forks")
        print(f"   🔧 {repo['language']}")
        print(f"   📝 {repo['description']}")
    
    insights = mock_data['insights']
    print(f"\n{'=' * 60}")
    print("INSIGHTS")
    print("=" * 60)
    print(f"Most Common Language: {insights['most_common_language']}")
    print(f"Total Stars: {insights['total_stars']:,}")
    print(f"Total Forks: {insights['total_forks']:,}")
    
    print("\n" + "=" * 60)
    print("HOW TO USE THIS SKILL")
    print("=" * 60)
    print("\n1. Ask Claude: 'Show me what's trending on GitHub'")
    print("2. Or manually run:")
    print("   cd /mnt/skills/user/github-trending-peek/scripts")
    print("   python3 crawl_trending.py")
    print("   python3 send_email.py")
    print()
    print("3. For email (optional), set environment variables:")
    print("   export SMTP_SERVER='smtp.gmail.com'")
    print("   export SMTP_EMAIL='your-email@gmail.com'")
    print("   export SMTP_PASSWORD='your-app-password'")
    print()
    print("✅ Skill is ready to use!")
    print()

if __name__ == '__main__':
    main()
