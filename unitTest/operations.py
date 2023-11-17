import logging
import typing
import math
import utils.unitTest.otherTools
from utils.unitTest.exceptions import Error


logging.root.setLevel(1)
logging.addLevelName(level=1, levelName="StandardLogInfo")
logging.basicConfig(level=1, format="%(levelname)s : %(message)s")



msgs = {
    "warnings": {
        "WNSTV": "Warning: provided values, which are nested, however stored value is incorrect.",
        "VLWERF" : "Value must be inside in a iterable object, such as: list or tuple (which support addition)! Skipping",
        "VLWERF2" : "There is an element inside the list, which is not equal to the other value. Skipping."
    },
    "errors" : {
        "PMERROR" : "Parameter error",
    }
}

states = {
    10 : "warning"
}

class to_object(object):

    def __init__(self, value: any, verbose: bool = False):
        # #TODO error resolution.
        if not isinstance(value, (list, tuple)):
            raise Error("0x0bad")
        self.verbose = verbose
        self.value = value
        self.countAll = 0
        self.MinMax = {}
        self.valFreqDupl = {}
        super().__init__()
    
    def pack(self, elements: list, functionLength: int):
        actual = []
        temp = []
        for index, element in enumerate(elements, 1):
            if not index % functionLength: temp.append(element); actual.append(tuple(temp)); temp = []; continue
            temp.append(element)
        if len(temp) != 0:
            fill_additional_data = [0 for _ in range(0, functionLength - len(temp), 1)]
            fill_additional_data.extend(temp)
            actual.append(tuple(fill_additional_data))
        return actual

    def extract_only_specific_type(self, type_: type) -> list:
        only_elements = self.elements_only(self.value)
        elm = []
        for elements in only_elements:
            if isinstance(elements, type_):
                elm.append(elements)
        return elm

    def abs_(self):
        """
            This method's purpose is to change all numbers in array from negative to positive (|-a| = a)
A
            This method does not take any parameters.
            It is using the attribute (value) that is part of that class.

        """
        # |-x| = x... Absolute value.
        self.verbose_output("Preparing to convert %d elements (only and only if integers) to | -x | = x (absolute value)." % (len(self.value)))
        return [abs(n) for n in self.value if isinstance(n, int)]

    def elements_only(self, values: list) -> list:
        """
            The purpose of this method is index only the elements that can be found in the target array.

            (where :keyword = param)
            :values (list): the actual target array, where the user must supply an argument for that array.

            Return:
                list: a new array, with only the elements that were found in the specified array.

            For example:
                [[(a1,),(a2,),(a3,),(a4,),(a5,) ... (an,)] -> [a1,a2,a3,a4,a5 ... an].

        """
        newArray = []
        for elements in values:
            temp = []
            if isinstance(elements, (list, tuple)):
                temp = self.elements_only(elements)
            if temp:
                for element in temp:
                    newArray.append(element)
                continue
            newArray.append(elements)
        return newArray

    def verbose_output(self, msg: str):
        """
        A method, which purpose is to output messages, primarily used within a scenario when a user provided "verbosity" to be True as a parameter.
        """
        if self.verbose: logging.log(1, msg)

    def prettify(self):
        """
            The purpose of this method is to provide a better for reading and manipulation data.

            This method does not take any parameters.
            It uses the attribute (value) that is defined in that class.
        """
        solutions = {}
        for index, elements in enumerate(self.value, 0):
            if not isinstance(self.value[index], (list)): self.value[index] = [self.value[index]]
            if any(self.value[index]):
                solutions["case:%d" % (index)] = self.value[index][0]
                if self.value[index][1:]:
                    solutions["under-case:%d" % (index)] = self.value[index][1:]
                continue
            solutions["case-%d" % (index)] = elements
        self.value = solutions

    def sumall(self, value: list) -> int:
        """
            The purpose of this method is to sum all elements in the target array.

            It takes a list as an argument.
            (where :keyword = param)

            :value - that parameter is used later to sum all elements that can be found in the array (if integers).

            Return:
                int : the sum of all elements in the target array.
        """
        sum = 0
        for _, elements in enumerate(value, 0):
            if isinstance(elements, (list, tuple)):
                if len(elements) == 1:
                    if isinstance(elements[0], (list, tuple)) and len(elements[0]) == 0: continue
                    sum += elements[0][0] if isinstance(elements[0], (list, tuple)) else elements[0]
                else:
                    sum += self.sumall(elements)
                continue
            if not isinstance(elements, int):
                logging.warning("A non integer element found in array at index (%d)!" % (_))
            sum += elements
        return sum
    
    def countall(self, values: list) -> int:
        """
            The purpose of this method is to count elements inside the array.

            It takes a list as an argument.
            (where :keyword = param)

            :value - that parameter is used later to count all elements that can be found in the array (type: any).

            Return:
                int: total count of all elements inside the target array.


            [1,2,3,[[[[[4]]]]] ... n] (where n=45) (for instance with a nested array as a 4th element (3rd)). Hence, there will be 45-elements at total (44). 

        """
        count = 0
        for element in values:
            if isinstance(element, (list, tuple)):
                count += self.countall(element)
            else:
                count += 1
        return count

    def avgall(self, values: list) -> float:
        """
            The purpose of this method is to calculate the average of all elements in an array
            This is achieved by summing all the elements in the array and dividing the total by the count of elements.

            (where :keyword = param)
            :values - that parameter is used later to find average of all elements in the array.

            Returns:
                float: the average number.
        """
        return self.sumall(values)/self.countall(values)

    def refresh(self):
        """
            The purpose of this method is to reorder the array.
        """
        if self.verbose:
            self.verbose_output("Reordering array (if in case the type is anything else than list, it'll be within a 'list') ...")
        newArray = []
        for elements in self.value:
            actualElement = elements if isinstance(elements, list) else list(elements) if isinstance(elements, tuple) else [elements]
            self.verbose_output("%s (changed to) %s" % (elements, actualElement))
            newArray.append(actualElement)
        self.value = newArray

    def radix_operations(self, radix_operation: object):
        """
            (CEIL):
            The purpose of this method is to perform fixed pointing (radix point) operations.
            (CEIL (example)):
                    E.g 2.45 -> 3.00.
            (ROUND (example)):
                    E.g 2.45 -> 2.
                        2.50 -> 3.
    
        """

        self.verbose_output("Preparing to perform rounding operation based on the elements in the list (total elements: %d)" % (len(self.value)))
        self.value = otherTools.tools_comp(self.value, self.verbose_output).perform_operation(radix_operation)

    def sortElements(self, func: object):
        """
            The purpose of this method is to sort elements.
            Paramater (func) must be provided:
            (where :keyword = param)
            :func - a function must be supplied as an argument to the parameter, where it returns a logical value (1|0 (True | False)).
        """
        self.verbose_output("Preparing to sort elements of the array (total elements: %d)" % (len(self.value)))
        self.value = otherTools.tools_comp(self.value, self.verbose_output).sort_array(func)

    def duplicates(self):
        """
            The purpuse of this method is to find duplicates within the target array.
        """
        from collections import Counter
        self.verbose_output("Searching for duplicates ...")
        self.refresh()
        dicts = [str(element) for element in self.value]
        count = Counter(dicts)
        self.valFreqDupl = {element: freq for element, freq in count.items() if freq >= 1}
    
    def max_min_element(self):
        """
            The purpose of this method is to find min and max elements, which could be found inside target array.
        """
        if not self.valFreqDupl or len(self.valFreqDupl) < 2: raise ValueError("At least 2-elements in the array of the duplicates, are required for max_min_element(...)!")
        actp = [[_, value] for _, value in self.valFreqDupl.items()]

        foundMax = [actp[0][0], actp[0][1]]
        for element, count in self.valFreqDupl.items():
            #print(element)
            if count > foundMax[1]: foundMax = ["max(%s)" % (element), count]; continue
            if count < foundMax[1]: foundMin = ["min(%s)" % (element), count]
            if count == foundMax[1] and foundMax[0] != element: foundMin = ["%s=%s" % (element, foundMax[1]), count]
        foundMax[0] = "max(%s)" % (foundMax[0])
        self.MinMax = otherTools.tools_comp({"Maximum" : foundMax, "Minimum" : foundMin})
        self.MinMax.set_attributes_dict()
        return self.MinMax

