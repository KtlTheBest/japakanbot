with open("headers") as f:
    lines = f.readlines()

res = {}
for line in lines:
    splitted = line.rstrip().split(": ")
    res[splitted[0]] = splitted[1]

print(res)
