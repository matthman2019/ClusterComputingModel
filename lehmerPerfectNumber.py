def is_mersenne_prime(number : int):
    mersenne_number = (2 ** number) - 1
    s = 4
    for i in range(number - 2):
        s = ((s * s) - 2) % mersenne_number
    return s == 0


# gets factors
def get_factors(number : int) -> list:
    factorList = []
    for i in range(1, int(number ** 0.5) + 1, 1):
        if number % i == 0:
            factorList.append(i)
            if i == 1:
                continue
            factorList.append(int(number / i))
    
    return factorList

# brute forces to see if a number is perfect
def is_number_perfect(number : int) -> bool:
    if number == 0: return False
    if number == 1: return False
    return sum(get_factors(number)) == number


number = 0
while True:
    number += 1

    if not is_mersenne_prime(number):
        continue

    p = (2 ** (number - 1)) * ((2 ** number) - 1)
    print(f"Prime: {number} Perfect Number: {p}")