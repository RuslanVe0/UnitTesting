# UnitTesting

### Introduction:
  Embarking on the Unit Testing project marks a pivotal decision in my software development journey and as a student in software engineering. I take it as an excellent choice for a project, in order to enhance my coding abilities. This initiative stems from the strategic aim of crafting a specialized tool that not only I have developed but one that will play a crucial role in rigorously testing and validating my future projects. The primary goal is to enhance the reliability, stability, and overall quality of my software endeavors.


### How to use this framework as a module?
  The usage of this framework is simple & straightforward.
  Here's an example Python function that accepts 2 parameters (param 1 has int as annotation, as well as param 2):
  ```python
      def a1(a: int, b: int):
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
  ```
      It performs a basic arithmetic operation (addition) of the product of two values (in this case they're integers as types).
      We can create a testing function, which will test function a1. Let's call it - b1.
