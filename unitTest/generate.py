from random import randint, choice
from string import ascii_lowercase, ascii_uppercase

class generate():
    def __init__(self): pass

    def generate_list(self, max_size_list = 64, total_times_to_iterate: int = 1024):
        generatedList = []
        times = total_times_to_iterate
        while len(generatedList) < max_size_list:
            randomized = randint(1, 1280000)
            if not(randomized % 2): generatedList.append(self.list_generator_randomized(times=times))
            else: generatedList.append([_ for _ in range(0, 1024, 1)])
        return generatedList

    def list_generator_randomized(self, times: int) -> list:
        actualToGenerate = []
        for _ in range(1, times, 1):
            temp = []
            for _ in range(0, times/2):
                temp.extend([_ for _ in range(1, randint(1, 1024), 1)])
        return actualToGenerate

    def generate_random_integers(self, max_size_list = 64) -> list:
        generated = []
        while len(generated) < max_size_list:
            generated.append(randint(1, 1280000))
        return generated
    
    def generate_random_strings(self, max_size_list = 64) -> list:
        generated = []
        times = 0
        while len(generated) < max_size_list:
            generated.append("".join(choice(ascii_lowercase) for _ in range(0, times, 1)))
            times += 1
        return generated