##
## SPARK PROJECT, 2022
## spark
## File description:
## coding_style_analyser
##

from spark_printer import print_spark_error

class CodingStyleError:
    def __init__(self, error:str):
        self.file = error.split(":")[0]
        self.line = error.split(":")[1]
        self.type = error.split(":")[2]
        self.index = error.split(":")[3]

        if self.type.startswith(" "):
            self.type = self.type[1:]

    def __str__(self):
        return f"[{self.file}:{self.line}:{self.type}:{self.index}]"

class CodingStyleReport:
    def __init__(self, report:str):
        _report = report.split('\n')
        self.errors = []
        for error in _report:
            if error != "":
                self.errors.append(CodingStyleError(error))

def analyse_coding_style_report(report):
    return CodingStyleReport(report)

def display_coding_style_report(report):
    for error in report.errors:
        print_spark_error(error)
