#iterative methods

def factorial(n):
    i = 1
    for num in range(2, n+1):
        i *= num
    return i

number = 5
print(number, "! =", factorial(number))