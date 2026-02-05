#!/usr/bin/env python3
"""
Instagram Reels AI Content Extractor
Extract viral AI-generated Reels from Instagram
"""

import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict, Optional


class InstagramAIReelExtractor:
    """
    Extract viral AI-generated Reels from Instagram
    
    IMPORTANT: Instagram's official API (Instagram Graph API) has limitations:
    - Requires Facebook Business account
    - Only works for your own Instagram Business/Creator accounts
    - Cannot search public content broadly
    
    This implementation provides multiple approaches:
    1. Official Instagram Graph API (for your own account)
    2. Unofficial methods using instaloader library
    3. Manual collection workflow
    """
    
    def __init__(self, output_dir: str = "ai_reels_data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # AI-related hashtags to monitor
        self.ai_hashtags = [
            'aiart', 'aigenerated', 'aivideo', 'runwayml', 'midjourney',
            'stablediffusion', 'pikalabs', 'aianimation', 'texttoimage',
            'aiartcommunity', 'generativeart', 'neuralart', 'deeplearningart',
            'machinelearningart', 'artificialintelligenceart', 'soraai',
            'lumaai', 'klingai', 'haiperai', 'gen3', 'gen2'
        ]
        
        # Prompt detection patterns
        self.prompt_patterns = [
            r'prompt[:\s]+["\'](.+?)["\']',
            r'prompt[:\s]+(.+?)(?:\n|#|$)',
            r'used[:\s]+["\'](.+?)["\']',
            r'generated with[:\s]+(.+?)(?:\n|#|$)',
            r'"([^"]{30,250})"',
        ]
    
    def extract_prompt(self, caption: str) -> Optional[str]:
        """Extract prompt from Instagram caption"""
        if not caption:
            return None
        
        for pattern in self.prompt_patterns:
            match = re.search(pattern, caption, re.IGNORECASE | re.MULTILINE)
            if match:
                prompt = match.group(1).strip()
                # Clean hashtags from end
                prompt = re.sub(r'\s*#\w+.*$', '', prompt)
                if len(prompt) > 10:
                    return prompt
        
        return None
    
    def contains_ai_keywords(self, text: str) -> bool:
        """Check if text contains AI-related keywords"""
        if not text:
            return False
        
        text_lower = text.lower()
        ai_keywords = [
            'ai generated', 'ai art', 'runway', 'midjourney', 'stable diffusion',
            'pika', 'sora', 'luma', 'kling', 'haiper', 'gen-2', 'gen-3',
            'text to video', 'ai video', 'ai animation'
        ]
        
        return any(keyword in text_lower for keyword in ai_keywords)
    
    # ==================== METHOD 1: Instaloader (Recommended) ====================
    
    def extract_with_instaloader(self, max_posts: int = 50) -> List[Dict]:
        """
        Extract posts using instaloader library
        This is an unofficial but widely-used method
        
        Installation: pip install instaloader
        """
        
        try:
            import instaloader
        except ImportError:
            print("❌ Instaloader not installed")
            print("Install with: pip install instaloader --break-system-packages")
            return []
        
        print("\n" + "=" * 70)
        print("INSTAGRAM EXTRACTION (Instaloader Method)")
        print("=" * 70)
        
        # Create Instaloader instance
        L = instaloader.Instaloader(
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )
        
        # Optional: Login for better rate limits (commented out for safety)
        # username = input("Instagram username (or press Enter to skip): ").strip()
        # if username:
        #     password = input("Password: ").strip()
        #     try:
        #         L.login(username, password)
        #         print("✓ Logged in successfully")
        #     except Exception as e:
        #         print(f"⚠ Login failed: {e}")
        #         print("Continuing without login (may have rate limits)")
        
        results = []
        
        # Search by hashtags
        for hashtag in self.ai_hashtags[:5]:  # Limit to avoid rate limits
            print(f"\nSearching hashtag: #{hashtag}")
            
            try:
                posts = instaloader.Hashtag.from_name(L.context, hashtag).get_posts()
                
                count = 0
                for post in posts:
                    if count >= max_posts // len(self.ai_hashtags[:5]):
                        break
                    
                    # Only process video posts (Reels)
                    if not post.is_video:
                        continue
                    
                    caption = post.caption if post.caption else ""
                    
                    # Check if it's AI-related
                    if not self.contains_ai_keywords(caption):
                        # Also check hashtags
                        hashtags = ' '.join([f"#{tag}" for tag in post.caption_hashtags])
                        if not self.contains_ai_keywords(hashtags):
                            continue
                    
                    # Extract prompt
                    prompt = self.extract_prompt(caption)
                    
                    # Build result
                    result = {
                        'platform': 'Instagram',
                        'post_id': post.shortcode,
                        'url': f"https://www.instagram.com/p/{post.shortcode}/",
                        'caption': caption[:500] if caption else "",
                        'likes': post.likes,
                        'comments': post.comments,
                        'views': post.video_view_count if hasattr(post, 'video_view_count') else 0,
                        'posted_at': post.date_utc.isoformat(),
                        'owner': post.owner_username,
                        'extracted_prompt': prompt,
                        'hashtags': list(post.caption_hashtags)[:10],
                        'is_reel': post.typename == 'GraphVideo',
                        'search_hashtag': hashtag
                    }
                    
                    results.append(result)
                    count += 1
                    
                    print(f"  ✓ Found: @{post.owner_username} ({post.likes:,} likes)")
                    
                    # Rate limit protection
                    time.sleep(2)
                
            except Exception as e:
                print(f"  ✗ Error with #{hashtag}: {e}")
                continue
        
        return results
    
    # ==================== METHOD 2: Official Graph API ====================
    
    def extract_with_graph_api(self, access_token: str, instagram_business_account_id: str) -> List[Dict]:
        """
        Extract using official Instagram Graph API
        
        Requirements:
        - Facebook Business account
        - Instagram Business or Creator account
        - Access token from Facebook Graph API
        
        Get started: https://developers.facebook.com/docs/instagram-api
        """
        
        import requests
        
        print("\n" + "=" * 70)
        print("INSTAGRAM EXTRACTION (Official Graph API)")
        print("=" * 70)
        
        base_url = "https://graph.facebook.com/v18.0"
        
        results = []
        
        # Get recent media
        endpoint = f"{base_url}/{instagram_business_account_id}/media"
        params = {
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count,owner',
            'access_token': access_token,
            'limit': 100
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            for media in data.get('data', []):
                # Only process videos/reels
                if media.get('media_type') not in ['VIDEO', 'REEL']:
                    continue
                
                caption = media.get('caption', '')
                
                # Check if AI-related
                if not self.contains_ai_keywords(caption):
                    continue
                
                # Extract prompt
                prompt = self.extract_prompt(caption)
                
                result = {
                    'platform': 'Instagram',
                    'post_id': media['id'],
                    'url': media.get('permalink', ''),
                    'caption': caption[:500],
                    'likes': media.get('like_count', 0),
                    'comments': media.get('comments_count', 0),
                    'posted_at': media.get('timestamp', ''),
                    'media_type': media.get('media_type', ''),
                    'extracted_prompt': prompt
                }
                
                results.append(result)
                print(f"  ✓ Found: {caption[:50]}... ({result['likes']:,} likes)")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Graph API Error: {e}")
            print("\nMake sure:")
            print("1. Access token is valid")
            print("2. Instagram account is a Business/Creator account")
            print("3. Token has instagram_basic and pages_show_list permissions")
        
        return results
    
    # ==================== METHOD 3: Manual Collection ====================
    
    def generate_manual_collection_guide(self):
        """Generate guide for manual Instagram data collection"""
        
        guide = """
=" * 70)
INSTAGRAM MANUAL COLLECTION GUIDE
=" * 70)

Since Instagram's API has limitations, here's a manual workflow:

STEP 1: Find Viral AI Reels
───────────────────────────────────────────────────────────────────────
Search these hashtags on Instagram:
"""
        
        for i, hashtag in enumerate(self.ai_hashtags[:15], 1):
            guide += f"\n  {i:2d}. #{hashtag}"
        
        guide += """

STEP 2: Identify Top Reels
───────────────────────────────────────────────────────────────────────
Look for reels with:
• High view counts (100k+)
• High engagement (likes, comments, shares)
• Clear AI watermarks or mentions
• Prompts in captions

STEP 3: Extract Data
───────────────────────────────────────────────────────────────────────
For each reel, record:
• URL (e.g., https://instagram.com/p/ABC123/)
• Caption (including prompts if mentioned)
• Like count
• View count
• Creator username
• Post date

STEP 4: Use Browser Extensions (Optional)
───────────────────────────────────────────────────────────────────────
Tools that can help:
• DownloadGram - Download reels
• 4K Stogram - Bulk download from profiles/hashtags
• Instaloader (command line) - Automated scraping

STEP 5: Create JSON File
───────────────────────────────────────────────────────────────────────
Save as: ai_reels_data/instagram_manual_YYYYMMDD.json

Format:
[
  {
    "platform": "Instagram",
    "post_id": "ABC123",
    "url": "https://instagram.com/p/ABC123/",
    "caption": "Amazing AI video! Prompt: ...",
    "likes": 50000,
    "views": 500000,
    "comments": 1200,
    "owner": "username",
    "extracted_prompt": "cinematic shot of...",
    "posted_at": "2024-01-15T10:30:00Z"
  }
]

RECOMMENDED TOOLS:
───────────────────────────────────────────────────────────────────────
• Instaloader (Python): Best for automated collection
• Apify Instagram Scraper: Paid but reliable
• Phantombuster: Browser automation
• Manual spreadsheet: Simple but time-consuming

RATE LIMIT TIPS:
───────────────────────────────────────────────────────────────────────
• Don't scrape too fast (Instagram will block you)
• Use delays between requests (2-5 seconds)
• Consider using multiple accounts (carefully)
• Rotate IP addresses if needed
"""
        
        print(guide)
        
        # Save to file
        guide_file = os.path.join(self.output_dir, "instagram_manual_guide.txt")
        with open(guide_file, 'w') as f:
            f.write(guide)
        
        print(f"\n✓ Guide saved to: {guide_file}")
    
    # ==================== Main Extraction ====================
    
    def extract(self, method: str = 'instaloader', max_posts: int = 50, **kwargs) -> List[Dict]:
        """
        Main extraction method
        
        Args:
            method: 'instaloader', 'graph_api', or 'manual'
            max_posts: Maximum number of posts to extract
            **kwargs: Additional arguments for specific methods
        """
        
        results = []
        
        if method == 'instaloader':
            results = self.extract_with_instaloader(max_posts=max_posts)
        
        elif method == 'graph_api':
            access_token = kwargs.get('access_token')
            account_id = kwargs.get('instagram_business_account_id')
            
            if not access_token or not account_id:
                print("❌ Graph API requires access_token and instagram_business_account_id")
                return []
            
            results = self.extract_with_graph_api(access_token, account_id)
        
        elif method == 'manual':
            self.generate_manual_collection_guide()
            return []
        
        else:
            print(f"❌ Unknown method: {method}")
            print("Available methods: 'instaloader', 'graph_api', 'manual'")
            return []
        
        # Save results
        if results:
            self.save_results(results)
        
        return results
    
    def save_results(self, results: List[Dict]):
        """Save results to JSON file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"instagram_ai_reels_{timestamp}.json")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'=' * 70}")
        print(f"✓ Saved {len(results)} Instagram posts to:")
        print(f"  {filename}")
        print(f"{'=' * 70}")
        
        # Print summary
        if results:
            total_likes = sum(r.get('likes', 0) for r in results)
            with_prompts = sum(1 for r in results if r.get('extracted_prompt'))
            
            print(f"\nSummary:")
            print(f"  Total posts: {len(results)}")
            print(f"  Posts with prompts: {with_prompts}")
            print(f"  Total likes: {total_likes:,}")
            print(f"  Average likes: {total_likes // len(results):,}")


def main():
    """Main execution"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract AI-generated Reels from Instagram')
    parser.add_argument('--method', '-m', choices=['instaloader', 'graph_api', 'manual'],
                       default='instaloader', help='Extraction method')
    parser.add_argument('--max-posts', '-n', type=int, default=50,
                       help='Maximum posts to extract')
    parser.add_argument('--access-token', help='Facebook Graph API access token (for graph_api method)')
    parser.add_argument('--account-id', help='Instagram Business Account ID (for graph_api method)')
    
    args = parser.parse_args()
    
    extractor = InstagramAIReelExtractor()
    
    print("=" * 70)
    print("INSTAGRAM AI REELS EXTRACTOR")
    print("=" * 70)
    
    if args.method == 'instaloader':
        print("\nUsing Instaloader method (unofficial but effective)")
        print("Install if needed: pip install instaloader --break-system-packages")
    elif args.method == 'graph_api':
        print("\nUsing Official Graph API")
        if not args.access_token or not args.account_id:
            print("\n❌ Missing required arguments:")
            print("  --access-token YOUR_TOKEN")
            print("  --account-id YOUR_INSTAGRAM_BUSINESS_ACCOUNT_ID")
            return
    elif args.method == 'manual':
        print("\nGenerating manual collection guide...")
    
    # Extract
    results = extractor.extract(
        method=args.method,
        max_posts=args.max_posts,
        access_token=args.access_token,
        instagram_business_account_id=args.account_id
    )
    
    if results:
        print(f"\n✓ Successfully extracted {len(results)} posts!")
    

if __name__ == "__main__":
    main()