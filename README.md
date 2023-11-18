# UnitTesting (still in development)

### Introduction:
  Embarking on the Unit Testing project marks a pivotal decision in my software development journey and as a student in software engineering. I take it as an excellent choice for a project, in order to enhance my coding abilities. This initiative stems from the strategic aim of crafting a specialized tool that not only I have developed but one that will play a crucial role in rigorously testing and validating my future projects. The primary goal is to enhance the reliability, stability, and overall quality of my software endeavors.


### Basics
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
    
  Now there's something particular, and now we performs operations within the elements in targetArray, basic addition operations, and then we return the updated list.
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

### Basics of this project
  Provided operations:
     <p style="margin-right: 15px"> *addition(...)*: The purpose of this function is to perform basic addition operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *subtraction(...)*: The purpose of this function is to perform basic subtraction operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *division(...)*: The purpose of this function is to perform basic division operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *multiplication(...)*: The purpose of this function is to perform basic multiplication operations, where user must provide arguments. </p>
      <p style="margin-right: 15px"> *concate(...)*: The purpose of this function is to perform basic concate operations, where user must provide arguments. </p>

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
The value returned from any operation available (whether it is: addition, subtraction, multiplication, division or concate) it returns it as an object, where the user can perform varius operations
onto the list. You can experiment with it.

Let's dive deeper, and instead of defining our own function and manually to create a list, to create it automatically using the method *create_test_values(...)*.
The required parameters are:<br>
  rangeVals: (list, tuple): <br>
    which parameter requires a list with 2 elements inside. 1st element must be either a tuple or a list, and it must signify the interval between the values
    that are required to be provided. The other element must be a type, here's is due to user choice and needs. Here's an example
    create_test_values(rangeVals=[(1, 255), int]), thus we can interpret that the interval is (1; 255) and the type that we need is *int*.
### How to use this project as a module?
  The usage of this project is simple & straightforward.
