import time
import math
from mpmath import *


RED = "\x1B[31m"
GREEN = "\x1B[32m"
RESET = "\x1B[0m"
mp.dps = 100
PI_CONST = str(mp.pi)


def print_as_text(pi):
    pi_string = str(pi)
    print("Constant:       " + PI_CONST)
    print("Approximation:  ", end="")
    for i in range(0, len(pi_string)):
        if pi_string[i] == PI_CONST[i]:
            print(GREEN +  pi_string[i] + RESET, end="")
        else:
            print(RED +  pi_string[i] + RESET, end="")
    print("\n")


def decimal_is_correct(pi, decvalue):
    pi_string = str(pi)
    print(pi_string)
    if pi_string[decvalue] == PI_CONST[decvalue]:
        return True
    elif pi_string == "0.0":
        return False
    else:
        return False


def madhavaleibniz(iter):
    piapprox = 0
    i = 0 

    t1 = time.time()
    while not decimal_is_correct(piapprox * mp.sqrt(12), 10):
        #for i in range(iter):
        # This is a direct mirror of the summation from the formula
        piapprox += mp.power(-3, -i) / (2*i+1)
        i += 1
    piapprox *= mp.sqrt(12)
    t2 = time.time()

    print_as_text(piapprox)

    # Return the time spent (t2-t1) and number of iterations
    return t2-t1


def viete(iter):
    piapprox = 1
    numer = 0

    t1 = time.time()

    # Viete's method
    for i in range(1, iter + 1):
        numer = mp.sqrt(2.0 + numer)
        piapprox *= (numer / 2.0)
    piapprox = (1.0 / piapprox) * 2.0

    t2 = time.time()

    print_as_text(piapprox)

    # Return the time spent (t2-t1) getting d value of decimal places
    return t2-t1

if __name__ == "__main__":
    iter = 10
    trials = 3 

    print("time: ", madhavaleibniz(iter))
    print("time: ", viete(iter))