import subprocess
import time
import sys
import os

# First, ensure the library is installed
try:
    import ollama
    from ollama._types import ChatResponse  # Ensure correct import
except ImportError:
    print("Installing Ollama Python client...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ollama"])
    import ollama
    

def ensure_ollama_running():
    """Ensure the Ollama server is running"""
    try:
        # Try to list models as a simple test
        ollama.list()
        return True
    except Exception as e:
        print(f"Ollama server check failed: {e}")
        print("Starting Ollama server...")
        try:
            # Start Ollama server in the background
            subprocess_args = ["ollama", "serve"]
            
            # Handle different OS requirements for background processes
            if os.name == 'nt':  # Windows
                from subprocess import CREATE_NEW_PROCESS_GROUP, DETACHED_PROCESS
                subprocess.Popen(
                    subprocess_args,
                    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
                )
            else:  # Unix/Linux/Mac
                subprocess.Popen(
                    subprocess_args,
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Give it time to start
            time.sleep(5)
            return True
        except Exception as e:
            print(f"Failed to start Ollama server: {e}")
            return False

def generate_from_ollama(prompt, model="llama2", system_prompt=None):
    """
    Send a prompt to a local Ollama model and receive the generated output.
    
    Args:
        prompt (str): The prompt to send to the model
        model (str): The name of the Ollama model to use
        system_prompt (str, optional): Optional system prompt to guide the model
        
    Returns:
        str: The generated text from the model
    """
    if not ensure_ollama_running():
        return "Failed to start Ollama server"
    
    try:
        # Check if model exists - with better error handling
        model_exists = False
        try:
            models_list = ollama.list()
            # Debug print to see the structure
            print("Available models:", models_list)
            
            # Check if the model exists based on the actual structure
            if isinstance(models_list, dict) and 'models' in models_list:
                model_exists = any(m.get('name') == model for m in models_list['models'])
            else:
                # Alternative structure - directly iterate over the list
                model_exists = any(m.get('name') == model for m in models_list)
        except Exception as e:
            print(f"Error checking models: {e}")
        
        if not model_exists:
            print(f"Model {model} not found. Pulling it now...")
            try:
                ollama.pull(model)
            except Exception as e:
                print(f"Error pulling model: {e}")
                return f"Failed to pull model {model}: {str(e)}"
        
        # Generate response
        try:
            print("Generating response...")
            if system_prompt:
                response = ollama.chat(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
            else:
                response = ollama.chat(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            
            # Debug print to see the structure
            print("Response structure:", response)
            print("type:", type(response))
            
            # Extract the content safely
            if isinstance(response, ChatResponse) and 'message' in response:
                return response['message']['content']
            else:
                return str(response)
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"
    
    except Exception as e:
        print(f"Error using Ollama: {e}")
        return f"General error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    model_name = "codellama:7b"
    user_prompt = "Write a function to calculate the Fibonacci sequence in Python"
    system_instruction = "You are a helpful coding assistant."
    
    response = generate_from_ollama(
        prompt=user_prompt,
        model=model_name,
        system_prompt=system_instruction
    )
    
    if response:
        print("\nModel Response:")
        print(response)