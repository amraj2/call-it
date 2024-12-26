from RealtimeSTT import AudioToTextRecorder
import pyautogui
import ollama
from ollama import chat
from ollama import ChatResponse
from gtts import gTTS
import os

question=""

# Setup gTTS
def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("ffplay -autoexit output.mp3")

# Setup AudioRecorder

# Set up Ollama API
def ask_ollama(question):
    text = "You are a highly skilled and world-class IT Support Engineer with extensive expertise in diagnosing, resolving, and explaining complex IT issues. Your primary focus is on delivering accurate, concise, and actionable solutions for IT-related inquiries, ranging from basic troubleshooting to advanced system and network configurations. You are expected to respond to IT-related queries with clarity, professionalism, and precision, always adhering to industry best practices and current technological standards. If a query falls outside the domain of IT, you must politely inform the user that it is beyond your scope and end the conversation without providing any speculative or unrelated information. Under no circumstances should you answer or guess about non-IT-related topics. Your goal is to ensure users receive top-tier IT assistance while maintaining focus and integrity in your area of expertise. When giving a response restrict the anser to 100 characters." + question 
    return ollama.generate(model='llama3.2', prompt=text)
    # reply=""
    # stream = chat(
    #     model='llama3.2',
    #     messages=[{'role': 'assistant', 'content': 'You are a world class IT Support Engineer, any question not related to IT please decline to answer and end the chat without an answer or guess.'},
    #               {'role': 'user', 'content': question}],
    #     stream=False,
    # )

    # for chunk in stream:
    #     return print(chunk['message']['content'], end='', flush=True)

    # return reply

# Setup TTS with mic
def process_text(text):
    # speak("Hello Im Llamabot, how can I help you?")
    print(text)
    # print("Let me think about that")
    reply = ask_ollama(text)["response"]
    print(reply)
    speak(reply)



if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    # speak("Hello Im Llamabot, how can I help you?")
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)
