import tkinter as tk
from tkinter import filedialog
from sys import platform

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"


path = None
name = None
new_line = ""
new_decision = ""
next_decision = ""
option_seperator = ""

customs = {
    "new_line": "",
    "new_d": "",
    "jump": "",
    "opts": "",
}



def process(newline="··> ", new_decision_indicator="#", jump=None, opt_sep=">"):
    global path
    global name

    global customs

    if customs["new_line"] != "":
        newline = customs["new_line"]

    if customs["new_d"] != "":
        new_decision_indicator = customs["new_d"]

    if customs["jump"] != "":
        jump = customs["jump"]
    else:
        jump = None

    if customs["opts"] != "":
        opt_sep = customs["opts"]


    try:
        open(f"{name}.py", "x")
    except FileExistsError:
        label3.config(text="That file already exists. Please change the name and try again.")
        return

    print(newline,"; ", new_decision_indicator,"; ", jump,"; ", option_seperator_entry)



    if path is None or name is None:
        label3.config(text="You're missing some inputs. Please fill them out and try again.")
        return

    file_path = path
    file_name = name

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
                    if opt_sep in line:
                        text_count = 0
                        text_string = ""
                        break_count = 0
                        print(YELLOW,line,RESET)
                        options = line.split(opt_sep)

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
                    elif jump is not None:
                        if line[0] == jump:
                            # gets the ID
                            next_decision = line.replace(jump, "").strip()

                            # prints the line & the fetched ID
                            print(GREEN, line, RESET)
                            print("Next decision: ", next_decision)

                            # assigning stuff
                            current[current_key][current_option][2] = next_decision
                            if current_chance is not None:
                                current[current_key][current_option].append(current_chance)
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

    with open(f"{file_name}.py", "a", encoding="utf-8") as f:
        f.write("from classes import Decision\n")
        for item in current:
            all_decisions += f'"{item}": {item},\n'
            written_line = item + " = Decision(" + str(current[item]) + ")\n"
            f.write(written_line)
        f.write(all_decisions + "}")

    print("Completed")
    end_label.config(text="Compiling Complete")



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
    else:
        path = None


def get_name():
    global name
    n = entry2.get()
    try:
        if n.strip != "" and n.isalnum():
            name = n
            label2.config(text=f"Ok! The file will save as {name}.py")
        else:
            label2.config(text=f"You haven't entered a valid name. The file will save as {name}.py")
    except FileExistsError:
        label2.config(text="That file already exists. Please delete or move it and try again.")
        name = None


def custom():
    if custom_ind.get():
        label4.grid(row=5, column=0, sticky=tk.NE)

        check1.grid(row=6, column=0, sticky=tk.NE)
        check2.grid(row=7, column=0, sticky=tk.NE)
        check3.grid(row=8, column=0, sticky=tk.NE)

        newline.grid(row=10, column=0, sticky=tk.W)

        if var1.get():
            new_decision_entry.grid(row=6, column=1, sticky=tk.W)
        if var2.get():
            jump_entry.grid(row=7, column=1, sticky=tk.W)
        if var3.get():
            option_seperator_entry.grid(row=8, column=1, sticky=tk.W)

        if custom_newline.get():
            newline_enter.grid(row=11, column=1, sticky=tk.W)
            newline_text.grid(row=11, column=0, sticky=tk.NE)
    else:
        label4.grid_forget()

        check1.grid_forget()
        check2.grid_forget()
        check3.grid_forget()

        new_decision_entry.grid_forget()
        jump_entry.grid_forget()
        option_seperator_entry.grid_forget()


def check_new_d():
    if var1.get():
        new_decision_entry.grid(row=6, column=1, sticky=tk.W)
    else:
        new_decision_entry.grid_forget()
        new_decision_entry.delete(0, 'end')

def check_jump():
    if var2.get():
        jump_entry.grid(row=7, column=1, sticky=tk.W)
    else:
        jump_entry.grid_forget()
        jump_entry.delete(0, 'end')

def check_option_sep():
    if var3.get():
        option_seperator_entry.grid(row=8, column=1, sticky=tk.W)
    else:
        option_seperator_entry.grid_forget()
        option_seperator_entry.delete(0, 'end')

def custom_line():
    if custom_newline.get():
        if custom_ind.get():
            newline_enter.grid(row=11, column=1, sticky=tk.W)
            newline_text.grid(row=11, column=0, sticky=tk.NE)
        else:
            newline_enter.grid(row=17, column=1, sticky=tk.W)
            newline_text.grid(row=17, column=0, sticky=tk.NE)
    else:
        newline_enter.grid_forget()
        newline_text.grid_forget()
        newline_enter.delete(0, 'end')