def check_errors_based(arguments: tuple):
    """
        The purpose of this function is based on error handling.

        If it is logically False, that function will return as values -> 1, args[1] (where index 1: means
        that the user must proivde at least 2-values to that function). If of course it was intended to be used, and
        in some circumstances something that it was supposed to be False or True, it must be inverted to the other number.
        Always after True follows False, False follows True & so on to infinity.

        Args:
            arguments (tuple): A tuple of arguments, each containing two elments (True | False (bool), "..." (str))
        
        Returns:
            - if no errors are found before checking each elements in the provided argument (which is a tuple), it'll return False, an empty string.
            - if the input to the function is not a tuple, it'll return True.
            - if any of the arguments in the tuple do not have 2 elements, True will be returned an a string indicating about the scenario.
            - if argument is False, it'll return True, and the 2nd index element.
    """
    if not isinstance(arguments, tuple): return 1, "'check_errors_based' requires a tuple!"
    for args in arguments:
        if len(args) != 2: return 1, "2 elements must be provided inside the tuple!"
        if not args[0]: return 1, args[1]
    return 0, ""

def is_nested(values: typing.Union[list, tuple]):
    for elements in values:
        if not isinstance(elements, (tuple, list)): return False
        for element in elements:
            if isinstance(element, (tuple, list)): return True

