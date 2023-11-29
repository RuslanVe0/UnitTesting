def b1(level1:int=2, level2:int=64):
    elementsToTest = []
    n = 0
    while len(elementsToTest) < level2:
        temp = []
        while len(temp) < level1:
            temp.append(n+1)
            n += 1
        elementsToTest.append(tuple(temp))

if __name__ == "__main__": b1()