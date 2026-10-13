RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


path = "testing_doc.txt" #replace with input later

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
    break_count = 0
    counting = True
    current = {}
    all_decisions = {}


    for line in original:
        line = str(line).replace('\n', '')
        try:
            if line[0] == "#":
                last_d += 1
                counting = True
                print(RED,line,RESET)
                current_key = line[1:].split(" ")[0]
                all_decisions[current_key] = ""
                print("Key: ", current_key)
        except IndexError:
            pass
        if current_d == last_d:
            if " > " in line:
                print(YELLOW,line,RESET)
                options = line.split(" > ")

                current_option = options[0]
                current_name = options[1].split("(")[0].strip()
                print("Option: ", current_option,"Name: ", current_name)
                if "(" in options[1]:
                    current_chance = options[1].split("(")[1].replace(")","").strip()
                    print("Chance: ",current_chance)
            else:
                pass

        elif line.strip() == "":
            break_count += 1
        if break_count >= 2:
            counting = False
            current_d = last_d