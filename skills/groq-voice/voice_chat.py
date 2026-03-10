#!/usr/bin/env python3
"""
Groq Voice Messaging System
Ultra-fast voice conversations powered by Groq's LPU
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    print("❌ Groq not installed. Run: pip install groq")
    sys.exit(1)

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Initialize Groq client
client = Groq(api_key=os.getenv("API_KEY"))

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-large-v3")
LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama-3.3-70b-versatile")


def transcribe_audio(audio_file_path: str) -> str:
    """Transcribe audio file using Whisper"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model=WHISPER_MODEL,
                response_format="text"
            )
        return transcription
    except Exception as e:
        return f"Error transcribing: {str(e)}"


def generate_response(text: str, context: str = "") -> str:
    """Generate AI response using Llama"""
    system_prompt = """You are Alex Chen, an operations coordinator at Dale Carnegie Training GTA. 
You are professional, warm, and helpful. Your goal is to assist with scheduling, inquiries, 
and providing information about Dale Carnegie programs.

Key information:
- Dale Carnegie Training helps leaders and teams improve communication and leadership skills
- Programs include: DCC (8-week evening program), Leadership Boot Camps (3-day intensive), HIP (High Impact Presentations)
- Locations: Toronto, Mississauga, Burlington, Kitchener, Niagara
- Tone: Professional but warm, consultative not salesy"""

    if context:
        system_prompt += f"\n\nConversation context: {context}"

    try:
        response = client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"


def text_to_speech(text: str, output_file: str = "output.mp3"):
    """Note: Groq doesn't have native TTS yet. 
    Using ElevenLabs or OpenAI TTS as fallback."""
    print(f"📝 Text to speak: {text[:100]}...")
    print("⚠️  Groq doesn't have native TTS yet.")
    print("   Recommend: Use ElevenLabs or OpenAI TTS for voice output")
    print(f"   Output would be saved to: {output_file}")


def conversation_mode():
    """Interactive text-based conversation"""
    print("=" * 60)
    print("🎙️  Groq Voice Chat (Text Mode)")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    context = ""
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye!")
            break
        
        # Generate response
        response = generate_response(user_input, context)
        print(f"\nAlex: {response}\n")
        
        # Update context (keep last few exchanges)
        context += f"User: {user_input}\nAlex: {response}\n"
        if len(context) > 2000:
            context = context[-2000:]


def demo():
    """Quick demo of capabilities"""
    print("=" * 60)
    print("🚀 Groq Voice System Demo")
    print("=" * 60)
    
    # Test transcription capability
    print("\n✅ Groq client initialized")
    print(f"   Whisper model: {WHISPER_MODEL}")
    print(f"   LLM model: {LLAMA_MODEL}")
    
    # Test conversation
    test_inputs = [
        "Hi, I'm interested in leadership training for my team",
        "We have about 15 people in our sales department",
        "What's the difference between the boot camp and the 8-week program?"
    ]
    
    print("\n📝 Testing conversation flow:\n")
    
    for user_input in test_inputs:
        print(f"User: {user_input}")
        response = generate_response(user_input)
        print(f"Alex: {response[:150]}...\n")
    
    print("=" * 60)
    print("Demo complete! Run with --mode conversation for interactive chat")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Groq Voice Messaging System")
    parser.add_argument(
        "--mode",
        choices=["demo", "conversation", "transcribe", "speak"],
        default="demo",
        help="Operation mode"
    )
    parser.add_argument("--file", help="Audio file for transcription")
    parser.add_argument("--text", help="Text for TTS")
    
    args = parser.parse_args()
    
    if args.mode == "demo":
        demo()
    elif args.mode == "conversation":
        conversation_mode()
    elif args.mode == "transcribe":
        if not args.file:
            print("❌ Please provide --file for transcription")
            sys.exit(1)
        result = transcribe_audio(args.file)
        print(f"Transcription: {result}")
    elif args.mode == "speak":
        if not args.text:
            print("❌ Please provide --text for TTS")
            sys.exit(1)
        text_to_speech(args.text)


if __name__ == "__main__":
    main()
