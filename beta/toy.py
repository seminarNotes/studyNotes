import os
import math
from time import sleep


def slow_donut() :
    A = 0
    B = 0
    while True:
        z = [0] * 1760
        b = [' '] * 1760
        for j in range(0, 628, 7):  
            j /= 100  
            for i in range(0, 628, 2):  
                i /= 100  
                sini = math.sin(i)
                cosj = math.cos(j)
                sinA = math.sin(A)
                sinj = math.sin(j)
                cosA = math.cos(A)
                cosj2 = cosj + 2
                mess = 1 / (sini * cosj2 * sinA + sinj * cosA + 5)
                cosi = math.cos(i)
                cosB = math.cos(B)
                sinB = math.sin(B)
                t = sini * cosj2 * cosA - sinj * sinA
                x = int(40 + 30 * mess * (cosi * cosj2 * cosB - t * sinB))
                y = int(12 + 15 * mess * (cosi * cosj2 * sinB + t * cosB))
                o = int(x + 80 * y)
                N = int(8 * ((sinj * sinA - sini * cosj * cosA) * cosB - sini * cosj * sinA - sinj * cosA - cosi * cosj * sinB))
                if 0 <= o < 1760 and y < 22 and x > 0 and x < 80 and mess > z[o]:
                    z[o] = mess
                    b[o] = ".,-~:;=!*#$@"[N if N > 0 else 0]

        os.system('cls' if os.name == 'nt' else 'clear')
        
        for k in range(1760):
            print(b[k] if k % 80 else '\n', end='')
            A += 0.00004
            B += 0.00002

        sleep(0.001)  


def fast_donut() :

    A = 0
    B = 0
    while True:
        z = [0] * 1760
        b = [' '] * 1760
        for j in range(0, 628, 7):
            j /= 100  
            for i in range(0, 628, 2):  
                i /= 100  
                sini = math.sin(i)
                cosj = math.cos(j)
                sinA = math.sin(A)
                sinj = math.sin(j)
                cosA = math.cos(A)
                cosj2 = cosj + 2
                mess = 1 / (sini * cosj2 * sinA + sinj * cosA + 5)
                cosi = math.cos(i)
                cosB = math.cos(B)
                sinB = math.sin(B)
                t = sini * cosj2 * cosA - sinj * sinA
                x = int(40 + 30 * mess * (cosi * cosj2 * cosB - t * sinB))
                y = int(12 + 15 * mess * (cosi * cosj2 * sinB + t * cosB))
                o = int(x + 80 * y)
                N = int(8 * ((sinj * sinA - sini * cosj * cosA) * cosB - sini * cosj * sinA - sinj * cosA - cosi * cosj * sinB))
                if 0 <= o < 1760 and y < 22 and x > 0 and x < 80 and mess > z[o]:
                    z[o] = mess
                    b[o] = "012345689@#&"[N if N > 0 else 0]

     
        os.system('cls' if os.name == 'nt' else 'clear')
        
        for k in range(1760):
            print(b[k] if k % 80 else '\n', end='')
            A += 0.00008  
            B += 0.00004  

        sleep(0.01)  

if __name__ == "__main__" :
    fast_donut()
