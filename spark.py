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
import json
import re

SPARK_DIR = "/usr/local/lib/spark/"

def replace_placeholders(content:str):
    placeholders = re.findall("%*%", content)
    for placeholder in placeholders:
        content = content.replace(placeholder, ask_string(placeholder))
    return content

def create_file_from_template(template:str):
    templates = json.loads(open(SPARK_DIR + "templates/manifest.json", "r").read())
    for t in templates:
        if t["name"] == template:
            with open(t["file"], "r") as f:
                content = f.read()
            if t["name_replace"].count("%") == 2:
                with open(ask_string("File name"), "w") as f:
                    f.write(replace_placeholders(content))
            else:
                with open(t["name_replace"], "w") as f:
                    f.write(replace_placeholders(content))
            break

def print_spark_header():
    with open(SPARK_DIR + "header.txt", "r") as f:
        rich.print("[bold #FFD533]" + f.read() + "[/bold #FFD533]")

def print_spark_prefix():
    rich.get_console().print("[bold #FFD533]Spark[/bold #FFD533] > ", end="")

def is_directory_empty():
    return len(os.listdir(".")) == 0

def can_create_project(x):
    if x == "Create a new project":
        return is_directory_empty()
    return True

def ask_string(name="Name"):
    try:
        return inquirer.text(
            message=name + ": ",
            validate=lambda x: x != "",
            invalid_message="You must enter a [" + name + "]"
        ).execute()
    except KeyboardInterrupt:
        error_keyboard_interrupt()

def create_project():
    name = ask_string("Project name")

def select_file_template():
    try:
        choice = inquirer.select(
            message="Select a file template",
            choices=[
                "C Main project Makefile    (Makefile)",
                "C lib Makefile             (Makefile)",
                "C Header file              (header.h)",
                ".gitignore                 (.gitignore)",
            ],
            filter=lambda result: result.split("  ")[0],
            border=True,
            show_cursor=False,
            cycle=True
        ).execute()
        create_file_from_template(choice)
    except KeyboardInterrupt:
        error_keyboard_interrupt()

def error_keyboard_interrupt():
    print_spark_prefix()
    rich.print("[bold red]Keyboard interrupt.[/bold red]\n")

def check_update():
    if requests.get("https://raw.githubusercontent.com/Kapsulon/spark/main/VERSION").text != open(SPARK_DIR + "VERSION", "r").read():
        print_spark_prefix()
        rich.print("[bold yellow]A new version of Spark is available, would you like to update it ?\n[/bold yellow]")
        if inquirer.confirm(message="Update Spark ?").execute():
            os.system("curl https://raw.githubusercontent.com/Kapsulon/spark/main/install.sh | sh")
            print_spark_prefix()
            rich.print("[bold green]Spark has been updated.[/bold green]")
            exit(0)
        else:
            print_spark_prefix()
            rich.print("[bold red]Spark has not been updated.[/bold red]")
    else:
        print_spark_prefix()
        rich.print("[bold green]Spark is up to date.[/bold green]")

def main():
    os.system("clear")
    print_spark_header()
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
