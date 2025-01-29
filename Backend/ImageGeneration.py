import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt: str):
    # Create a folder path based on the query name
    folder_path = os.path.join("Data/Images", prompt.replace(" ", "_"))
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    Files = [f"{prompt.replace(' ', '_')}{i}.png" for i in range(1, 5)]

    # Check if all files exist first
    for png_file in Files:
        image_path = os.path.join(folder_path, png_file)

        # Check if the image file exists before opening it
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                print(f"Opening image: {image_path}")
                img.show()
                sleep(1)
            except IOError:
                print(f"Unable to open {image_path}")
        else:
            print(f"Image not found: {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt: str):
    tasks = []
    image_bytes_list = []

    # Create a folder path based on the query name
    folder_path = os.path.join("Data/Images", prompt.replace(" ", "_"))
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Generate images asynchronously
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Gather all image responses
    image_bytes_list = await asyncio.gather(*tasks)

    # Save the images sequentially to the newly created folder
    for i, image_bytes in enumerate(image_bytes_list):
        image_path = os.path.join(folder_path, f"{prompt.replace(' ', '_')}{i+1}.png")
        with open(image_path, "wb") as f:
            f.write(image_bytes)
            sleep(1.5)
        print(f"Saved image: {image_path}")

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

while True:
    try:
        with open(r"Frontend/Files/ImageGeneration.data", "r") as f:
            Data: str = f.read()

        Prompt, Status = Data.split(",")

        if Status == "True":
            print("Generating Images...")
            ImageStatus = GenerateImages(prompt=Prompt)

            with open(r"Frontend/Files/ImageGeneration.data", "w") as f:
                f.write("False,False")
                break

        else:
            sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        sleep(1)
