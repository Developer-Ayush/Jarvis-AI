import pygame
import random
import os
import asyncio
import edge_tts
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

# Ensure 'Data' directory exists
os.makedirs("Data", exist_ok=True)

async def TextAudioFile(text) -> None:
    file_path = "Data/speech.mp3"
    
    # Validate the AssistantVoice
    if not AssistantVoice or not isinstance(AssistantVoice, str):
        raise ValueError("AssistantVoice is either not set or invalid in the .env file.")
    
    print(f"Using voice: {AssistantVoice}")
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)

def TTS(Text, func=lambda: True):
    try:
        # Generate audio asynchronously
        asyncio.run(TextAudioFile(Text))

        file_path = "Data/speech.mp3"
        if os.path.exists(file_path):
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if not func():
                    break
                pygame.time.Clock().tick(10)
        else:
            raise FileNotFoundError("Audio file was not created successfully.")
    except ValueError as ve:
        print(f"Error in TTS: {ve}")
    except Exception as e:
        print(f"Error in TTS: {e}")
    finally:
        try:
            func()
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error in the finally block: {e}")

def TextToSpeech(Text, func=lambda: True):
    Data = str(Text).split(".")
    
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    if len(Data) > 4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 and len(Text) >= 10000000000000000000000000000000000000000000000000000000000000000000000000:
        TTS(". ".join(Data[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

if __name__ == "__main__":
    try:
        print("Text-to-Speech Program (Type 'exit' to quit)")
        print(f"AssistantVoice loaded from .env: {AssistantVoice}")
        while True:
            TextToSpeech(input("Enter the text: "))
    except KeyboardInterrupt:
        print("\nExiting program.")