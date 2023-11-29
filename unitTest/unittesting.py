from inspect import isfunction, getfullargspec
from utils.unitTest.inspector import inspect
import typing
from contextlib import contextmanager
from utils.unitTest import operations as operationsBased
from utils.unitTest.exceptions import Error
import typing
from random import randint, choice, shuffle
import regex
from string import ascii_lowercase, ascii_uppercase

"""
    This program, just for the experience, is to provide unit testing for the UCN project, which can be found in github (#TODO: upload
    in GitHub). It is very simple to use, all arguments can be from matter and good use!
    I am a Bulgarian student, 19-years old, and I have a great passion towards - software engineering, and programming. I have programmed this
    UnitTesting program just for the experience. I have developed it, in order to create a great project!

    Straightforward, and user-friendly.
"""

class CObj(object):

    def __init__(self):
        self.val = {}
    
    def joinValue(self, _key: str, _value: any):
        if not isinstance(_key, str): raise Error("0x0bac")
        self.val[_key] = _value
    
    def get_value(self, key: str):
        if key  not in self.val: raise Error("0x0415")
        return self.val[key]

    def all_values_to(self, to_: typing.Optional[dict] = dict):
        elements = []
        if to_ not in [list, tuple, dict]: raise Error("0x0ba4")
        for key, value in self.val.items():
            elements.append((key, value))
        return to_(elements)
    
    def remove_element(self, key: str):
        if key not in self.val: raise Error("0x0415")
        del self.val[key]

class BObj(object):

    def __init__(self, compare_value: object):
        self.compare_value = compare_value
        super().__init__()

    def get_success(self):
        filtered = []
        for _, elements in self.compare_value.items():
            for element in elements:
                if "success" in element and element["success"]: filtered.append(element)
        return filtered

    def get_failure(self):
        filtered = []
        for _, elements in self.compare_value.items():
            for element in elements:
                if "success" in element and not element["success"]: filtered.append(element)
        return filtered
    
    def get_elements_only(self):
        """
            The purpose of this method is to return all elements in a list-based generator object, all comparison results.
        """
        for elements in self.compare_value["results"]:
            yield elements

class AObj(object):

    def __init__(self, fmeth: object):
        self.actual_function = fmeth
        self.suppliedValuesOperations = None
        self.actualValues = None
        super().__init__()

    def get_arg_length(self):
        #print(dir(getfullargspec(self.actual_function)))
        return len(getfullargspec(self.actual_function).args)
    
    def get_args_no_regarding_matches(self):
        return getfullargspec(self.actual_function).args

    def get_default_arguments(self):
        return getfullargspec(self.actual_function).defaults

    def get_name(self):
        """
            The purpose of this method is to get the unique name of the function, method provided.

            Returns:
                (str): the unique name of the method, function.
        """
        return self.actual_function.__name__

    def function_arg_requirements(self) -> dict:
        """
            The purpose of this method is to return a value, containing the function's annotations, where it'll be easier to test the actual function, method, for any input
            and to test, whether the result is as expected.

            Returns:
                (dict): containg informationp, about the function or method annotations. (E.g {"a" : "<class 'int'>", "b" : "<class 'str'>"} & etc.
        """
        actual = getfullargspec(self.actual_function).annotations
        return actual
    
    def call_function(self, arguments: tuple, warnings: bool = True, flag: bool = False) -> any:
        """
            Call the function with the desired arguments.

            The required arguments, are the arguments that are going to be used when the function is being called.
            For instance... self.actual_function(*arguments), where arguments = (1,2,3,4), however it must meet according to the
            function's or method's arguments that are required to be inputted!

            Returns:
                any type, e.g. (int, float ...) according to what the function or method returns.
        """
        #print(arguments)
        if not isinstance(arguments, (list, tuple)) and not flag: raise Error("0x0bad")
        if warnings:
            argsFunction = self.get_arg_length()
            if len(arguments) > argsFunction and not flag: raise Error("It is required to provide %d elements for function '%s'" % (argsFunction, self.get_name()), custom=True)
        returned_value = self.actual_function(*arguments)
        return returned_value

