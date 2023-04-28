##
## EPITECH PROJECT, 2023
## spark
## File description:
## errors
##

def get_error_desc(code: str) -> str:
    errors = {
        "C-O1": "Compiled, temporary or unnecessary file",
        "C-O3": "Too many functions in a file (>=5)",
        "C-O4": "Name not following snake case convention",
        "C-G1": "Missing or invalid header",
        "C-G2": "Separation of functions",
        "C-G3": "Indentation of preprocessor directives",
        "C-G4": "Global variables",
        "C-G5": "Including non header files",
        "C-G6": "Invalid line ending",
        "C-G7": "Trailing spaces",
        "C-G8": "Trailing lines",
        "C-F3": "Too many characters in a line (>=80)",
        "C-F4": "Too many lines in a function (>=20)",
        "C-F5": "Too many parameters in a function (>=4)",
        "C-F6": "Function without a parameter",
        "C-F8": "Comment inside a function",
        "C-F9": "Nested function",
        "C-L2": "Invalid indentation",
        "C-L3": "Invalid number of spaces",
        "C-L4": "Curly brackets",
        "C-C1": "Too many conditional statements (>=3)",
        "C-C3": "Goto statement (cringe)",
        "C-H1": "Header content",
        "C-H2": "Include guard",
        "C-A3": "Line break at End Of File",
    }
    if code in errors:
        return errors[code]
    return f"Unknown error ({code})"
