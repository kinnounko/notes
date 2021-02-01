import time
from mpmath import *
import csv 
import pandas as pd


mp.dps = 100
PI_CONST = mp.pi


# Function that determines if the approximated value of
# pi is correct to a specified decimal
def decimal_is_correct(pi, decvalue):
    #pi_diff = str(abs(pi))
    zeros = 0
    pistr = str(pi)[2:]
    piconst = str(PI_CONST)[2:]
    for i in range(len(pistr)):
        if pistr[i] != piconst[i]: break
        else: 
            zeros += 1
    if zeros == decvalue:
        return True
    else:
        return False

def madhava(decimals):
    piapprox = 0
    i = 0 

    t1 = time.time()
    
    while not decimal_is_correct(piapprox * mp.sqrt(12), decimals):
        # This is a direct mirror of the summation from the formula
        piapprox += mp.power(-3, -i) / (2*i+1)
        i += 1
    piapprox *= mp.sqrt(12)
    t2 = time.time()

    # Return the time spent (t2-t1) getting d value of decimal places
    return i


# Function that approximates pi using Viete's method
def viete(decimals):
    piapprox = 1
    numer = 0
    i= 0

    while not decimal_is_correct((1.0 / piapprox) * 2.0, decimals):
        numer = mp.sqrt(2.0 + numer)
        piapprox *= (numer / 2.0)
        i += 1
    piapprox = (1.0 / piapprox) * 2.0


    # Return the time spent (t2-t1) getting d value of decimal places
    return i

if __name__ == "__main__":
    decimals = [68]

    for dec in decimals:
        print(viete(dec))
        print(madhava(dec))
