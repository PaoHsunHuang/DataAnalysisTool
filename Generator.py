import os
import random
inputString = input("File Name (column): ")
rangeL = 1
rangeH = 10
dataCount = 10
inputtemp = inputString.split()
name = inputtemp[0]
name += ".csv"
columnCount = 1;

#read the number of column if exist
if len(inputtemp) == 2:
    columnCount = int(inputtemp[1])


f = open(name, "w+")
#write column name default number counting
for i in range(columnCount):
    f.write(str(i))
    if i != (columnCount - 1):
        f.write(",")

f.write("\n")
#write data by random number
for i in range(dataCount):
    for j in range(columnCount):
        temp = random.randint(rangeL, rangeH)
        f.write(str(temp))
        if j != (columnCount - 1):
            f.write(",")
    f.write("\n")
f.close()



print("finish")
input()
