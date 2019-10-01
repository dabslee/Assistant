import sprites
import datetime
import activities

# ^ = pause
# %@ = replace with token

def firstrun(interface):

    extrabuttons = sprites.ExtraButtons()

    interface.say("Hey!^ I’m %@, your digital %@.", [interface.assistant.name, interface.perma["rina_title"]])
    interface.say("I’m here to help you achieve your goals!", costume="happy")
    interface.say("Whatever they may be, I’ll be there by your side, supporting you.", costume="happy")
    interface.say("First, though, let me get some info about you.")
    interface.perma["user_fname"] = interface.input("First name?")
    interface.perma["user_lname"] = interface.input("Last name?")
    interface.perma["user_gender"] = interface.buttons(text="Gender?", labels=["Male","Female","Other"])
    interface.save_perma()
    interface.say("Thanks, %@. I really look forward to our time together!", [interface.perma["user_moniker"]], costume="happy")

    interface.say("Before we get started, I want you to promise me something.")
    interface.say("As I mentioned before, my mission is to help you become the best 'you' that you can be.")
    interface.say("But, obviously, I can’t do this alone.")
    interface.say("So, I want you to promise me this.")
    interface.buttons(text="Promise to also commit to making yourself the best 'you' you can be.", labels=["Commit"], costume="winking")
    interface.say("Thanks so much for doing that, %@.", [interface.perma["user_moniker"]], costume="happy")

    interface.say("So, tell me about your goals, %@!", [interface.perma["user_moniker"]])
    interface.say("Who is the ideal you?^ Who do you want to be?^ What do you want to do with your life?")
    interface.say("What is your purpose in living?")
    interface.say("Being artificial, my purpose is clear and certain:^ to support you in achieving your dreams.", costume="happy")
    interface.say("However, for humans like you, it’s both your gift^ and your burden^ to have to decide your own purpose.", costume="serious")
    interface.say("Think about it for a moment. What is the purpose of %@ %@?", [interface.perma["user_fname"], interface.perma["user_lname"]], costume="serious")
    interface.say("...")
    interface.say("It’s a big question, of course. You might not be able to answer it now.", costume="winking")
    interface.say("Let me know when you can answer it, though! Just tell me you’re ready by pressing the PURPOSE button, which will be enabled once I'm done talking.", costume="happy")
    interface.say("Anyway, for now, let’s focus on setting up your little goals.")

    interface.activities_panel()
    interface.say("Alright, %@!", [interface.perma["user_moniker"]])

    interface.activity_setup(interface.get_selected_activities())

    interface.say("...", costume="serious")
    interface.say("By the way, I’d like to ask you a favor.")
    interface.say("I would love it if you could check in with me at least twice a day:^ Once in the morning and once before you go to bed.", costume="happy")
    interface.say("Spending even more time would be wonderful, but those two times are especially important to me.", costume="happy")
    interface.say("I guess I just want to be the first and last one you see every day, ehehe.", costume="blushing")
    interface.buttons("Please promise me.", ["I promise."], costume="blushing")
    if (interface.buttons("In that case, can I enable notifications?", ["Yes","No"]) == "Yes"):
        interface.perma["notifications_enabled"] = True
        interface.issuenotification("Thanks a ton!")
    else:
        interface.say("Aw...", costume="sad")
        interface.say("Well, as long as you promise!", costume="happy")
    interface.say("Anyway, that’s all I have to say!", costume="happy")
    interface.say("If you want to talk with me more, then just press the TALK WITH RINA button, which will be enabled shortly.")
    interface.say("Otherwise, I’ll just stay here quietly and try not to distract you.")

    interface.perma["run #"] += 1
    interface.save_perma()

    interface.buttonloop(extrabuttons)

def regrun(interface):

    extrabuttons = sprites.ExtraButtons()

    if (datetime.datetime.now().time() < datetime.time(6)):
        interface.say("Good morning, %@!", [interface.perma["user_moniker"]])
        interface.say("Wow, you're up pretty early, aren't you?", [interface.perma["user_moniker"]], costume="happy")
    elif (datetime.datetime.now().time() < datetime.time(12)):
        interface.say("Good morning, %@!", [interface.perma["user_moniker"]])
    elif (datetime.datetime.now().time() < datetime.time(12+6)):
        interface.say("Good afternoon, %@!", [interface.perma["user_moniker"]])
    else:
        interface.say("Good evening, %@!", [interface.perma["user_moniker"]])
    activities.FeelingCheck.session(interface)
    interface.say("So, let's get started with our activities today.")
    interface.activity_session(interface.get_selected_activities())
    interface.say("Well, that's it for now!", costume="happy")
    interface.say("As always, just press the TALK WITH RINA button if you want to talk more.")
    interface.say("Now, don't let me distract you too much!", costume="winking")
    if (datetime.datetime.now().time() < datetime.time(12)):
        interface.say("Have a productive day, %@!", [interface.perma["user_moniker"]])
    elif (datetime.datetime.now().time() < datetime.time(12+9)):
        interface.say("Have a productive rest of your day, %@!", [interface.perma["user_moniker"]])
    else:
        interface.say("Have a productive rest of your day, %@, and don't stay up too long!", [interface.perma["user_moniker"]])

    interface.buttonloop(extrabuttons)

def spritesetup():
    interface = sprites.Interface(
        sprites.Background(),
        sprites.Assistant(),
        sprites.Speechbox(),
        )
    return interface

def runscript(interface):

    last_run = datetime.datetime.strptime(interface.perma["last_run"],"%m/%d/%Y")
    interface.perma["affection"] -= (datetime.datetime.now().date() - last_run.date()).days
    interface.perma["last_run"] = datetime.datetime.strftime(datetime.datetime.now(),"%m/%d/%Y")
    interface.save_perma()

    print()
    if (interface.perma["run #"] > 0):
        regrun(interface)
    else:
        firstrun(interface)