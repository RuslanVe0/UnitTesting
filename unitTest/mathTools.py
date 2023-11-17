class OtherTools():


    def __init__(self, value):
        self.value = value
    
    def find_fact(self):
        if not isinstance(self.value, int): raise TypeError("An integer is required!")
        sum_ = 1
        for iterator in range(1, self.value, 1):
            sum_ *= iterator
        return sum_