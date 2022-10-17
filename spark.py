##
## KAPSULON PROJECT, 2022
## spark
## File description:
## spark main file
##

import os
import rich
from InquirerPy import inquirer

def is_directory_empty():
    return len(os.listdir(".")) == 0

def can_create_project(x):
    if x == "Create a new project":
        return is_directory_empty()
    return True

def ask_project_name():
    return inquirer.text(
        message="Project name: ",
        validate=lambda x: x != "",
        invalid_message="You must enter a project name"
    ).execute()

def create_project():
    name = ask_project_name()

def select_file_template():
    choice = inquirer.select(
        message="Select a file template",
        choices=[
            "Main project Makefile  (Makefile)",
            "lib Makefile           (Makefile)",
            "C Header file          (header.h)",
            ".gitignore             (.gitignore)",
        ],
        border=True,
        show_cursor=False,
        cycle=True
    ).execute()

def main():
    action = inquirer.select(
        message="Select an action: ",
        choices=[
            "Create a new project",
            "Create a new file"
        ],
        default=None,
        validate=can_create_project,
        invalid_message="You can't create a new project in a non-empty directory",
        border=True,
        show_cursor=False,
        cycle=True
    ).execute()
    if action == "Create a new project":
        create_project()
    elif action == "Create a new file":
        select_file_template()

if __name__ == "__main__":
    main()
