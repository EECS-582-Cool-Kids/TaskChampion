import json

def load_config(config_file):
    """
    Loads configuration data from a file into a dictionary attribute.

    This method reads a JSON formatted configuration file specified by the
    `config_file` parameter and populates the `config` attribute with the
    parsed content.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file's contents are not
            valid JSON.
    """
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # return some arbitrary default config if the file doesn't exist
        return {"priorities": {'H': 10, 'M': 5, 'L': 1, None: 0.5}, "tags": {}, "projects": {}, "modules": {}}

def save_xp_config(config, config_file):
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=2)

def load_module_config(config_file):
    try:
        with open(config_file, 'r') as file:
            module_data = json.load(file)
            return module_data['modules']
    except (FileNotFoundError, json.JSONDecodeError):
        return {"modules": {"Main": ["Priority", "Due Date", "Project", "Tags", "Recur", "Status", "Start", "Urgency"]}}

def save_module_config(config, config_file):
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=2)
