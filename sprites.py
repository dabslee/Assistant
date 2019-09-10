import threading
import math
import time
import random
import os
import weakref
import inspect
import datetime

import pygame
import win10toast

import activities

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

class Sprite():
    _instances = list()
    def __init__(self):
        Sprite._instances.append(self)
    def event_update(self, event):
        pass
    def continuous_update(self):
        pass
    def render(self, screen):
        pass

    @classmethod
    def getinstances(cls):
        return cls._instances

    def delete(self):
        Sprite._instances.remove(self)

# All sprites should have the following methods:
#  __init__(self)
#  event_update(self, event)
#  continuous_update(self)
#  render(self, screen)

class Background(Sprite):
    # Template
    def __init__(self):
        Sprite.__init__(self)
    def event_update(self, event):
        pass
    def continuous_update(self):
        pass
    def render(self, screen):
        screen.blit(get_image("assets/background.png"), (0,0))
        t = pygame.time.get_ticks()//20
        surface = pygame.Surface((screen.get_width(),screen.get_height()), pygame.SRCALPHA)
        for x in range(-screen.get_height(), screen.get_width(), 200):
            for y in range(t%100-screen.get_height(), screen.get_height(), 100):
                pygame.draw.ellipse(surface, (186,223,243,75), (x+y, y, 90, 90))
        screen.blit(surface, (0,0))
        screen.blit(pygame.transform.rotozoom(get_image("assets/logo.png"), 0, 0.3), (3,3))

class Assistant(Sprite):
    # Template
    def __init__(self):
        Sprite.__init__(self)
        self.costume = "assets/neutral.png"
    def event_update(self, event):
        pass
    def continuous_update(self):
        pass
    def render(self, screen):
        start_x = 280
        start_y = 50
        thickness = 14
        screen.blit(get_image("assets/avatarcircle.png"), (start_x,start_y))
        #pygame.draw.ellipse(screen, (39,143,200), (start_x, start_y, screen.get_width()-2*start_x, screen.get_width()-2*start_x))
        screen.blit(pygame.transform.scale(get_image(self.costume),(screen.get_width()-2*start_x-thickness, screen.get_width()-2*start_x-thickness)),
                    (start_x+thickness/2, start_y+thickness/2))

class Speechbox(Sprite):
    # Template
    def __init__(self):
        Sprite.__init__(self)
        self.message = ""
        self.spacebardown = False
        self.textdelay = 0.01
    def event_update(self, event):
        pass
    def continuous_update(self):
        keys = pygame.key.get_pressed()
        self.spacebardown = keys[pygame.K_SPACE]
    def render(self, screen):

        maxchars = 68

        lines = []
        words = self.message.split(" ")
        line = ""
        for word in words:
            if (len(line) + len(word) < maxchars):
                line += " "+word
            else:
                lines.append(line)
                line = " "+word
        lines.append(line)

        start_x = 90
        start_y = 370
        #pygame.draw.rect(screen,(200,230,255),(start_x, start_y, screen.get_width()-2*start_x, 70))
        speechboximage = get_image("assets/speechbox.png")
        screen.blit(speechboximage, (screen.get_width()/2-speechboximage.get_width()/2,start_y))
        myfont = pygame.font.SysFont("consolas", 16, bold=False, italic=True)
        
        linenos = 0
        for line in lines:
            textsurface = myfont.render(line, False, (20,40,100))
            screen.blit(textsurface,(start_x+5,start_y+7+linenos*20))
            linenos += 1

