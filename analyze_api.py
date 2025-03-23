import requests
from config import OPENAI_API_KEY,GEMINI_API_KEY


def analyzebyGPT(frames_file, output_summary):
    """
    Analyzes the given frames file using OpenAI's GPT API and writes the summary to a file.
    """
    with requests.Session() as session:
        try:
            
            with open(frames_file, 'r', encoding='utf-8', errors='replace') as file:
                file_content = file.read()
        except Exception as e:
            return f"Error reading frames file: {e}"

        # Prepare headers and payload for GPT API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": "The content contains descriptions of frames in a video. Please analyze it."},
                {"role": "user", "content": file_content}
            ],
            "max_tokens": 1000
        }

        try:
            # Send the request to OpenAI API
            response = session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            summary = response.json()["choices"][0]["message"]["content"]

            # Write the summary to the output file
            with open(output_summary, 'w', encoding='utf-8', errors='replace') as out_file:
                out_file.write(summary)

            return summary
        except requests.exceptions.RequestException as e:
            return f"Error making API request: {e}"
        except Exception as e:
            return f"Error processing API response: {e}"


def analyze_by_gemini(frames_file, output_summary):
    """
    Analyzes the given frames file using Gemini API and writes the summary to a file.
    """
    with requests.Session() as session:
        try:
            # Read the content of the frames file
            with open(frames_file, 'r', encoding='utf-8', errors='replace') as file:
                file_content = file.read()
        except Exception as e:
            return f"Error reading frames file: {e}"

        # Adjust headers and payload as per Gemini API documentation
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GEMINI_API_KEY}"
        }

        payload = {
            "model": "gemini-v1",  # Replace with the correct Gemini model
            "messages": [
                {"role": "user", "content": "Analyze the content describing video frames."},
                {"role": "user", "content": file_content}
            ],
            "max_tokens": 1000
        }

        try:
            # Send the request to Gemini API
            response = session.post("https://api.gemini.ai/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            summary = response.json()["choices"][0]["message"]["content"]

            # Write the summary to the output file
            with open(output_summary, 'w', encoding='utf-8', errors='replace') as out_file:
                out_file.write(summary)

            return summary
        except requests.exceptions.RequestException as e:
            return f"Error making API request: {e}"
        except Exception as e:
            return f"Error processing API response: {e}"
