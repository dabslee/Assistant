import re, math
from collections import Counter
from difflib import SequenceMatcher

import stringdist

WORD = re.compile(r'\w+')

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

def get_cosine(str1, str2):
    vec1 = text_to_vector(str1)
    vec2 = text_to_vector(str2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def gettuples():
    mytuples = []
    sc = open("chatbot.txt",'r')

    line = sc.readline().strip()
    while (line != "%start%"):
        line = sc.readline().strip()
    while (line != "%end%"):
        while (line != "%entry start%"):
            line = sc.readline().strip()
            if (line == "%end%"):
                sc.close()
                return mytuples
        key = sc.readline().strip().split("|")
        line = sc.readline().strip()
        value = []
        while (line != "%entry end%"):
            value.append(line)
            line = sc.readline().strip()
        mytuples.append((key, value))
        line = sc.readline().strip()

    sc.close()

def reply(prompt):

    # cleaning
    prompt = prompt.lower()
    for char in prompt:
        if not char.isalnum() and char!=' ':
            prompt = prompt.replace(char,"")

    # check for exact query matches
    for keys, value in gettuples():
        if (prompt in keys):
            return value

    # return with max similarity if max sim > 0.3
    max_value = ["Sorry! I didn't understand that."]
    max_simil = 0.3
    for keys, value in gettuples():
        for key in keys:
            simil = (get_cosine(key, prompt) + SequenceMatcher(None, key, prompt).ratio() + (1-stringdist.levenshtein(key, prompt)/15))/3
            if (simil > max_simil):
                max_value = value
                max_simil = simil
    return max_value

"""
print("I'm so glad you chose to talk to me!")
print("Type in whatever you want to say to me, or type 'GOODBYE' when you're done.")
prompt = ""
prompt = input(">>> ")
while (prompt != "GOODBYE"):
    for line in reply(prompt):
        print(line)
    prompt = input(">>> ")
"""