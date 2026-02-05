#!/usr/bin/env python3
"""
Viral AI Reels Extractor
Extract viral AI-generated videos from YouTube, TikTok, and X (Twitter)
and attempt to identify the prompts used to create them.
"""

import json
import re
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests


class AIReelExtractor:
    """Base class for extracting AI-generated viral reels"""
    
    def __init__(self, output_dir: str = "ai_reels_data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Common AI video generation keywords
        self.ai_keywords = [
            "AI generated", "AI video", "midjourney", "runway", "pika labs",
            "gen-2", "gen-3", "stable diffusion video", "text to video",
            "AI animation", "AI art", "dall-e", "sora", "luma ai", "kling ai",
            "haiper", "pixverse", "synthesia", "d-id", "fliki", "invideo ai",
            "veed ai", "pictory", "deepbrain ai", "hour one"
        ]
        
        # Patterns to extract prompts from descriptions/titles
        self.prompt_patterns = [
            r'prompt[:\s]+["\'](.+?)["\']',
            r'prompt[:\s]+(.+?)(?:\n|$)',
            r'used prompt[:\s]+(.+?)(?:\n|$)',
            r'generated with[:\s]+(.+?)(?:\n|$)',
            r'made with prompt[:\s]+(.+?)(?:\n|$)',
            r'["\'](.+?)["\'](?:\s+in\s+(?:runway|midjourney|pika|sora))',
        ]
    
    def contains_ai_keywords(self, text: str) -> bool:
        """Check if text contains AI-related keywords"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.ai_keywords)
    
    def extract_prompt(self, text: str) -> Optional[str]:
        """Extract AI generation prompt from text"""
        for pattern in self.prompt_patterns:
            matches = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                return matches.group(1).strip()
        return None
    
    def save_results(self, results: List[Dict], platform: str):
        """Save extracted results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/{platform}_ai_reels_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(results)} results to {filename}")
        return filename


class YouTubeAIReelExtractor(AIReelExtractor):
    """Extract viral AI-generated videos from YouTube"""
    
    def __init__(self, api_key: str, output_dir: str = "ai_reels_data"):
        super().__init__(output_dir)
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def search_viral_ai_videos(self, 
                               max_results: int = 50,
                               days_back: int = 30,
                               min_views: int = 100000) -> List[Dict]:
        """Search for viral AI-generated videos on YouTube"""
        
        results = []
        
        # Calculate date range
        published_after = (datetime.now() - timedelta(days=days_back)).isoformat() + "Z"
        
        # Search queries for AI content
        search_queries = [
            "AI generated video viral",
            "runway gen-3 viral",
            "sora AI video",
            "AI animation viral",
            "text to video AI",
            "midjourney video",
            "pika labs viral",
            "AI generated music viral",
            "Suno ai audio",
            "eleven labs ai audio",
            "ai influencer openart prompts"
        ]
        
        for query in search_queries:
            print(f"Searching YouTube for: {query}")
            
            # Search for videos
            search_params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "order": "viewCount",
                "maxResults": max_results,
                "publishedAfter": published_after,
                "key": self.api_key,
                "videoDuration": "short"  # Focus on shorts/reels
            }
            
            try:
                response = requests.get(f"{self.base_url}/search", params=search_params)
                response.raise_for_status()
                data = response.json()
                
                video_ids = [item['id']['videoId'] for item in data.get('items', [])]
                
                if not video_ids:
                    continue
                
                # Get detailed video statistics
                stats_params = {
                    "part": "statistics,snippet,contentDetails",
                    "id": ",".join(video_ids),
                    "key": self.api_key
                }
                
                stats_response = requests.get(f"{self.base_url}/videos", params=stats_params)
                stats_response.raise_for_status()
                stats_data = stats_response.json()
                
                # Process each video
                for video in stats_data.get('items', []):
                    view_count = int(video['statistics'].get('viewCount', 0))
                    
                    if view_count < min_views:
                        continue
                    
                    title = video['snippet']['title']
                    description = video['snippet']['description']
                    
                    # Check if it's AI-generated
                    combined_text = f"{title} {description}"
                    if not self.contains_ai_keywords(combined_text):
                        continue
                    
                    # Extract prompt if available
                    extracted_prompt = self.extract_prompt(description)
                    
                    video_info = {
                        "platform": "YouTube",
                        "video_id": video['id'],
                        "url": f"https://www.youtube.com/watch?v={video['id']}",
                        "title": title,
                        "description": description,
                        "views": view_count,
                        "likes": int(video['statistics'].get('likeCount', 0)),
                        "comments": int(video['statistics'].get('commentCount', 0)),
                        "published_at": video['snippet']['publishedAt'],
                        "channel": video['snippet']['channelTitle'],
                        "extracted_prompt": extracted_prompt,
                        "duration": video['contentDetails']['duration'],
                        "search_query": query
                    }
                    
                    results.append(video_info)
                    print(f"  ✓ Found: {title[:50]}... ({view_count:,} views)")
                
            except requests.exceptions.RequestException as e:
                print(f"  ✗ Error searching YouTube: {e}")
                continue
        
        # Remove duplicates by video_id
        unique_results = {r['video_id']: r for r in results}.values()
        final_results = sorted(unique_results, key=lambda x: x['views'], reverse=True)
        
        return list(final_results)


