import os
from dotenv import load_dotenv
import requests


def ComputerVision(encoded_image):
  # Load environment variables from the .env file
  load_dotenv()

  # Access the API key
  api_key = os.getenv('OPENAI_API_KEY')

  # Getting the base64 string
  base64_image = encoded_image

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }

  payload = {
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "You are a robot in a warehouse and your goal is to detect what you are seeing. There are 4 possible options: A box, a rack, a pile of boxes or other robots. There can be multiple things in the same image like a robot and a box. Identify what you are seeing and the image and return a text saying 'Im seeing x'."
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  return response.json()['choices'][0]['message']['content']