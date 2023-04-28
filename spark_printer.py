##
## SPARK PROJECT, 2022
## spark
## File description:
## spark_printer
##

import rich
import sys

SPARK_DIR = "/usr/local/lib/spark/"

def print_spark_header():
    with open(SPARK_DIR + "header.txt", "r") as f:
        rich.print("[bold #FFD533]" + f.read() + "[/bold #FFD533]")

def print_spark_prefix():
    rich.print("[bold #FFD533]Spark[/bold #FFD533] > ", end="")

def print_spark(text):
    print_spark_prefix()
    rich.print(text)

def print_spark_error(text):
    rich.print("[bold #FFD533]Spark[/bold #FFD533] [bold #FF4545][Error][/bold #FF4545] > ", end="")
    print(text)

def error_keyboard_interrupt():
    print_spark_prefix()
    rich.print("[bold red]Keyboard interrupt.[/bold red]\n")
    sys.exit(84)
