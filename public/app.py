import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

# Replace 'your_deepseek_api_key' with your actual DeepSeek API key
DEEPSEEK_API_KEY = 'sk-87bbe9b28cbb42bd911a33b9b8b10f11'
DEEPSEEK_API_URL = 'https://api.deepseek.ai/generate'  # Replace with the actual endpoint

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

        # Step 1: Use DeepSeek AI API to generate a summary
        payload = {
            'url': url,
            'tone': tone,
        }

        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception('Failed to generate content from DeepSeek AI')

        summary_text = response_data.get("summary", "No summary generated.")

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
