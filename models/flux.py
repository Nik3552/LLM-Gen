import requests
from io import BytesIO
from g4f.client import Client
from utils import history

client = Client()


def query_flux(prompt):
    if len(prompt) <= 0:
        return

    try:
        response = client.images.generate(
            model="flux", prompt=prompt, response_format="url"
        )
        url = response.data[0].url

        if not url:
            return "Failed to generate image"

        image_response = requests.get(url)
        image_data = BytesIO(image_response.content)

        history.add_to_history("flux", prompt, image_response)
        return image_data
    except Exception as e:
        return f"Error from Flux API: {e}"
