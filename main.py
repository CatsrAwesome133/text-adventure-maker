import sys
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"


path = "testing_doc.txt" #replace with input later

if "/" in path:
    name = path.split("/")
else:
    name = path.split("\\")

name = name[len(name)-1].split(".")[0]
print(name)


"""# creates a new file; currently not used since that function is not yet neccessary
try:
    n = input("Please enter the name for the output file: ")
    if n.strip != "" and n.isalnum():
        n = open(f"{n}.py", "x")
    else: 
        print(f"You haven't entered a valid name. The file will save as {BLUE}{name}.py{RESET}")
        n = open(f"{name}.py", "x")
except FileExistsError:
    sys.exit("That file already exists. Please delete or move it and restart the program.")
"""


with open(path, "r") as original:
    current_d = 0
    last_d = -1
    break_count = 0
    counting = True
    current = {}
    all_decisions = {}


    # scans through the document by line
    for line in original:
        line = str(line).replace('\n', '')
        # removes newlines so I don't suffer

        # try-except stops errors from occuring when the line is empty
        try:
            # detects decisions
            if line[0] == "#":
                last_d += 1
                break_count = 0
                counting = True
                print(RED,line,RESET)
                current_key = line[1:].split(" ")[0]
                # adds the ID of the current decision to the master list
                all_decisions[current_key] = '' # single quotes to be replaced later
                print("Key: ", current_key)
        except IndexError:
            pass

        # only counts when there is a new decision
        if current_d < last_d:
            # detects new option
            try: 
                if " > " in line:
                    break_count = 0
                    print(YELLOW,line,RESET)
                    options = line.split(" > ")

                    # takes the option id
                    current_option = options[0]

                    # takes the option name
                    current_name = options[1].split("(")[0].strip()

                    # prints them
                    print("Option: ", current_option,"Name: ", current_name)

                    # detects wether there's a chance value
                    if "(" in options[1]:
                        # registers and prints it
                        current_chance = options[1].split("(")[1].replace(")","").strip()
                        print("Chance: ",current_chance)
                    else:
                        current_chance = None
                elif line[0] == "[":
                    next_decision = line[1:].replace("]","").strip()
                    print(GREEN,line,RESET)
                    print("Next decision: ", next_decision)
                elif line.strip() != "":
                    print(BLUE,line,RESET)
                else:
                    pass
            except IndexError:
                pass

        # counts line breaks
        elif line.strip() == "":
            break_count += 1

        # new decision occurs when there are 2-3 line breaks, so it's set to >= 2
        if break_count >= 2:
            counting = False
            current_d = last_d