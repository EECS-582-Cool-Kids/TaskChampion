""" Prologue:
 *  Module Name: extra_styles.py
 *  Purpose: Access extra specific styles for the GUI.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Jacob Wilkus, Mo Morgan, Richard Moser, Derek Norton
 *  Date: 2/26/2025
 *  Last Modified: 2/28/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""
style_string = None  # Start as None to distinguish "not loaded" from "empty file"


def get_style_string():
    # open style.qss, read it to a global string
    style_str = ""
    with open ('styles/style.qss', 'r') as f:  # Open the style file.
        style_str = f.read()  # Read the style file.
    return style_str  # Return the style string


def get_style(style_name):
    global style_string
    if style_string is None:  # Only load if it's never been loaded
        style_string = get_style_string()  # Load the style string
        
    # find the style in the style string. The style will be named #style_name have contents with curly braces
    start = style_string.find(f"#{style_name}")  # Find the style name in the style string.
    if start == -1:  # If the style name is not found.
        return None
    
    end = style_string.find("}", start)  # Find the closing curly brace.
    # print(f"Found style {style_name} contents: {style_string[start:end]}")
    return style_string[start:end+1]  # Return the style contents