def get_custom():
    global customs

    customs = {
        "new_line": str(newline_enter.get()).strip(),
        "new_d": str(new_decision_entry.get()).strip(),
        "jump": str(jump_entry.get()).strip(),
        "opts": str(option_seperator_entry.get()).strip(),
    }

    stuff=[
        [customs["new_d"], confirm1, "New Decision Indicator", 18],
        [customs["jump"], confirm2, "Next Decision Indicator", 19],
        [customs["opts"], confirm3, "Option Seperator", 20],
        [customs["new_line"], confirm4, "New Line Symbol", 21]
    ]

    for i in stuff:
        if i[0] != "":
            i[1].config(text=f"{i[2]}: {i[0]}")
            i[1].grid(row=i[3], column=0)
        else:
            i[1].grid_forget()

    


# the UI
root = tk.Tk(baseName='Text Adventure Maker')
root.title("Text Adventure Game Maker (Compiler)")
root.geometry("700x500")

container = tk.Frame(root)
container.pack(expand=True)

main_options = tk.Frame(container)
main_options.pack()

file_selector = tk.Frame(main_options)
output_selector = tk.Frame(main_options)

file_label = tk.Label(file_selector, text="File path: ")
file_label.grid(row=0, column=0, sticky=tk.W)
output_label = tk.Label(output_selector, text="Output File Name: ")
output_label.grid(row=0, column=0, sticky=tk.W)

file = tk.Button(file_selector, text="Open File", command=open_file)
entry2 = tk.Entry(output_selector)

file.grid(row=0, column=1)
entry2.grid(row=0, column=1)

button1 = tk.Button(output_selector, text="OK", command=get_name)
button1.grid(row=0, column=2)

file_selector.pack()
label1 = tk.Label(main_options, text="")
label1.pack()
output_selector.pack()
label2 = tk.Label(main_options, text="")
label2.pack()



# custom indicators
custom_options = tk.Frame(container)
custom_options.pack()

custom_ind = tk.IntVar()
check0 = tk.Checkbutton(custom_options, text="I used custom indicators", variable=custom_ind, command=custom)
check0.grid(row=3, column=0, sticky=tk.W)

label4 = tk.Label(custom_options, text="Indicators Customized: ")

var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()

check1 = tk.Checkbutton(custom_options, text="New Decision: ", variable=var1, command=check_new_d)
check2 = tk.Checkbutton(custom_options, text="Next Decision: ", variable=var2, command=check_jump)
check3 = tk.Checkbutton(custom_options, text="Option seperator: ", variable=var3, command=check_option_sep)

new_decision_entry = tk.Entry(custom_options)
jump_entry = tk.Entry(custom_options)
option_seperator_entry = tk.Entry(custom_options)

custom_newline = tk.IntVar()
newline = tk.Checkbutton(custom_options, text="I want a custom symbol for new lines", variable=custom_newline, command=custom_line)
newline.grid(row=4, column=0, sticky=tk.W)

newline_enter = tk.Entry(custom_options)
newline_text = tk.Label(custom_options, text="Custom Symbol: ")

button2 = tk.Button(custom_options, text="Confirm Custom Symbols", command=get_custom)
button2.grid(row=18, column=1)

confirm1 = tk.Label(custom_options, text="")
confirm2 = tk.Label(custom_options, text="")
confirm3 = tk.Label(custom_options, text="")
confirm4 = tk.Label(custom_options, text="")


label3 = tk.Label(main_options, text="")
label3.pack()

end_label = tk.Label(container,text="")
end_label.pack()

button3 = tk.Button(container, text="Start Compiling", width=15, command=process)
button3.pack()

# colors!
all_widgets = [
    root,
    container,
    custom_options,
    main_options,
    file_label,
    output_label,
    file_selector,
    output_selector,
    newline_text,
    newline,
    button1,
    button2,
    button3,
    label1,
    label2,
    label3,
    label4,
    check0,
    check1,
    check2,
    check3,
    confirm1,
    confirm2,
    confirm3,
    confirm4,
    file,
    end_label,
]

fill_options = [
    new_decision_entry,
    jump_entry,
    option_seperator_entry,
    newline_enter,
    entry2
]

small_text = [
    confirm1,
    confirm2,
    confirm3,
    confirm4,
    label1,
    label2
]

colors = {"fg": "ivory1",
          "bg": "ivory4",
          "small": "ivory3"}

root.configure(bg=colors["fg"])
custom_options.configure(bg=colors["fg"])
main_options.configure(bg=colors["fg"])

for i in all_widgets:
    i.configure(bg=colors["fg"])
    if isinstance(i, tk.Label) or isinstance(i, tk.Checkbutton):
        i.configure(fg=colors["bg"])
    if isinstance(i, tk.Button):
        i.configure(highlightbackground=colors["fg"], fg=colors["bg"])

for i in fill_options:
    i.configure(bg=colors["bg"],fg=colors["fg"])
    i.configure(highlightbackground=colors["fg"])

for i in small_text:
    i.configure(fg=colors["small"])

button3.configure(bg=colors["bg"], fg=colors["fg"])
if platform == "darwin":
    button3.configure(fg=colors["bg"])

root.mainloop()