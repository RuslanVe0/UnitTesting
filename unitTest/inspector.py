from random import randint
from itertools import permutations
from random import randint, choice
from utils.unitTest.generate import generate
from utils.unitTest.mathTools import OtherTools
import sys

class Silent():

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self
    
    def __exit__(self, exception_type, value, traceback):
        sys.stdout = self.stdout
        if exception_type: raise TypeError("Exception: %s > %s > %s" % (exception_type, value, traceback))

    def write(self, x): pass

    def flush(self): pass

class inspect(generate):

    def __init__(self): super().__init__()

    def start_inspection(self):
        if self.annotation:
            matches, mismatches = self.which_matches_types()
            self.print_verbose("success-inspection-[matches, mismatches]: Total matched: %d, total mismatched: %d" % (len(matches), len(mismatches)))
        else: matches, mismatches = [], []; self.print_verbose("warning-inspection-[matches, mismatches]: Unknown annotations. Proceeding with non-types. Make sure to provide in future reference!")
        self.print_verbose("inspection-info: Proceeding with next tasks ... ")
        self.call_test_(matches, mismatches)

    def call_test_(self, matches: list, mismatches: list):
        argumentsCalls = self.generateArgumentsCallsNoMatch()
        self.print_verbose(f"inspection: Generated: {self.sizeof(argumentsCalls)} elements!")
        argumentsCalls = self.cast_to_list(argumentsCalls)
        argumentsCalls = self.is_ordered(argumentsCalls)
        self.print_verbose("inpsection: Finished ordering elements!")
        self.print_verbose("inspection: Finished generated test arguments ...")
        self.print_verbose(f"inspection: Analyzing now with {self.sizeof(argumentsCalls)}-generated arguments!")
        self.test_FunctionWithoutArgs() # check if function can be called, in case, without arguments.
        req, passed = self.which_argument_not() # check which argument is not required to be passed.
        self.final_Analyzation(argumentsCalls, [req, passed])
    
    def final_Analyzation(self, argumentsCalls: list, reqpassed: list):
        dicts = {}
        for elements in argumentsCalls:
            temp = {}
            temp[elements[0]] = []
            for element in elements[1:]:
                temp[elements[0]].append(element)
            dicts[elements[0]] = temp[elements[0]]
        newArgs = {}
        types = []
        for elementsd in dicts:
            if elementsd.split("-")[0] in newArgs: newArgs[elementsd.split("-")[0]].append(dicts[elementsd]); continue
            newArgs[elementsd.split("-")[0]] = [dicts[elementsd],]
            if elementsd.split("-")[1] not in types:
                types.append(elementsd.split("-")[1])
        
        perms = permutations(newArgs)
        dump_errors = []
        for index, elements in enumerate(perms, 0):
            for indexing in range(0, self.sizeof(argumentsCalls),1): 
                runArgs = {}
                for elms in elements:
                    runArgs[elms] = self.random_choose(newArgs[elms])
                try:
                    with Silent(): self.function.actual_function(**runArgs)
                except Exception as failure:
                    dump_errors.append(failure)
        self.print_verbose("inspector: Analyzation finished! With %d errors!" % (len(dump_errors)))
        if dump_errors: self.print_verbose("inspector: DUMP-ERRORS[ %s ]" % ("\n,".join(str(error) for error in dump_errors)))
                 
    def random_choose(self, listed_arguments: list):
        for elements in listed_arguments:
            while isinstance(elements, list):
                elements = choice(elements) if elements else 0
            return elements

    def which_argument_not(self):
        paddings = permutations([_ for _ in range(0, self.function_length, 1)])
        actualArguments = []
        defaultArgs = self.function.get_args_no_regarding_matches()
        for elements in paddings:
            dictionaries = {}
            for index, value in enumerate(elements, 0):
                dictionaries[defaultArgs[index]] = value
            actualArguments.append(dictionaries)
        self.print_verbose(f"inspection: Performing a long-run test ... / {len(actualArguments)}-elements!")
        actualArguments = actualArguments
        newArguments = []
        for arguments in actualArguments:
            casted = permutations(self.cast_to_list(arguments))
            for index, casted_arguments__ in enumerate(casted, 0):
                casted_arguments__ = list(casted_arguments__)
                del casted_arguments__[self.function_length-1]
                newArguments.append(casted_arguments__)
        requiredArgs, passed_without = [], []
        for elements in newArguments:
            casted = dict(elements) # test the tests.
            try:
                with Silent(): self.function.actual_function(**casted)
                passed = self.missing_args(casted)
                if passed in passed_without: continue
                passed_without.append(self.missing_args(casted))
            except Exception as f:
                missed = self.missing_args(casted)
                if missed in requiredArgs: continue
                requiredArgs.append(self.missing_args(casted))
        self.print_verbose(f"Total required args: {len(requiredArgs)}, total that has defaults: {len(passed_without)} (total: {len(requiredArgs) + len(passed_without)})\n\n " + \
        "Required args: \n"+ "\n".join("  %s - required" % (_[0]) for _ in requiredArgs) + "\n\n" + " Arguments with default values:\n %s\n" % (
        "\n".join("  %s - default" % (_[0]) for _ in passed_without)))
        self.print_verbose(f"inspector: Finished analyzing required and default arguments ...")
        return requiredArgs, passed_without

    def missing_args(self, casted_dict: dict):
        missing = []
        nu = {}
        for elements in self.function.get_args_no_regarding_matches():
            nu[elements] = 1
        for elements in nu:
            if elements not in casted_dict: missing.append(elements)
        return missing

    def test_FunctionWithoutArgs(self):
        try:
            self.function.call_function(arguments = (), warnings=False)
        except TypeError: self.print_verbose("warning-inspection: Function cannot be called without arguments!"); return
        self.print_verbose("success-inspection: The function can be called without any arguments provided!")
        
    def cast_to_list(self, argumentsCalls: dict):
        list_ = []
        for key, elements in argumentsCalls.items():
            list_.append([key, elements])
        return list_

    def is_ordered(self, array: list) -> list:
        total_mismatched = []
        suitable = [_ for _ in range(0, len(array), 1)]
        previous = ""
        for indexe, elements in enumerate(array, 0):
            if elements[0] != self.only_keywords[indexe] and previous != elements[0].split("-")[0]:
                new_index = self.traverse_index(elements[0].split("-")[0], self.only_keywords)
                suitable[new_index] = elements # switch positions of elements inside the array.
                # notify the user, which argument where it has been moved inside the provided array.
                total_mismatched.append("changed positions to: %d from %d. Corrected: %d" % (indexe, new_index, _))
                previous = elements[0].split("-")[0]
                continue
            suitable[indexe] = elements
            previous = ""
        self.print_verbose("inspection: Total mismatched: %s.\n%s" % (len(total_mismatched), "\n".join(" %d. %s" % (_, String) for _, String in enumerate(total_mismatched, 0))))
        if suitable != array: return suitable
        return array

    def traverse_index(self, argument: int, correct_array : list) -> int:
        print(argument, correct_array)
        for index, elements in enumerate(correct_array, 0):
            if argument == elements: return index

    def sizeof(self, array: list) -> int:
        return sum([(len(_) if isinstance(_, (str, list, tuple)) else _) for _ in array])

    def generateArgumentsCallsNoMatch(self):
        calls = {list : (self.generate_list, "list"), int : (self.generate_random_integers, "int"), str : (self.generate_random_strings, "str")}
        self.only_keywords = []
        generated = {}
        for args in self.function.get_args_no_regarding_matches():
            for typing in self.types:
                if typing in calls: generated[args+"-"+calls[typing][1]] = calls[typing][0].__call__(); self.only_keywords.append(args+"-"+calls[typing][1])
        return generated    

    def generateArgumentsCallsMatch(self, matches: list, mismatches: list):
        argument = {}
        self.only_keywords = []
        calls = {list : (self.generate_list, "list"), int : (self.generate_random_integers, "int"), str : (self.generate_random_strings, "str")}
        for _, matched in matches:
            if _ not in argument: argument[_] = []
            if matched in calls:
                called = calls[matched][0].__call__()
                argument[_ + "-" + calls[matched][1]] = called
                self.only_keywords.append(_ + "-" + calls[matched][1])
        return argument

    def which_matches_types(self):
        functionArgs = [(_, element) for _, element in self.function_arg_requirements.items()]
        matches = [[], []]
        for elements_types in self.types:
            for elements_key, elements_element in functionArgs:
                if elements_types == elements_element: matches[0].append((elements_key, elements_element))
                else: matches[1].append((elements_key, elements_element, elements_types))
        return matches