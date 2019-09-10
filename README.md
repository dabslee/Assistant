![Rina logo](https://raw.githubusercontent.com/dabslee/Assistant/master/assets/logo.png)
***
## Running the Program
First, make sure you have Python 3.7 installed. If you don't, you can install [here](python.org/downloads).
Before you run the program, you're going to have to install a couple python libraries. If you have pip, just call `pip install -r requirements.txt` on your command line to install everything you need.
To run the program, run *game.py* using Python 3.7 (32 bit).

## Adding to the Conversational Script
To add to the prompts that Rina can respond to, open up *chatbox.txt*. In the text file, add entries between the `%start%` and the `%end%` lines following the format below:
```
%entry start%
triggerphrase1|triggerphrase2|triggerphrase3
dialogueline1
dialogueline2
dialogueline3
%entry end%
```

## Adding New Activities
To add new activities (things Rina can do, essentially), open up *activities.py*. Then, add a new class to the file following the template below:
```python
class ExampleActivity(Activity):
    verbose = ""
    @classmethod
    def setup(cls, interface):
        pass
    @classmethod
    def session(cls, interface):
        pass
    @classmethod
    def trigger_init(cls, interface):
        pass
    @classmethod
    def triggered(cls, interface):
        pass
```
Assign a `verbose` name to the class, which will be used to identify it in various locations in the program. If you want to make the activity one of those you can sign up for during the first run of the game, then add its verbose name to the `activities` list at the top of the file.

The `setup` method is executed during the game's first run and is used to get information from the user that is important for when the activity will run later. The `session` method is executed every time the game runs after the first run. The `trigger_init` is executed once per run as well, but it runs after all the `session` methods for all the activities have already been run. The `triggered` method runs when various triggers in the game (e.g. time of day) occur.

Here are some of the commands that you can put in each of these methods:
* **interface.say(*text* \[,*iterable* \[,*costume*]])**: Makes Rina say in the speechbox a string *text*. You can add pauses in Rina's speech by adding the carrot character `^` in this string variable. You can also add in `%@`s in the *text* variable, which will be substituted by values you put in the `tokens` list argument (think string formatting--I don't know why I reinvented the wheel on this one). The *costume* string variable is the name of the image/expression you want Rina to assume while saying the `text`.
* **interface.input(*text* \[,*default*, \[,*costume*]]):** Prompts the user for an input with Rina saying string variable `text`. Returns the input as a string. String variable `default` is the default value the user input box will hold. The *costume* string variable is the name of the image/expression you want Rina to assume while saying the `text`.
* **interface.buttons(*text*, *iterable*, \[,*costume*]):** Prompts the user to choose from various buttons with Rina saying string variable `text` in the meantime. The buttons available are given in the `iterable` variable as strings. Returns the label of the button selected by the user. The *costume* string variable is the name of the image/expression you want Rina to assume while saying the `text