class unitTest(inspect):

    def __init__(self, function: object, verbosity: bool = False, types: list = [int, str, float, list, dict]) -> None:
        if not isinstance(types, list): raise Error("0x1baf")
        if not types: return
        self.annotation = True
        self.compare_results = BObj({"results" : []})
        self.function = function
        self.types = types
        self.stored_operations = {}
        self.cache_memory_tvc = []
        self.test_values = []
        self.is_created_man = False
        self.additional_functions_map = []
        self.actualValues = None
        self.verbosity = verbosity
        self.print_verbose(f"Starting inspection ... \n * Total types declared: {len(self.types)}\n * Function: {self.function}\n\n")
        super().__init__()
        self.load_function()
        self.print_verbose(f"Function information: \n * Function name: '{self.function.actual_function.__name__}'\n * Total arguments required: {len(self.function_arg_requirements)}\n")

    def analyze(self):
        self.start_inspection()

    def new_test_values(self):
        pass

    def main_function_length(self):
        return self.function.get_arg_length()

    def get_all_functions_length(self) -> dict:
        """
            The purpose of this method is to get the elements (which must be functionhs) inside the list, and enumerate
            the length of functions, and to create a dictionary to make it more readable.
        """
        functions_gather = {}
        for functions in self.additional_functions_map:
            if not isinstance(functions, AObj):
                # in case if the element is not an object of AObj, or it is not an object at all.
                self.print_verbose("warning: Skipping. Element is not an object of that class...")
            if not hasattr(functions, "get_arg_length") or not hasattr(functions, "get_name"):
                # in case if there are no attributes inside 'AObj' class.
                self.print_verbose("warning: Skipping. Object has no attribute 'get_arg_length' or 'get_name' ... ")
                continue
            functions_gather[functions.get_name()] = functions.get_arg_length()
        return functions_gather
            
    def get_operation_function(self, name: str):
        if name not in self.stored_operations: raise Error("0x0415")
        function, params = self.stored_operations[name]
        return function, params

    def store_as_operations(self, _function: object, manualKey: any = None, targetParams: tuple = ()) -> bool:
        __object = AObj(_function)
        manualKey = __object.get_name() if not manualKey else manualKey
        self.stored_operations[manualKey] = (__object, targetParams)
        self.print_verbose("function '%s(...)' converted to 'AObj' and stored in operations (further functions)." % (__object.get_name()))

    def use_as_operations(self, _function, _targetParameters: tuple):
        if not isinstance(_targetParameters, tuple): raise Error("0x0bad")
        if isinstance(_function, AObj):
            self.stored = _function.call_function(arguments=_targetParameters, flag=True)
        else:
            self.stored = _function.__call__(*_targetParameters)
        self.print_verbose(f"Values were stored (total: {len(self.stored)}).")

    def search_FunctionByName(self, functionName: str) -> object:
        for elements in self.additional_functions_map:
            if not hasattr(elements, ("get_name")): self.print_verbose(f"warning: missing attribute 'get_name' from object ??'{elements}'??. Skipping"); continue
            if elements.get_name() == functionName: return elements
        self.print_verbose("warning: '%s' seems to not exist in all '%d' functions. Functions: \n%s\n\n" % (
        functionName, len(self.additional_functions_map),
        "\n".join("    * %s(...)" % (__object.get_name()) for __object in self.additional_functions_map if hasattr(__object, "get_name"))))

    def print_verbose(self, text: str):
        if self.verbosity: print(f"verbose_output: {text}")

    def exit_error(self, text: str) -> str:
        exit("error: %s" % (text))

    def strict_equals(self, expected, floatPointSymb: int = 3):
        if isinstance(self._called, float):
            self._called = round(self._called, floatPointSymb)
        if isinstance(self._called, str):
            self._called = self._called.strip() # in case if there are unwanted characters, like - "\x0A", "\r" & etc.
        
        return self._called == expected

    def perform_basic_operations(self, testValues: list, operation: str, type_only: type, args_for_operation: dict = {}) -> None:
        """
            The purpose of this method is to handle basic mathematical operations such as:
                - subtraction;
                - addition;
                - multiplication;
                - division;
            By using the module "operations".

            (:keyword - param)
            :testValues - the user is required to provide arguments in a list, with N-elements
                which will be used later, while testing the values that are returned by the 'target' function.
                E.g [1,2,3,4,5,6,7,8 ... N]
            
            :operation - the user is required to specify an operation (addition, subtraction, multiplication, division, concate).

            :type_only - the user is required to specify a type, which will be used TO only use that type (in the provided array with elements).

            :args_for_operation - the user is not required to specify arguments for the operations, basically the user can specify own arguments for the parameters,
            and experiment with the elements.
        """
        if not isinstance(testValues, list) or not isinstance(operation, str):
            raise Error("0x1baf")
        if not operation: return testValues
        # casting the inner elements to -> list, and the whole array to a tuple, in order to be used in 
        # operations.
        if "warnings" not in args_for_operation:
            args_for_operation["warnings"] = False
        if "stored" not in args_for_operation:
            args_for_operation["stored"] = True 
        arrayContainingValues = tuple([list(element) for element in testValues])
        argumentsForFunction = [argument for argument in arrayContainingValues]
        invokeOps = {"multiplication" : [operationsBased.multiplication, arrayContainingValues], "addition": [operationsBased.addition, arrayContainingValues],
        "concate" : [operationsBased.concate, arrayContainingValues]}
        if operation not in invokeOps:
            raise Error(f"Provided operation could not be located ({operation})", custom=True)
        __functionReferenceOperation, argsToCall = invokeOps[operation]
        objectref = __functionReferenceOperation(argsToCall, **args_for_operation)
        for index, resultfromoperation in enumerate(objectref.value, 0):
            if type_only and not isinstance(resultfromoperation, type_only): continue
            elementRefRFO = argumentsForFunction[index][len(argumentsForFunction[index])-1]
            if not isinstance(elementRefRFO, int) and isinstance(elementRefRFO, dict):
                argumentsForFunction[index][len(argumentsForFunction[index])-1]["results-of-operations"].append(resultfromoperation)
            else:
                argumentsForFunction[index].append({"results-of-operations": [resultfromoperation]})
        argumentsForFunction = argumentsForFunction
        self.actualValues = True
        self.stored = argumentsForFunction

    def enumerate_function(self, functionName: str) -> dict:
        enumData = CObj()
        for index, elements in enumerate(self.additional_functions_map, 0):
            if not isinstance(elements, AObj): self.print_verbose(f"warning: {index} index element in the array, seems to be a non 'AObj' class object."); continue
            if functionName == elements.get_name():
                enumData.val = {"length" : elements.get_arg_length(), "paramspec" : elements.get_default_arguments(),
                "paramspec-2" : elements.get_args_no_regarding_matches(), "paramspec-3" : elements.function_arg_requirements(), "index" : index}
        return enumData

    def add_function_for_creating_tests(self, function):
        """
            The purpose of this method is to call a user-based function, and use it to test values.
            The return value from the function to the call-point, must be of type: (list, tuple).
            Where the elements inside will be stored and used later in comparison.
        """
        functionObject = AObj(fmeth=function)
        self.print_verbose(f"Putting object in a list ('{functionObject.get_name()}(arg1, arg2 ...)')...")
        self.additional_functions_map.append(functionObject)

    def assertEquals(self, element: list, correct_element: any,
        text: str = "Incorrect results!", text_on_correct: any = "Correct::result",
        strict_equals: typing.Optional[bool] = False,
        strict_equals_args: typing.Optional[dict] = {}, values_Stored: bool = False,
        manualOperation: bool = False) -> None:
        self.compare_results.compare_value = {"results":[]}
        """
            The purpose of this method is to compare two values for their correctness. In case if they are not equal
            to one another, it'll throw an AssertionError, which indicates that the value requested is not equal to the other value.
            - Each argument, that expects a parameter, in this method is required for specific purposes.
            In case if correct_element is a list, hence the user must use the values_Stored parameter and make it - True.
            (:keyword - param)
            
            :element - It is required the user to provide ANY kind of element. Of course, make sure that it meets the functions
                arguments, else it'll raise an error indicating that the user provided more arguments than required.
                - Example usage:
                    element=[1, 2, 3, 4], hence that function accepts 4 arguments. They will be used later in the context. It is required
                    the correct_element paramater to be supplied with the same amount elements in the list, or a tuple.

                - Additionally, there's an auxiliary method called "create_test_values()" designed to generate test values based on the function's argument count.
                - For functions with default arguments, the number of arguments should be in the range (0 <= N <= 2),
                where 'N' refers to the number of arguments. If the function doesn't have default arguments, it should strictly have 3 arguments.
            
            :correct_elements - It is required the user to provide ANY kind of element, which must be the expected result that has to be returned from a function.
                - Example usage:
                correct_elements=[45,13,45,64] the function must return for instance [45,13,45,64], else: it'll raise an assertion error.
                
                - Additionally, there's an auxiliary method called "perform_basic_operations(...)": which is specifically for that type of parameter.
                - There's no limitation, regarding the elements provided in "correct_element" parameter.
            
            :text - it isn't required the user to provide an argument (it has a default value), however the user can change the output text.

            :text_on_correct - it isn't required the user to provide an argument (it has its own default value), however the user can change the output text.

            :strict_equals - it isn't required the user to provide an argument. It accepts a boolean value (1 | 0 (True | False)) as value.
                It is basically used in context of greater precision based on comparison between the values.
            
            :strict_equals_args - E.G floatPointSymb, for controlling floating-point precision. E.g in some cases
                like 0.1 + 0.2, it'll give a result of 0.300...04 which might lead to inaccurate results.
            
            :values_Stored - it is used in different context, where there are stored Values, e.g there might be more 
            test values.

            :is_created - is used when there are already created values.

        """
        self.print_verbose(f"Preparing to compare {len(element)} values.")
        if ((not isinstance(element, (list, tuple))) and (not values_Stored)): raise Error("0x0bad)s")
        if not isinstance(text, str): raise Error("0x0bac")
        self.print_verbose("Total arguments provided: %d\n On correct: %s, On incorrect: %s" % (len(element), text_on_correct, text))
        test_passed = 0
        if self.actualValues:
            targets = []
            for _ in enumerate(correct_element, 0):
                results = None
                args = []
                for elms in _[1]:
                    if isinstance(elms, dict): results = elms; continue
                    args.append(elms)
                if not results:
                    self.print_verbose("warning: got none?")
                    self.compare_results.compare_value["results"].append({"targets": {"s1" : "Unknown", "s2": None}, "success" : -1}); continue
                results = results["results-of-operations"]
                self._called = self.function.call_function(arguments=tuple(args))
                temporary = self._called
                if isinstance(results, list):
                    if isinstance(temporary, (list, tuple)):
                        for index, returned in enumerate(temporary, 0):
                            self._called = returned
                            self.assertion(compare_1=self._called, compare_2=results[index], is_strict_equals=strict_equals, args=strict_equals_args, text=text)
                            test_passed += 1
                            targets = [returned, results[index]]
                            self.compare_results.compare_value["results"].append({"targets": {"s1": returned, "s2": results[index]}, "success": 1})
                    else:
                        self._called = temporary
                        results = results[0]
                        self.assertion(compare_1=self._called, compare_2=results, is_strict_equals=strict_equals, args=strict_equals_args, text=text)
                        test_passed += 1
                        targets = [self._called, results]
                        self.compare_results.compare_value["results"].append({"targets": {"s1": self._called, "s2": results}, "success": 1})
                else:
                    self.assertion(compare_1=self._called, compare_2=results[0], is_strict_equals=strict_equals, args=strict_equals_args, text=text)
                    targets = [self._called, results]
                    self.compare_results.compare_value["results"].append({"targets": {"s1": self._called, "s2": results}, "success": 1})
                if targets:
                    self.print_verbose(f"Test case #{_[0]+1} (s1: {targets[0]}, s2: {targets[1]}): passed!")
                    continue
                self.print_verbose(f"Test case #{_}: failed!")
        elif manualOperation: 
            for index, elements in enumerate(correct_element, 0):
                self._called = self.function.call_function(arguments=element[index])
                self.assertion(compare_1=self._called, compare_2=elements[0], is_strict_equals=strict_equals, args=strict_equals_args, text=text)
                test_passed += 1
                self.compare_results.compare_value["results"].append({"targets" : {"s1" : self._called, "s2" : correct_element}, "success" : 1})
        elif values_Stored:
            for elements in element:
                self._called = self.function.call_function(arguments=elements)
                self.assertion(compare_1=self._called, compare_2=correct_element, is_strict_equals=strict_equals, args=strict_equals_args, text=text)
                test_passed +=1
                self.compare_results.compare_value["results"].append({"targets": {"s1": self._called, "s2": correct_element}, "success": 1})
        else:
            self._called = self.function.call_function(arguments=element)
            self.assertion(compare_1=self._called, compare_2=correct_element, is_strict_equals=strict_equals, args=strict_equals_args)
            self.compare_results.compare_value["results"].append({"targets": {"s1": self._called, "s2": correct_element}, "success": 1}, text=text)
            test_passed += 1
        # checking in case if there are any errors with values that are used to be outputed.
        if not isinstance(text_on_correct, str): raise Error("0x0bac")
        if not isinstance(text, str): raise Error("0x0bac")

        # outputing that the test was finished: successfully, indicating: failures and successes based on the values.
        print("\n\n" + text_on_correct + "\n\nTests passed...: %d/%d, total failed: %d." % (len(self.compare_results.get_success()), len(correct_element), len(self.compare_results.get_failure()))\
         + "\n\n\nTesting has finished ... ", end="\n\n")
        return
        
    def assertion(self, compare_1: any, compare_2: any, is_strict_equals: bool, args: list, text: str) -> None:
        """
        Compare values.
        """
        assert (compare_1 == compare_2) if not is_strict_equals else (self.strict_equals(compare_2, **args)),\
        f"It must be {compare_2}, instead we got {compare_1}. Msg: {text}"
    
    def create_test_values(self, rangeVals: typing.Union[list, tuple], size: typing.Optional[int] = 64, inner_Size: typing.Optional[int] = 2, random_: typing.Optional[bool] = True,
        args: dict = {"stringLengthMax" : 8, "stringLengthMin" : 2, "regexMatchOnly": r"[A-z,0-9]"}):

        if "regexMatchOnly" not in args:
            args["regexMatchOnly"] = None
        if "stringLengthMax" not in args:
            args["stringLengthMax"] = 8
        if "stringLengthMin" not in args:
            args["stringLengthMin"] = 2
        self.print_verbose(f'''Preparing to create elements:
    * Range values: interval [{rangeVals[0][0]}; {rangeVals[0][1]}], type: {rangeVals[1]};
    * Size (total size): {size};
    * Random: {random_} generated values;
''')
        if rangeVals[0][1] >= 65535: raise Error("Maximum value of 'rangeVals...' cannot be greater or equal to 65535", custom=True)
        created = []
        
        while len(created) < inner_Size+1:
            temp = []
            while len(temp) < size:
                actual = []
                while len(actual) < inner_Size:
                    actual.append(self.genAccordingType(rangeVals[1], interval=rangeVals[0], arguments=args))
                temp.append(tuple(actual))
            created.extend(temp)
        self.print_verbose("Created %d elements! Inner-size: %d. \r\x0A" % (len(created), inner_Size))
        """
        Perhaps... in that shifting, which data-type is a list, we can nest the elements in 3-dimensional array
        where the 3rd level array will include a: nested element (which must be a list), and an integer which indicates the size of that array.
        In order to be more efficient, instead of getting the length of the whole list that is nested, which is the 2nd lervel list. 
        Let... a defined function accepts 4 params (parameters).... the list must include: [[([1,2,3,4],[4,3,2,1] ... ]), 4]].
        """
        self.is_created_man = True
        self.test_values = created

    def use_as_test_function(self, _object: object, size: int, _types: list, to_list: bool = False, manual_innerSize: int = 0, size_limit=pow(2, 16),
        otherArgs: tuple = ()):
        otherArgs = [otherArgs]
        if size >= size_limit: raise ValueError(f"Size can't be higher than or equal to {size_limit}!") # in case. It can be of course deactivated.
        requestedFuncLength = self.main_function_length() if not manual_innerSize else manual_innerSize
        returnValue = _object.call_function(arguments=(size, requestedFuncLength, _types, to_list, otherArgs), flag=True)
        self.print_verbose(f"Using '{_object.get_name()}' function as value generate function (k(inner Size (level 2)), (m(level 1 side)), k={size}, m={requestedFuncLength}.")
        if not isinstance(returnValue, typing.Union[list, tuple]) or not returnValue: raise Error("0x0bad")
        self.test_values = returnValue

    def timeConsumption(self, target: object, kwargs: dict = {}) -> float:
        """
        The purpose of this method is to measure time consumption based on function call; and processes in the function that are implemented.
        
        (where :key = param)
        target: It is required an object as value to be passed as argument to that method.
        kwargs (optional): a dictionary list with args for the target function. 

        Returns:
            float: the measured time.
            
        """
        from time import time
        if not callable(target): raise ValueError("Provided target object is not callable!")
        rec = time()
        target(**kwargs)
        return time() - rec

    def perform_changes(self, type_required: type):
        function_length = self.function.get_arg_length()
        IObject = operationsBased.to_object(self.test_values[0])
        elements = IObject.extract_only_specific_type(type_required)
        self.test_values = IObject.pack(elements, function_length)

    def prepare_list_accordingType(self, _type: object, interval: tuple) -> list:
        actual = list(ascii_lowercase)
        actual.extend(list(ascii_uppercase))
        actual.extend([_ for _ in range(interval[0], interval[1], 1)])
        actual.extend([float(_) for _ in range(interval[0], interval[1], 1)])
        shuffle(actual)
        for index, elements in enumerate(actual, 0):
            if not isinstance(elements, _type):
                del actual[index]
        return actual

    def genAccordingType(self, actual_Type: object, interval: tuple, arguments: dict):
        actual = self.prepare_list_accordingType(_type=actual_Type, interval=interval)
        n = 0
        n1 = 0
        chosen = actual[0]
        findcharacters = lambda target, range_min, range_max: "".join(choice(target) for _ in range(0, randint(range_min, range_max), 1))
        while n1 < abs(interval[0]-interval[1]):
            if actual_Type == list or actual_Type == tuple:
                if isinstance(chosen, (list, tuple)):chosen.append(actual[n]); n+=1; continue
                chosen = [actual[n]]
            else:
                perm = list(ascii_lowercase)
                perm.extend(ascii_lowercase)
                if actual_Type == str:
                    padd = findcharacters(perm, arguments["stringLengthMin"],arguments["stringLengthMax"])
                    if arguments["regexMatchOnly"]:
                        while not regex.match(arguments["regexMatchOnly"], padd):
                            padd += findcharacters(perm, arguments["stringLengthMin"], arguments["stringLengthMax"])
                    chosen = padd
                    temp_n = 0
                    while not isinstance(chosen, str):
                        chosen = actual[temp_n]
                        temp_n += 1
                    n += 1
                    n1 += 1
                    continue
                chosen = actual[n]
                temp_N = 0
                while not isinstance(chosen, actual_Type):
                    if temp_N > len(actual)-1: chosen = self.genAccordingType(actual_Type, interval=(interval[0], interval[1])); break
                    chosen = actual[temp_N]
                    temp_N += 1
            n += 1
            n1 += 1
        return chosen

    def load_function(self):
        # or use callable(...).
        if not callable(self.function):
            self.exit_error("error: provided function is not callable")
        self.print_verbose("success: provided function is callable!")
        self.function = AObj(self.function) # actual target method
        self.function_length = self.function.get_arg_length()
        self.function_arg_requirements = self.function.function_arg_requirements()
        if len(self.function_arg_requirements) == 0: self.annotation = False; self.function_arg_requirements = getfullargspec(self.function.actual_function).args
        if self.function_length == 0: self.exit_error(f"error: Function '{self.function.get_name()}(...)' has no arguments included for input!\n")