def recheck(values: list, type: any, warnings: typing.Optional[bool] = True):
    rechecked = []
    for elements in values:
        if isinstance(elements, type):
            rechecked.append(elements)
            continue
        if warnings:
            logging.warning("%s element skipped, due to unmatched type occurance! Within (%s)" % (elements, ",".join(str(elements) for elements in type)))
    return rechecked

def addition(values: typing.Union[list, tuple], stored=False, verbosity: typing.Optional[bool] = False, warnings : typing.Optional[bool] = True):
    """
        The purpose of this method is to perform basic addition operations, where user must provide arguments.

        (where :keyword, param)
        :values - the parameter expects elements of type list in a tuple to be provided, and of course according to the function that is about
        to be implemented.
            e.g (addition as function)([a1:(int), a2:(int), a3:(int), ..., limit:(int)]) where limit = system maximum capacity or size.
            Note:
                if provided non-integer values, hence these values will be skipped.
        
        :stored - the paremeter expects a boolean value (1|0) (True | False) to be provided, it's default value is: False. That argument is required
        to point whether there are nested elements.
            e.g: ([[1,2,3,4], [1,2,3,4,5,[[[[6]]]]]]), in this case stored must be True.

        :verbosity - the parameter expects a boolean value (1|0) (True|False) to be provided and use for verbosity output.

        :warnings - the parameter expects a boolean value (1|0) (True | False) to be provided and used for alerting the user what actually happens.
            
    """
    exception_based(values)
    if not stored: values = [values]
    if is_nested(values) and not stored:
        if warnings:
            logging.warning("%(WNSTV)s" % (msgs["warnings"]))
        values = [value for value in values]
    newVals = []
    for elements in values:
        #print(elements)
        if isinstance(elements, (list, tuple)):
            elements = flatten(elements)
        elements = recheck(elements, (int, float), warnings=warnings)
        newVals.append(sum(elements)) # sum elements, e.g (1, 2) the sum of (1, 2) will be 3.
    return __convert(newVals)

def exception_based(values: typing.Union[list, tuple]) -> None:
    _exception = check_errors_based(((isinstance(values, typing.Union[list, tuple]), "Required is 'tuple' or 'list'!"), ))
    if _exception[0]:
        raise ValueError(_exception[1])

def flatten(elements: list):
    new_array = []
    for element in elements:
        if isinstance(element, (list, tuple)):
            new_array.extend(flatten(element))
        else: new_array.append(element)
    return new_array