class Interface(Sprite):
    permafilepath = "permas/perma.txt"
    session_variables = {}

    # Template
    def __init__(self, background, assistant, speechbox):
        Sprite.__init__(self)

        self.background = background
        self.assistant = assistant
        self.speechbox = speechbox

        self.perma = {
            "run #":0,
            "affection":0,
            "rina_title":"Blank",
            "rina_moniker":"Blank",
            "user_fname":"Blank",
            "user_lname":"Blank",
            "user_age":0,
            "user_gender":"Blank",
            "user_moniker":"Blank",
            "notifications_enabled":"False",
            "last_run":datetime.datetime.strftime(datetime.datetime.now(),"%m/%d/%Y"),}

        if (os.path.exists(Interface.permafilepath)):
            self.read_perma()

        self.save_perma()

    def event_update(self, event):
        pass
    def continuous_update(self):
        self.perma["affection"] += 0.001
        self.save_perma()
    def render(self, screen):
        pass

    # Extras
    def read_perma(self):
        sc = open(Interface.permafilepath, 'r')
        for line in sc:
            self.perma[line.strip().split(":")[0]] = line.strip().split(":")[1]
        
        self.perma["affection"] = float(self.perma["affection"])
        self.perma["user_age"] = int(self.perma["user_age"])
        self.perma["run #"] = int(self.perma["run #"])
        
        sc.close()

    def save_perma(self):

        if (self.perma["affection"] < 216*5):
            self.perma["rina_title"] = "supporter"
            self.perma["rina_moniker"] = "Miss Rina"
            if (self.perma["user_gender"] == "Male"):
                self.perma["user_moniker"] = "Sir"
            elif (self.perma["user_gender"] == "Female"):
                self.perma["user_moniker"] = "Ma'am"
            else:
                self.perma["user_moniker"] = "Mx. " + self.perma["user_lname"]
        elif (perma["affection"] < 216*14):
            self.perma["rina_title"] = "friend"
            self.perma["rina_moniker"] = "Rina"
            if (self.perma["user_gender"] == "Male"):
                self.perma["user_moniker"] = "Mr. " + self.perma["user_lname"]
            elif (self.perma["user_gender"] == "Female"):
                self.perma["user_moniker"] = "Ms. " + self.perma["user_lname"]
            else:
                self.perma["user_moniker"] = "Mx. " + self.perma["user_lname"]

        pw = open(Interface.permafilepath, 'w')
        for key, value in self.perma.items():
            pw.write(key+":"+str(value)+"\n")
        pw.close()

    def say(self, text, tokens=[], costume="neutral"):

        costumepath = "assets/rina/"
        self.assistant.costume = costumepath + costume + ".png"

        text_array = text.split("%@")
        output = ""
        for piece in text_array:
            output += piece
            if (len(tokens) > 0):
                output += str(tokens.pop(0))

        self.speechbox.message = ""
        for c in output:
            if (c == '^'):
                while (not self.speechbox.spacebardown):
                    time.sleep(self.speechbox.textdelay)
                while (self.speechbox.spacebardown):
                    time.sleep(self.speechbox.textdelay)
            else:
                self.speechbox.message += c
                time.sleep(self.speechbox.textdelay)

        while (not self.speechbox.spacebardown):
            time.sleep(self.speechbox.textdelay)
        while (self.speechbox.spacebardown):
            time.sleep(self.speechbox.textdelay)

    def input(self, text, default="", costume="neutral"):

        costumepath = "assets/rina/"
        self.assistant.costume = costumepath + costume + ".png"
        
        self.speechbox.message = text

        textbox = InputBox((110,413),(630,20), default)
        while (not textbox.submitted):
            time.sleep(0.005)
        output = textbox.text
        textbox.delete()

        return output

    def buttons(self, text, labels, costume="neutral"):

        costumepath = "assets/rina/"
        self.assistant.costume = costumepath + costume + ".png"

        self.speechbox.message = text

        labels_buttons = {}
        xval = 110
        for label in labels:
            labels_buttons[label] = Button(label, (xval,413), (120,20), (39,136,200), (255,255,255))
            xval += 140

        while True:
            for label in labels:
                if (labels_buttons[label].clicked):
                    for x in labels:
                        labels_buttons[x].delete()
                    return label
            time.sleep(0.05)

    def activities_panel(self):
        self.speechbox.message = "Select the activities you would like to work on. Press enter when you're done."
        panel = ActivityPanel()

        while (not panel.submitted):
            time.sleep(0.01)

        selected_activities = []
        for key, value in panel.selected.items():
            if (value):
                selected_activities.append(key)
        panel.delete()

        pw = open("permas/selected_activities.txt",'w')
        for activity in selected_activities:
            pw.write(activity+"\n")
        pw.close()

    def get_selected_activities(self):
        selected_activities = []
        
        sc = open("permas/selected_activities.txt",'r')
        for line in sc:
            selected_activities.append(line.strip())
        sc.close()
        
        return selected_activities

    def activity_setup(self, activities_list):
        for name, obj in inspect.getmembers(activities):
            if inspect.isclass(obj) and obj.verbose in activities_list:
                obj.setup(interface=self)
                self.say("...")

    def activity_session(self, activities_list):
        for name, obj in inspect.getmembers(activities):
            if inspect.isclass(obj) and obj.verbose in activities_list:
                obj.session(interface=self)
        self.say("...")

    def buttonloop(self, extrabuttons):

        for name, obj in inspect.getmembers(activities):
            if inspect.isclass(obj) and obj.verbose in self.get_selected_activities():
                obj.trigger_init(interface=self)

        while True:
            extrabuttons.enabled = True

            for name, obj in inspect.getmembers(activities):
                if inspect.isclass(obj) and obj.verbose in self.get_selected_activities():
                    obj.triggered(interface=self)

            if (extrabuttons.buttons_clicked["Purpose"]):
                extrabuttons.enabled = False
                activities.Purpose.session(self)
                extrabuttons.enabled = True
            elif (extrabuttons.buttons_clicked["Talk with Rina"]):
                extrabuttons.enabled = False
                activities.TalkWithRina.session(self)
                extrabuttons.enabled = True
            elif (extrabuttons.buttons_clicked["Credits"]):
                extrabuttons.enabled = False
                sc = open("credits.txt",'r')
                for line in sc:
                    self.say(line.strip())
                sc.close()
                extrabuttons.enabled = True
            else:
                self.speechbox.message = "..."
                time.sleep(0.02)
            extrabuttons.enabled = False

    def issuenotification(self, message):
        if not self.perma["notifications_enabled"]:
            return
        if (os.name == "nt"): # Windows
            toaster = win10toast.ToastNotifier()
            toaster.show_toast("Rina", message, threaded=True,
                   icon_path="assets/favicon.png", duration=10)
        elif (os.name == "posix"):
            os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(message, "Rina"))

