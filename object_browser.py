import json
import os
import random
import requests

def get_commit_url(instance_id: str):
    """Get the url of related commit"""
    repo_author = instance_id.split('__', 1)[0]
    repo = instance_id.split('__', 1)[1]
    pr = repo.split('-')[-1]
    repo_name = '-'.join(repo.split('-')[:-1])
    pr_response = requests.get(f"https://api.github.com/repos/{repo_author}/{repo_name}/pulls/{pr}")
    commit_sha = pr_response.json().get('merge_commit_sha')
    if commit_sha:
        commit_url = f"https://github.com/{repo_author}/{repo_name}/commit/{commit_sha}"
    else: 
        commit_response = requests.get(f"https://api.github.com/repos/{repo_author}/{repo_name}/pulls/{pr}/commits")
        commit_sha = commit_response.json()[-1]['sha']
        commit_url = f"https://github.com/{repo_author}/{repo_name}/commit/{commit_sha}"

    return commit_url

def load_json_file(filename,  sample: int = 236):
    """Load and parse JSON file"""
    try:
        if filename.endswith('.json'):
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        
        sampled_mutants = data
        
        return sampled_mutants
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filename}': {e}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def display_object(obj, index, total):
    """Display a single object with formatting"""
    commit_url = get_commit_url(obj.get('instance_id'))
    print("\n" + "="*50)
    print(f"Object {index + 1} of {total}")
    print(f"Mutant ID: {obj.get('mutant_id')}")
    print(f"Commit URL: {commit_url}")
    print("="*50)
    print("Code for Evaluation:\n", obj.get('full_function'))
    print("="*50)

def browse_json_objects(filename, sample: int = 236):
    """Main function to browse JSON objects"""
    data = load_json_file(filename, sample)
    
    if data is None:
        return
    
    # Handle different JSON structures
    if isinstance(data, list):
        objects = data
    elif isinstance(data, dict):
        # If it's a dict, treat each key-value pair as an object
        objects = [{"key": k, "value": v} for k, v in data.items()]
    else:
        # If it's a single value, wrap it in a list
        objects = [data]
    
    if not objects:
        print("No objects found in the JSON file.")
        return
    
    print(f"Found {len(objects)} objects in '{filename}'")
    
    index = 0
    total = len(objects)

    label_results = []

    while index < total:
        display_object(objects[index], index, total)

        current_object = {
            'mutant_id': objects[index].get('mutant_id'),
            'natural': 2,
            'equivalent': 2
        }
        
        # Wait for user input
        print("Check for equivalent: Does the changed program behaves identically to the original program for ALL possible inputs?")
        user_input = input("Press 1 for YES, 0 for NO, enter for UNSURE, or 'q' to quit: ").strip().lower()
        
        if user_input == 'q':
            print("Goodbye!")
            break
        elif user_input == "1":
            current_object["equivalent"] = 1
        elif user_input == "0":
            current_object['equivalent'] = 0

        # Wait for user input
        print("\nCheck for natural: Does the change represent a REALISTIC change that a developer might make?")
        user_input = input("Press 1 for YES, 0 for NO, enter for UNSURE, or 'q' to quit: ").strip().lower()
        
        if user_input == 'q':
            print("Goodbye!")
            label_results.append(current_object)
            break
        elif user_input == "1":
            current_object["natural"] = 1
        elif user_input == "0":
            current_object["natural"] = 0
        
        label_results.append(current_object)

        index += 1
        
        # Clear screen for better readability (optional)
        os.system('cls' if os.name == 'nt' else 'clear')
    
    if index >= total:
        print("\nReached the end of all objects!")
    
    return label_results

def main():
    """Main entry point"""
    print("JSON Object Browser")
    print("-" * 20)
    
    # CHANGE FILENAME HERE
    filename = "test_sampled_mutants.json"
    file_id = filename.split('_')[0]
    
    if not filename:
        print("No filename provided.")
        return
    
    # Change sample size here
    label_results = browse_json_objects(filename)

    with open(f"label_{file_id}.json", 'w') as f:
        json.dump(label_results, f, indent=2)

if __name__ == "__main__":
    main()