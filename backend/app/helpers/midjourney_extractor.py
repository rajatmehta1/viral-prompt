#!/usr/bin/env python3
"""
Midjourney Gallery Extractor
Extract AI-generated images and prompts from Midjourney's public gallery
"""

import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
import requests


class MidjourneyGalleryExtractor:
    """
    Extract AI-generated images and prompts from Midjourney
    
    Methods:
    1. Midjourney Community Feed (website scraping)
    2. Discord Bot (requires bot setup)
    3. Third-party APIs (Midjourney API services)
    4. Manual collection from public showcases
    """
    
    def __init__(self, output_dir: str = "ai_reels_data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Midjourney public endpoints
        self.community_feed_url = "https://www.midjourney.com/app/feed/"
        self.api_base = "https://www.midjourney.com/api/app"
        
    # ==================== METHOD 1: Web Scraping (Community Feed) ====================
    
    def extract_from_community_feed(self, max_images: int = 100) -> List[Dict]:
        """
        Extract from Midjourney community feed
        
        Note: Requires web scraping. May need Selenium/Playwright for dynamic content
        """
        
        print("\n" + "=" * 70)
        print("MIDJOURNEY EXTRACTION (Community Feed)")
        print("=" * 70)
        
        results = []
        
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("❌ BeautifulSoup not installed")
            print("Install with: pip install beautifulsoup4 --break-system-packages")
            return []
        
        # Try to fetch community feed
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            # Note: Midjourney's feed is heavily JavaScript-based
            # This basic approach may not work; Selenium/Playwright recommended
            response = requests.get(self.community_feed_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for image containers (structure may vary)
            # This is a simplified example; actual scraping needs inspection
            image_containers = soup.find_all('div', class_='image-container')
            
            print(f"Found {len(image_containers)} images")
            
            for container in image_containers[:max_images]:
                # Extract image data (adjust selectors based on actual HTML)
                img_url = container.find('img')['src'] if container.find('img') else None
                prompt_elem = container.find('div', class_='prompt')
                prompt = prompt_elem.text.strip() if prompt_elem else None
                
                if img_url and prompt:
                    result = {
                        'platform': 'Midjourney',
                        'image_url': img_url,
                        'prompt': prompt,
                        'source': 'community_feed',
                        'extracted_at': datetime.now().isoformat()
                    }
                    results.append(result)
            
        except Exception as e:
            print(f"✗ Web scraping failed: {e}")
            print("\nFor better results, use:")
            print("1. Selenium/Playwright for dynamic content")
            print("2. Midjourney API (if available)")
            print("3. Manual collection method")
        
        return results
    
    # ==================== METHOD 2: Midjourney API (Third-party) ====================
    
    def extract_with_api(self, api_key: str, max_images: int = 100) -> List[Dict]:
        """
        Extract using third-party Midjourney APIs
        
        Popular services:
        - useapi.net/midjourney
        - thenextleg.io
        - goapi.ai
        
        Note: These are paid services and not official Midjourney APIs
        """
        
        print("\n" + "=" * 70)
        print("MIDJOURNEY EXTRACTION (Third-party API)")
        print("=" * 70)
        
        # Example using a generic API structure
        # You'll need to adapt this to your chosen service
        
        results = []
        
        # Example: UseAPI.net structure (adjust based on actual API)
        api_url = "https://api.useapi.net/v1/midjourney/gallery"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'limit': max_images,
            'sort': 'trending'  # or 'recent', 'popular'
        }
        
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('images', []):
                result = {
                    'platform': 'Midjourney',
                    'image_id': item.get('id'),
                    'image_url': item.get('url'),
                    'prompt': item.get('prompt'),
                    'full_prompt': item.get('full_prompt'),  # includes parameters
                    'upscaled': item.get('upscaled', False),
                    'variation': item.get('variation'),
                    'grid_index': item.get('grid_index'),
                    'created_at': item.get('created_at'),
                    'user_id': item.get('user_id'),
                    'likes': item.get('likes', 0),
                    'model_version': item.get('model_version'),  # v5, v6, niji, etc.
                    'parameters': item.get('parameters', {}),  # --ar, --chaos, etc.
                    'source': 'third_party_api'
                }
                
                results.append(result)
                print(f"  ✓ Extracted: {result['prompt'][:60]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ API Error: {e}")
            print("\nMake sure:")
            print("1. API key is valid")
            print("2. You have API credits/subscription")
            print("3. API endpoint URL is correct")
        
        return results
    
    # ==================== METHOD 3: Discord Bot Integration ====================
    
    def setup_discord_monitoring(self):
        """
        Generate guide for monitoring Midjourney Discord
        
        Midjourney operates primarily through Discord, so monitoring
        the Discord server can capture all generations with prompts
        """
        
        guide = """
=" * 70)
MIDJOURNEY DISCORD MONITORING SETUP
=" * 70)

Midjourney primarily operates through Discord. Here's how to capture data:

OPTION 1: Discord Bot (Automated)
───────────────────────────────────────────────────────────────────────

STEP 1: Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Create New Application
3. Go to Bot section → Add Bot
4. Enable Message Content Intent
5. Copy Bot Token

STEP 2: Install discord.py
pip install discord.py --break-system-packages

STEP 3: Bot Code Example
───────────────────────────────────────────────────────────────────────
import discord
import json
import re

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

results = []

@client.event
async def on_message(message):
    # Only process Midjourney bot messages
    if message.author.id != 936929561302675456:  # Midjourney Bot ID
        return
    
    # Look for image generations
    if message.attachments:
        # Extract prompt from message content
        content = message.content
        
        # Midjourney format: "**prompt here** - <@user_id>"
        prompt_match = re.search(r'\*\*(.+?)\*\*', content)
        
        if prompt_match:
            prompt = prompt_match.group(1)
            
            data = {
                'platform': 'Midjourney',
                'prompt': prompt,
                'image_url': message.attachments[0].url,
                'message_id': str(message.id),
                'channel': str(message.channel.id),
                'timestamp': message.created_at.isoformat(),
                'user_id': str(message.author.id)
            }
            
            results.append(data)
            print(f"Captured: {prompt[:50]}...")

@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')

# Save on shutdown
@client.event
async def on_disconnect():
    with open('midjourney_captures.json', 'w') as f:
        json.dump(results, f, indent=2)

client.run('YOUR_BOT_TOKEN_HERE')
───────────────────────────────────────────────────────────────────────

STEP 4: Add Bot to Server
1. Go to OAuth2 → URL Generator
2. Select 'bot' scope
3. Select 'Read Messages/View Channels' permission
4. Use generated URL to add bot to a server
5. Note: Cannot add to official Midjourney server

STEP 5: Monitor Public Channels
- Join Midjourney Discord server
- Monitor public showcase channels
- Manually copy or automate with bot in allowed servers


OPTION 2: Manual Collection (Recommended)
───────────────────────────────────────────────────────────────────────

BEST SOURCES:
1. Midjourney Showcase Website
   https://www.midjourney.com/showcase
   
2. Midjourney Discord Public Rooms
   - Look for public generation channels
   - Screenshot or manually copy prompts
   
3. Midjourney Community Feed
   https://www.midjourney.com/app/feed/
   
4. User Profiles
   https://www.midjourney.com/app/users/[username]/

MANUAL EXTRACTION TIPS:
• Right-click images → "Copy Image Address"
• Prompts are shown in image descriptions
• Parameters shown: --v 6, --ar 16:9, --chaos 50, etc.
• Save both base prompt and full command


OPTION 3: Third-Party Tools
───────────────────────────────────────────────────────────────────────

Paid Services:
• UseAPI.net - Midjourney API wrapper
• TheNextLeg.io - Midjourney automation
• GoAPI.ai - AI image generation APIs

Free Tools:
• Midjourney Prompt Generator websites
• Public prompt databases (promptbase.com, etc.)
• GitHub prompt collections


DATA TO COLLECT:
───────────────────────────────────────────────────────────────────────
For each image:
• Prompt text (base prompt)
• Full command (with parameters)
• Model version (v5, v6, niji 5, etc.)
• Aspect ratio (--ar 16:9, etc.)
• Chaos value (--chaos 0-100)
• Stylize value (--s 0-1000)
• Image URL (high resolution)
• Generation date
• Upscale/variation info
• User who created it


PROMPT PARAMETER EXAMPLES:
───────────────────────────────────────────────────────────────────────
--v 6          Model version 6
--niji 5       Niji model version 5
--ar 16:9      Aspect ratio
--chaos 50     Variation level (0-100)
--stylize 100  Style strength (0-1000)
--quality 2    Image quality (.25, .5, 1, 2)
--seed 12345   Reproducible results
--tile         Seamless patterns
--style raw    Less opinionated generations


JSON FORMAT:
───────────────────────────────────────────────────────────────────────
[
  {
    "platform": "Midjourney",
    "prompt": "cinematic portrait of a cyberpunk warrior",
    "full_command": "cinematic portrait of a cyberpunk warrior --v 6 --ar 16:9 --chaos 30",
    "image_url": "https://cdn.midjourney.com/...",
    "model_version": "v6",
    "parameters": {
      "aspect_ratio": "16:9",
      "chaos": 30,
      "quality": 1,
      "stylize": 100
    },
    "upscaled": true,
    "created_at": "2024-01-15T10:30:00Z",
    "user_id": "12345",
    "likes": 150
  }
]


RATE LIMITS & ETHICS:
───────────────────────────────────────────────────────────────────────
• Respect Discord ToS
• Don't spam or auto-post
• Don't scrape official Midjourney servers without permission
• Use public showcases and community feeds
• Credit original prompt creators
• Consider privacy when sharing user data
"""
        
        print(guide)
        
        # Save to file
        guide_file = os.path.join(self.output_dir, "midjourney_discord_guide.txt")
        with open(guide_file, 'w') as f:
            f.write(guide)
        
        print(f"\n✓ Guide saved to: {guide_file}")
    
    # ==================== METHOD 4: Popular Prompt Databases ====================
    
    def extract_from_prompt_databases(self) -> List[Dict]:
        """
        Extract from public Midjourney prompt databases
        """
        
        print("\n" + "=" * 70)
        print("MIDJOURNEY PROMPT DATABASES")
        print("=" * 70)
        
        databases = {
            'PromptBase': 'https://promptbase.com/marketplace?model=midjourney',
            'PublicPrompts': 'https://publicprompts.art/',
            'PromptHero': 'https://prompthero.com/midjourney-prompts',
            'Lexica.art': 'https://lexica.art/?q=midjourney',
            'PromptFolder': 'https://promptfolder.com/midjourney-prompts/',
            'GitHub Collections': 'https://github.com/search?q=midjourney+prompts',
        }
        
        print("\nPublic Midjourney Prompt Resources:")
        print("-" * 70)
        
        for name, url in databases.items():
            print(f"\n{name}")
            print(f"  URL: {url}")
            print(f"  Method: Manual browsing and collection")
        
        print("\n" + "=" * 70)
        print("RECOMMENDATION:")
        print("=" * 70)
        print("\n1. Visit these sites manually")
        print("2. Filter by 'trending' or 'popular'")
        print("3. Copy prompts and image URLs")
        print("4. Save to JSON file using format below")
        
        # Return empty list as these require manual collection
        return []
    
    # ==================== Main Extraction ====================
    
    def extract(self, method: str = 'manual', max_images: int = 100, **kwargs) -> List[Dict]:
        """
        Main extraction method
        
        Args:
            method: 'web', 'api', 'discord', 'databases', 'manual'
            max_images: Maximum number of images to extract
            **kwargs: Additional arguments for specific methods
        """
        
        results = []
        
        if method == 'web':
            print("\n⚠ Note: Web scraping Midjourney requires Selenium/Playwright")
            results = self.extract_from_community_feed(max_images=max_images)
        
        elif method == 'api':
            api_key = kwargs.get('api_key')
            
            if not api_key:
                print("❌ API method requires api_key")
                print("Get API access from services like:")
                print("  • useapi.net/midjourney")
                print("  • thenextleg.io")
                print("  • goapi.ai")
                return []
            
            results = self.extract_with_api(api_key, max_images)
        
        elif method == 'discord':
            self.setup_discord_monitoring()
            return []
        
        elif method == 'databases':
            results = self.extract_from_prompt_databases()
        
        elif method == 'manual':
            self.generate_manual_collection_guide()
            return []
        
        else:
            print(f"❌ Unknown method: {method}")
            print("Available methods: 'web', 'api', 'discord', 'databases', 'manual'")
            return []
        
        # Save results
        if results:
            self.save_results(results)
        
        return results
    
    def generate_manual_collection_guide(self):
        """Generate comprehensive manual collection guide"""
        
        guide = """
=" * 70)
MIDJOURNEY MANUAL COLLECTION GUIDE
=" * 70)

BEST SOURCES FOR VIRAL MIDJOURNEY CONTENT:
───────────────────────────────────────────────────────────────────────

1. MIDJOURNEY SHOWCASE (Official)
   URL: https://www.midjourney.com/showcase
   • Curated best images
   • Click images to see full prompts
   • Filter by theme/style
   • All images include prompts

2. MIDJOURNEY COMMUNITY FEED
   URL: https://www.midjourney.com/app/feed/
   • Real-time generations
   • Filter by "Hot" or "New"
   • See trending prompts
   • Requires Midjourney account

3. MIDJOURNEY DISCORD SERVER
   URL: discord.gg/midjourney
   • Public showcase channels
   • See all generations in real-time
   • Prompts embedded in messages
   • Huge volume of content

4. USER PROFILES
   URL: https://www.midjourney.com/app/users/[username]/
   • Browse top creators
   • See their best work
   • Consistent style examples
   • Portfolio of prompts


STEP-BY-STEP COLLECTION:
───────────────────────────────────────────────────────────────────────

STEP 1: Find Viral Images
• Visit Midjourney Showcase
• Sort by "Hot" or "Trending"
• Look for high engagement (likes/upvotes)
• Note unique/interesting styles

STEP 2: Extract Prompt
• Click on image
• Prompt appears below image
• Copy full prompt including parameters
• Example: "portrait of a warrior --v 6 --ar 2:3"

STEP 3: Get Image URL
• Right-click image
• "Copy Image Address" or "Open in new tab"
• Save high-resolution URL
• Usually: cdn.midjourney.com/...

STEP 4: Note Parameters
• Model version: --v 6, --niji 5
• Aspect ratio: --ar 16:9
• Chaos: --chaos 50
• Stylize: --s 100
• Quality: --q 2
• Other: --tile, --video, etc.

STEP 5: Record Metadata
• Creation date
• Number of likes/upvotes
• Creator username
• Upscale/variation info


DATA FORMAT:
───────────────────────────────────────────────────────────────────────

Save as: ai_reels_data/midjourney_manual_YYYYMMDD.json

[
  {
    "platform": "Midjourney",
    "image_id": "optional_id",
    "image_url": "https://cdn.midjourney.com/...",
    "prompt": "cinematic portrait of a cyberpunk warrior in neon city",
    "full_command": "cinematic portrait of a cyberpunk warrior in neon city --v 6 --ar 16:9 --chaos 30 --s 100",
    "model_version": "v6",
    "parameters": {
      "version": "6",
      "aspect_ratio": "16:9",
      "chaos": 30,
      "stylize": 100,
      "quality": 1
    },
    "upscaled": true,
    "variation": false,
    "grid_index": null,
    "created_at": "2024-01-15T10:30:00Z",
    "creator": "username",
    "likes": 250,
    "source": "midjourney_showcase"
  }
]


TOOLS TO HELP:
───────────────────────────────────────────────────────────────────────

Browser Extensions:
• DownThemAll - Bulk image download
• Copy All URLs - Extract multiple links
• JSON Formatter - View/edit JSON easily

Automation:
• Selenium/Playwright - Automate browsing
• Beautiful Soup - Parse HTML
• Requests - Download images

Organization:
• Notion - Database of prompts
• Airtable - Spreadsheet with images
• Google Sheets - Simple tracking


PROMPT ANALYSIS TIPS:
───────────────────────────────────────────────────────────────────────

Look for patterns in successful prompts:
• Descriptive style keywords (cinematic, ethereal, etc.)
• Specific subjects (portrait, landscape, etc.)
• Art styles (photorealistic, anime, oil painting)
• Lighting (golden hour, dramatic, soft)
• Camera angles (wide shot, close-up, aerial)
• Parameters that create best results


QUALITY INDICATORS:
───────────────────────────────────────────────────────────────────────

Collect prompts from images with:
• High engagement (100+ likes)
• Unique/creative concepts
• Professional quality
• Clear subject matter
• Good composition
• Effective use of parameters


TIME-SAVING TIPS:
───────────────────────────────────────────────────────────────────────

1. Focus on "Hot" section for viral content
2. Follow top creators for consistent quality
3. Use browser bookmarks for quick access
4. Set aside specific time for collection
5. Batch process (collect 20-50 at once)
6. Use templates for consistent data format
"""
        
        print(guide)
        
        # Save to file
        guide_file = os.path.join(self.output_dir, "midjourney_manual_guide.txt")
        with open(guide_file, 'w') as f:
            f.write(guide)
        
        print(f"\n✓ Guide saved to: {guide_file}")
    
    def save_results(self, results: List[Dict]):
        """Save results to JSON file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"midjourney_gallery_{timestamp}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'=' * 70}")
        print(f"✓ Saved {len(results)} Midjourney images to:")
        print(f"  {filename}")
        print(f"{'=' * 70}")
        
        # Print summary
        if results:
            with_prompts = sum(1 for r in results if r.get('prompt'))
            total_likes = sum(r.get('likes', 0) for r in results)
            
            print(f"\nSummary:")
            print(f"  Total images: {len(results)}")
            print(f"  Images with prompts: {with_prompts}")
            if total_likes > 0:
                print(f"  Total likes: {total_likes:,}")
                print(f"  Average likes: {total_likes // len(results):,}")


def main():
    """Main execution"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract Midjourney images and prompts')
    parser.add_argument('--method', '-m', 
                       choices=['web', 'api', 'discord', 'databases', 'manual'],
                       default='manual',
                       help='Extraction method')
    parser.add_argument('--max-images', '-n', type=int, default=100,
                       help='Maximum images to extract')
    parser.add_argument('--api-key', help='API key for third-party services')
    
    args = parser.parse_args()
    
    extractor = MidjourneyGalleryExtractor()
    
    print("=" * 70)
    print("MIDJOURNEY GALLERY EXTRACTOR")
    print("=" * 70)
    
    if args.method == 'manual':
        print("\nGenerating manual collection guide...")
        print("(Recommended for best results)")
    elif args.method == 'discord':
        print("\nGenerating Discord monitoring setup guide...")
    elif args.method == 'databases':
        print("\nListing public prompt databases...")
    elif args.method == 'web':
        print("\nWeb scraping (requires Selenium/Playwright)")
    elif args.method == 'api':
        print("\nUsing third-party API")
        if not args.api_key:
            print("\n❌ Missing --api-key")
            return
    
    # Extract
    results = extractor.extract(
        method=args.method,
        max_images=args.max_images,
        api_key=args.api_key
    )
    
    if results:
        print(f"\n✓ Successfully extracted {len(results)} images!")


if __name__ == "__main__":
    main()