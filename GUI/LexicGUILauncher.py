#!/usr/bin/env python3

#Import dependencies
import sys
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Atk
#Import the predictor
#Next line changes the python import focus
sys.path.insert(0, "../Predictor/")
import Predictor


#Functions |---

#Function for creating the buttons
def createButtons(amount):
    print ("[GUI] Creating " + str(amount) + " buttons")
    for i in range(1, amount + 1):
        #Add the buttons to the window class
        setattr(win, "prediction" + str(i), Gtk.Button(label = "Prediction #" + str(i)))
        #Add the buttons to the box
        win.box.pack_start(getattr(win, "prediction" + str(i)), True, True, 0)
        #Connect the buttons clicked event to the on_prediction_click function
        getattr(win, "prediction" + str(i)).connect("clicked", on_prediction_click, i)

def convertSuggestion(suggestion):
    sList = []
    for i in range(10):
        row = suggestion.fetchone()

        if row == None:
            break

        sList.append(str(row[1]))

    return sList

#Function to update suggestions
def updateSuggestions(suggestionList, amount):
    print ("[GUI] Updating suggestions")
    #Try to change the button labels (Will probably fail if the inputtet suggestions are not a list)
    try:
        #Run the loop for the amount of buttons
        for i in range(0,amount + 1):
            #If only attempt to change the labels,
            if i < len(suggestionList):
                #Get the button using getattr(), then set the label to the respective item of the list.
                getattr(win, "prediction" + str(i + 1)).set_label(suggestionList[i])
            else:
                #Return if the length of the list has been reached
                return
    except:
        print ("[GUI] Error during suggestion update (might be due to input not being a list)")

def getConvertUp(word):
    #This function takes a string, looks it up in the database, converts the output to a list, and then updates the suggestions
    return updateSuggestions(convertSuggestion(Predictor.getWords(word)), buttonAmount)

def on_prediction_click(widget, sn):
    print ("[GUI] Suggestion #" + str(sn) + " was pressed.")
    #Return userchoice to script that emulates keypresses.

def on_search_click(widget, searchTerm):
    #Updates the userchoices arcoding to the searchterm in the text input field
    getConvertUp(win.searchField.get_text())

def enter_check(widget, key):
    if key.keyval == 65293:
        #Updates the userchoices arcoding to the searchterm in the text input field
        getConvertUp(win.searchField.get_text())

#---|

#Customizable variables |---

#The amount of buttons that will be created:
buttonAmount = 9

#---|

#Create class for the main window
class mainWindow (Gtk.Window):
    #Initiating function for the window
    def __init__(self):
        Gtk.Window.__init__(self, title="LexicGUITest")
        self.set_keep_above(True)
        self.set_decorated(False)

        #Creates the top level parent box contain 2 children boxes
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.add(self.mainBox)

        #Creates the box for the top of the GUI
        self.topBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.mainBox.pack_start(self.topBox, True, True, 0)

        #Create vertical box that the buttons will be placed in
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        #Add the box to the window
        #self.add(self.box)
        self.mainBox.pack_start(self.box, True, True, 0)

        #Add textField, and add it to the box
        self.searchField = Gtk.Entry()
        self.searchField.connect("key-release-event", enter_check)

        self.topBox.pack_start(self.searchField, True, True, 0)
        self.searchField.set_text("is")

        #Add search button
        self.search = Gtk.Button(label = "Search")
        self.topBox.pack_start(self.search, True, True, 0)
        self.search.connect("clicked", on_search_click, self.searchField.get_text())

        #Add the Suggestions label
        self.label = Gtk.Label(label="Suggestions:")
        self.box.pack_start(self.label, True, True, 0)


win = mainWindow()

#Connect the closing of the main window, to ending the script with Gtk.main_quit
win.connect("delete-event", Gtk.main_quit)

#Run the createButtons function
createButtons(buttonAmount)

#Show the window and it's children(buttons)
win.show_all()

#Start the predictor
Predictor.initiateDB("MarkovComplete.db")

#Executes the main function of Gtk
Gtk.main()