class Button(Sprite):
    # Template
    def __init__(self, label, position, dimensions, button_color, text_color):
        Sprite.__init__(self)

        self.label = label
        self.position = position
        self.dimensions = dimensions

        self.default_button_color = button_color
        self.default_text_color = text_color

        self.button_color = button_color
        self.text_color = text_color
        self.clicked = False
    def event_update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (pos[0] > self.position[0] and pos[0] < self.position[0]+self.dimensions[0]
            and pos[1] > self.position[1] and pos[1] < self.position[1]+self.dimensions[1]):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
    def continuous_update(self):
        if (pygame.time.get_ticks()%100>50):
            pos = pygame.mouse.get_pos()
            if (pos[0] > self.position[0] and pos[0] < self.position[0]+self.dimensions[0]
                and pos[1] > self.position[1] and pos[1] < self.position[1]+self.dimensions[1]):
                self.button_color = tuple([0.6*x for x in self.default_button_color])
                self.text_color = tuple([0.6*x for x in self.default_text_color])
            else:
                self.button_color = self.default_button_color
                self.text_color = self.default_text_color
    def render(self, screen):
        pygame.draw.rect(screen,self.button_color,(self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]))
        myfont = pygame.font.SysFont("consolas", 16, bold=False, italic=True)
        textsurface = myfont.render(self.label, False, self.text_color)
        screen.blit(textsurface,(self.position[0]+7, self.position[1]+2))

