path = input()

if "/" in path:
    name = path.split("/")
else:
    name = path.split("\\")

name = name[len(name)-1].split(".")[0]
print(name)

#n = open(f"~\{name}.py")

with open(path, "r") as original:
    current_d = 0
    last_d = -1
    counting = True
    for line in original:
        print(current_d, " ", last_d)
        if str(line)[0] == "#":
            last_d += 1
            counting = True
        if current_d == last_d:
            print(line)
            print(current_d)
        if str(line).strip() == "" and counting:
            current_d += 1
            counting = False