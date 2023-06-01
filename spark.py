##
## SPARK PROJECT, 2022
## spark
## File description:
## spark main file
##

from spark_printer import *
from coding_style_analyser import *
from project_manager import *

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
    sys.exit(0)

def run_coding_style_check():
    print_spark("[bold yellow]Running coding style check...[/bold yellow]")
    os.system("docker exec -it epitest-daemon bash -c \"check.sh $PWD $PWD\"")
    run_coding_style_report()

def place_lib(libs: list[str]) -> str:
    string = ""
    for lib in libs:
        string += "-l" + lib + " "
    string[-1] = ""
    return string

def replace_placeholders(content:str):
    placeholders = re.findall("%[a-zA-Z]+%", content)
    place = {}
    for placeholder in placeholders:
        if not placeholder in place:
            place[placeholder] = ask_string(placeholder.replace("%", ""))
    for placeholder in place:
        while placeholder in content:
            if placeholder == "%LIBS%":
                content = content.replace(placeholder, place_lib(place[placeholder].split(" ")))
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

def ask_string(name="Name"):
    try:
        return inquirer.text(
            message=name + ": ",
            validate=lambda x: x != "",
            invalid_message="You must enter a [" + name + "]"
        ).execute()
    except KeyboardInterrupt:
        error_keyboard_interrupt()

def ask_yes_no(name="Name"):
    try:
        return inquirer.confirm(
            message=name + ": ",
            default=False
        ).execute()
    except KeyboardInterrupt:
        error_keyboard_interrupt()

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
    while True:
        os.system("clear")
        print_spark_header()
        check_update()
        check_spark_project()
        try:
            action = inquirer.select(
                message="Select an action: ",
                choices=[
                    "Run coding style check",
                    "Manage Spark Project"
                ],
                default=None,
                border=True,
                show_cursor=False,
                cycle=True
            ).execute()
            if action == "Manage Spark Project":
                manage_spark_project()
            elif action == "Run coding style check":
                run_coding_style_check()
        except KeyboardInterrupt:
            error_keyboard_interrupt()

if __name__ == "__main__":
    main()