def subtraction(values: typing.Union[list, tuple], stored=False, verbosity: typing.Optional[bool] = False, warnings: typing.Optional[bool] = False):
    """
        The purpose of this method is to perform basic subtraction operations, where user must provide arguments.

        (where :keyword, param)
        :values - the parameter expects elements of type list in a tuple to be provided, and of course according to the function that is about
        to be implemented.
            e.g (addition as function)([a1:(int), a2:(int), a3:(int), ..., limit:(int)]) where limit = system maximum capacity or size.
            Note:
                if provided non-integer values, hence these values will be skipped.
        
        :stored - the paremeter expects a boolean value (1|0) (True | False) to be provided, it's default value is: False. That argument is required
        to point whether there are nested elements.
            e.g: ([[1,2,3,4], [1,2,3,4,5,[[[[6]]]]]]), in this case stored must be True.

        :verbosity - the parameter expects a boolean value (1|0) (True|False) to be provided and use for verbosity output.

        :warnings - the parameter expects a boolean value (1|0) (True | False) to be provided and used for alerting the user what actually happens.
            
    """
    if verbosity:
        logging.log(1, "Preparing to perform subtraction information on provided elements (%d)" % len(values))
    exception_based(values)
    if not stored: values = [values]
    if is_nested(values) and not stored:
        if warnings:
            logging.warning("%(WNSTV)s" % (msgs["warnings"]))
        values = values[0]
    newVals = []
    for elements in values:
        if isinstance(elements, (list, tuple)): elements = flatten(elements)
        elements = recheck(elements, (int, float), warnings)
        if len(elements) == 0:
            if warnings:
                logging.warning("Element cannot be empty! Skipping (empty list) ...")
                continue
        n = elements[0]
        logging.log(1, "Selected first element of the array. %.2f!" % (n))
        for element in elements[1:]:
            elementAbsValue = element
            n -= elementAbsValue
            if verbosity:
                logging.log(1, "Subtracting %.2f-%.2f=%.2f. Elements: %.2f, %.2f" % (n, elementAbsValue, n-elementAbsValue, n, elementAbsValue))
        newVals.append(n)
    if verbosity:
        logging.log(1, "Subtraction was completed! Total elements generated: %d\r\x0A\r\x0AReturning as object ...\r\x0A" % (len(newVals)))
    return __convert(newVals)

def iterate_array(array: list):
    newlist = []
    for elements in array:
        if isinstance(elements, (list, tuple)):
            newlist = iterate_array(array=elements)
            continue
        newlist.append(elements)
    return newlist

def division(values: typing.Union[list, tuple], stored=False, round_to_nearest: typing.Optional[bool] = False, basic_round: typing.Optional[bool] = False):
    exception_based(values)
    if is_nested(values) and not stored:
        logging.warning("%(1)s" % (msgs["warnings"]))
        values = values[0]
    newVals = []
    for elements in values:
        elements = recheck(elements, int)
        if len(elements) == 0: continue
        n = elements[0]
        for element in elements[1:]:
            n /= element
        if round_to_nearest: n = math.ceil(n)
        elif basic_round: n = round(n)

        newVals.append(n)
    return __convert(newVals)

def multiplication(values: typing.Union[list, tuple], stored=False, verbosity: typing.Optional[bool] = False,
    warnings: typing.Optional[bool] = True, seperate: typing.Optional[bool] = False):
    
    """
    The purpose of this function is to perform basic multiplication operations within elements of arrays.

    (where :keyword = param)
  
    
    :values - the parameter requires to be supplied a tuple value that has elements, according to the functionality that is implemented. 
       - e.g: [0,2,4,6,8 ... limit] where limit=system maximum size.
    
    :stored - the parameter requires to be supplied a boolean value ((1|0), (True|False)), where this actual parameter and its actual value is used to point whether
    there are provided nested values inside the array, e.g stored -> True if [[[[[1,2,3,4,]], [[[1,2,3,4]]], ..., & so on], ... , & so on], ..., & so on]
    

    :verbosity - the parameter requires to be supplied a boolean value ((1|0), (True|False)), where this actual paremeter and its actual value is used to perform verbose output, in order
    to alert the user what is really going on, while the implementation.

    
    :warnings - the parameter requires to be supplied a boolean value((1|0), (True | False)), where this actual parameter and its actual value is used to to activate/deactivate
    warning output. 
       - For instance: x is not an integer. Skipping & etc.


    :seperate - #TODO seperate!!!!!!!!!!!!!!!!!

    """
    if not isinstance(verbosity, bool) or not isinstance(warnings, bool):
        raise TypeError("Verbosity and warnings requires a boolean value (1|0), (True|False) as an argument")
    if verbosity:
        logging.log(1, "Preparing to multiply %d values!" % (len(values)))
    exception_based(values)
    if is_nested(values) and not stored:
        logging.warning("%(WNSTV)s" % (msgs["warnings"]))
        values = [bob for bob in values]
    newValues = []
    for elements in values:
        n = elements[0]
        if isinstance(n, (list, tuple)):
            n = iterate_array(array=n)
            if len(n) == 0: logging.warning("Insufficient elements in array."); continue
            n = n[0]
        #print(n)
        if not isinstance(n, (float, int)):
            if warnings:
                logging.warning("%s is not an integer. Skipping!" % n)
            continue
        if verbosity:
            logging.log(1, "Indexed, selected element '%s'." % (n))
        for element in (elements[1:] if not isinstance(elements, int) else values[1:]):
            if isinstance(element, (list, tuple)):
                element = iterate_array(array=element)
                element = element[0]
            if not isinstance(element, (float, int)):
                if warnings:
                    logging.warning("%s is not an integer. Skipping!" % (element))
                continue
            if verbosity:
                logging.log(1, "Multiplying: %s*%s=%d (elements: %s,%s)" % (n, element, n*element, n, element))
            n *= element
        newValues.append(n)
    return __convert(newValues, verbosity=verbosity)