class TikTokAIReelExtractor(AIReelExtractor):
    """Extract viral AI-generated videos from TikTok"""
    
    def __init__(self, output_dir: str = "ai_reels_data"):
        super().__init__(output_dir)
        # Note: TikTok API requires approval and has strict rate limits
        # This implementation uses unofficial methods
    
    def search_viral_ai_videos(self, max_results: int = 50) -> List[Dict]:
        """
        Search for viral AI-generated videos on TikTok
        
        Note: This requires TikTok API access or web scraping.
        For production use, consider:
        1. TikTok Research API (requires approval)
        2. TikTok Creative Center (manual browsing)
        3. Third-party APIs like RapidAPI's TikTok endpoints
        """
        
        print("TikTok extraction requires API access or web scraping setup.")
        print("Recommended approaches:")
        print("1. Use TikTok Research API (https://developers.tiktok.com/)")
        print("2. Use unofficial TikTok scraping libraries (TikTokApi)")
        print("3. Manual browsing of trending hashtags: #AIart, #AIvideo, #RunwayML")
        
        # Placeholder for implementation
        results = []
        
        # Example hashtags to monitor
        ai_hashtags = [
            "#AIgenerated", "#AIart", "#AIvideo", "#RunwayML",
            "#MidjourneyAI", "#PikaLabs", "#TextToVideo", "#AIanimation"
        ]
        
        print(f"\nMonitor these TikTok hashtags: {', '.join(ai_hashtags)}")
        
        return results


