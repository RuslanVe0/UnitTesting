# UnitTesting

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
    

### How to use this project as a module?
  The usage of this project is simple & straightforward.
