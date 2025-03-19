# README

## Overview

This repository contains a Python script `Requesting.py` that interacts with a local Ollama model to generate responses based on user prompts. The script ensures that the Ollama server is running, checks for the existence of the specified model, and generates responses using the model.

## Requirements

- Python 3.x
- Ollama Python client (`ollama`)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python package:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure the Ollama server is running (run `ollama` in your command line and you should see the help text about how to use it). The script will attempt to start the server if it is not already running.

2. Run the script with a prompt:
    ```sh
    python Requesting.py
    ```

3. The script will generate a response based on the provided prompt and model.

## Example

To generate a response using the `codellama:7b` model with a specific prompt and system instruction, you can modify the `__main__` section of the script:

```python
if __name__ == "__main__":
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
```

## Troubleshooting

If you get a ModuleNotFoundError it means that your environment cannot resolve the ollama component of the code. Make sure to install the Ollama client from [ollama.com](https://ollama.com) and have it running on your device before running this code.
Also, try running Ollama on your command line before running Requesting.py.

## Extending the Script

### Adding More Models

To add more models, ensure they are available in the Ollama repository and modify the `model_name` variable accordingly.
The system will install the model if it can find a model with that name.

### Customizing Prompts

You can customize the user prompt and system instruction to suit different needs. Modify the `user_prompt` and `system_instruction` variables in the `__main__` section.

### Error Handling

The script includes basic error handling. You can extend this by adding more specific exceptions and handling mechanisms as needed.

### Background Process Management

The script handles starting the Ollama server in the background for different operating systems. You can modify the `ensure_ollama_running` function to include additional configurations or logging.

## Contributing

Feel free to fork the repository and submit pull requests for any enhancements or bug fixes.