def concate(values: typing.Union[list, tuple], stored: typing.Optional[bool]=False, verbosity: typing.Optional[bool] = False, warnings: typing.Optional[bool] = True):
    if verbosity: logging.log(1, "Concatenating '%d'-elements of types:\n%s" % (len(values),
    "\x0A".join("  * %d %s  ->  %s" % (_, type(element[0]), element) for _, element in enumerate(values, 1))))
    """
        * The purpose of this method is to perform basic concatenation operations.
        
        :values (list): requires elements that are able to be concatenated.
            * note that:
                    any elements inside the list must be with their types:
                        e.g (list, list, list)
                        It'll raise an error if: ("a", list, list)
        :stored (bool [Optional]): requires a boolean value (1(True), 0(False)), in order
        to know when they are nested (elements).

        Example usage:
            * concate((["Hello, ", "World!"], [[1], [2], [3]]))
            -> (hence, the result will be): ['Hello, World!', [1, 2, 3]].
    """
    exception_based(values) # in case if there are provided invalid values inside :param: value.
    # in case if it is nested, and not stored... it'll output on the screen a warning message
    # indicating that store is False, however elements are nested.
    state = False
    if is_nested(values) and not stored:
        if warnings:
            logging.warning("%(WNSTV)s" % (msgs["warnings"]))
        values = [value for value in values]
        state = True
    if verbosity:
        logging.log(1, "Elements if nested. " + "Warning" if state else "")
    newValues = []
    for elements in values:
        n = elements[0]
        if not isinstance(n, (list, str, tuple)): 
            if warnings:
                logging.warning("%(VLWERF)s" % (msgs["warnings"]))
            continue
        if verbosity:
            logging.log(1, "Indexed, selected an element (%s)." % (n))
        for element in elements[1:]:
            if type(n) != type(element):
                if warnings:
                    logging.warning("%(VLWERF2)s" % (msgs["warnings"]))
                continue
            n += element
            if verbosity:
                logging.log(1, "Current progress...: %s" % (n))
        newValues.append(n)
    if verbosity: logging.log(1, "Concatenation successful! Total elements generated: %d\r\x0A\r\x0AReturning as object ...\r\x0A" % (len(newValues)))
    return __convert(newValues, verbosity)

def check_passed_functionsERR(listed_operations: list) -> bool:
    # include in this block, to be accessed only in this function and the body of that function.
    """
        * The purpose of this method is to check whether user provided (for parameter: operation) a valid values.

            (params)
            
            :operation (that parameter takes an argument of type list [func1, func2 ... limit] where limit depends on your system maximum size)

        - returns:
            bool

        :True
            - means that an element inside the list is not callable.
        
        :False
            - means that all elements inside the list are callable.
    """
    from inspect import isfunction
    # include that module only in this block, in that particular function and to be accessed only in this body.
    for operations in listed_operations:
        if not isfunction(operations) or not callable(operations): return True

    return False

