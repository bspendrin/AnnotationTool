from __future__ import annotations
from distutils.filelist import FileList
from textwrap import wrap
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Grid
from tkinter import filedialog

import os

def close_window():
    mainWindow.destroy()

def openFile():
    name = filedialog.askopenfilename() 
    #print(name)
    return name

#Pfad zur Dateiliste setzen
def setDateilistePfad():
    global FileListPath
    FileListPath = os.path.abspath(openFile())
    with open(FileListPath, 'r', encoding = "utf8") as f:
        DateiListe.insert(INSERT, f.read())
        DateiListe.config(state = DISABLED)
    labDateiListenPfad.config(text = FileListPath)

#Pfad zur Tagliste setzen
def setWordListPath():
    global WordListPath
    WordListPath = os.path.abspath(openFile())
    with open(WordListPath, 'r', encoding = "utf8") as f:
        TagListe.insert(INSERT, f.read())
        TagListe.config(state = DISABLED)
    labWordListPath.config(text = WordListPath)

#Pfad zum Quellordner der xml Dateien setzen
def setSourceFolder():
    global sourceFolderPath
    sourceFolderPath = filedialog.askdirectory()
    #print("Source Folder: " + sourceFolderPath)
    labSourceFolder.config(text = sourceFolderPath)

#Pfad zum Zielordner der annotierten xml Dateien setzen
def setDestinationFolder():
    global destinationFolderPath
    destinationFolderPath = filedialog.askdirectory()
    #print("Destination Folder: " + destinationFolderPath)
    labDestinationFolder.config(text = destinationFolderPath)

#Hauptfunktion: Annotation starten
def annotationStarten(FileListPath, WordListPath, destinationFolderPath, sourceFolderPath):

    ###########################################################
    #Backups anlegen
    # def BackupXML(ListFilename):
    #     import shutil #Bibliothek zum Dateien kopieren
    #     fileList = open(ListFilename, 'r', encoding = "utf8").read().splitlines()
    #     for line in fileList:
    #         shutil.copyfile((line+".xml"),(line+".xml.backup"))
    ###########################################################

    ###########################################################
    #Backups einspielen (nur f??rs Testen)
    # def restoreXMLBackups(ListFilename):
    #     import shutil #Bibliothek zum Dateien kopieren
    #     fileList = open(ListFilename, 'r', encoding = "utf8").read().splitlines()
    #     for line in fileList:
    #         shutil.copyfile((line+".xml.backup"),(line+".xml"))
    ###########################################################

    ###########################################################
    #Einlesen von Tags und W??rtern, die getaggt werden sollen
    def readAnnotationData(WordListPath):
        listOfWords = open(WordListPath, 'r', encoding = "utf8").read().splitlines()
    ###########################################################

    import re #Library f??r RegEx
    #Pfade f??r Dateien

    #Nur im Testen: Backups wiederherstellen (sp??ter Backups anlegen!)
    #restoreXMLBackups(FileListPath)
    #BackupXML(FileListPath)

    #Gehe alle Dateien aus der fileList durch
    fileList = open(FileListPath, 'r', encoding = "utf8").read().splitlines()
    #print(fileList)

    for currFile in fileList:
        # Aktuelle Datei einlesen
        if os.name == "nt":
            with open((sourceFolderPath + "\\" + currFile+".xml"), 'r', encoding = "utf8") as file :
                filedata = file.read()
        elif os.name == "posix":
            #print("Curr File: " + sourceFolderPath  + "/" + currFile + ".xml")
            with open((sourceFolderPath  + "/" + currFile + ".xml"), 'r', encoding = "utf8") as file :
                filedata = file.read()

        # Zeichenkette ersetzen
        ### Einlesen von Tags und W??rtern
        wordList = open(WordListPath, 'r', encoding = "utf8").read().splitlines()
        #Gehe alle W??rter durch
        for currWord in wordList:
            #Wenn aktuelles Wort mit # beginnt, setze aktuelles Tag darauf
            if currWord.startswith("#"):
                currTag = currWord[1:] #Entferne das # (=den 1. char des strings)
            #Wenn nicht, ersetze aktuelles Wort mit dem Tag
            else:
                #Annotiert wird:
                #Wenn das Wort von Leerzeichen angef??hrt und gefolgt wird
                #a) von einem Leerzeichen
                filedata = filedata.replace(" " + currWord + " ", (" <term key=\"" + currTag + "\">" + currWord + "</term> "))
                #Richtiges Format f??r die Tags:                <term key="Alkohol">alkoholischer Getr??nke</term>
                #b) von einem Komma
                filedata = filedata.replace(" " + currWord + ",", (" <term key=\"" + currTag + "\">"+ currWord + "</term>,"))
                #c) von einem Punkt (= Satzende)
                filedata = filedata.replace(" " + currWord + ".", (" <term key=\"" + currTag + "\">"+ currWord + "</term>."))
                #d) von einem Ausrufezeichen
                filedata = filedata.replace(" " + currWord + "!", (" <term key=\"" + currTag + "\">"+ currWord + "</term>!"))
                #e) von einem Fragezeichen
                filedata = filedata.replace(" " + currWord + "?", (" <term key=\"" + currTag + "\">"+ currWord + "</term>?"))
        
        #Checken, ob Zielordner existiert, sonst anlegen
        if os.path.exists(destinationFolderPath) == False:
            os.makedirs(destinationFolderPath)
        
        #Annotierte Dateien schreiben
        if os.name == "nt":
            with open(destinationFolderPath  + "\\" +  currFile + ".xml", "w", encoding = "utf8") as file:
                file.write(filedata)
                #print("Wrote File: " + destinationFolderPath + "\\" + currFile+ ".xml")
        elif os.name == "posix":
            with open(destinationFolderPath  + "/" +  currFile + ".xml", "w", encoding = "utf8") as file:
                file.write(filedata)
                #print("Wrote File: " + destinationFolderPath + "/" + currFile + ".xml")


