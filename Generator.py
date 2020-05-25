import os
import random
name = input("File Name: ")
rangeL = 1
rangeH = 10
dataCount = 10

name += ".txt"
f = open(name, "w+")
for i in range(dataCount):
    temp = random.randint(rangeL, rangeH)
    f.write(str(temp) + "\n")


f.close()
print("finish")
input()
