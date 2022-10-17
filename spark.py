##
## KAPSULON PROJECT, 2022
## spark
## File description:
## spark main file
##

import requests
import os
import rich
from InquirerPy import inquirer

SPARK_DIR = "/usr/local/lib/spark/"

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
            "C Main project Makefile  (Makefile)",
            "C lib Makefile           (Makefile)",
            "C Header file          (header.h)",
            ".gitignore             (.gitignore)",
        ],
        border=True,
        show_cursor=False,
        cycle=True
    ).execute()

def error_keyboard_interrupt():
    rich.print("[bold red]Aborted.\n[/bold red]")

def check_update():
    if requests.get("https://raw.githubusercontent.com/Kapsulon/spark/main/VERSION").text != open(SPARK_DIR + "VERSION", "r").read():
        rich.print("[bold yellow]A new version of Spark is available, would you like to update it ?\n[/bold yellow]")
        if inquirer.confirm(message="Update Spark ?").execute():
            os.system("curl https://raw.githubusercontent.com/Kapsulon/spark/main/install.sh | sh")
            rich.print("[bold green]Spark has been updated.[/bold green]")
            exit(0)
        else:
            rich.print("[bold red]Spark has not been updated.[/bold red]")
    else:
        rich.print("[bold green]Spark is up to date.[/bold green]")

def main():
    check_update()
    try:
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
    except KeyboardInterrupt:
        error_keyboard_interrupt()

if __name__ == "__main__":
    main()
