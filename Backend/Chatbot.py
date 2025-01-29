import datetime
from json import dump, load

from dotenv import dotenv_values
from groq import Groq


env_vars = dotenv_values(".env")


Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages: list = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

SystemChatBot = [
    {"role": "system", "content": System},
]


try:
    with open(r"Data\ChatLog.json", "r") as file:
        messages = load(file)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as file:
        dump([], file, indent=4)


def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = "Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date} {month} {year}\nTime: {hour}:{minute}:{second}"
    return data


def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer


def ChatBot(Query):
    try:
        with open(r"Data\ChatLog.json", "r") as file:
            messages = load(file)

        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot
            + [{"role": "system", "content": RealtimeInformation()}]
            + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )
        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as file:
            dump(messages, file, indent=4)

        return AnswerModifier(Answer)
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as file:
            dump([], file, indent=4)
        return ChatBot(Query)


if __name__ == "__main__":
    while True:
        user_input = input("Enter your question: ")
        print(ChatBot(user_input))
