import requests

class VisionEngine:
    def __init__(self, ollama_url="http://localhost:11434"):
        self.url = f"{ollama_url}/api/generate"

    def analyze_screen(self, base64_image: str, context_prompt: str) -> str:
        payload = {
            "model": "llava",  # Ensure you ran `ollama pull llava`
            "prompt": f"Analyze this UI capture and outline clickable regions or UI components related to the task. Context/Task: {context_prompt}",
            "stream": False,
            "images": [base64_image]
        }
        try:
            response = requests.post(self.url, json=payload)
            return response.json().get("response", "")
        except Exception as e:
            return f"Vision Model Error: {str(e)}"