import os
import sys
import csv
from datetime import datetime


def searchuser():
    if not "user" in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        os.makedirs(os.path.join(os.path.dirname(__file__), "user"))

    userfolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user")

    userlist = []
    for user in os.listdir(userfolder):
        userlist.append(user[:-4])

    return userlist

def chooseuser(chosenuser = ""):
    # rangelimit 0 lässt noch das Anlegen neuer User zu
    # beim zweiten Durchlauf wird der Chatpartner gewählt - hier wird also niemand mehr neu angelegt

    os.system("cls")
    userlist = searchuser()

    if chosenuser == "":
        rangelimit = 0
        print("Willkommen beim ultimativen Chat-Programm *räusper*.")
        print("Bitte wähle dich aus der Liste aus oder lege einen neuen User an!")
        print("- - - - - - - - - - - ")
        print("0: Neuen User anlegen!")

    else:
        print("")
        print("Hallo " + chosenuser + " :)")
        print("Bitte wähle den User aus, mit dem du chatten möchtest!")
        rangelimit = 1
        userlist.remove(chosenuser)

    usercounter = 1
    for user in userlist:
        if user == chosenuser:
            usercounter += 1
            continue
        print(str(usercounter) + ": " + user)
        usercounter += 1

    userchoice = -1
    while not userchoice in range(rangelimit, len(searchuser()) + 1):

        userchoice = int(input("Wähle einen User per Nummer aus:"))

        if userchoice == 0 and chosenuser == "":
            return newuser()

        else:
            try:
                print("Du hast " + userlist[userchoice - 1] + " gewählt.")

            except IndexError:
                print("User existiert nicht! Eingabe wiederholen")

    return userlist[userchoice-1]

def newuser():
    username = input("Gib deinen Namen ein: ")
    with open(os.path.dirname(os.path.abspath(__file__)) + "//user//" + username + ".csv", "w") as userfile:
        newuser = csv.writer(userfile, delimiter = ";", quotechar='"')

    return username


def searchlog(username1, username2):

    with open(os.path.dirname(os.path.abspath(__file__)) + "//user//" + username1 + ".csv", "r") as userfile:
        userlogs = csv.reader(userfile, delimiter = ";", quotechar='"')

        for line in userlogs:
            if username2 == line[0]:
                return line[1]
            else:
                continue

        return (createlog(username1, username2))

def createlog(username1, username2):

    logfile = username1 + "_" + username2

    #user-eintrag erweitern (user1)
    with open(os.path.dirname(os.path.abspath(__file__)) + "//user//" + username1 + ".csv", "a", newline='') as userfile:
        userlogs = csv.writer(userfile, delimiter = ";", quotechar='"')
        userlogs.writerow([username2, logfile])

    # user-eintrag erweitern (user2)
    with open(os.path.dirname(os.path.abspath(__file__)) + "//user//" + username2 + ".csv", "a", newline='') as userfile:
        userlogs = csv.writer(userfile, delimiter = ";", quotechar='"')
        userlogs.writerow([username1, logfile])

    #Chat-Verlauf-Datei anlegen
    if not "chats" in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        os.makedirs(os.path.join(os.path.dirname(__file__), "chats"))

    with open(os.path.dirname(os.path.abspath(__file__)) + "//chats//" + logfile + ".csv", "w") as chatfile:
        logwriter = csv.writer(chatfile, delimiter = ";", quotechar='"')

    return logfile

def showlog(logfile):
    with open(os.path.dirname(os.path.abspath(__file__)) + "//chats//" + logfile + ".csv", "r", newline='') as chatfile:
        logreader = csv.reader(chatfile, delimiter = ";", quotechar='"')

        for line in logreader:
            print("Am " + line[0] + " schrieb " + line[1] + " an " + line[2] + " :")
            print(line[3])
            print("")

def savelog(logfile, content):
    with open(os.path.dirname(os.path.abspath(__file__)) + "//chats//" + logfile + ".csv", "a", newline='') as chatfile:
        logwriter = csv.writer(chatfile, delimiter = ";", quotechar='"')

        logwriter.writerow(content)

def chat(logfile):
    message = ""
    os.system("cls")

    while message != "exit":
        showlog(logfile)

        log = []
        now = datetime.now()

        print("Hinweis: 'exit' beendet die Chateingabe!")
        message = input(user1 + ": ")

        if message != "exit":
            log = [now, user1, user2, message]
            savelog(logfile, log)

            os.system("cls")


# Hier beginnt das Programm

os.system("cls")

if len(searchuser()) == 0:
    print("Lege den ersten User an!")
    newuser()
    print("Lege den zweiten User an!")
    newuser()
#elif nur für den Fall, dass das Programm abschmiert oder user-Dateien gelöscht werden!
elif len(searchuser()) == 1:
    print("Lege den zweiten User an!")
    newuser()

user1 = chooseuser()
user2 = chooseuser(user1)
chatlog = searchlog(user1, user2)
chat(chatlog)
