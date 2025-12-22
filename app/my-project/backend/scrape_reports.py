import requests
from bs4 import BeautifulSoup
import json
import re
import time

# List of URLs to scrape (Rank 100-51, 50-11, Top 10)
URLS = [
    "https://www.espn.com/nba/story/_/id/46304114/nba-rank-2025-2026-flagg-beal-reaves-best-players-100-51",
    "https://www.espn.com/nba/story/_/id/46306594/nba-rank-2025-2026-williams-harden-morant-best-players-50-11",
    "https://www.espn.com/nba/story/_/id/46306892/nba-rank-2025-rankings-top-10-players-jokic-durant-lebron"
]

def scrape_espn_rankings():
    all_reports = []
    
    # Fake browser headers are crucial for ESPN
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }

    print("🚀 Starting ESPN 2025-26 Rankings Scrape...")

    for url in URLS:
        print(f"   ↳ Scraping: {url}...")
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Failed to retrieve {url} (Status: {response.status_code})")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ESPN formatting usually puts player names in <h2> tags like: "1. Nikola Jokic"
            # The analysis follows in <p> tags until the next <h2>
            
            # Find the main content container to avoid sidebar junk
            article_body = soup.find('div', class_='article-body') or soup
            
            # Get all H2s (Player Headers)
            headers_list = article_body.find_all('h2')
            
            for header in headers_list:
                header_text = header.get_text().strip()
                
                # Regex to find "Rank. Name" (e.g., "1. Nikola Jokic" or "50. Austin Reaves")
                # Also handles "100. Cooper Flagg"
                match = re.match(r"^(\d+)\.\s+(.*)", header_text)
                
                if match:
                    rank = match.group(1)
                    full_name_raw = match.group(2)
                    
                    # sometimes name includes team, e.g. "Nikola Jokic, Denver Nuggets"
                    # We split by comma or hyphen to get just the name
                    player_name = full_name_raw.split(',')[0].split('–')[0].strip()

                    # Now get the description. It's usually the <p> tags immediately following the <h2>
                    summary_text = ""
                    next_node = header.find_next_sibling()
                    
                    while next_node and next_node.name != 'h2':
                        if next_node.name == 'p':
                            summary_text += next_node.get_text().strip() + " "
                        next_node = next_node.find_next_sibling()
                    
                    if summary_text:
                        all_reports.append({
                            "rank": rank,
                            "player_name": player_name,
                            "summary": summary_text.strip(),
                            "source": "ESPN NBA Rank 2025-26"
                        })
                        print(f"      ✅ Found #{rank}: {player_name}")
            
            # Sleep to be polite to ESPN servers
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")

    # Save to JSON
    if all_reports:
        with open('analyst_reports.json', 'w', encoding='utf-8') as f:
            json.dump(all_reports, f, indent=4)
        print(f"\n🎉 Successfully saved {len(all_reports)} player reports to 'analyst_reports.json'")
    else:
        print("\n⚠️ No players found. ESPN structure might have changed or blocked the bot.")

if __name__ == "__main__":
    scrape_espn_rankings()