# open p1.in 
file = open("p1.in", "r")

digitsMap = {
  "one": "1",
  "two": "2",
  "three": "3",
  "four": "4",
  "five": "5",
  "six": "6",
  "seven": "7",
  "eight": "8",
  "nine": "9",
}

reversedDigitsMap = {}
for digit in digitsMap.keys():
  reversedDigit = digit[::-1]
  reversedDigitsMap[reversedDigit] = digitsMap[digit]

def getFirstNumberInLine(line):
  for i,c in enumerate(line):
    if c.isnumeric():
      return c

    firstFive = line[i:] # only need this substring since max len of digits is 5
    for digit in digitsMap.keys():
      if firstFive.startswith(digit):
        return digitsMap[digit]

def getLastNumberInLine(line):
  reversedLine = line[::-1]
  for i,c in enumerate(reversedLine):
    if c.isnumeric():
      return c

    firstFive = reversedLine[i:] # only need this substring since max len of digits is 5
    for digit in reversedDigitsMap.keys():
      if firstFive.startswith(digit):
        return reversedDigitsMap[digit]

total = 0
for line in file:
  strippedLine = line.strip()
  first = getFirstNumberInLine(strippedLine)
  last = getLastNumberInLine(strippedLine)
  combined = int(first + last)
  
  total += combined

print(total)
  