class InputBox(Sprite):
    # Template
    def __init__(self, position, dimensions, default=""):
        Sprite.__init__(self)
        self.text = default
        self.cursor = len(default) # before the 0th character
        self.position = position
        self.dimensions = dimensions

        self.submitted = False

    def event_update(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT):
                self.cursor += 1
            elif (event.key == pygame.K_LEFT):
                self.cursor -= 1
            elif (event.key == pygame.K_BACKSPACE):
                self.text = self.text[0:self.cursor-1]+self.text[self.cursor:]
                self.cursor -= 1
            elif (event.key == pygame.K_RETURN):
                self.submitted = True
            else:
                if (len(self.text)<self.dimensions[0]/9.5):
                    self.text = self.text[0:self.cursor]+event.unicode+self.text[self.cursor:]
                    self.cursor += 1
    
    def continuous_update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(screen,(0,0,0),(self.position[0]-1, self.position[1]-1, self.dimensions[0]+2, self.dimensions[1]+2))
        pygame.draw.rect(screen,(255, 255, 255),(self.position[0], self.position[1], self.dimensions[0], self.dimensions[1]))
        myfont = pygame.font.SysFont("consolas", 16, bold=False, italic=True)
        if (pygame.time.get_ticks()%1000>500):
            textsurface = myfont.render(self.text[0:self.cursor]+"|"+self.text[self.cursor:], False, (0,0,0))
        else:
            textsurface = myfont.render(self.text[0:self.cursor]+" "+self.text[self.cursor:], False, (0,0,0))
        screen.blit(textsurface,(self.position[0]+7, self.position[1]+2))

class ActivityPanel(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.selected = {}
        for activity in activities.activities:
            self.selected[activity] = False
        self.submitted = False

        self.checkbox = {}

    def event_update(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            self.submitted = True
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            for activity in activities.activities:
                if (abs(self.checkbox[activity][0]-pos[0]) < 8
                    and abs(self.checkbox[activity][1]-pos[1]) < 8):
                    self.selected[activity] = not self.selected[activity]
                    break

    def continuous_update(self):
        pass

    def render(self, screen):
        panelimage = get_image("assets/panel.png")
        screen.blit(panelimage, (screen.get_width()/2-panelimage.get_width()/2,10))

        xval = 110
        yval = 35
        myfont = pygame.font.SysFont("consolas", 16, bold=False, italic=True)
        for activity, status in self.selected.items():
            pygame.draw.rect(screen,(100, 120, 200),(xval, yval, 16, 16))
            pygame.draw.rect(screen,(255, 255, 255),(xval, yval, 15, 15))
            if (self.selected[activity]):
                pygame.draw.rect(screen,(100, 120, 200),(xval+3, yval+3, 9, 9))
            self.checkbox[activity] = (xval+7, yval+7)
            textsurface = myfont.render(activity, False, (0,0,0))
            screen.blit(textsurface,(xval + 30, yval))
            yval += 23
            if (yval > 330):
                xval += 250
                yval = 35

class ExtraButtons(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # label, enabled
        self.enabled = False
        self.buttons = ["Purpose","Talk with Rina","Credits"]
        self.button_rects = {}
        self.button_colors = {}
        self.buttons_clicked = {"Purpose":False,
                                "Talk with Rina":False,
                                "Credits":False}

    def event_update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for label in self.buttons:
                if (self.enabled):
                    if (pos[0] > self.button_rects[label][0] and pos[0] < self.button_rects[label][0]+self.button_rects[label][2]
                        and pos[1] > self.button_rects[label][1] and pos[1] < self.button_rects[label][1]+self.button_rects[label][3]):
                        self.buttons_clicked[label] = True
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            for label in self.buttons:
                self.buttons_clicked[label] = False
        
    def continuous_update(self):
        pos = pygame.mouse.get_pos()
        for label in self.buttons:
            if (self.enabled):
                if (pos[0] > self.button_rects[label][0] and pos[0] < self.button_rects[label][0]+self.button_rects[label][2]
                    and pos[1] > self.button_rects[label][1] and pos[1] < self.button_rects[label][1]+self.button_rects[label][3]):
                    self.button_colors[label] = (23,86,120)
                else:
                    self.button_colors[label] = (39,143,200)
            else:
                self.button_colors[label] = (128,128,128)

    def render(self, screen):
        xval = 690
        yval = 50
        myfont = pygame.font.SysFont("consolas", 16, bold=False, italic=True)
        for button in self.buttons:
            self.button_rects[button] = (xval, yval, 150, 20)
            pygame.draw.rect(screen,self.button_colors[button],self.button_rects[button])
            myfont = pygame.font.SysFont("consolas", 16, bold=False, italic=True)
            textsurface = myfont.render(button, False, (255,255,255))
            screen.blit(textsurface,(xval+7, yval+2))
            yval += 23