import os
import requests
import json

def run_llm_reader_test():
    txt_path = "data/yt_transcript.txt"
    
    print("[1/3] Checking for existing transcript data file...")
    if not os.path.exists(txt_path):
        print(f"Error: Could not find '{txt_path}'. Please run your transcript extractor tool first!")
        return
        
    print(f"SUCCESS: Found video data file at '{txt_path}'")

    print("\n[2/3] Reading file contents safely into memory text context...")
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            saved_transcript_text = f.read()
            
        print(f"SUCCESS: Loaded {len(saved_transcript_text)} characters from disk.")
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    print("\n[3/3] Sending file text to Local Ollama (Qwen) for safe summary...")
    try:
        # Build the structured prompt telling Qwen to process the file content
        prompt = (
            "You are a helpful desktop assistant. Below is a text transcript read directly from a local storage file.\n"
            "Please read it carefully and provide a clean, high-level summary highlighting the key takeaways.\n\n"
            f"--- START OF FILE DATA ---\n{saved_transcript_text}\n--- END OF FILE DATA ---"
        )
        
        # Connect directly to your local Ollama endpoint
        ollama_url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": "qwen3:8b",  # Adjust to match your exact local name if it's "qwen:8b"
            "prompt": prompt,
            "stream": False   # Keep stream False to prevent sudden I/O floods in the terminal
        }
        
        response = requests.post(ollama_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            summary_text = result.get("response", "")
            
            print("\n" + "="*50)
            print("🌟 CHAT AGENT VIDEO SUMMARY RESPONSE (OLLAMA QWEN):")
            print("="*50)
            print(summary_text)
            print("="*50 + "\n")
        else:
            print(f"Ollama returned an error status: {response.status_code} - {response.text}")
        
    except Exception as e:
        print(f"Local Ollama connection failed: {e}")

if __name__ == "__main__":
    run_llm_reader_test()