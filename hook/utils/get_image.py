import requests
import csv
import os
import uuid
from urllib.parse import urljoin

csv_file = "image_links.csv"

def get_image(img_url:str,filename:str) -> None:
    os.makedirs(f"images/{filename}", exist_ok=True)
    try:
        img_data = requests.get(img_url).content
        img_name = f"images/{filename}/image_{uuid.uuid4().hex}.jpg"
        with open(img_name, "wb") as img_file:
            img_file.write(img_data)
        print(f"Image saved: {img_name}")
    except Exception as e:
        print(f"Failed to download image from {img_url}: {e}")

    print("All images have been successfully downloaded.")
