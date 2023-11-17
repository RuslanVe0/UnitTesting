import re

class Error(Exception):

    text_cont: dict = {
        "0x0bac" : "Incorrect type: It is required string type!",
        "0x0bad" : "Incorrect type: It is required a tuple or a list!",
        "0x1baf" : "Incorrect arguments: Not enough or incorrect type provided.",
        "0x0415" : "Missing unique key.",
        "0x0ba4" : "Incorrect type: It is required a tuple, dict or a list!",
        "0xf341" : "Invalid number of arguments provided.",
        "c" : "That is not a function.",
        "user-validated" : {
            
        }
    }

    def __init__(self, error: str, custom: bool = False):
        if not custom:
            if error not in self.text_cont: raise KeyError(f"{error} could not be located!")
            text = self.text_cont[error]
        else:
            text = error
            error = "custom-Exception(0x0000): "
        super().__init__(f"{error}: {text}")
    
    def _inputError(self, new_exception: str, value: str):
        """
            In this system, exception unique names are preferred to be written in hexadecimal notation.
            The criterion for a valid exception name is defined by the following regular expression:
                '^0x?[a-fA-F0-9]+$' will be used to match if all the characters meets the rules used in
                the regular expression.
            Intuition:
                On first thought, the name of the exceptions to be a normal character pattern ([a-Z] characters
                only allowed), then after a bit of analysis I decided to make it with hexadecimals.
            Reasoning:
                The choice of hexadecimal notation, used in uniqueness of exception names, is driven by its uniqueness
                and ease of management. Hexadecimal representations provides a concise and easily distinguishable format,
                particularly in computing and programming contexts.
        """
        if new_exception in self.text_cont or not re.match(r"^0x?[a-fA-F0-9]+$", new_exception):
            raise ValueError("error: Cannot create new exception.")
        self.text_cont["user-validated"][new_exception] = value