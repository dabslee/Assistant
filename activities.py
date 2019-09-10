import sprites
import datetime
import os
import csv
import convo

# list of registered activities
activities = ["Sleeping",
            "School",
            "Work",
            #"Homework",
            #"Studying",
            #"Diet",
            #"Reading",
            #"Writing",
            #"Dancing",
            #"Exercise",
            #"Cooking",
            #"Drawing",
            #"Volunteering",
            #"Gardening",
            #"Playing an Instrument",
            #"Cleaning",
            #"Website regulation",
            ]

class Activity():
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

class FeelingCheck(Activity):

    verbose = "Feeling Check"

    @classmethod
    def session(cls, interface):
        interface.input("How are you feeling today?")
        interface.say("Thanks for letting me know!")

class TalkWithRina(Activity):
    
    verbose = "Talk with Rina"

    @classmethod
    def setup(cls, interface):
        pass

    @classmethod
    def session(cls, interface):
        interface.say("I'm so glad you chose to talk to me!")
        interface.say("Type in whatever you want to say to me, or type 'GOODBYE' when you're done.")
        prompt = ""
        while (prompt != "GOODBYE"):
            prompt = interface.input("What do you want to talk about?")
            for line in convo.reply(prompt):
                interface.say(line)

class Purpose(Activity):
    
    verbose = "Review your Purpose"

    @classmethod
    def setup(cls, interface):
        pass

    @classmethod
    def session(cls, interface):
        if (os.path.exists("permas/purpose.txt")):
            sc = open("permas/purpose.txt", 'r')
            interface.say("Your purpose is: %@", [sc.readline().strip()])
            sc.close()
            if (interface.buttons("Would you like to revise your purpose?", ["Yes", "No"]) == "Yes"):
                pw = open("permas/purpose.txt", 'w')
                pw.write(interface.input("Your purpose is: "))
                pw.close()
                interface.say("Thanks! I'll keep it in mind.")
                interface.say("If you ever want to review it, just press on the PURPOSE button again!")
            else:
                interface.say("Alright! I hope you're feeling inspired!")
                interface.say("If you ever want to review it, just press on the PURPOSE button again!")
        else:
            interface.say("Glad to see you've made up your mind.")
            interface.say("I'm excited to know your purpose!")
            pw = open("permas/purpose.txt", 'w')
            pw.write(interface.input("Your purpose is: "))
            pw.close()
            interface.say("Thanks! I'll keep it in mind.")
            interface.say("If you ever want to review it, just press on the PURPOSE button again!")

