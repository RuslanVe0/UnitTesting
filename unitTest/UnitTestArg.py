import argparse
from unittesting import unit_Test
class ArgumentBased(object):

    """
        Arguments that are used within the command-line arguments, where it may require:
            --fileTarget: it is a required argument that requires a file to be supplied as value to the argument.
            --verbose: it isn't a required argument, and is basically for verbose output.
            --usage: it is an argument, that is used to output a usage, user-friendly, message: it is a hint, and to hint the
            user, regarding to the usage of that program.

        Since it is used for UCN, it knows about arguments, and etc.
        If this program is used, IT IS RECOMMENDED method name to be: main(...) (of course with specific arguments, let's say x,y or UCN: str)

    """

    def __init__(self: object):
        self.parser = argparse.ArgumentParser(prog="Unittesting for UCN project", description="All you need to do is provide a file, and get the required results.")
        self.add_arguments()

    def add_arguments(self) -> None:
        self.subparser = self.parser.add_subparsers(title="Available sub commands(s)", dest="subcommand")
        self.parser.add_argument("-f", "--fileTarget", help="A required target file, where the unit testing to be used. It is required to supply a method, where it can be initiated!", type=str, required=True)
        self.parser.add_argument("-v", "--verbose", help="Verbose output: with additional information, regarding to the testing.", required=False, default=False, type=bool)
        self.parser.add_argument("-u", "--usage",
        help="Usage: python3 unittesting.py -f=helloworld.py -m=OutputHelloWorld export -log=log.txt --prettify=True", required=False, default=None, type=bool)
        self.add_export_arguments()
    
    def add_export_arguments(self) -> None:
        # arguments related to exporting.
        actualParser = self.subparser.add_parser(name="export", help="Export\
        available information: from the unittesting. Where user is possible to, visually, interpret information for reasons")
        actualParser.add_argument("-log", "--log", required=False, default=None, help="Provide a log file, where to write contents.", type=str, required=True)
        actualParser.add_argument("-prettify", "--prettify", required=False, default=False, help="Use prettifier: for easily readable information.",  type=bool)