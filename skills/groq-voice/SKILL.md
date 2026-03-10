# Groq Voice Messaging Skill

Real-time voice conversations powered by Groq's ultra-fast inference.

## Features

- **Ultra-low latency**: Groq's LPU delivers 10x faster responses than GPUs
- **Streaming audio**: Real-time voice conversations
- **Whisper transcription**: Accurate speech-to-text
- **Llama 3.3**: State-of-the-art conversational AI

## Setup

1. API key stored in `.env`
2. Install dependencies: `pip install groq`
3. Run demo: `python3 voice_chat.py`

## Usage

### Start a Voice Conversation

```bash
python3 voice_chat.py --mode conversation
```

### Transcribe Audio

```bash
python3 voice_chat.py --mode transcribe --file audio.mp3
```

### Text-to-Speech

```bash
python3 voice_chat.py --mode speak --text "Hello from Groq!"
```

## Models

- **Whisper Large v3**: Speech-to-text
- **Llama 3.3 70B**: Conversational AI
- **Llama 3.1 8B**: Fast, efficient responses

## Rate Limits

- 30 requests/minute
- 6,000 tokens/minute

## Integration with Voice-Call Plugin

Groq provides the AI brain for voice conversations:
1. User speaks → Audio captured
2. Whisper transcribes → Text sent to Llama
3. Llama generates response
4. TTS converts to speech → User hears reply

Total latency: ~300-500ms (vs 2-3 seconds on traditional systems)
