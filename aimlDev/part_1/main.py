import os
import json
import google.generativeai as genai

INPUT_FILE_PATH = "prompts.txt"
OUTPUT_FILE_PATH = "gemma_responses.json"
MODEL_NAME = "gemma-3-1b-it"


def initialize_llm_client():
    
    try:
        
        api_key = os.environ["GOOGLE_API_KEY"] = "AIzaSyCtc7OovMoq_jXyR-wABg99DR0q05mxkwI"
        if not api_key:
            raise ValueError("API key not found. Set the GOOGLE_API_KEY environment variable.")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)
        print(f"Successfully initialized the '{MODEL_NAME}' model.")
        return model
    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during initialization: {e}")
        return None


def read_prompts_from_file(file_path):

    try:
        with open(file_path, 'r') as file:
            # Read all lines and strip whitespace. Ignore any that are empty.
            prompts = [line.strip() for line in file if line.strip()]
            print(f"Found {len(prompts)} prompts in '{file_path}'.")
            return prompts
    except FileNotFoundError:
        print(f"Error: The input file was not found at '{file_path}'.")
        return []


def generate_responses(model, prompts_list):

    results = []
    total_prompts = len(prompts_list)
    for i, prompt in enumerate(prompts_list):
        print(f"Processing prompt {i + 1}/{total_prompts}: '{prompt}'")
        try:
            response = model.generate_content(prompt)
            results.append({
                "prompt": prompt,
                "response": response.text.strip()
            })
        except Exception as e:
            print(f"An error occurred while processing the prompt: {e}")
            results.append({
                "prompt": prompt,
                "response": f"ERROR: Failed to get a response. Details: {str(e)}"
            })
    return results


def save_data_to_json(data, file_path):
    
    try:
        with open(file_path, 'w') as json_file:
            # indent=4 makes the JSON file human-readable.
            json.dump(data, json_file, indent=4)
        print(f"Successfully saved all responses to '{file_path}'.")
    except IOError as e:
        print(f"Error: Could not write to the file at '{file_path}'. Details: {e}")


def main():

    print("--- Starting Gemma API Script ---")
    
    gemma_model = initialize_llm_client()
    if not gemma_model:
        print("Exiting due to initialization failure.")
        return

    prompts = read_prompts_from_file(INPUT_FILE_PATH)
    if not prompts:
        print("No prompts found to process. Exiting.")
        return

    llm_results = generate_responses(gemma_model, prompts)
    
    if llm_results:
        save_data_to_json(llm_results, OUTPUT_FILE_PATH)
    
    print("--- Script finished ---")


if __name__ == "__main__":
    main()