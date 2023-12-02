# open p1.in 
file = open("p1.in", "r")

def getFirstNumberInLine(line):
  for c in line:
    if c.isnumeric():
      return c

def getLastNumberInLine(line):
  for c in reversed(line):
    if c.isnumeric():
      return c

total = 0
for line in file:
  strippedLine = line.strip()
  first = getFirstNumberInLine(strippedLine)
  last = getLastNumberInLine(strippedLine)
  combined = int(first + last)
  
  total += combined

print(total)
  