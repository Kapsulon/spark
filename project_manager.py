##
## SPARK PROJECT, 2023
## spark
## File description:
## project_manager
##

from spark_printer import *
from time import sleep
from spark import ask_string, ask_yes_no
import requests
import os
import sys
import rich
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import json
import re
import datetime
import subprocess
import glob

def get_spark_project_name():
    path = os.getcwd()
    while path != "/" and path != "":
        if os.path.exists(path + "/.spark.json"):
            return path
        path = "/".join(path.split("/")[:-1])
    return None

def is_git_directory(path = '.'):
    return subprocess.call(['git', '-C', path, 'status'], stderr=subprocess.STDOUT, stdout = open(os.devnull, 'w')) == 0

def get_default_project_name():
    if is_git_directory():
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').replace("\n", "").split("/")[-1]
    return "project_name"

def is_spark_project():
    return get_spark_project_name() != None

def check_spark_project():
    if not is_spark_project():
        print_spark("[bold red]Spark project file not found.[/bold red]")
    else:
        print_spark("[bold green]Spark project file found.[/bold green]")

def create_spark_project():
    print_spark("[bold yellow]Creating spark project...[/bold yellow]")
    data = {}
    try:
        data["YEAR"] = inquirer.text(
            message="Project date: ",
            validate=lambda x: x != "",
            invalid_message="You must enter a date.",
            default=str(datetime.date.today().year)
        ).execute()
        data["PROJECTNAME"] = inquirer.text(
            message="Project name: ",
            validate=lambda x: x != "",
            invalid_message="You must enter a name.",
            default=get_default_project_name()
        ).execute()
        data["LDFLAGS"] = inquirer.text(
            message="Libraries (split by spaces): ",
            validate=lambda x: x != "",
            invalid_message="You must enter libraries.",
            default=""
        ).execute()
        data["LDFLAGS"] = data["LDFLAGS"].split(" ")
    except KeyboardInterrupt:
        error_keyboard_interrupt()
    if len(data.keys()) != 3:
        print_spark("[bold red]Spark project creation failed.[/bold red]")
        sys.exit(84)
    json.dump(data, open(".spark.json", "w"), indent=4)
    print_spark("[bold green]Spark project created.[/bold green]")

def is_path_ignored(path: str) -> bool:
    ignored_paths = []
    for gitignore in glob.glob(get_spark_project_name() + "/**/.gitignore", recursive=True):
        ignored_paths += [line.strip() for line in open(gitignore, "r").readlines() if line.strip() != ""]
    for ignored_path in ignored_paths:
        if ignored_path == path:
            return True
        if ignored_path.endswith("/"):
            if path.startswith(ignored_path):
                return True

def get_actions():
    actions = []
    actions.append("Change project information")
    actions.append("Exit")
    actions.append(Separator(""))
    for folder in os.listdir(get_spark_project_name()):
        if os.path.isdir(get_spark_project_name()+"/"+folder) and not is_path_ignored(folder) and not folder.startswith("."):
            actions.append(Separator(f"==== {folder} ===="))
            actions.append(f"Create Makefile (or recreate)          {folder}")
            actions.append(f"Create .gitignore                      {folder}")
            actions.append(Separator(""))
    return actions

def create_makefile(folder: str) -> None:
    data_file = open(get_spark_project_name()+"/.spark.json", "r")
    data = json.load(data_file)
    data_file.close()
    makefile = open(get_spark_project_name()+"/"+folder+"/Makefile", "w")
    template = open(os.path.dirname(os.path.realpath(__file__))+"/templates/Makefile", "r").read()
    template = template.replace("%YEAR%", data["YEAR"])
    template = template.replace("%PROJECTNAME%", data["PROJECTNAME"])
    template = template.replace("%LDFLAGS%", " ".join(data["LDFLAGS"]))
    template = template.replace("%DESCRIPTION%", ask_string("Project description: "))
    if ask_yes_no("Compile to executable?"):
        template = template.replace("%EXECUTABLENAME%", f"\nname = {ask_string('Executable name: ')}\n")
        template = template.replace("%NAME%", """\n$(NAME): $(OBJ)
	@gcc -o $(NAME) $(OBJ) $(LDFLAGS)
	@echo -e "$(CLEARL)$(BLUE)[$(GREEN)Build$(BLUE)] $(GOLD)$(NAME)$(COL_END)\n""")
    else:
        template = template.replace("%EXECUTABLENAME%", "")
        template = template.replace("%NAME%", "")
    makefile.write(template)

def create_gitignore(folder: str) -> None:
    template = open(os.path.dirname(os.path.realpath(__file__))+"/templates/.gitignore", "r").read()
    with open(get_spark_project_name()+"/"+folder+"/.gitignore", "w") as gitignore:
        gitignore.write(template)

def manage_spark_project():
    if not is_spark_project():
        create_spark_project()
    data_file = open(get_spark_project_name()+"/.spark.json", "r")
    data = json.load(data_file)
    data_file.close()
    try:
        action = inquirer.select(
            message="Select an action: ",
            choices=get_actions(),
            border=True,
            show_cursor=False,
            cycle=True
        ).execute()
        if action == "Change project information":
            create_spark_project()
        elif action == "Exit":
            return
        elif action.startswith("Create Makefile"):
            create_makefile(action.split(" ")[-1])
        elif action.startswith("Create .gitignore"):
            create_gitignore(action.split(" ")[-1])
    except KeyboardInterrupt:
        error_keyboard_interrupt()
