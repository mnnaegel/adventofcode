sequences = []
try:
    while True:
        sequences.append(list(map(int, input().split())))
except EOFError:
    pass

def process_sequences(sequence):
    stack = []
    stack.append(sequence)

    while True:
        next_level = []

        if len(stack[-1]) == 1:
            break

        if len(stack[-1]) == stack[-1].count(0):
            break 

        for i in range(len(stack[-1])-1):
            next_level.append(stack[-1][i+1]-stack[-1][i])
        stack.append(next_level)

    if len(stack) == 1:
        return sequence[-1]

    stack = stack[::-1]
    for i in range(len(stack)-1):
        stack[i+1].append(stack[i][-1]+stack[i+1][-1])
    return stack[-1][-1]

res = 0
for sequence in sequences:
    res += process_sequences(sequence)
print(res)

