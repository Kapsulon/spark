##
## SPARK PROJECT, 2022
## spark
## File description:
## spark main file
##

from spark_printer import *
from coding_style_analyser import *

from time import sleep
import requests
import os
import sys
import rich
from InquirerPy import inquirer
import json
import re

SPARK_DIR = "/usr/local/lib/spark/"

def run_coding_style_report():
    print_spark("[bold yellow]Analyzing coding style report...[/bold yellow]")
    report = open("coding-style-reports.log", "r").read()
    if report == "":
        print_spark("[bold green]No errors found.[/bold green]")
    else:
        print_spark("[bold red]Errors found.[/bold red]")
        errors = analyse_coding_style_report(report)
        display_coding_style_report(errors)
    os.system("rm coding-style-reports.log")

def run_coding_style_check():
    console = rich.console.Console()
    print_spark("[bold yellow]Running coding style check...[/bold yellow]")
    os.system("coding-style . . > /dev/null")
    run_coding_style_report()


def replace_placeholders(content:str):
    placeholders = re.findall("%[a-zA-Z]+%", content)
    place = {}
    for placeholder in placeholders:
        if not placeholder in place:
            place[placeholder] = ask_string(placeholder.replace("%", ""))
    for placeholder in place:
        while placeholder in content:
            if placeholder == "%FILENAME%":
                content = content.replace(placeholder, place[placeholder].upper())
            else:
                content = content.replace(placeholder, place[placeholder])
    return content

def create_file_from_template(template:str):
    templates = json.loads(open(SPARK_DIR + "templates/manifest.json", "r").read()).get("templates")
    for t in templates:
        if t["name"] == template:
            with open(SPARK_DIR + "templates/" + t["path"], "r") as f:
                content = f.read()
            if t["name_replace"].count("%") == 2:
                fname = ask_string(t["name_replace"].replace("%", ""))
                if fname.endswith(".h.h"):
                    fname = fname[:-2]
                elif not fname.endswith(".h"):
                    fname += ".h"
                with open(fname, "w") as f:
                    f.write(replace_placeholders(content))
            else:
                with open(t["name_replace"], "w") as f:
                    f.write(replace_placeholders(content))
            print_spark_prefix()
            rich.print("[bold green]File created.[/bold green]")
            break

def is_directory_empty():
    content = os.listdir(".")
    if ".git" in content:
        content.remove(".git")
    return len(content) == 0

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
    os.mkdir("lib")
    os.mkdir("lib/my")
    os.mkdir("include")
    select_file_template(".gitignore")
    select_file_template("C Header File")
    os.system("mv *.h include/")
    select_file_template("C lib Makefile")
    os.system("mv Makefile lib/my/")
    select_file_template("C Main project Makefile")
    print_spark_prefix()
    rich.print("[bold green]Project created.[/bold green]")


def select_file_template(choice=None):
    try:
        if choice == None:
            choice = inquirer.select(
                message="Select a file template",
                choices=[
                    "C Main project Makefile    (Makefile)",
                    "C lib Makefile             (Makefile)",
                    "C Header File              (header.h)",
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
    version = open(SPARK_DIR + "VERSION", "r").read()
    if requests.get("https://raw.githubusercontent.com/Kapsulon/spark/main/VERSION").text != open(SPARK_DIR + "VERSION", "r").read():
        print_spark_prefix()
        rich.print("[bold yellow]A new version of Spark is available, would you like to update it ?\n[/bold yellow]")
        if inquirer.confirm(message="Update Spark ?").execute():
            os.system("curl https://raw.githubusercontent.com/Kapsulon/spark/main/install.sh | sh")
            print_spark_prefix()
            rich.print("[bold green]Spark has been updated.[/bold green]")
            sleep(1)
            os.execv(sys.executable, ["python3"] + sys.argv)
        else:
            print_spark_prefix()
            rich.print("[bold red]Spark has not been updated.[/bold red]")
    else:
        print_spark_prefix()
        rich.print(f"[bold green]Spark is up to date. ({version})[/bold green]")

def main():
    os.system("clear")
    print_spark_header()
    check_update()
    try:
        action = inquirer.select(
            message="Select an action: ",
            choices=[
                "Run coding style check",
                "Create new project from template",
                "Create new file from template"
            ],
            default=None,
            validate=can_create_project,
            invalid_message="You can't create a new project in a non-empty directory",
            border=True,
            show_cursor=False,
            cycle=True
        ).execute()
        if action == "Create new project from template":
            create_project()
        elif action == "Create new file from template":
            select_file_template()
        elif action == "Run coding style check":
            run_coding_style_check()
    except KeyboardInterrupt:
        error_keyboard_interrupt()

if __name__ == "__main__":
    main()
