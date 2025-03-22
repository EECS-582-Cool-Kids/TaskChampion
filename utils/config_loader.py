""" Prologue
 *  Module Name: config_loader.py
 *  Purpose: Exports tools for dealing with config files.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Jacob Wilkus, Ethan Berkley
 *  Date: 3/12/2025
 *  Last Modified: 3/22/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: FileNotFoundError: if the configuration file does not exist, json.JSONDecodeError:
                                if the contents of the configuration file are not valid JSON.
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

import json
import os

# Used by XPConfigDialog
XP_CONFIG="config/user_defined_xp.json"

def load_config(config_file):
    """
    Loads configuration data from a file into a dictionary attribute.

    This method reads a JSON formatted configuration file specified by the
    `config_file` attribute and populates the `config` attribute with the
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
        return {"priorities": {'H': 10, 'M': 5, 'L': 1, None: 0.5}, "tags": {}, "projects": {}}

def save_config(config, config_file):
    os.makedirs('config/', exist_ok=True)
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=2)