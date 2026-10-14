import sys
import tkinter as tk
from tkinter import filedialog

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"

# STRICTLY USE DOUBLE QUOTES IN THIS CODE

path = "testing_doc.txt" #replace with input later


n = ''

# creates a new file; currently not used since that function is not yet necessary



 # take these as an input later
newline = "··> "
new_decision_indicator = "#"

def process(file_path, file_name, newline, new_decision_indicator):
    with open(file_path, "r") as original:
        current_d = 0
        last_d = 0
        break_count = 0
        counting = True
        current = {}
        all_decisions = ""


        # scans through the document by line
        for line in original:
            line = str(line).replace('\n', '')
            # removes newlines so I don't suffer

            # try-except stops errors from occurring when the line is empty
            try:
                # detects decisions
                if line[0] == f"{new_decision_indicator}":
                    last_d += 1
                    break_count = 0
                    counting = True
                    print(RED,line,RESET)
                    current_key = line[1:].split(" ")[0]
                    # adds the ID of the current decision to the master list

                    # single quotes to be replaced later
                    current[current_key] = {}
                    print("Key: ", current_key)
            except IndexError:
                pass

            # only counts when there is a new decision
            if current_d < last_d:
                try:
                    # detects new option
                    if ">" in line:
                        text_count = 0
                        text_string = ""
                        break_count = 0
                        print(YELLOW,line,RESET)
                        options = line.split(">")

                        # takes the option id
                        current_option = options[0].strip()

                        # takes the option name
                        current_name = options[1].split("(")[0].strip()

                        # prints them
                        print("Option: ", current_option,"Name: ", current_name)

                        # assigning stuff
                        current[current_key][current_option] = ["","",""]
                        current[current_key][current_option][0] = current_name

                        # detects whether there's a chance value
                        if "(" in options[1]:
                            # registers and prints it
                            current_chance = options[1].split("(")[1].replace(")","").strip()
                            print("Chance: ",current_chance)
                        else:
                            current_chance = None

                    # detects next decision indicator
                    elif line[0] == "[":
                        # gets the ID
                        next_decision = line[1:].replace("]","").strip()

                        # prints the line & the fetched ID
                        print(GREEN,line,RESET)
                        print("Next decision: ", next_decision)

                        # assigning stuff
                        current[current_key][current_option][2] = next_decision
                        if current_chance is not None:
                            current[current_key][current_option].append(current_chance)


                    # detects narration text
                    elif line.strip() != "" and line[0] != f"{new_decision_indicator}":
                        print(BLUE,line,RESET)
                        # tests whether it's the first line
                        try:
                            text_count += 1
                            if text_count != 1:
                                text_string += f"\n{newline}"
                            text_string += line
                            print(text_string)
                        except NameError:
                            pass

                        # assigning stuff
                        current[current_key][current_option][1] = text_string
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

    all_decisions = "all_decisions = {"
    written_line = ''

    print(current)

    with open(f"{file_name}.py", "a") as f:
        f.write("from classes import Decision\n")
        for item in current:
            all_decisions += f'"{item}": {item},\n'
            written_line = item + " = Decision(" + str(current[item]) + ")\n"
            f.write(written_line)
        f.write(all_decisions + "}")



# the UI
root = tk.Tk(baseName='Text Adventure Maker')
root.geometry("500x100")

frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="File path").grid(row=0, column=0)
tk.Label(frame, text="Output File Name").grid(row=1, column=0)
label1 = tk.Label(frame, text="")
label1.grid(row=0,column=2)

def open_file():
    # Opens the file dialog and stores the selected file path
    file_path = filedialog.askopenfilename(
        title="Select a File",
        initialdir="/",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    label1.config(text="Selected: " + file_path)

    if file_path:  # Check if the user selected a file or cancelled
        global path
        global name
        path = str(file_path)

        if "/" in path:
            name = path.split("/")
        else:
            name = path.split("\\")

        name = name[len(name) - 1].split(".")[0]
        print(name)


def get_name():
    global name
    n = entry2.get()
    if n is not None:
        if n.strip != "" and n.isalnum():
            name = n
            open(f"{name}.py", "x")
        else:
            print(f"You haven't entered a valid name. The file will save as {BLUE}{name}.py{RESET}")
            open(f"{name}.py", "x")
    else:
        sys.exit("That file already exists. Please delete or move it and restart the program.")


file = tk.Button(frame, text="Open File", command=open_file)
entry2 = tk.Entry(frame)

file.grid(row=0, column=1)
entry2.grid(row=1, column=1)

button = tk.Button(frame, text="OK", width=15, command=get_name)
button.grid(row=2, column=1)

root.mainloop()