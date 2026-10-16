import random


class Decision:

    def __init__(self,options:dict,text_tags:dict={
        "SysPre": "·",
        "SysPost": " > ",
        "Choose": "  I choose··> ",
        "ChooseFail": "          ··> ",
        "Bar": "   · ··>    -    <·· ·   ",
    }, id_all_caps=True):
        # Options should be a dictionary in this format: {index: [choice text, narration text, jump id]}
        # Text tags are here for formatting
        # The dict, if passed, should contain the following keys: "SysPre", "SysPost", "Choose", "ChooseFail", and "Bar"
        
        # Making variables with a scope of the entire class
        self.options = options
        self.numbers = {}
        self.text_tags = text_tags
        self.id_all_caps = id_all_caps

        # Tries a bit to make sure that the values in options are valid
        if type(self.options) != dict:
            raise TypeError("options must be a dictionary")
        if type(text_tags) != dict:
            raise TypeError("text_tags must be a dictionary")
        for key in ["SysPre", "SysPost", "Choose", "ChooseFail", "Bar"]:
            if key not in self.text_tags:
                raise KeyError(f"text_tags must contain the key '{key}'")
        counter = 1
        for index in self.options:
            if type(index) != int and type(index) != str:
                raise TypeError("indexes must be integers or strings")
            if type(self.options[index]) != list:
                raise TypeError("keys should be lists in this format: [choice text, narration text, jump id]")
            
            self.numbers[str(counter)] = index # Adds indexted numbers so the user can input that too. Selectors under show() have no effect on this
            counter += 1


    # A snippet so that the object can be printed in a more readable format
    def __repr__(self):
        return f"Decision({self.options})"


    def show(self,selectors="All",newline=True):
        # Selectors can be one of the following: "All", "ID", "Index"
        # Selectors defaults to "All" and so do any invalid inputs
        # newline adds a line before options are displayed. wow what a suprise

        # initiates counter & adds a new line if that's True
        if newline:
            print()

        counter = 1

        # Displaying options
        for option in self.options:
            if selectors.lower() == "ID":
                print(f"{self.text_tags['SysPre']}{option}{self.text_tags['SysPost']}" +
                    self.options[option][0])
            elif selectors.lower() == "Index":
                print(f"{self.text_tags['SysPre']}{counter}{self.text_tags['SysPost']}" +
                    self.options[option][0])
            else:
                print(f"{self.text_tags['SysPre']}{option}/{counter}{self.text_tags['SysPost']}" +
                    self.options[option][0])
            counter += 1


    def make(self):
        # in hindsight, 'make' was a terrible name
        # id_all_caps is true because mine are, in fact, all caps

        # Gets first choice & initializes result to be returned later
        # Does the random thing if options have a 4th value (weights)
        manual = False
        try:
            chances = []
            for key in self.options:
                chances.append(self.options[key][3])
            
            new = random.choices(list(self.options.keys()), weights=chances, k=1)
            result = self.options[new[0]]
        except IndexError:
            manual = True

        # Does the normal thing if manual is true
        if manual:
            choice = input(self.text_tags["Choose"])
            result = ""

            # Validation for the choice
            valid = False
            while not valid:
                if self.id_all_caps:
                    choice = choice.upper()
                try:

                    # Inner try/except for if the user inputs a number
                    try:
                        choice = self.numbers[choice]
                        print("Choice: "+choice)
                    except KeyError:
                        pass

                    # Sets result if choice is valid
                    result = self.options[choice]
                    valid = True

                # Except says "nope" if the choice is invalid
                except (IndexError,KeyError):
                    print("Um, you can't do that. Try again?")
                    choice = input(self.text_tags["ChooseFail"])

        # Displays the narration text and returns the jump id
        print("\n"+self.text_tags["Bar"]+"\n")
        print(self.text_tags["SysPre"] + self.text_tags["SysPost"] + result[1])
        return result[2]

if __name__ == '__main__':
    # Initiaizes every decision to make
    new = Decision({"A": ["choose a","A!!", "B"]})
    second = Decision({"A": ["choose a", "No!!!", "A"],
                       "B": ["choose b", "yea!", "C"]
                       })
    third = Decision({"A": ["choose a", "A!", "D", 0.5],
                           "B": ["choose b", "B!", "D", 0.5]
                           })
    
    # Dict of all options with IDs
    all_options = {
        "A": new,
        "B": second,
        "C": third
    }

    # Game loop
    all_options["A"].show()
    next = all_options["A"].make()
    playing = True
    while playing:
        all_options[next].show()
        print()
        next = all_options[next].make()
        if next == "D":
            playing = False
    