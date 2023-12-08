from collections import defaultdict

class Node:
  def __init__(self, name, left, right):
    self.name = name
    self.leftStr = left
    self.rightStr = right

strToNode = {}

directions = input()
input()
ghostStarts = []

# create nodes
try:
  while True:
    line = input().split('=')
    vertexStr = line[0].strip()
    leftstr = line[1].split(',')[0].strip()[1:]
    rightStr = line[1].split(',')[1].strip()[:-1]
    
    strToNode[vertexStr] = Node(vertexStr, leftstr, rightStr)
    if (vertexStr[-1] == "A"):
      ghostStarts.append(vertexStr)
except EOFError:
  pass

def validState(ghostPositions):
  for ghostPosition in ghostPositions:
    if ghostPosition[-1] != "Z":
      return False
  return True

AStartToZEnd = {
  "KTA": "DLZ",
  "PLA": "RGZ",
  "LJA": "BGZ",
  "AAA": "ZZZ",
  "JXA": "NTZ",
  "NFA": "HBZ"
}

znodes = {
  0: "DLZ",
  1: "RGZ",
  2: "BGZ",
  3: "ZZZ",
  4: "NTZ",
  5: "HBZ",
}

# want to know history of i positions for each value in AStartToZEnd.values() 

i = 0
zhistories = defaultdict(list)

while i<=1000000:
  for j,ghostStart in enumerate(ghostStarts):
    current = strToNode[ghostStart]
    
    if (current.name[-1] == "Z"):
      zhistories[j].append(i)

    if directions[i % len(directions)] == "R":
      current = strToNode[current.rightStr]
    else:
      current = strToNode[current.leftStr]
    ghostStarts[j] = current.name
  i += 1    

# turn each list in zhistories into a list of differences
for val in zhistories.values():
  print(list(map(lambda x: x[1] - x[0], zip(val[:-1], val[1:]))))
    
# from this code we see that each time a ghost reaches Z, it will reach on a step mod ki, where i is the ith ghost and k is the ghost's corresponding val
# in this arrray
cycleLengths = [12083, 14893, 16579, 17141, 19951, 22199]

# want to find the smallest number such that it is a multiple of all of these numbers?
# consider euler's prime factorizaton for each and take the max of each prime factor

def get_factors(n):
  factors = []
  i = 2
  while i * i <= n:
    if n % i:
      i += 1
    else:
      n //= i
      factors.append(i)
  if n > 1:
    factors.append(n)
  return factors

primeFactors = defaultdict(int)
for cycleLength in cycleLengths:
  for factor in get_factors(cycleLength):
    primeFactors[factor] = max(primeFactors[factor], get_factors(cycleLength).count(factor))

res = 1
for key in primeFactors.keys():
  res *= key ** primeFactors[key]
print(res)