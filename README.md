# UnitTesting (still in development)

### Introduction:
  Embarking on the Unit Testing project marks a pivotal decision in my software development journey and as a student in software engineering. I take it as an excellent choice for a project, in order to enhance my coding abilities. This initiative stems from the strategic aim of crafting a specialized tool that not only I have developed but one that will play a crucial role in rigorously testing and validating my future projects. The primary goal is to enhance the reliability, stability, and overall quality of my software endeavors.


### Basics
  **Section 1.1**
  Here's an example Python function that accepts 2 parameters (param 1 has int as annotation, as well as param 2) (let's create it with functions, and call the functions a1 and b1 as unique names:
  ```python

      def a1(a: int, b: int) -> list:
        return a+b
      
      def b1(level1:int=2, level2:int=64):
        elementsToTest = []
        n = 0
        while len(elementsToTest) < level2:
            temp = []
            while len(temp) < level1:
                temp.append(n+1)
                n += 1
            elementsToTest.append(tuple(temp))
        return elementsToTest
  ```
  Function A1:
    It performs a basic arithmetic operation (addition) of the product of two values (in this case they're integers as types).

  Function B1:
    It aims is to test a1 with different values. Inside (level-2, 2nd dimension of the list (which is a tuple, and consists of integer-like elements) will have elements like (1,2), (3,4) ... (n, n) as "n" to be the product of a value 
    that is added with one each time, that will be level1(size)*level2(size) times n, based on both iterations.
    For the present and current state, the algorithm is dummy. It does not perform any kind of special operations, both functions can be acccessed, however the difference is that
    function **b1** performs dummy operations like adding elements (a tuple with 2 elements inside) to a list, and function **a1** only performs addition operation. To enhance that we need to call these functions, and of course perform multiple operations on the list that are returned from **b1**. Let's create a function "b2" (b in this scenario stands for basic_operations).
  ```python
    
    def b2(targetList: list) -> list:
      return [sum(element) for element in targetList]
      
  ```
  **Section 1.2**
  Now there's something particular, and now we performs operations within the elements in targetList, basic addition operations, and then we return the updated list.
  Hence after that was implemented, let's use the create elements and call N-times (in this case 64 times) "a1" function
  ```python
    testVals = b1()
    correctVals = b2()
    for index, element in enumerate(testVals, 0):
      if correctVals[index] == a1(*element): print("Success!")
      else: print("Unsucess!")
  ```
  Under these basic principles this project works.
  It'll detour the whole testVals list, and with its actual index will check for correctness between the returned value and the value from correctVals list.

### Basics of the project
  Provided operations:
     <p style="margin-right: 15px"> *addition(...)*: The purpose of this function is to perform basic addition operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *subtraction(...)*: The purpose of this function is to perform basic subtraction operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *division(...)*: The purpose of this function is to perform basic division operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *multiplication(...)*: The purpose of this function is to perform basic multiplication operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *concate(...)*: The purpose of this function is to perform basic concate operations, where user must provide arguments. </p>

  **Section 1.1**
  
  Let's experiment a bit. These operations are located in "operations.py" file.
  We'll use the same template as we used before, we will have the functions (a1, b1), where
  function a1 accepts two parameters (a annotation: integer, b annotation: integer), and returns an *integer* as value.
  function b1 accepts two parameters (with default *integer* values)
  ```python
 from utils.unitTest import operations

def a1(a: int, b: int) -> int:
    return a+b
      
def b1(level1:int=2, level2:int=64):
    elementsToTest = []
    n = 0
    while len(elementsToTest) < level2:
        temp = []
        while len(temp) < level1:
            temp.append(n+1)
            n += 1
        elementsToTest.append(tuple(temp))
    return elementsToTest

# now let's use as example: addition.
if __name__ == "__main__":
    targetList = b1()
    opnod = operations.addition(targetList, sep=True)
    for index, element in enumerate(opnod.value, 0):
        if a1(*targetList[index]) == element:
            print("Success!")
        else:
            print("Unsuccess")

  ```
The value returned from any operation available (whether it is: addition, subtraction, multiplication, division or concate) it returns it as an object, where the user can perform various operations on the list. You can experiment with it.

**Section 1.2**
Let's dive deeper, and instead of defining our own function and manually to create a list, to create it automatically using the method *create_test_values(...)*.
The required parameters are:
```
  rangeVals: (list, tuple):
  
    which parameter requires a list with 2 elements inside. 1st element must be either a tuple or a list, and it must signify the interval between the values
    that are required to be provided. The other element must be a type, here's is due to user choice and needs. Here's an example
    create_test_values(rangeVals=[(1, 255), int]), thus we can interpret that the interval is (1; 255) and the type that we need is *int*.
```
Parameters which do not require an argument to be passed:
```
  size: int:
    This parameter is the 1st level length of the list. This has nothing to do with the length of the parameters a function has.
  innerSize: int:
    This parameter is the 2nd level length of the list, which is for the length of the parameters a function has.
  random_: bool (optional):
    This parameter is required to point whether the values that will be generated to be randomized.
  args: dict (optional):
    This parameter will be used later, while generating values in method 'genAccordingType(...)'.
```
This method, the purpose of this method, is to generate a list with elements inside. The array consists of 1st level elements, and 2nd level elements.
Where in the first level, it's important to note that, it includes N count of elements. There's no limitation based on the elements that can be added
in the first level of the array: (example [(1,2,3,4), (45,33,21,77), ... N)]). While the 2nd level of array is important, ergo it consists elements according
to the function parameter length (param1, param2 ... paramN), where paramN points how many elements is required to be added in the 2nd level of the array.
```python
from utils.unitTest import operations
from utils.unitTest.unittesting import unitTest

# we will use again the same function, with same length of parameters, and same unique name "a1(...)".
def a1(a: int, b: int) -> int:
    return a+b

if __name__ == "__main__":
  example_usage = unitTest(a1, verbosity=True) # call "unitTest(...)" class, and load function.
  example_usage.create_test_values(rangeVals=[(1, 64), int], size=64, inner_Size=example_usage.function.get_arg_length(), random_=True)
  example_usage.perform_basic_operations(testValues=example_usage.test_values, operation="addition", type_only=int, verbosity=True)
  example_usage.perform_changes(type_required=int)
  example_usage.assertEquals(element=example_usage.test_values, correct_element=example_usage.stored, strict_equals=True, is_created=True)
  
```
**Section 1.3**
The purpose of *perform_basic_operations(...)* as a method, is to perform operations on the target list (which "test_vakues" is the variable that holds it, and which is part of the class). 
The basic operations are: addition, subtraction, division, multiplication, concatenation. That method uses operations from "operations.py", which we described in section 1.2.
Parameters regarding to perform_basic_operations are:
  ```
  testValues: list. It requires a value to be passed as list, containing all test values generated either manually or automatically (create_test-values(...) section 1.2);
  operation: str. It requires a value to be passed as string, pointing what operation to be used;
  type_only: type. It requires a value, of class: type, to be passed, pointing what type to be used only;
  args_for_operation: dict = {}. Specific args provided by user to be used, while calling the desired operation;
  ```
<br>
The next operation is to call *perform_changes(...)* method, it is important to note that I programmed this method in case if there are bugs going on within test_values. It is not essential to call it.
The next operation is assertEquals, this is the step that can be regarded as important. It compares all values, by detouring the *stored* list, and comparing if the returned value from the target function
is equal to the correct element.
Parameters regarding to *assertEquals(...)*:

  ```
  element: list, the user is required to provide a target list that will be iterated, that specific parameter is not being used: if "is_created" parameter is set to True.
  correct_element: list, the user is required to provide a list that includes all correct elements, if "is_created" parameter is set to True, ergo it must consists the test elements on the inside and as well as the expected element.
  text: str (optional), this parameter is due to user's choice. The user can set whatever text he wants.
  text_on_correct: str (optional), this parameter is again due to user's choice. The user can set whatever text he wants, if the comparison between the correct and the returned value from the function it'll output the text that the user inputed.
  strict_equals: bool (optional), this parameter can be set to True, if the user requires a more detailed and enhanced comparison between the elements.
  strict_equals_args: dict (optional), this parameter is used for arguments based on *strict_equals(...)* method.
  values_Stored: bool (optional), if in case values are stored.
  is_created: bool (optional), if in case the values were automatically generated.
  manualOperation: bool (optional), if in case the values were manually generated.
  ```

Let's use the functionality related to adding functions as operations, we'll use function b2 from section 1.1
  ```python
  from utils.unitTest import operations
  from utils.unitTest.unittesting import unitTest

  def b2(targetList: list) -> list:
      return [sum(element) for element in targetList]

  def b1(level1:int=2, level2:int=64):
        elementsToTest = []
        n = 0
        while len(elementsToTest) < level2:
            temp = []
            while len(temp) < level1:
                temp.append(n+1)
                n += 1
            elementsToTest.append(tuple(temp))
        return elementsToTest

  def a1(x: int, y: int):
      return x+y

  if __name__ == "__main__":
      example_usage = unitTest(a1, verbosity=True)

  ```
  

### How to use this project as a module?
  The usage of this project is simple & straightforward.
