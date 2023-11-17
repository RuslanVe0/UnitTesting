class tools_comp(object):

    maximum: tuple = ()
    minimum: tuple = ()

    def __init__(self, value: any, argumentObjectVerbosity: bool = None):
        self.verbose_output = argumentObjectVerbosity
        self.value = value
        super().__init__()
    
    def set_attributes_dict(self):
        if "Maximum" not in self.value or "Minimum" not in self.value:
            raise ValueError("'Maximum' and/or 'Mininum' are missing!")
        self.maximum = (self.value["Maximum"][0], self.value["Maximum"][1])
        self.minimum = (self.value["Minimum"][0], self.value["Minimum"][1])

    def perform_operation(self, operation: object):
        if not callable(operation): raise ValueError("The value used for parameter - 'operation' is incorrect. It has to be method or a function.")
        for i in range(0, len(self.value), 1):
            for j in range(0, len(self.value[i]), 1):
                if isinstance(self.value[i][j], (list, tuple)):
                    for k in range(0, len(self.value[i][j])):
                        ceil_ = operation(self.value[i][j][k])
                        self.verbose_output("Iterating through elements [i=%d, j=%d, k=%d] producing in: %.2f (with floating point:: %.2f)" % (
                        i, j, k, self.value[i][j][k], ceil_))
                        self.value[i][j][k] = ceil_
                else:
                    ceil_ = operation(self.value[i][j][k])
                    self.verbose_output("Iterating through elements [i=%d, j=%d] producing in: %s (with floating point:: %.2f)" % (i, j, self.value[i][j], ceil_))
                    self.value[i][j] = operation(self.value[i][j])
        return self.value
    
    def sort_array(self, type_: object):
        """
            The purpose of this method is to sort an array under specific condition provided, in a function.

            (where :keyword is param),
            type_:  This parameter takes as an argument a function, that is callable, and that function must return
            perform comparison operations, where from that parameter depends: whether to sort the array in ascending
            or descending order.
        """
        if not callable(type_): raise TypeError("The value used for parameter - 'type_' is not callable. It has to be method or a function!")
        for _ in range(0, len(self.value), 1):
            min_ = self.value[0][0][0]
            for i in range(1, len(self.value), 1):
                if len(self.value[i][0]) == 0: continue
                sel = self.value[i][0][0]
                if type_(min_, sel):
                    self.value[i-1][0][0] = sel
                    self.value[i][0][0] = min_
                else:
                    min_ = sel

        return self.value
    

