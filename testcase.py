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
