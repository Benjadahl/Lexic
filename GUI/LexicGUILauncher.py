#!/usr/bin/env python3

#Import dependencies
import sys
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk
#sys.path.insert(0, "../Predictor/")
#import Predictor

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

def on_prediction_click(widget, sn):
    print ("[GUI] Suggestion #" + str(sn) + " was pressed.")
    #Return userchoice to script that emulates keypresses.

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
        self.menu = Gtk.Menu()
        self.menu_items = Gtk.MenuItem("lel")
        self.menu.append(self.menu_items)
        self.menu_items.show()
        self.menu_bar = Gtk.MenuBar()
        self.root_menu = Gtk.MenuItem("Root Menu")
        self.root_menu.set_submenu(self.menu)

        #Create vertical box that the buttons will be placed in
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)


        #Add the box to the window
        self.add(self.box)

win = mainWindow()

#Connect the closing of the main window, to ending the script with Gtk.main_quit
win.connect("delete-event", Gtk.main_quit)

#Run the createButtons function
createButtons(buttonAmount)

#Show the window and it's children(buttons)
win.show_all()

updateSuggestions(["example1","example2","example3"], buttonAmount)

#Executes the main function of Gtk
Gtk.main()
