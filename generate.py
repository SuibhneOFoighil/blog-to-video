import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm
from PIL import Image
from io import BytesIO
from openai import OpenAI
load_dotenv()
client = OpenAI()

def description(chunks: list) -> list[str]:

    print("Generating visual descriptions...")
    prompts = [
        f"""You are an expert visual artist. You are given a chunk of text and asked to describe a visual representation of the text.

        Here are some examples of visual descriptions:
        Example 1: A dystopian city in the desert with massive sharp spike-like architecture. A colossal floating snake like creature glides between the spikes. a man with a mech-suit is flying with boosters at the same height as the creature. Inspired by "Dune" and Syd Mead.
        Example 2: Scene from the movie "Wall E". the text "Walmart" as a hologram in a massive shopping district inside of a spaceship. People are eating and drinking coffee at a cafe to the side, overlooking a large aquarium decoration with fish and jellyfish.

        The chunk of text is: {chunk}
        Your visual description:
        """
        for chunk in chunks
    ]
    
    results = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompts,
        max_tokens=500,
    )
    descriptions = [result.text for result in results.choices]
    
    #save descriptions 
    for i, description in enumerate(descriptions):
        with open(Path(__file__).parent / "descriptions" / f"{i}.txt", "w") as fl:
            fl.write(description)

    return descriptions


def narrative(chunks: list):
    print("Generating audio narrative...")
    for i, chunk in enumerate(tqdm(chunks)):
        speech_file_path = Path(__file__).parent / "audio" / f"{i}.mp3"
        text = f"{chunk}"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(speech_file_path)

def visuals(descriptions: list[str]):
    print("Generating visuals...")
    urls = []
    for description in tqdm(descriptions):
        response = client.images.generate(
            model="dall-e-3",
            prompt=description,
            n=1
        )
        url = response.data[0].url
        urls.append(url)
    
    #download images
    print("Downloading images...")
    for i, url in enumerate(urls):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.save(Path(__file__).parent / "images" / f"{i}.png")


