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

FFFF = Decision({'1': ['what were you even doing to cause this??', "You were looking for your friend, right? Atlas, the stupid little artist. They're really smart, but... not the most present. And that... meant you got kidnapped? Oh for Wyrm's sake. You should at least try to get out.", 'EEEE'], '2': ['what in Manku happened?', 'You had been wandering around the city, looking for your friend Atlas... When something hit you over the head. Gods, did you get kidnapped??\n··> You stand up and glare. Wow, this place looks cursed.', '']})
EEEE = Decision({'1': ['look around', "You're trapped in a jar. The glass is thick and hard to break, so you don't know if you'll  be getting out any time soon.\n··> The room you're in is very blue and very bright. The floor is littered with shrunken corpses.", 'A']})
A = Decision({'a1': ['say "well this sucks"', '"well this sucks."\n··> Maybe there\'s something you can do to avoid that fate...', 'B'], 'a2': ['panic', "You start hyperventillating. There's no way you'll meet the same fate as those corpses!", 'B'], 'a3': ["surely there's a way out!", "You tap at the glass. It makes a nice sound. Ding! But that doesn't help you.", 'C']})
B = Decision({'b1': ['is there really no way out?', "You tap at the glass. It makes a nice sound. Ding! But that doesn't help you.", 'C']})
C = Decision({'c1': ['tap again', 'You tap again. This time, glowing white runes appear on the inside of the glass.\n··> Ha!\n··> So maybe you just need to get rid of these runes?', 'D'], 'c2': ['frown at it', '(random text)\n··> You frown at the glass. Stupid glass.\n··> You frown at the glass. Its glass.\n··> You glare at the glass. It glares back.', 'C']})
D = Decision({'d1': ['punch it', 'You punch the glass. It rings, and the runes glow again. \n··> Your fist hurts.', 'E'], 'd2': ['scratch it', '', 'F'], 'd3': ['try to analyze them', "You take a step closer and study the runes carefully.\n··> ...\n··> You have no idea what you're looking at.", 'G']})
E = Decision({'e1': ['punch it harder!', '', ''], 'e2': ["nevermind, let's try something else", '(random text)\n··> You look at the glass for what feels like the hundreth time today.\n··> You look at the glass again.', 'D']})
F = Decision({'f1': ['it works!', 'The runes shimmer and vanish with a scream. Looks like you broke them!', 'I', '0.1'], 'f2': ['nope', 'The runes glow. Nothing happens.', '']})
G = Decision({'g1': ['damn', "You take as much of a step back as you can, and look for places where you could just cut the sequence.\n··> ...\n··> Aha! There's a very line-like line that could be forming a sentence!", 'H']})
H = Decision({'h1': ['scratch across the line', 'The runes shimmer and vanish with a scream. Looks like you broke them!', 'I'], 'h2': ['punch it!!', 'The runes shimmer, but stay. Owie.', 'H']})
I = Decision({'i1': ['punch the glass', 'You punch the glass. It shatters, suprisingly easily.', 'J'], 'i2': ['kick the glass', 'You kick the glass. It shatters, suprisingly easily.', 'J']})
J = Decision({'j1': ['get the heck outta here!', "Yeah... you're out. Time to leave! And never come back! You duck into the shadows and run as fast as you can.", 'K'], 'j2': ['look for your friend', "You slip into the shadows and search for Atlas.\n··> You can't see him anywhere...", 'Q']})
K = Decision({'k1': ['oh gods this is a maze', "Ugh, tunnels. You know there are nicer places to be, but you can't remember...", 'L']})
L = Decision({'l1': ['whatever', 'You keep running.', 'M'], 'l2': ['think harder...', '', 'N'], 'l3': ["you're going to sue whoever designed this", "And they'll regret it!", 'M']})
M = Decision({'m1': ["you're free!", "Finally, you see a door you recognize. It's the other side of the Sanctum's headquarters! The gits, trying to kidnap you!", 'END1', '1.0']})
N = Decision({'n1': ['keep going', 'You wrack your brain for information, but you come up empty. \n··> Resolving to figure this out later, you shut off your thoughts and keep on running.', 'M', '0.4'], 'n2': ['rip', "As you think, your running slows. You've barely noticed, but the warrior chasing you has!", 'O', '0.6']})
O = Decision({'o1': ['shi- crap.', "You really doubt your ability to fight that monster of a being. You make a sharp turn, trying to evade him, but it's too late.\n··> A glowing white dart appears in your periphery before the world vanishes again.", 'CAP'], 'o2': ['RUN HARDER!!', "You speed up as much as you can, but it's too late.\n··> In seconds the warrior catches up to you and a glowing white dart appears in your periphery before the world vanishes again.", 'CAP'], 'o3': ['quick! hide!', 'You roll behind a particularly large desk, hold your breath, and pray.', 'NORMAN']})
NORMAN = Decision({'n1': ['rip2', "The warrior seems to find you immediatley. You try to run again, but it's too late.\n··> A glowing white dart appears in your periphery before the world vanishes again.", 'CAP', '0.5'], 'n2': ['safe', "The warrior runs right past you, taking a turn you'd noticed only seconds ago. You let out your breath and cautiously emerge.", 'P', '0.4'], 'n3': ['norman', 'The warrior seems to find you immediatley. Before you can do anything, he speaks:\n··> "Hey man, I don\'t mean any harm. You\'re looking for the other moth, right?"', 'NO1', '0.1']})
P = Decision({'p1': ['run for it!', "You speed off in your previous direction after making sure there's nobody around. Phew!\n··> You keep running, making sure to not stop again.", 'M']})
NO1 = Decision({'n1': ['"Screw off"', 'The warrior looks offended. The nerve! Like he wasn\'t chasing you three seconds ago?\n··> "Fine," he says. And leaves.\n··> ...\n··> Wait, what?', 'P'], 'n2': ['"Yeah, why?"', 'The warrior looks a bit defeated.\n··> "I never really liked all the kidnappings, y\'know? And since you got out somehow, and I know where that other guy is, maybe we can break \'em out together and ditch the place?"', 'NO2'], 'n3': ['"I was running for my life, dude."', '', 'NORANDO']})
NORANDO = Decision({'1': ['gogo', 'He looks... embarrased? \n··> "Ah, right. I\'ll, uh, let you get back to that."\n··> He... leaves. Straight-up vanishes. Possibly teleports, but that shouldnt be possible.\n··> Time to go, then?', 'P', '0.8'], '2': ['cmonnnn', 'He looks embarrased, but then seems to gain confidence.\n··> "Right. But, well, I was thinking, since you got out somehow, and I know where that other guy is, maybe we can break \'em out together and ditch the place?"\n··> He pauses.\n··> "Not like I liked the literal crime, hah."', 'NO2', '0.2']})
NO2 = Decision({'n1': ['"Let\'s go, then."', 'You walk together to a room not unlike the one you woke up in. Dead, mangled bodies and all. Atlas sits in a jar, looking up blankly.', 'NO3'], 'n2': ['"Really, now? You guys kidnapped me, and now you want me to help with... whatever that is?"', '"Hey! I said I didn\'t like it!" The warrior complains.\n··> "You didn\'t even apologise."\n··> He huffs.\n··> "Whatever, I\'ll just get out of your way."\n··> He does exactly as he says, and... vanishes. Yeah, sure.\n··> You\'d better get going.', 'P']})
NO3 = Decision({'n1': ['"Again? Really?"', 'Atlas seems to hear you, because he yelps and cries "What! No!"\n··> You snort to cover a short laugh, and glare at the runes on this jar.', 'NO4']})
NO4 = Decision({'n1': ['time to find a line again...', 'You stare until you find another line like the one you broke in your jar.\n··> You point it out to Atlas, and tell him to sctatch it out.\n··> When they do, you kick the jar.\n··> "Damn," the warrior says.\n··> "What are you waiting for? Let\'s get out!"\n··> ...You might be a bit high on adrenaline', 'NO5']})
NO5 = Decision({'n1': ['let the warrior lead you out', "You follow the warrior as he takes you and Atlas out of the area.\n··> ...Through the Sanctum's main doors.\n··> Those whiny maggots! They're supposed to be researchers!", 'END2']})
Q = Decision({'q1': ['keep looking', "It's at least an hour before you find any leads. By now, you're tired and slow, and you've found two corpse-rooms with four prisoners.\n··> ...None of which are Atlas.", 'R']})
R = Decision({'r1': ['"I swear, the gods have forsaken me"', "The moment a word leaves your mouth, the hairs on your back stand up. You're in danger.\n··> But you can barely process that before a glowing white dart appears in your periphery and you're lost to the world.", 'CAP']})
CAP = Decision({'c1': ['This is a wip', '', 'CAP2']})
all_decisions = {"FFFF": FFFF,
"EEEE": EEEE,
"A": A,
"B": B,
"C": C,
"D": D,
"E": E,
"F": F,
"G": G,
"H": H,
"I": I,
"J": J,
"K": K,
"L": L,
"M": M,
"N": N,
"O": O,
"NORMAN": NORMAN,
"P": P,
"NO1": NO1,
"NORANDO": NORANDO,
"NO2": NO2,
"NO3": NO3,
"NO4": NO4,
"NO5": NO5,
"Q": Q,
"R": R,
"CAP": CAP,
}
first_option = 'FFFF'
last_option = 'CAP2'
all_decisions[first_option].show()

next = all_decisions[first_option].make()
playing = True
while playing:
    all_decisions[next].show()
    print()
    next = all_decisions[next].make()
    if next == last_option:
        playing = False