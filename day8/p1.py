class Node:
  def __init__(self, name, left, right):
    self.name = name
    self.leftStr = left
    self.rightStr = right

strToNode = {}

directions = input()
input()

# create nodes
try:
  while True:
    line = input().split('=')
    vertexStr = line[0].strip()
    leftstr = line[1].split(',')[0].strip()[1:]
    rightStr = line[1].split(',')[1].strip()[:-1]
    
    strToNode[vertexStr] = Node(vertexStr, leftstr, rightStr)
except EOFError:
  pass
start = "AAA"
current = strToNode[start]
i = 0
while current.name != "ZZZ":
  if directions[i % len(directions)] == "R":
    current = strToNode[current.rightStr]
  else:
    current = strToNode[current.leftStr]
  i += 1
print(i)