class XTwitterAIReelExtractor(AIReelExtractor):
    """Extract viral AI-generated videos from X (Twitter)"""
    
    def __init__(self, bearer_token: str, output_dir: str = "ai_reels_data"):
        super().__init__(output_dir)
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
    
    def search_viral_ai_videos(self, 
                               max_results: int = 100,
                               min_likes: int = 1000) -> List[Dict]:
        """Search for viral AI-generated videos on X"""
        
        results = []
        
        # Search queries for AI video content
        search_queries = [
            "AI generated video has:media -is:retweet",
            "runway gen-3 has:media min_faves:1000",
            "sora AI video has:media min_retweets:100",
            "text to video AI has:media viral",
            "midjourney animation has:media",
        ]
        
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }
        
        for query in search_queries:
            print(f"Searching X for: {query}")
            
            params = {
                "query": query,
                "max_results": min(max_results, 100),  # API limit
                "tweet.fields": "created_at,public_metrics,attachments,entities",
                "expansions": "attachments.media_keys,author_id",
                "media.fields": "url,preview_image_url,type,variants,public_metrics"
            }
            
            try:
                response = requests.get(
                    f"{self.base_url}/tweets/search/recent",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                tweets = data.get('data', [])
                media_dict = {m['media_key']: m for m in data.get('includes', {}).get('media', [])}
                users_dict = {u['id']: u for u in data.get('includes', {}).get('users', [])}
                
                for tweet in tweets:
                    metrics = tweet.get('public_metrics', {})
                    
                    if metrics.get('like_count', 0) < min_likes:
                        continue
                    
                    text = tweet.get('text', '')
                    
                    # Check if AI-related
                    if not self.contains_ai_keywords(text):
                        continue
                    
                    # Extract prompt
                    extracted_prompt = self.extract_prompt(text)
                    
                    # Get media URLs
                    media_keys = tweet.get('attachments', {}).get('media_keys', [])
                    media_urls = []
                    for key in media_keys:
                        if key in media_dict and media_dict[key].get('type') == 'video':
                            variants = media_dict[key].get('variants', [])
                            if variants:
                                # Get highest quality video
                                video_url = max(
                                    [v for v in variants if v.get('content_type') == 'video/mp4'],
                                    key=lambda x: x.get('bit_rate', 0),
                                    default={}
                                ).get('url')
                                if video_url:
                                    media_urls.append(video_url)
                    
                    author_id = tweet.get('author_id')
                    author_username = users_dict.get(author_id, {}).get('username', 'unknown')
                    
                    tweet_info = {
                        "platform": "X (Twitter)",
                        "tweet_id": tweet['id'],
                        "url": f"https://twitter.com/i/status/{tweet['id']}",
                        "text": text,
                        "author": author_username,
                        "likes": metrics.get('like_count', 0),
                        "retweets": metrics.get('retweet_count', 0),
                        "replies": metrics.get('reply_count', 0),
                        "created_at": tweet.get('created_at'),
                        "extracted_prompt": extracted_prompt,
                        "media_urls": media_urls,
                        "search_query": query
                    }
                    
                    results.append(tweet_info)
                    print(f"  ✓ Found: {text[:50]}... ({metrics.get('like_count', 0):,} likes)")
                
            except requests.exceptions.RequestException as e:
                print(f"  ✗ Error searching X: {e}")
                continue
        
        # Sort by engagement
        results.sort(key=lambda x: x['likes'] + x['retweets'] * 2, reverse=True)
        
        return results


def main():
    """Main function to demonstrate usage"""
    
    print("=" * 60)
    print("Viral AI Reels Extractor")
    print("=" * 60)
    print()
    
    # Configuration
    # You need to obtain API keys from respective platforms:
    # YouTube: https://console.cloud.google.com/
    # X (Twitter): https://developer.twitter.com/
    
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "AIzaSyCdOd--_iALUY-0Amkf_Vu906rjYqs_7iY")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "YOUR_TWITTER_BEARER_TOKEN_HERE")
    
    # Example 1: Extract from YouTube
    print("\n[1] Extracting from YouTube...")
    print("-" * 60)
    
    if YOUTUBE_API_KEY and YOUTUBE_API_KEY != "YOUR_YOUTUBE_API_KEY_HERE":
        youtube_extractor = YouTubeAIReelExtractor(api_key=YOUTUBE_API_KEY)
        youtube_results = youtube_extractor.search_viral_ai_videos(
            max_results=50,
            days_back=30,
            min_views=50000
        )
        
        if youtube_results:
            youtube_extractor.save_results(youtube_results, "youtube")
            
            print(f"\nTop 5 YouTube AI Videos:")
            for i, video in enumerate(youtube_results[:5], 1):
                print(f"\n{i}. {video['title']}")
                print(f"   Views: {video['views']:,} | Likes: {video['likes']:,}")
                print(f"   URL: {video['url']}")
                if video['extracted_prompt']:
                    print(f"   Prompt: {video['extracted_prompt'][:100]}...")
    else:
        print("⚠ YouTube API key not configured. Skipping YouTube extraction.")
        print("Get your API key at: https://console.cloud.google.com/")
    
    # Example 2: Extract from X (Twitter)
    print("\n[2] Extracting from X (Twitter)...")
    print("-" * 60)
    
    if TWITTER_BEARER_TOKEN and TWITTER_BEARER_TOKEN != "YOUR_TWITTER_BEARER_TOKEN_HERE":
        twitter_extractor = XTwitterAIReelExtractor(bearer_token=TWITTER_BEARER_TOKEN)
        twitter_results = twitter_extractor.search_viral_ai_videos(
            max_results=100,
            min_likes=500
        )
        
        if twitter_results:
            twitter_extractor.save_results(twitter_results, "twitter")
            
            print(f"\nTop 5 X AI Videos:")
            for i, tweet in enumerate(twitter_results[:5], 1):
                print(f"\n{i}. {tweet['text'][:80]}...")
                print(f"   Likes: {tweet['likes']:,} | Retweets: {tweet['retweets']:,}")
                print(f"   URL: {tweet['url']}")
                if tweet['extracted_prompt']:
                    print(f"   Prompt: {tweet['extracted_prompt'][:100]}...")
    else:
        print("⚠ Twitter bearer token not configured. Skipping X extraction.")
        print("Get your token at: https://developer.twitter.com/")
    
    # Example 3: TikTok (requires additional setup)
    print("\n[3] TikTok extraction...")
    print("-" * 60)
    tiktok_extractor = TikTokAIReelExtractor()
    tiktok_extractor.search_viral_ai_videos()
    
    print("\n" + "=" * 60)
    print("Extraction complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()