class Sleeping(Activity):

    verbose = "Sleeping"

    @classmethod
    def setup(cls, interface):
        interface.say("You mentioned you wanted to work on improving your sleeping.")

        hour_goal = float(interface.input("So, how much sleep do you want to get per night?", default="8.0"))
        wake_time = datetime.datetime.strptime(interface.input("And when do you want to get up by?", default="07:00 AM"), "%I:%M %p")
        
        pw = open("permas/"+cls.__name__+".txt", 'w')
        pw.write(str(hour_goal)+"\n")
        pw.write(datetime.datetime.strftime(wake_time, "%I:%M %p")+"\n")
        pw.close()

        interface.say("Thank you, %@!", [interface.perma["user_moniker"]])
        bed_time = wake_time - datetime.timedelta(hours=hour_goal)
        
        if (datetime.datetime.now().time() < bed_time.time()):
            interface.say("Make sure to sleep by %@ tonight, and check in with me tomorrow morning!", [datetime.datetime.strftime(bed_time, "%I:%M %p")])
        else:
            interface.say("Oh! To get the right amount of sleep, you should have slept at %@.", [datetime.datetime.strftime(bed_time, "%I:%M %p")])
            interface.say("Make sure to sleep as soon as you can, and check in with me tomorrow morning!")

    @classmethod
    def session(cls, interface):

        sc = open("permas/"+cls.__name__+".txt", 'r')
        hour_goal = float(sc.readline().strip())
        wake_time = datetime.datetime.strptime(sc.readline().strip(), "%I:%M %p")
        bed_time = wake_time - datetime.timedelta(hours=hour_goal)
        sc.close()

        interface.say("You mentioned that one of the things you wanted to work on was your sleeping habits.")

        already = False
        sc = open("permas/sleeping.csv", 'r')
        csvreader = csv.reader(sc, delimiter=',', quotechar='"')

        for row in csvreader:
            if len(row)>0:
                if row[0]==datetime.datetime.strftime(datetime.datetime.now(), "%m/%d/%Y"):
                    already = True
        sc.close()

        if (not already):
            interface.say("I hope you had a nice sleep last night.")

            pw = open("permas/sleeping.csv", 'a')
            csvwriter = csv.writer(pw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            row = []

            row.append(datetime.datetime.strftime(datetime.datetime.now(), "%m/%d/%Y"))
            row.append(interface.buttons("Do you feel well-rested today?", ["Yes", "Somewhat", "No"]))
            row.append(float(interface.input("From 1 to 10, how would you rate last night's sleep?")))
            row.append(interface.input("What time did you sleep last night?", default=datetime.datetime.strftime(bed_time, "%I:%M %p")))
            row.append(interface.input("When did you wake up this morning?", default=datetime.datetime.strftime(wake_time, "%I:%M %p")))
            row.append(interface.buttons("Did you wake up at all during the middle of the night?", ["Yes","No"]))

            csvwriter.writerow(row)
            pw.close()

            interface.say("Thanks for telling me all this. It'll help me help you with improving your sleeping habits.")
        else:
            interface.say("You've already done the entry for your sleeping goals today, so we'll skip it now.")

        if (interface.buttons("Would you like to view some metrics about your sleep?", ["Yes","No"]) == "Yes"):
            interface.say("Great!")

            sc = open("permas/sleeping.csv", 'r')
            csvreader = csv.reader(sc, delimiter=',', quotechar='"')

            no_entries = 0
            rested_percents = [0,0,0]
            avg_rating = 0
            avg_sleep_time = 0
            avg_wake_time = 0
            avg_sleep_dur = 0
            mid_wake_percent = 0

            for row in csvreader:
                if len(row)>0:
                    no_entries += 1
                    if (row[1] == "Yes"):
                        rested_percents[0] += 1
                    elif (row[1] == "Somewhat"):
                        rested_percents[1] += 1
                    else:
                        rested_percents[2] += 1
                    avg_rating += float(row[2])
                    avg_sleep_time += float(row[3].split(" ")[0].split(":")[0]) + float(row[3].split(" ")[0].split(":")[1])/60 + (12 if row[3].split(" ")[1]=="PM" else 0)
                    avg_wake_time += float(row[4].split(" ")[0].split(":")[0]) + float(row[4].split(" ")[0].split(":")[1])/60 + (12 if row[3].split(" ")[1]=="PM" else 0)
                    if (row[5] == "Yes"):
                        mid_wake_percent += 1

            if (no_entries > 0):
                rested_percents = [rested_percents[0]/no_entries, rested_percents[1]/no_entries, rested_percents[2]/no_entries]
                avg_rating /= no_entries
                avg_sleep_dur = (avg_wake_time-avg_sleep_time) if (avg_sleep_time<avg_wake_time) else (24-avg_sleep_time+avg_wake_time)
                avg_sleep_time = datetime.datetime(2000, 1, 1, hour=0)+datetime.timedelta(hours=avg_sleep_time/no_entries)
                avg_wake_time = datetime.datetime(2000, 1, 1, hour=0)+datetime.timedelta(hours=avg_wake_time/no_entries)
                mid_wake_percent /= no_entries

            sc.close()

            if (no_entries > 0):
                interface.say("You've logged %@ entries total.", [no_entries])
                interface.say("You were well-rested %@% of the time, somewhat well-rested %@% of the time, and were not well-rested %@% of the time.", [rested_percents[0]*100, rested_percents[1]*100, rested_percents[2]*100])
                interface.say("Your average sleep rating was %@ out of 10.", [avg_rating])
                interface.say("Your average bed time was %@.", [datetime.datetime.strftime(avg_sleep_time,"%I:%M %p")])
                interface.say("Your average wake-up time was %@.", [datetime.datetime.strftime(avg_wake_time,"%I:%M %p")])
                interface.say("Your average sleep duration was %@ hours.", [avg_sleep_dur])
                interface.say("You woke up in the middle of the night %@% of the time.", [mid_wake_percent*100])
            else:
                interface.say("It seems like there aren't any entries.")
        else:
            interface.say("Alright, then.")

    @classmethod
    def trigger_init(cls, interface):
        
        interface.session_variables["bed_alarmed?"] = False

    @classmethod
    def triggered(cls, interface):
        
        sc = open("permas/"+cls.__name__+".txt", 'r')
        hour_goal = float(sc.readline().strip())
        wake_time = datetime.datetime.strptime(sc.readline().strip(), "%I:%M %p")
        bed_time = wake_time - datetime.timedelta(hours=hour_goal)
        sc.close()

        if (interface.session_variables["bed_alarmed?"]):
            return False

        if ((bed_time.time() < wake_time.time()
            and datetime.datetime.now().time() > bed_time.time()
            and datetime.datetime.now().time() < wake_time.time())
            or (bed_time.time() > wake_time.time()
            and ((datetime.datetime.now().time() > bed_time.time() and datetime.datetime.now().time() < datetime.time(23,59))
                 or (datetime.datetime.now().time() > datetime.time(0) and datetime.datetime.now().time() < wake_time.time())))):
            interface.session_variables["bed_alarmed?"] = True
            interface.issuenotification("Time for bed!")

        return True

class School(Activity):
    verbose = "School"

    @classmethod
    def setup(cls, interface):
        interface.say("You mentioned that you go to school.")
        start_time = interface.input("What time do you leave to go?", default="08:00 AM")
        end_time = interface.input("What time do you come back?", default="03:00 PM")
        interface.say("Thanks for letting me know!", costume="happy")
    
        pw = open("permas/"+cls.__name__+".txt", 'w')
        pw.write(str(start_time)+"\n")
        pw.write(str(end_time)+"\n")
        pw.close()

    @classmethod
    def session(cls, interface):
        pass
    
    @classmethod
    def trigger_init(cls, interface):
        interface.session_variables["school_check"] = False
    
    @classmethod
    def triggered(cls, interface):
        sc = open("permas/"+cls.__name__+".txt", 'r')
        start_time = datetime.datetime.strptime(sc.readline().strip(), "%I:%M %p")
        end_time = datetime.datetime.strptime(sc.readline().strip(), "%I:%M %p")
        sc.close()

        if (not interface.session_variables["school_check"] and datetime.datetime.now().time() > end_time.time()):
            interface.session_variables["school_check"] = True
            schoolmood = interface.buttons("By the way, how was school today?", ["Great","Good","Okay","Bad","Terrible"])
            if (schoolmood == "Great"):
                interface.say("That's wonderful!", costume="happy")
                interface.say("Keep it up!", costume="happy")
            elif (schoolmood == "Good"):
                interface.say("I'm glad.", costume="happy")
                interface.say("Keep up the good work!")
            elif (schoolmood == "Okay"):
                interface.say("Alright. Remember, school is very important!")
                interface.say("I hope you have fun there.")
            elif (schoolmood == "Bad"):
                interface.say("Hey, that's too bad.", costume="serious")
                interface.say("Remember that school is very important, though!")
                interface.say("No matter what, never give up!")
            elif (schoolmood == "Terrible"):
                interface.input("Why was it so bad?", costume="serious")
                interface.say("Hey, I care about you.", costume="sad")
                interface.say("But there's only so much I can really do for you...", costume="serious")
                interface.say("If it keeps being so bad, try talking to someone.^ Maybe a teacher or a friend?^ Or your parents?", costume="serious")
                interface.say("Anyway, I hope things get better.", costume="serious")
            return True
        else:
            return False

class Work(Activity):
    verbose = "Work"

    @classmethod
    def setup(cls, interface):
        interface.say("You mentioned that you go to work.")
        start_time = interface.input("What time do you leave to go?", default="09:00 AM")
        end_time = interface.input("What time do you come back?", default="05:00 PM")
        interface.say("Thanks for letting me know!", costume="happy")
    
        pw = open("permas/"+cls.__name__+".txt", 'w')
        pw.write(str(start_time)+"\n")
        pw.write(str(end_time)+"\n")
        pw.close()

    @classmethod
    def session(cls, interface):
        pass
    
    @classmethod
    def trigger_init(cls, interface):
        interface.session_variables["work_check"] = False
    
    @classmethod
    def triggered(cls, interface):
        sc = open("permas/"+cls.__name__+".txt", 'r')
        start_time = datetime.datetime.strptime(sc.readline().strip(), "%I:%M %p")
        end_time = datetime.datetime.strptime(sc.readline().strip(), "%I:%M %p")
        sc.close()

        if (not interface.session_variables["work_check"] and datetime.datetime.now().time() > end_time.time()):
            interface.session_variables["work_check"] = True
            schoolmood = interface.buttons("By the way, how was work today?", ["Great","Good","Okay","Bad","Terrible"])
            if (schoolmood == "Great"):
                interface.say("That's wonderful!", costume="happy")
                interface.say("I'm glad you're enjoying your job.", costume="happy")
            elif (schoolmood == "Good"):
                interface.say("I'm glad.", costume="happy")
                interface.say("Keep up the good work!")
            elif (schoolmood == "Okay"):
                interface.say("Alright. Well, it can't always be fun.", costume="serious")
                interface.say("I hope you have fun there.")
            elif (schoolmood == "Bad"):
                interface.say("Hey, that's too bad.", costume="serious")
                interface.say("Work can definitely be hard.", costume="serious")
            elif (schoolmood == "Terrible"):
                interface.input("Why was it so bad?", costume="serious")
                interface.say("Hey, I care about you.", costume="sad")
                interface.say("But there's only so much I can really do for you...", costume="serious")
                interface.say("If it keeps being so bad, try talking to someone.^ Maybe a friend?^ Or a therapist?", costume="serious")
                interface.say("If you really don't enjoy your job, you could consider getting a new one...", costume="serious")
                interface.say("Though, of course, that's easier said than done.", costume="serious")
                interface.say("Anyway, I hope things get better.", costume="serious")
            return True
        else:
            return False