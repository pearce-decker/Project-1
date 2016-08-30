from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import itertools
import math
import time

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Example")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        self.button = Button(self, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=0, sticky=W)

    def load_file(self):
        start = time.time()
        fname = askopenfilename(filetypes=(("TSP file", "*.tsp;*.tsp"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                print("""File name: self.settings["template"].set(%s)""" % fname)
            except:                     
                showerror("Failed to read file\n'%s'" % fname)
            
        file = open(fname,'r')
        count = 0
        dataStore = data()
        dataStore.nodes = []
        dataStore.route = []
        for line in file:
            if count == 4:
                dataStore.dimensionStr = line.split()
                dataStore.dimension = int(dataStore.dimensionStr[1])                
            #Get each nodes data
            if count > 6: 
                newNode = node()
                newNode.dataStr = line.split()
                newNode.id = newNode.dataStr[0]
                newNode.x = newNode.dataStr[1]
                newNode.y = newNode.dataStr[2]
                #Places node into list in the parent object
                dataStore.nodes.append(newNode)
            count+=1   
    
        #Get a list of all possible permutations of nodes
        listOfPermutations = list(itertools.permutations(dataStore.nodes))
        dist = -1
        tempDist = 0
        idList = []
        counter = 0
        #iterates through the list of Permutations
        for item in listOfPermutations:
            tempDist = 0
            counter = 0
            xList = []
            yList = []
            tempList = []
            #Iterates through the list of nodes in a specific permutation
            for i in item:
                #Appends the list with their respective data
                tempList.append(i.id)
                xList.append(i.x)
                yList.append(i.y)  
            #Appends the first location on to caluclate travel back to it from the last one          
            xList.append(item[0].x)
            yList.append(item[0].y)
            #Iterates through the list and calculates total disance traveled
            while(counter < len(item)):
               tempDist = tempDist + distanceCalc(float(xList[counter+1]),float(xList[counter]),float(yList[counter+1]),float(yList[counter]))     
               counter = counter + 1 
            #Checks to see if the current distance is less than the new distance and replaces it if tempDist is lower          
            if(dist > tempDist or dist < 0):
                dist = tempDist
                idList = tempList
        end = int((time.time() - start) *1000)
        print("%d tours" %len(listOfPermutations))
        print("Route:" , end=" ")
        for id in idList:
            print(id , end=" ")
        print(" ")
        print("Shortest distance is %f" %dist)
        print(" ")
        print("%d ms" %end)
        return

#Distance calculation
def distanceCalc(x1,x2,y1,y2):
    x = math.pow(x2 - x1,2)
    y = math.pow(y2 - y1,2)
    sum = x + y
    return math.sqrt(sum)

#Object which holds dimension and a list of all the nodes
class data(object):
        nodes = []
        dimension = 0
        dimensionStr = []
        route = []

#Object which holds the id and coordinates for the nodes
class node(object):
        id = 0
        dataStr = []
        x = 0.0
        y = 0.0

#Loops the main function
if __name__ == "__main__":
    MyFrame().mainloop()