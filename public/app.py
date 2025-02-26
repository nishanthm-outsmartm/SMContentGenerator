import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "localhost:3000"}})

# Replace 'your_openai_api_key' with your actual OpenAI API key
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

def extract_images(url):
    """Extract images from a given webpage URL using BeautifulSoup."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all image URLs
        images = [img["src"] for img in soup.find_all("img") if "src" in img.attrs]

        # Convert relative URLs to absolute URLs
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        full_image_urls = [img if img.startswith("http") else base_url + img for img in images]

        return full_image_urls[:5]  # Return up to 5 images
    except Exception as e:
        print("Image extraction error:", e)
        return []

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        url = data.get("url", "")
        tone = data.get("tone", "neutral")

        # Step 1: Use OpenAI's GPT-4 Turbo to generate a summary
        prompt = f"Summarize the following webpage content in a {tone} tone:\n{url}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Use GPT-4 turbo model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        summary_text = response['choices'][0]['message']['content']

        # Step 2: Extract images from the URL
        extracted_images = extract_images(url)

        # Final API response
        final_response = {
            "summary": summary_text,
            "media": extracted_images
        }

        print("Generated Response:", final_response)  # ✅ Debugging output
        return jsonify(final_response)

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