def manual_operations(values: tuple, operations: typing.Optional[list] = [],
    operations_significant: typing.Optional[list] = [], stored=False, warnings: typing.Optional[bool]=False, verbosity: typing.Optional[bool] = False, seperate: bool = False):
    """
        :values (tuple): a parameter that requires a tuple containing list of values. These values will be iterated and used for user provided operations.
            Example usage:
                ([n1, n2, n3 ... limit])
                    Note: 
                        where the limit depends on your system maximum size or capacity.

            - Values must be always provided in a list inside.
            - Ensure that all elements are of the appropriate type (e.g ([1, 1, 1, 1], ["h", "a", "i"]), list constaining int, only integers, list containing str, only strings). 
        
            Errors:
                - An error will be raised, indicating that the user has provided item (element) inside the tuple that is not in a list, which may lead to other problems.
                - An error will be not reaised, if all elements are not from the appropriate type. They will be skipped, and the result may not as the user expects...
        
        :operations (Optional[list, tuple]): a parameter that requires a list containing elements of operations. These values will be used on the values provided by the user.
            Example usage:
                (math.sqrt, math.asin, ... limit)
                    Note:
                        where the limit depends on your system maximum size.        
            - Values must be always provided in a list.
            
        
        :operations_significant (Optional[list, tuple]): a parameter that requires a list or a tuple containing elements of operations that are functions part of that program.
            Example usage:
                (addition, subtraction, ... limit)
                    Note:
                        where the limit depends on your system maximum size.

        :stored (Optional[bool]): a parameter that, when used, requires a bool value, which will indicate that the following (values) parameter has other nested elements:
            Example usage:
                True | False.
                    Note:
                        the operation is recommended to be used correctly in the scenario!

        :verbosity (Optional[bool]): is a parameter that takes a boolean value (1|0), hence if True (1) it'll proceed with a verbose output, and it'll
        output additional information based on the information.

    """
    if verbosity:
        logging.info("Preparing to perform manual-operation on %d-elements with %d-operations and %d-significant operations!" % (len(values), len(operations), len(operations_significant)))
    
    # error handling, for: values, operations, operations_significant.
    for process in [values, operations, operations_significant]:
        exception_based(process) # calling "exception_based(...)" function, to check for errors. If there's an error: an exception will be raised!

    # check in case if user provided an element inside the list of (either: operations, either: operations_significant) that is not callable
    # in case if callable: an error will be raised.
    if check_passed_functionsERR(operations) or check_passed_functionsERR(operations_significant):
        # raise an error indicating that an element inside the list in invalid, and perhaps it is not callable... or cannot be accessed.
        raise ValueError("Invalid values provided for 'operations' and 'operations_significant'!\
Perhaps provided an element that is not callable?")
    
    if not isinstance(values, (str, int)) and is_nested(values) and not stored:
        # incase if user provided a nested list to the parameter "values: list" and
        # it is missing the store parameter to be set to True (it is recommended the user to perform that operation), 
        # hence it'll output the warning message according to the scenario.
        if warnings:
            logging.warning("%(WNSTV)s" % (msgs["warnings"]))
        values = [value for value in values]
        # variable -> values, which is the parameters.

    newVals = []
    for element in values:
        newvals = element if len(operations_significant) == 0 else [] # incase if operations_significant is 0, hence the newvals will be set to empty.
        for opss in operations_significant:
            newvals.append(opss([element], stored=False, verbosity=verbosity).value)
        temp = []
        for ops in operations:
            if verbosity:
                logging.info("Processing element %s ..." % (element))
            # if there are more operations provided on the inside (let's say [(addition, subtraction), multiplication]), hence
            # it'll start iterating the inner elements of operations. It is doing it by each.
            if isinstance(ops, (list, tuple)):
                temporary = []
                for element_operation__ in ops:
                    temporary.append([element_operation__(element) for element in newvals if isinstance(element, int)])
                newvals = temporary
            else:
                if isinstance(newvals, (list, tuple)):
                    op = [bob[0] if isinstance(bob, list) else bob for bob in newvals]
                    op = [ops(elements) for elements in op if not isinstance(elements, (list, tuple))]
                    if seperate: temp.append(op)
                    else: newvals = op    
                else:
                    if seperate: temp.append(ops(newvals))
                    else: newvals = ops(newvals)
            if verbosity:
                logging.info("Newvals (%d) -> %s" % (len(newvals), newvals))
            temp.append(newvals if not isinstance(newvals, int) and len(newvals) != 1 else newvals[0])
        newVals.append(tuple(temp)) if len(temp) else newVals.append(tuple(newvals))
    return __convert(newVals, verbosity=verbosity)

def __convert(reference, verbosity: bool = False):
    """
    Create the performed operations on the array an object, where the user can interact with the values (by manipulating them).
    """
    # convert the value to an object, in order user to have access to other tools according to the values.
    object_ = to_object(reference, verbose=verbosity)
    if verbosity:
        logging.log(1, "Object created successfully at %s" % (object_))
    return object_
    
def ExampleOperation(x: int):
    """
        This function is created to be part of a demonstration of how it can be used in scenarios, where additional operations can be provided in "manual_operations" as a parameter
        in "operations""

    """
    return x*4

def TurnToAbs(x: int):
    """
        An example function that is created to turn the given value to parameter "x" to absolute value:
            | -x | = x, hence | -45 | = 45.
    """
    if not isinstance(x, int): raise TypeError("It is required the type of value, passed to parameter 'x' to be integer!")
    return abs(x)