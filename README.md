# Text Adventure Maker
Program that compiles a formatted text file into a python file with dictionaries to be used with the code in the `folktale-palm` repo. Intended to make writing easier.

## How to Use
First, you need Python installed. Er, you can get it from the [official site](https://www.python.org/)?

Prepare your script file in `.txt` format like this:

```
#Decision Name
Option Name > Selection Text
Narration text if the option is selected
This can go multiple lines
[name of next decision if this option is selected]

etc...
```

Then, run `main.py` and choose your script file. Add a name for the output file (or skip to keep the file name of your script), select "OK", and then click "Start Compiling".

The text "Compiling Complete" will appear when it's done. This usually takes under a second.

You can now find the output file in the same folder as `main.py`!

**If you're using the standalone build:**

Drag `classes.py` and your output file into a folder for your project. Now, you'll need to do some coding.

Make a file called `main.py` in your project folder (or call it anything else, just remember to run this file when playing your game). 

Now go into it, and create a game loop (refer to [the README](https://www.python.org/) of `folktale-palm` as to how). 

Now you're set! You can add whatever other features you want, of course.

**If you're using the automatic build:**

Run the output file, and play your game!

## Using Custom Indicators
Instead of using `#`,`>`, and `[]`, you can use custom symbols or phrases to indicate different parts of the script to the program. Currently, prefix-suffix systems like `[text]` aren't supported for customization, but you can still add prefix indicators.

To use one, simply do so in your script and check "I used custom indicators" while compiling.

Once you've checked the box, you'll see a list of available custom indicators and you can check & input the ones you used.

## How Does This Work?
Mainly with Python file handling. You can write to `.py` files like any other text file, and this compiler takes great advantage of that. The indicators are not *that* strict but it's still basically Walmart Ren'Py. 
The UI is made with Tkinter because Tkinter is a built-in library, and there is a (G)UI because I don't want to deal with consle stuff and I'm sure others don't usually do either.
