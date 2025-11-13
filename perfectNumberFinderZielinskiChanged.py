# Matthew Zielinski

# perfect numbers are related to mersenne primes, so I'm just going to generate mersenne numbers and see if they're perfect

from tqdm import tqdm

primeList = [2, 3, 5, 7, 11]
def is_prime(number : int) -> bool:
    if number == 0:
        return False
    
    for i in primeList:
        if i == number:
            return True
        elif i > number:
            primeList.append(number)
            return True
        
        if number % i == 0:
            return False
    return True

for i in range(100):
    is_prime(i)
print(primeList)

def mersenne_number(power : int) -> int:
    return (2 ** power) - 1

# let's revise this to break into prime factors!
def get_factors(number : int) -> list:


    factorList = []
    for i in range(1, int(number ** 0.5) + 1, 1):
        if number % i == 0:
            factorList.append(i)
            if i == 1:
                continue
            factorList.append(int(number / i))
    
    return factorList

def is_number_perfect(number : int) -> bool:
    if number == 0: return False
    if number == 1: return False
    return sum(get_factors(number)) == number


for power in (range(1,100)):
    number = (2 ** (power - 1)) * ((2 ** power) - 1)
    print(f"Testing {number}")
    if is_number_perfect(number=number):
        print(f"{number} is perfect with factors {sorted(get_factors(number))}")
        print()