#Kreiert Fenster
mainWindow = Tk()
mainWindow.title("Annotations-Tool NsRdMi") #Fenstertitel
mainWindow.geometry("1000x600") #Fenstergr????e: Breite x H??he
mainWindow.minsize(width = 800, height = 800) #Mindestgr????en
#root.maxsize(width = 1000, height = 750) #Maximalgr????en
#mainWindow.resizable(width = False, height = False) #Sperre Ver??nderbarkeit der Gr????e

FileListPath = "Keine Dateiliste ausgew??hlt"
WordListPath = "Keine Tagliste ausgew??hlt"
sourceFolderPath = "Kein Quellordner ausgew??hlt"
destinationFolderPath = "Kein Zielordner ausgew??hlt"

#Anzeige der ausgew??hlten Dateien
global labDateiListenPfad
DateiListe = Text(mainWindow)
labDateiListenPfad = tk.Label(mainWindow, text = FileListPath)

global labWordListPath
TagListe = Text(mainWindow)
labWordListPath = tk.Label(mainWindow, text = WordListPath)

BeschreibungAllgemein = tk.Label(mainWindow, text = "Die beiden Spalten zeigen die zu bearbeitenden Dateien links und die zu setzenden Tags und ihre dazugeh??rigen Signalworte rechts. \n ??ber die darunterstehenden Buttons k??nnen die jeweiligen Dateien sowie der Quell- und Zielordner angegeben werden.", wraplength=800, justify=LEFT)

BeschreibungDateiliste = tk.Label(mainWindow, text = "In diese Liste m??ssen die zu annotierenden Dateien in einzelnen Zeilen, ohne Dateiendung (d.h. nur die ID) eingetragen werden.", wraplength=400,justify=LEFT)

BeschreibungTagliste = tk.Label(mainWindow, text = "In die Tagliste m??ssen die Tags und dazugeh??rigen zu markierenden Worte in einzelnen Zeilen wie folgt eingetragen werden:\n Das # markiert ein Schlagwort, alle bis zum n??chsten # folgenden Worte werden mit diesem annotiert. Es werden *nur* die angegebenen Schreibweisen annotiert, keine Abwandlungen davon (d.h. Pause != Pausen). Sobald das n??chste # folgt, wird ein neues Tag annotiert.", wraplength=400,justify=LEFT)

#Button: Dateiliste ausw??hlen
btnDateiliste = tk.Button(mainWindow, text = "Dateiliste ausw??hlen", command = lambda: [setDateilistePfad()])

#Button: Tagliste ausw??hlen
btnWordList = tk.Button(mainWindow, text = "Tagliste ausw??hlen", command = lambda: [setWordListPath()])

#Button: Quellordner
btnChooseSourceFolder = tk.Button(mainWindow, text = "Quellordner ausw??hlen", command = lambda: [setSourceFolder()])
global labSourceFolder
labSourceFolder = tk.Label(mainWindow, text = sourceFolderPath)


#Button: Zielordner
btnChooseDestinationFolder = tk.Button(mainWindow, text = "Zielordner w??hlen", command = lambda: [setDestinationFolder()])
global labDestinationFolder
labDestinationFolder = tk.Label(mainWindow, text = destinationFolderPath)

#Button, um die Annotation zu starten
btnAnnotieren = tk.Button(mainWindow, text="Annotation starten", command = lambda: annotationStarten(FileListPath, WordListPath, destinationFolderPath, sourceFolderPath))

#Abbrechen-Button
btnAbbrechen = tk.Button(mainWindow, text="Schlie??en", command = close_window)



#Grid bauen: jede Spalte bekommt ein Gewicht; so werden sie auf die Breite verteilt
mainWindow.columnconfigure(0, weight = 1)
mainWindow.columnconfigure(1, weight = 1)

#Widgets anordnen
BeschreibungAllgemein.grid(column = 0, row = 0, padx=5, pady=5, columnspan=2)

BeschreibungDateiliste.grid(column = 0, row = 1, padx=5, pady=5)
BeschreibungTagliste.grid(column = 1, row = 1, padx=5, pady=5)

DateiListe.grid(column=0, row=2, padx=5, pady=5)
TagListe.grid(column=1, row=2, padx=5, pady=5)

btnDateiliste.grid(column = 0, row = 3)
btnWordList.grid(column = 1, row = 3)

labWordListPath.grid(column=1, row=4, padx=5, pady=5)
labDateiListenPfad.grid(column=0, row=4, padx=5, pady=5)

btnChooseSourceFolder.grid(column = 0, row = 5)
btnChooseDestinationFolder.grid(column = 1, row = 5)

labSourceFolder.grid(column=0, row=6, padx=5, pady=5)
labDestinationFolder.grid(column=1, row=6, padx=5, pady=5)

btnAnnotieren.grid(column=0, row=7)
btnAbbrechen.grid(column=1, row=7)

#Mainloop-Methode --> "Eventloop" --> muss aufgerufen werden --> Endlosschleife, die Interaktionen mit GUI abf??ngt
mainWindow.mainloop()
#Was hier drunter steht, wird erstmal nicht ausgef??hrt!!!!