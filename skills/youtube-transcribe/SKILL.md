# YouTube Video Transcribe Skill

Extract transcripts from YouTube videos using youtube-transcript-api.

## Installation

```bash
pip install youtube-transcript-api
```

## Usage

```bash
# Basic transcript
python3 skills/youtube-transcribe/transcribe.py https://www.youtube.com/watch?v=VIDEO_ID

# With timestamp markers
python3 skills/youtube-transcribe/transcribe.py https://www.youtube.com/watch?v=VIDEO_ID --timestamps

# Save to file
python3 skills/youtube-transcribe/transcribe.py https://www.youtube.com/watch?v=VIDEO_ID --output /path/to/file.txt
```

## Example

```bash
python3 skills/youtube-transcribe/transcribe.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python3 skills/youtube-transcribe/transcribe.py "https://youtu.be/vP4xn5653Y"
python3 skills/youtube-transcribe/transcribe.py "https://youtube.com/shorts/B6RcG9zTwaQ"
```

## Notes

- Works with regular YouTube videos
- Some videos don't have auto-generated captions
- Shorts may have limited transcript availability
- Falls back to YouTube's automatic captions when available
