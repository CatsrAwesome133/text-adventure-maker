path = input()

name = path.split("/")
name = name[len(name)-1].split(".")[0]
print(name)

n = open(f"~/{name}.py")

with open(path, "r") as original:
    for line in original:
        print(line)