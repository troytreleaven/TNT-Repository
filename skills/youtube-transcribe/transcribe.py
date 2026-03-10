#!/usr/bin/env python3
"""
YouTube Video Transcript Extractor
Extracts transcripts from YouTube videos using youtube-transcript-api
"""

import sys
import re
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{9,11})',  # youtu.be short URLs
        r'shorts/([a-zA-Z0-9_-]{11})',  # YouTube Shorts
        r'^([a-zA-Z0-9_-]{11})$',  # Direct ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(video_url, timestamps=False, output_file=None):
    """Fetch and print transcript"""
    video_id = extract_video_id(video_url)
    
    if not video_id:
        print(f"Error: Could not extract video ID from: {video_url}")
        return False
    
    print(f"Fetching transcript for video: {video_id}")
    
    try:
        # Create instance and fetch
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=['en'])
        
        if timestamps:
            # Print with timestamps
            print("\n--- Transcript (with timestamps) ---")
            for segment in transcript_data:
                start = segment['start']
                minutes = int(start // 60)
                seconds = int(start % 60)
                print(f"[{minutes:02d}:{seconds:02d}] {segment['text']}")
        else:
            # Plain text
            formatter = TextFormatter()
            text = formatter.format_transcript(transcript_data)
            
            print("\n--- Transcript ---")
            print(text)
        
        # Save to file if requested
        if output_file:
            with open(output_file, 'w') as f:
                if timestamps:
                    for segment in transcript_data:
                        start = segment['start']
                        minutes = int(start // 60)
                        seconds = int(start % 60)
                        f.write(f"[{minutes:02d}:{seconds:02d}] {segment['text']}\n")
                else:
                    f.write(text)
            print(f"\nTranscript saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Extract YouTube video transcripts')
    parser.add_argument('url', help='YouTube video URL or ID')
    parser.add_argument('--timestamps', action='store_true', help='Include timestamps')
    parser.add_argument('--output', '-o', help='Output file path')
    
    args = parser.parse_args()
    
    success = get_transcript(args.url, args.timestamps, args.output)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
