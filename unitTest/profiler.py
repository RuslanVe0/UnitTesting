"""
This piece of code is developed to implement various analysis based on functions part of the UnitTesting project.
These analysis may include: 
    * time profiler;
    * function analysis;
"""


import typing

from threading import Thread
from time import time
import numpy as np

class statistics(object):

    def __init__(self) -> None:
        super().__init__()

    def count_elements(self):
        return len(self.results)
    
    def get_top_5(self, lowest: typing.Optional[bool] = False) -> list:
        """
        The purpose of this method is sort a list, using 5 elements (top 5 elements either in: ascending way, or descending),
        in either ascending or descending sort.

        (where :key = param)
        :lowest - it requires a value that is a boolean (True || False (1 || 0)). False means in: ascending way. True means in: descending way.
        """
        if self.count_elements()-1 < 5: return False
        first = [self.results[0], self.results[1], self.results[2], self.results[3], self.results[4]]
        for _ in range(0, len(self.results)):
            for _, elements in self.results.items():
                for index, elements1 in enumerate(first, 0):
                    if elements > elements1 and not lowest and elements not in first:
                        first[index] = elements
                    elif elements < elements1 and lowest and elements not in first:
                        first[index] = elements
        return self.re_sort(first, lowest)
    
    def re_sort(self, targetList: list, lowest: bool) -> list:
        for _ in range(0,len(targetList), 1):
            for index, element in enumerate(targetList, 0):
                if index+1 > len(targetList)-1: break
                if (element > targetList[index+1] and not lowest) or element < targetList[index+1] and lowest:
                    last = targetList[index+1]
                    targetList[index+1] = element
                    targetList[index] = last
        return targetList
    
    def get_top_n(self, numberOfElements: int, lowest: typing.Optional[bool] = False) -> list:
        if numberOfElements > len(self.results)-1: raise ValueError("'n' cannot be greater than results!")
        listOfElements = []
        for _ in range(0, numberOfElements, 1):
            listOfElements.append(self.results[_])
        for _ in range(0, len(self.results)):
            for _, elements in self.results.items():
                for index, elements1 in enumerate(listOfElements, 0):
                    if elements > elements1 and not lowest and elements not in listOfElements:
                        listOfElements[index] = elements
                    if elements < elements1 and lowest and elements not in listOfElements:
                        listOfElements[index] = elements
        return self.re_sort(listOfElements, lowest)

    def find_avg(self) -> float:
        """
        The purpose of this method is to calculate the average of elements, and the function returns the result in float.
        This method doesn't require any arguments to be provided.
        """
        total_sum = 0
        for _, element in self.results.items():
            total_sum += element
        return total_sum/len(self.results)

    def find_max(self) -> float:
        """
            I'll use a classical algorithm of finding the maximum value (instead of using 'max(...)' built-in function).
        """
        maximumValue = self.results[0]
        for _, element in self.results.items():
            if element > maximumValue: maximumValue = element
        return maximumValue
    
    def find_min(self, array = None) -> float:
        minimumValue = self.results[0] if not array else array[0]
        for _, element in self.results.items() if not array else enumerate(array, 0):
            if element < minimumValue: minimumValue = element
        return minimumValue
    
    def find_total_time(self):
        return sum([element for _, element in (self.results.items() if isinstance(self.results, dict) else enumerate(self.results, 0))])
    
    def cut_to_n_after_dec_point(self, n: int, save: typing.Optional[bool] = False) -> list:
        padd = "%" + ".%d" % (n) + "f"
        arr = [float(padd % (element)) for _, element in self.results.items()]
        if save: self.results = arr
        return arr
    
    def run_analytics(self, experiment_dict: dict = None):
        if not experiment_dict: experiment_dict = self.results
        if not isinstance(experiment_dict, dict): raise TypeError("'experiment_dict' parameter must be from a type 'dict'...")
        values = []
        data = {"basic-analytics":{}}
        for _, _value in experiment_dict.items():
            values.append(_value)
        middle = len(values)//2 # the median part will be used to compare both arrays, each element with each element.
        array_1, array_2 = values[:-middle], values[middle:]
        total_matches = []
        totalLargestLSide = []
        for i, element in enumerate(array_1, 0):
            for _, element2 in enumerate(array_2, 0):
                if (element, i) in total_matches or (element, i) in totalLargestLSide: continue
                if element == element2: total_matches.append((element, i))
                if element >= element2: totalLargestLSide.append((element, i))
        timeMax, timeMin = sorted(values)[(len(values)-3):], sorted(values)[:-(len(values)-3)]
        differences = []
        differences_percentage = []
        for i, element in enumerate(timeMax, 0):
            calc = abs(timeMin[i] - element) if timeMin[i] else timeMin[i] - element
            differences.append(calc)
            if not element or not timeMin[i]: continue
            differences_percentage.append((timeMin[i]/element) * 100)
        data["basic-analytics"] = {"comparison" : {"Largest" : len(totalLargestLSide), "total_matches" : len(total_matches),
        "Other" : (len(array_1)+len(array_2))-len(totalLargestLSide)}}
        data["comparison"] = {"differenceSum" : sum(differences), "averageSum" : sum(differences) / len(differences),
        "HighestDifference" : ((0, differences[0]), (len(differences)-1, differences[len(differences)-1])),
        "Biggest": max(differences), "Smallest": min(differences)}
        return data

    def smallest_time_estimation(self) -> dict:
        analytics = {}
        actualList = [element for _, element in (self.results.items() if isinstance(self.results, dict) else enumerate(self.results, 0))]
        if len(actualList) == 1: return actualList
        parts_cut = [actualList[:-((len(actualList)//2)-1)], actualList[(len(actualList)//2)-1:]]
        first_part, second_part = parts_cut
        first_part, second_part = sorted(first_part), sorted(second_part)
        highest_top_3fp, highest_top3sp = sum(first_part[(len(first_part)-1)-3:]), sum((second_part[(len(second_part)-1)-3:]))
        smallestfp, smallestsp = sum(first_part[:-3]), sum(second_part[:-3])
        if not smallestfp or not smallestsp: smallestfp+=0.01; smallestsp += 0.01
        if not highest_top3sp or not highest_top_3fp:
            highest_top3sp += 0.001
            highest_top_3fp += 0.001
        analytics["percentage-highest-fpsp"] = (highest_top_3fp/highest_top3sp if highest_top_3fp < highest_top3sp else highest_top3sp/highest_top_3fp) * 100
        analytics["percentage-smallest-fpsp"] = (smallestfp+0.001 / smallestsp+0.001 if smallestfp < smallestsp else smallestsp+0.001 / smallestfp+0.001) * 100
        analytics["percentage-smallest-highest-fpsp"] = ((smallestsp/highest_top3sp)*100,
        (smallestfp/highest_top3sp)*100)
        smallest_values = []
        highest_values = []
        if not highest_top3sp or not highest_top_3fp:
            highest_top_3fp += 0.001
            highest_top3sp += 0.001
        total = (highest_top3sp + highest_top_3fp)/(0.2/(highest_top_3fp+0.001)+highest_top3sp+0.001)
        for elements in sorted(actualList):
            if elements >= total: highest_values.append(elements); continue
            smallest_values.append(elements)
        analytics["percentage-smallest-to-highest"] = len(smallest_values), len(highest_values)
        return analytics

    def middle_value(self):
        middle = len(self.results)//2
        return self.results[middle]

class timeProfiler(statistics):


    def __init__(self, targetFunction: object, kwargs: dict, runTests: typing.Optional[int] = 1):
        self.targetFunction = targetFunction
        self.kwargs = kwargs
        self.totalTests = runTests
        super().__init__()
        self.results = {}
    
    def startProfiler(self):
        if not isinstance(self.kwargs, tuple): pass
        for _ in range(0, self.totalTests, 1):
            self.results[_] =  "unfinished"
            Thread(target=self.analyze, args=(_,)).start()
        while self.is_there_unfinished():
            print("Waiting for all workers to finish their job...")
        print(f"All tests, invokations: {self.totalTests}, ran successfully!")
        return self

    def is_there_unfinished(self) -> bool:
        for _, elements in self.results.items():
            if elements == "unfinished": return True
        return False
    
    def analyze(self, key: int):
        timeStarted = time()
        self.targetFunction(**self.kwargs)
        self.results[key] = time() - timeStarted