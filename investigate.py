# Open the file in read mode
with open('file2.txt', 'r') as file:
    lineNumber=0
    for line in file:
        if lineNumber == 1344:
            line = file.readline()
            numbers = line.split(',')
            print(numbers)
        lineNumber +=1

print(len(numbers)-1)