# Loads configuration settings from JSON file
import json

# Reads config file and handles missing/invalid JSON safely
def load_config(path = "config.json"):
    try:
        with open(path,'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("JSON is Missing!")
        return {}
    except json.JSONDecodeError:
        print("Invalid JSON format!")
        return {}
