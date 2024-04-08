# -*- coding: utf-8 -*-
#Programme par Titouan - Responsable EEDF Meudon
##Imports & vars
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteEntryListbox #besoin de pip install
# from HoverInfo import HoverInfo #Fichier local
import sqlite3
import os
import sys
import inspect

APP_NAME = "Denethor"
APP_VERSION = "beta 0.2"
dbName = "DenethorDB.db"
regimeList = ["Viande","Sans-porc","Végétarien","Végétalien"]
allergeneList = ["Gluten", "Arachides", "Crustacé", "Œuf", "Poisson", "Soja", "Lait", "Fruits à coque", "Céleri", "Moutarde", "Graines de sésame", "Anhydrides sulfureux/sulfites", "Lupin", "Mollusques"]
regimeNot = "Ignorer"
ordreList = ["Entrée","Plat","Dessert","Goûter","Ptit-dèj","Autre"]
tailleList = ("Enfant", "Adulte")
exportExtension = ".txt"

#Dossier de travail = dossier de l'exécutable
try:
    if getattr(sys, 'frozen', False):
        directory = os.path.dirname(sys.executable)
    elif __file__:
        directory = os.path.dirname(__file__)
except NameError:
    file_path = inspect.getfile(lambda: None)
    directory = os.path.dirname(file_path)
print(directory)
os.chdir(directory)

BDD_path = os.path.join(directory, dbName)

#Création d'une BDD
def setSQL(request):
    BDD.execute(request)
    connection.commit()
    return None

def askSQL(request):
    BDD.execute(request)
    res = BDD.fetchall()
    return res

def formatBDD():
    global connection
    global BDD
    connection = sqlite3.connect(BDD_path)
    BDD = connection.cursor()
    setSQL("CREATE TABLE IF NOT EXISTS ingredients (id_ing INTEGER PRIMARY KEY, nom VARCHAR(255), unit VARCHAR(255), regime INTEGER, allergenes VARCHAR(255))")
    #Régime : 0 = Viande, 1 = sans-porc, 2 = veg1, 3 = veg2, None = non spécifié
    setSQL("CREATE TABLE IF NOT EXISTS plats (id_plat INTEGER PRIMARY KEY, nom VARCHAR(255), ordre INTEGER, regimes VARCHAR(8))")
    #0 = entrée, 1 = plat, 2 = dessert, 3 = gouter, 4 = ptit-dej, 5 = autre, -1 = non spécifié
    setSQL("CREATE TABLE IF NOT EXISTS plats_ing (id_plat INTEGER, id_ing INTEGER, regime INTEGER, qte_enfant INTEGER, qte_adulte INTEGER)")
    #Régime : 0 = Viande, 1 = sans-porc, 2 = veg1, 3 = veg2
    #taille : 0 = enfant, 1 = adulte
    setSQL("CREATE TABLE IF NOT EXISTS pers (val INTEGER, regime INTEGER, taille INTEGER)")

    setSQL("CREATE TABLE IF NOT EXISTS listes (id_list INTEGER PRIMARY KEY, is_ing INTEGER, id INTEGER, qte_enfant INTEGER, qte_adulte INTEGER, '0' INTEGER, '1' INTEGER, '2' INTEGER, '3' INTEGER)")

##Fonctions diverses
def get_path(filename):     #Utilisé pour .exe avec pyinstaller
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    return None

def getRegimeName(val):
    res = ""
    if val == -1:
        res = "Non spécifié"
    elif val == 0:
        res = "Viande"
    elif val == 1:
        res = "Sans-porc"
    elif val == 2:
        res = "Végétarien"
    elif val == 3:
        res = "Végétalien"
    else:
        val = "Erreur"
    return res

def getRegimeVal(val):

    if val == "Non spécifié":
        res = -1
    elif val == "Viande":
        res = 0
    elif val == "Sans-porc":
        res = 1
    elif val == "Végétarien":
        res = 2
    elif val == "Végétalien":
        res = 3
    elif val == regimeNot:
        res = -3
    else:
        val = -2
    return res

def getTailleName(val):
    res = ""
    if val == 0:
        res = "Enfant"
    elif val == 1:
        res = "Adulte"
    else:
        val = "Erreur"
    return res

def getTailleVal(val):
    if val == "Enfant":
        res = 0
    elif val == "Adulte":
        res = 1
    else:
        val = -1
    return res


def getOrdreName(val):
    res = ""
    if val == -1:
        res = "Autre"
    elif val == 0:
        res = "Entrée"
    elif val == 1:
        res = "Plat"
    elif val == 2:
        res = "Dessert"
    elif val == 3:
        res = "Goûter"
    elif val == 4:
        res = "Ptit-dèj"
    else:
        val = "Erreur"
    return res

def getOrdreVal(val):

    if val == "Autre":
        res = -1
    elif val == "Entrée":
        res = 0
    elif val == "Plat":
        res = 1
    elif val == "Dessert":
        res = 2
    elif val == "Goûter":
        res = 3
    elif val == "Ptit-dèj":
        res = 4
    else:
        val = -2
    return res

def getIngName(id_ing):
    res = askSQL("SELECT nom FROM ingredients WHERE id_ing = '%s'" % (id_ing))
    if res != []:
        return res[0][0]
    else:
        return "Erreur"

def getIngVal(ingName):
    res = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingName))
    if res != []:
        return res[0][0]
    else:
        return 0

def makeErrorWindow(error):
    errorWin= Toplevel(root)
    errorWin.grab_set()
    errorWin.title("Erreur")
    errorWin.grid_columnconfigure(0, weight=1)
    errorLbl = Label(errorWin, text=error, justify="left", bd = 5, font="Verdana 10 bold",bg = "red")
    errorLbl.grid(row=0, column=0, sticky='news')

    closeButton = Button(errorWin,
        text="Fermer",
        font = "Verdana 10 bold",
        bd = 2,
        relief = "groove",
        command= errorWin.destroy
        )
    closeButton.grid(row=1, column=0, sticky='ns')

    errorWin.bind('<Return>', lambda event:errorWin.destroy())
    errorWin.bind('<Escape>', lambda event:errorWin.destroy())

    errorWin.after(1, lambda: errorWin.focus_force())
    center(errorWin)
    errorWin.mainloop()
    return None

##Gérer les ingrédients

def updateIngList(ingList):
    ingList.delete(0,END)
    ingpayload = askSQL("SELECT nom FROM ingredients ORDER BY nom")

    for i in range(len(ingpayload)):
        ingList.insert(i,ingpayload[i][0].capitalize())

    return None

def ingSelect(event, ingName, ingUnit, ingRegime, ingAllergenes):
    w = event.widget
    if w.curselection() == ():
        return None
    index = int(w.curselection()[0]) #Index dans la ListBox
    nom = w.get(index)  #Nom dans la liste
    ingInfoUnit = askSQL("SELECT unit FROM ingredients WHERE nom = '%s'" % (nom.lower()))[0][0]
    # print(ingInfoUnit)

    ingInfoRegime = askSQL("SELECT regime FROM ingredients WHERE nom = '%s'" % (nom.lower()))[0][0]
    # print(ingInfoRegime)

    ingInfoAllergenes = askSQL("SELECT allergenes FROM ingredients WHERE nom = '%s'" % (nom.lower()))[0][0]
    # print(ingInfoAllergenes)
    allergenes = ""
    if ingInfoAllergenes == None:
        allergenes = "Néant"
    else:
        ingInfoAllergenes = ingInfoAllergenes[1::]  #On yeet le 1 du début
        for pos in range(len(ingInfoAllergenes)//4):
            packet = int(ingInfoAllergenes[4*pos:4*pos+4])
            # print(packet)
            if packet >= 1000:
                allergenes += "Traces de " + allergeneList[packet-1000] + ",\n "
            else:
                allergenes += allergeneList[packet] + ",\n"
        allergenes = allergenes.strip(",\n") + "\n\n"

    ingAllergenes.config(text = allergenes)
    ingName.config(text = nom)
    ingUnit.config(text = ingInfoUnit)
    ingRegime.config(text = getRegimeName(ingInfoRegime))

    return None

def ingAddEditDone(ingList, ingAddWin, wgName, wgUnit, wgRegime, editing, prevName, allergeneBools, allergeneTracesBools):
    ingNameStr = wgName.get()
    ingUnitStr = wgUnit.get()
    ingRegimeStr = wgRegime.get()
    # print(ingNameStr,ingUnitStr,ingRegimeStr)
    if ingNameStr == "":
        makeErrorWindow("Erreur : Vous devez donner un nom à l'ingrédient.")
    else:
        if editing:
            setSQL("DELETE FROM ingredients WHERE nom = '%s'" % (prevName.lower()))
        existsCheck = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingNameStr.lower()))
        if len(existsCheck) != 0:
            makeErrorWindow("""Erreur : Un ingrédient avec le nom "%s" existe déjà.""" % (ingNameStr))
        else:
            #Allergenes
            allergenes = "1"
            for pos in range(len(allergeneList)):
                allergene = allergeneList[pos]
                if allergeneBools[allergene].get() == 1:
                    if allergeneTracesBools[allergene].get() == 0:
                        valstr = str(pos)
                        code = (4-len(valstr))*"0" + valstr
                    elif allergeneTracesBools[allergene].get() == 1:
                        code = str(1000 + pos)
                    else:
                        code = ""
                    allergenes += code
            # print(allergenes)

            ingRegimeVal = getRegimeVal(ingRegimeStr)
            if allergenes == "1":
                allergenes = "NULL"
            if ingRegimeVal == None:
                setSQL("INSERT INTO ingredients (nom, unit, regime, allergenes) VALUES ('%s', '%s', NULL, '%s')" % (ingNameStr.lower(), ingUnitStr, allergenes))
            else:
                setSQL("INSERT INTO ingredients (nom, unit, regime, allergenes) VALUES ('%s', '%s', %s, '%s')" % (ingNameStr.lower(), ingUnitStr, ingRegimeVal, allergenes))
            ingAddWin.destroy()
            updateIngList(ingList)

    return None

def allergeneTracesUpdate(allergeneCheckButtons, allergeneBools, allergeneTracesCheckButtons):
    for allergene in allergeneList:
        if allergeneBools[allergene].get() == 1:
            allergeneTracesCheckButtons[allergene].grid()
        else:
            allergeneTracesCheckButtons[allergene].grid_remove()

    return None

def ingAddEdit(ingList, prevName):


    ingAddWin= Toplevel(root)
    ingAddWin.geometry("850x500")
    center(ingAddWin)
    ingAddWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie

    editing = 0

    ingAddWin.grid_columnconfigure(2, weight=1)
    ingAddWin.grid_rowconfigure(4, weight=1)
    # ingAddWin.grid_rowconfigure(6, weight=1)

    if prevName != "":
        editing = 1
        ingAddWin.title("Éditer un ingrédient de la base de données")
        label = Label(ingAddWin, text="Éditer un ingrédient de la base de données", bg="yellow", font = "8", bd=8)
    else:
            ingAddWin.title("Ajouter un ingrédient dans la base de données")
            label = Label(ingAddWin, text="Ajouter un ingrédient dans la base de données", bg="yellow", font = "8", bd=8)

    label.grid(row=0, column=0, columnspan = 3, sticky='nwe')

    sep = ttk.Separator(ingAddWin, orient='vertical')
    sep.grid(row=1, column=1, columnspan = 1, rowspan = 5, sticky='news')


    ingInfosFrame = Frame(ingAddWin)
    ingInfosFrame.grid(row=1, column=0, rowspan = 1, sticky='news')
    # ingInfosFrame.grid_columnconfigure(1, weight=1)

    ingInfosLbl = Label(ingInfosFrame, text="Informations : ", relief=RAISED, font="Verdana 10 bold")
    ingInfosLbl.grid(row=0, column=0, columnspan = 3, sticky='news')

    ingNameLbl = Label(ingInfosFrame, text="Nom : ")
    ingNameLbl.grid(row=1, column=0, sticky='e')
    ingNameEntry = Entry(ingInfosFrame, width = 30)
    ingNameEntry.grid(row=1, column=1, sticky='w')
    ingNameDesc = Label(ingInfosFrame, text="Nom de l'ingrédient.\nDeux ingrédients ne peuvent pas\navoir le même nom.\n", justify="left", bd = 5)
    ingNameDesc.grid(row=1, column=2, sticky='w')

    ingUnitLbl = Label(ingInfosFrame, text="Unité de mesure : ")
    ingUnitLbl.grid(row=2, column=0, sticky='e')
    ingUnitEntry = Entry(ingInfosFrame, width = 30)
    ingUnitEntry.grid(row=2, column=1, sticky='w')
    ingUnitDesc = Label(ingInfosFrame, text="L'unité dans laquelle vous allez\nentrer les quantités de cet\ningrédient en composant les plats.\n", justify="left", bd = 5)
    ingUnitDesc.grid(row=2, column=2, sticky='w')

    ingRegimeLbl = Label(ingInfosFrame, text="Convient au régime : ")
    ingRegimeLbl.grid(row=3, column=0, sticky='e')
    ingRegimeEntry = ttk.Combobox(ingInfosFrame, values = regimeList, state="readonly")
    ingRegimeEntry.set("Non spécifié")
    ingRegimeEntry.grid(row=3, column=1, sticky='w')
    ingRegimeDesc = Label(ingInfosFrame, text="Entrez le régime le plus\nrestrictif auquel cet ingrédient convient.\n", justify="left", bd = 5)
    ingRegimeDesc.grid(row=3, column=2, sticky='w')

    #Entrée des allergènes contenus dans l'ingrédient
    ingAllergeneFrame = Frame(ingAddWin)
    ingAllergeneFrame.grid(row=1, column=2, rowspan = 1, sticky='news')
    ingAllergeneFrame.grid_columnconfigure(1, weight=1)

    ingAllergeneLbl = Label(ingAllergeneFrame, text="Allergènes : ", relief=RAISED, font="Verdana 10 bold")
    ingAllergeneLbl.grid(row=0, column=0, columnspan = 2, sticky='news')

    allergeneCheckButtons = {}
    allergeneTracesCheckButtons = {}
    allergeneBools = {}
    allergeneTracesBools = {}
    for pos in range(len(allergeneList)):
        allergene = allergeneList[pos]
        allergeneBools[allergene] = IntVar(value=0)
        allergeneTracesBools[allergene] = IntVar(value=0)

        allergeneTracesCheckButtons[allergene] = Checkbutton(ingAllergeneFrame, text = "Traces", variable = allergeneTracesBools[allergene], onvalue = 1, offvalue = 0)
        allergeneTracesCheckButtons[allergene].grid(row=1+pos, column=1, columnspan = 1, sticky='w')
        allergeneTracesCheckButtons[allergene].grid_remove()

        allergeneCheckButtons[allergene] = Checkbutton(ingAllergeneFrame, text = allergene, variable = allergeneBools[allergene], onvalue = 1, offvalue = 0, command = lambda:allergeneTracesUpdate(allergeneCheckButtons, allergeneBools, allergeneTracesCheckButtons))
        allergeneCheckButtons[allergene].grid(row=1+pos, column=0, columnspan = 1, sticky='w')

    ingAllergeneDesc = Label(ingAllergeneFrame, text="Sélectionnez les allergènes contenus dans l'ingrédient.\nCochez 'Traces' s'ils sont présents à l'état de traces.", relief=SUNKEN)
    ingAllergeneDesc.grid(row=2+pos, column=0, columnspan = 2, sticky='news')

    #If pour l'édition d'ingrédients
    if editing:
        infoPrev = askSQL("SELECT nom,unit,regime FROM ingredients WHERE nom = '%s'" % (prevName.lower()))[0]
        # print(infoPrev)
        ingNameEntry.insert(0,infoPrev[0])
        ingUnitEntry.insert(0,infoPrev[1])
        ingRegimeEntry.current(infoPrev[2])

        ingInfoAllergenes = askSQL("SELECT allergenes FROM ingredients WHERE nom = '%s'" % (prevName.lower()))[0][0]
        # print(ingInfoAllergenes)
        allergenes = ""
        if ingInfoAllergenes == None:
            allergenes = "Néant"
        else:
            ingInfoAllergenes = ingInfoAllergenes[1::]  #On yeet le 1 du début
            for pos in range(len(ingInfoAllergenes)//4):
                packet = int(ingInfoAllergenes[4*pos:4*pos+4])
                # print(packet)
                if packet >= 1000:
                    allergene = allergeneList[packet-1000]
                    allergeneBools[allergene].set(1)
                    allergeneTracesBools[allergene].set(1)
                    allergeneTracesCheckButtons[allergene].grid()
                else:
                    allergene = allergeneList[packet]
                    allergeneBools[allergene].set(1)
                    allergeneTracesCheckButtons[allergene].grid()


    #Boutons
    ingButtonsFrame = Frame(ingAddWin)
    ingButtonsFrame.grid(row=4, column=0, columnspan = 4, sticky='ews')
    ingButtonsFrame.grid_columnconfigure(0, weight=1)
    ingButtonsFrame.grid_columnconfigure(1, weight=1)

    ingAddSaveButton = Button(ingButtonsFrame,
        text="\nEnregistrer\n",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:ingAddEditDone(ingList, ingAddWin, ingNameEntry, ingUnitEntry, ingRegimeEntry, editing, prevName, allergeneBools, allergeneTracesBools)
        )
    ingAddSaveButton.grid(row=0, column=0, sticky='ew')

    ingAddCancelButton = Button(ingButtonsFrame,
        text="\nAnnuler\n",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= ingAddWin.destroy
        )
    ingAddCancelButton.grid(row=0, column=1, sticky='ew')

    ingAddWin.bind('<Return>', lambda event:ingAddEditDone(ingList, ingAddWin, ingNameEntry, ingUnitEntry, ingRegimeEntry, editing, prevName, allergeneBools, allergeneTracesBools))
    ingAddWin.bind('<Escape>', lambda event:ingAddWin.destroy())

    ingAddWin.after(1, lambda: ingAddWin.focus_force())
    ingAddWin.mainloop()
    return None

def ingRemDone(ingList, nom, ingRemWin):
    id_ing = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (nom.lower()))[0][0]
    setSQL("DELETE FROM ingredients WHERE nom = '%s'" % (nom.lower()))

    #Nettoyage des entrées des ingrédients dans les BDD des plats and des listes de courses
    request = "DELETE FROM plats_ing WHERE id_ing = %s" % (id_ing)
    setSQL(request)
    request = "DELETE FROM listes WHERE id = %s AND is_ing = 1" % (id_ing)
    setSQL(request)
    updateIngList(ingList)
    ingRemWin.destroy()
    return None

def ingRem(ingList, nom):
    ingRemWin= Toplevel(root)
    ingRemWin.geometry("550x100")
    center(ingRemWin)
    ingRemWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie
    ingRemWin.title("Supprimer un ingrédient")

    ingRemWin.grid_columnconfigure(0, weight=1, uniform = "aaa")
    ingRemWin.grid_columnconfigure(1, weight=1, uniform = "aaa")
    ingRemWin.grid_rowconfigure(1, weight=1)

    label = Label(ingRemWin, text="Voulez-vous supprimer l'ingrédient " + nom + " ?\nCela la supprimera de tous les plats et de toutes les listes de courses.", bg="yellow", font = "6", bd=8)
    label.grid(row=0, column=0, columnspan = 2, sticky='nwes')

    yesButton = Button(ingRemWin,
        text="Oui",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "light green",
        relief = "groove",
        command= lambda:ingRemDone(ingList, nom, ingRemWin)
        )
    yesButton.grid(row=1, column=0, sticky='news')

    noButton = Button(ingRemWin,
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "red",
        relief = "groove",
        command= ingRemWin.destroy
        )
    noButton.grid(row=1, column=1, sticky='news')


    ingRemWin.bind('<Return>', lambda event:ingRemDone(ingList, nom, ingRemWin))
    ingRemWin.bind('<Escape>', lambda event:ingRemWin.destroy())

    ingRemWin.after(1, lambda: ingRemWin.focus_force())
    ingRemWin.mainloop()
    return None


def makeingFrame():
    global ingFrame

    ingFrame = Frame(master=container, borderwidth=5, relief=GROOVE, width=700, height=500)
    # ingFrame.pack(side=LEFT, padx=30, pady=30)
    ingFrame.grid(row=0, column=0, sticky='news')

    ingFrame.grid_rowconfigure(6, weight=1)
    ingFrame.grid_columnconfigure(0, weight=1, uniform="fred")
    # ingFrame.grid_columnconfigure(2, weight=1, uniform="fred")
    ingFrame.grid_columnconfigure(3, weight=1, uniform="fred")

    #LISTE des ingrédients
    label = Label(ingFrame, text="Gérer les ingrédients de la base de données", bg="yellow", font = "10")
    label.grid(row=0, column=0, columnspan = 4, sticky='nwe')

    ingListName = Label(ingFrame, text="Liste des ingrédients enregistrés", relief=RAISED)
    ingListName.grid(row=1, column=0, sticky='new')

    scrollIngList = Scrollbar(ingFrame)
    scrollIngList.grid(row=2, column=1, rowspan=6, sticky='nsw')

    ingpayload = askSQL("SELECT nom FROM ingredients ORDER BY nom")

    ingList = Listbox(ingFrame, yscrollcommand = scrollIngList.set)
    for i in range(len(ingpayload)):
        ingList.insert(i,ingpayload[i][0].capitalize())
    ingList.grid(row=2, column=0, rowspan=6, sticky='news')

    #INFOS sur un ingrédient
    ingSelectName = Label(ingFrame, text="Infos de l'ingrédient sélectionné", relief=RAISED)
    ingSelectName.grid(row=1, column=2, columnspan=2, sticky='new')

    ingNameLbl = Label(ingFrame, text="Nom : ")
    ingNameLbl.grid(row=2, column=2, sticky='nw')
    ingName = Label(ingFrame, text="")
    ingName.grid(row=2, column=3, sticky='nw')

    ingUnitLbl = Label(ingFrame, text="Unité de mesure : ")
    ingUnitLbl.grid(row=3, column=2, sticky='nw')
    ingUnit = Label(ingFrame, text="")
    ingUnit.grid(row=3, column=3, sticky='nw')

    ingRegimeLbl = Label(ingFrame, text="Convient au régime : ")
    ingRegimeLbl.grid(row=4, column=2, sticky='nw')
    ingRegime = Label(ingFrame, text="")
    ingRegime.grid(row=4, column=3, sticky='nw')

    ingAllergenesLbl = Label(ingFrame, text="Allergènes : \n")
    ingAllergenesLbl.grid(row=5, column=2, sticky='nw')
    ingAllergenes = Label(ingFrame, text="", justify="left")
    ingAllergenes.grid(row=5, column=3, sticky='nw')

    ingList.bind('<<ListboxSelect>>', lambda event:ingSelect(event, ingName, ingUnit, ingRegime, ingAllergenes))
    ingList.select_set(0)
    ingList.event_generate("<<ListboxSelect>>")

    #ACTIONS : Ajouter, supprimer, éditer
    addIngButton = Button(
        ingFrame,
        text="Ajouter un ingrédient",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:ingAddEdit(ingList, '')
        )
    addIngButton.grid(row=7, column=2, sticky='nw')

    editIngButton = Button(
        ingFrame,
        text="Éditer cet ingrédient",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "yellow",
        relief = "groove",
        command= lambda:ingAddEdit(ingList, ingName.cget("text"))
        )
    editIngButton.grid(row=6, column=2, sticky='nw')

    removeIngButton = Button(
        ingFrame,
        text="Supprimer cet ingrédient",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= lambda:ingRem(ingList, ingName.cget("text"))
        )
    removeIngButton.grid(row=6, column=3, sticky='nw')

    ingList.bind('<Delete>', lambda event:ingRem(ingList, ingName.cget("text")))
    ingFrame.after(100, lambda: ingList.focus_force())
    return None

def raiseing():
    ingFrame.tkraise()


##Gérer les plats
def remIngFromPlatDone(platName, ingName, remIngFromPlatWin, platIngList, platIngSelectFrame, platAllergenes):
    id_plat = askSQL("SELECT id_plat FROM plats WHERE nom = '%s'" % (platName.lower()))[0][0]
    id_ing = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]

    request = "DELETE FROM plats_ing WHERE id_plat = '%s' AND id_ing = '%s'" % (id_plat,id_ing)
    # print("done")
    setSQL(request)

    # for widget in platFrame.winfo_children():    #Reconstruction de tout
    #     widget.destroy()
    # makeplatFrame()
    platRegimeUpdate(platName, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes)
    remIngFromPlatWin.destroy()
    return None

def remIngFromPlat(platName, ingName, platIngList, platIngSelectFrame, platAllergenes):
    remIngFromPlatWin= Toplevel(root)
    remIngFromPlatWin.geometry("500x120")
    center(remIngFromPlatWin)
    remIngFromPlatWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie

    remIngFromPlatWin.title("Supprimer " + ingName + " de " + platName + " ? ")
    label = Label(remIngFromPlatWin, text="Supprimer " + ingName + " de " + platName + " ? ", bg="yellow", font = "8", bd=8)
    label.grid(row=0, column=0, columnspan = 2, sticky='nwe')

    remIngFromPlatWin.grid_columnconfigure(0, weight=1, uniform = "rem")
    remIngFromPlatWin.grid_columnconfigure(1, weight=1, uniform = "rem")
    remIngFromPlatWin.grid_rowconfigure(2, weight=1)

    remIngDesc = Label(remIngFromPlatWin, text="L'ingrédient sera supprimé de toutes les variantes du plat.", font = "Verdana 10 bold", relief=RAISED)
    remIngDesc.grid(row=1, column=0, columnspan=2, sticky='news')

    #SAVE/DISCARD
    remIngConfirmButton = Button(remIngFromPlatWin,
        text="Oui",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "light green",
        relief = "groove",
        command= lambda:remIngFromPlatDone(platName, ingName, remIngFromPlatWin, platIngList, platIngSelectFrame, platAllergenes)
        )
    remIngConfirmButton.grid(row=2, column=0, sticky='news')

    remIngCancelButton = Button(remIngFromPlatWin,
        # text="              Annuler              ",
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "red",
        relief = "groove",
        command= remIngFromPlatWin.destroy
        )
    remIngCancelButton.grid(row=2, column=1, sticky='news')

    remIngFromPlatWin.bind('<Return>', lambda event:remIngFromPlatDone(platName, ingName, remIngFromPlatWin, platIngList, platIngSelectFrame, platAllergenes))
    remIngFromPlatWin.bind('<Escape>', lambda event:remIngFromPlatWin.destroy())

    remIngFromPlatWin.after(1, lambda: remIngFromPlatWin.focus_force())
    remIngFromPlatWin.mainloop()
    return None

def editQteIngDone(platName, ingName, wSetQuantitesAdulteEntry, wSetQuantitesEnfantEntry, editQteIngWin, platIngList, platIngSelectFrame, platAllergenes):
    QteEnfantEntry = wSetQuantitesEnfantEntry.get()
    QteAdulteEntry = wSetQuantitesAdulteEntry.get()

    id_plat = askSQL("SELECT id_plat FROM plats WHERE nom = '%s'" % (platName.lower()))[0][0]
    id_ing = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]
    if platName == "":
        makeErrorWindow("Erreur système : Nom du plat vide.")
    elif id_plat == []:
        makeErrorWindow("Erreur système : Nom du plat inconnu.")
    elif id_ing == []:
        makeErrorWindow("Erreur système : Ingrédient inconnu : " + ingName)
    elif not QteEnfantEntry.replace('.','',1).isdigit():
        makeErrorWindow("Erreur : Valeur invalide pour la portion enfant : '" + QteEnfantEntry + "'")
    elif not QteAdulteEntry.replace('.','',1).isdigit():
        makeErrorWindow("Erreur : Valeur invalide pour la portion adulte : '" + QteAdulteEntry + "'")
    else:
        request = "UPDATE plats_ing SET qte_enfant = '%s', qte_adulte = '%s' WHERE id_plat = '%s' AND id_ing = '%s'" % (QteEnfantEntry, QteAdulteEntry, str(id_plat),str(id_ing))
        # print(request)
        setSQL(request)

        # for widget in platFrame.winfo_children():    #Reconstruction de tout
        #     widget.destroy()
        # makeplatFrame()
        editQteIngWin.destroy()
        platRegimeUpdate(platName, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes)

    return None

def editQteIng(platName, ingName, platIngList, platIngSelectFrame, platAllergenes):
    editQteIngWin= Toplevel(root)
    editQteIngWin.geometry("650x200")
    center(editQteIngWin)
    editQteIngWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie

    request = "SELECT unit FROM ingredients WHERE nom = '%s'" % (ingName.lower())
    # print(request)
    ingUnit = askSQL(request)[0][0]

    id_plat = askSQL("SELECT id_plat FROM plats WHERE nom = '%s'" % (platName.lower()))[0][0]
    id_ing = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]
    request = "SELECT qte_enfant FROM plats_ing WHERE id_plat = '%s' AND id_ing = '%s'" % (str(id_plat),str(id_ing))

    # print(request)
    prevQteEnfant = askSQL(request)[0][0]
    # print(prevQteEnfant)
    request = "SELECT qte_adulte FROM plats_ing WHERE id_plat = '%s' AND id_ing = '%s'" % (str(id_plat),str(id_ing))
    prevQteAdulte = askSQL(request)[0][0]

    editQteIngWin.grid_columnconfigure(6, weight=1)
    editQteIngWin.grid_columnconfigure(0, weight=1)
    editQteIngWin.grid_rowconfigure(6, weight=1)

    editQteIngWin.title("Éditer les quantités de " + ingName + " dans " + platName)
    label = Label(editQteIngWin, text="Éditer les quantités de " + ingName + " dans " + platName, bg="yellow", font = "8", bd=8)
    label.grid(row=0, column=0, columnspan = 7, sticky='nwe')


    setQuantitesLbl = Label(editQteIngWin, text="Nouvelles quantités : ", font = "Verdana 10 bold", relief=RAISED)
    setQuantitesLbl.grid(row=3, column=0, columnspan=7, sticky='news')

    setQuantitesLblEnfant = Label(editQteIngWin, text="\nEnfant : \n")
    setQuantitesLblEnfant.grid(row=4, column=1, columnspan=1, sticky='w')

    setQuantitesEnfantEntry = Entry(editQteIngWin, width = 5)
    setQuantitesEnfantEntry.grid(row=4, column=2, columnspan=1, sticky='w')
    setQuantitesEnfantEntry.insert(0, str(prevQteEnfant))

    setQuantitesUnitLbl1 = Label(editQteIngWin, text=ingUnit)
    setQuantitesUnitLbl1.grid(row=4, column=3, columnspan=1, sticky='w')


    setQuantitesLblAdulte = Label(editQteIngWin, text="\nAdulte : \n")
    setQuantitesLblAdulte.grid(row=4, column=4, columnspan=1, sticky='w')

    setQuantitesAdulteEntry = Entry(editQteIngWin, width = 5)
    setQuantitesAdulteEntry.grid(row=4, column=5, columnspan=1, sticky='w')
    setQuantitesAdulteEntry.insert(0, str(prevQteAdulte))

    setQuantitesUnitLbl2 = Label(editQteIngWin, text=ingUnit)
    setQuantitesUnitLbl2.grid(row=4, column=6, columnspan=1, sticky='w')

    setQuantitesDesc = Label(editQteIngWin, text="Les quantités sont à renseigner pour UNE personne.\nLe changement affectera toutes les variantes contenant cet ingrédient.", justify="left")
    setQuantitesDesc.grid(row=5, column=0, columnspan=7, sticky='news')

    #SAVE/DISCARD
    editQteIngSaveButton = Button(editQteIngWin,
        text="Confirmer",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:editQteIngDone(platName, ingName, setQuantitesAdulteEntry, setQuantitesEnfantEntry, editQteIngWin, platIngList, platIngSelectFrame, platAllergenes)
        )
    editQteIngSaveButton.grid(row=6, column=1, sticky='e')

    editQteIngCancelButton = Button(editQteIngWin,
        # text="              Annuler              ",
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= editQteIngWin.destroy
        )
    editQteIngCancelButton.grid(row=6, column=2, columnspan=3, sticky='')

    editQteIngWin.bind('<Return>', lambda event:editQteIngDone(platName, ingName, setQuantitesAdulteEntry, setQuantitesEnfantEntry, editQteIngWin, platIngList, platIngSelectFrame, platAllergenes))
    editQteIngWin.bind('<Escape>', lambda event:editQteIngWin.destroy())

    editQteIngWin.after(1, lambda: editQteIngWin.focus_force())
    editQteIngWin.mainloop()

    return None

def platRemDone(platList, nom, platRemWin):
    id_plat = askSQL("SELECT id_plat FROM plats WHERE nom = '%s'" % (nom.lower()))[0][0]
    setSQL("DELETE FROM plats WHERE nom = '%s'" % (nom.lower()))
    #Nettoyage BDD listes de courses
    request = "DELETE FROM listes WHERE id = %s AND is_ing = 0" % (id_plat)
    setSQL(request)
    updatePlatList(platList)
    platRemWin.destroy()
    return None

def platRem(platList, wnom):
    nom = wnom.cget("text")
    platRemWin= Toplevel(root)
    platRemWin.geometry("550x100")
    center(platRemWin)
    platRemWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie
    platRemWin.title("Supprimer un plat")

    platRemWin.grid_columnconfigure(0, weight=1, uniform = "aaa")
    platRemWin.grid_columnconfigure(1, weight=1, uniform = "aaa")
    platRemWin.grid_rowconfigure(1, weight=1)

    label = Label(platRemWin, text="Voulez-vous supprimer le plat " + nom + " ?", bg="yellow", font = "6", bd=8)
    label.grid(row=0, column=0, columnspan = 2, sticky='nwes')

    yesButton = Button(platRemWin,
        text="Oui",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "light green",
        relief = "groove",
        command= lambda:platRemDone(platList, nom, platRemWin)
        )
    yesButton.grid(row=1, column=0, sticky='news')

    noButton = Button(platRemWin,
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "red",
        relief = "groove",
        command= platRemWin.destroy
        )
    noButton.grid(row=1, column=1, sticky='news')


    platRemWin.bind('<Return>', lambda event:platRemDone(platList, nom, platRemWin))
    platRemWin.bind('<Escape>', lambda event:platRemWin.destroy())

    platRemWin.after(1, lambda: platRemWin.focus_force())
    platRemWin.mainloop()
    return None


def addIngToPlatDoneConfirm(platName, platRegimesVal, ingName, QteEnfantEntry, QteAdulteEntry, addIngToPlatWin, warnWin, platIngList, platIngSelectFrame, platAllergenes):
    if warnWin != 0:
        warnWin.destroy()
    id_plat = askSQL("SELECT id_plat FROM plats WHERE nom = '%s'" % (platName.lower()))[0][0]
    id_ing = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]

    for regime in platRegimesVal:
        query = "INSERT INTO plats_ing (id_plat, id_ing, regime, qte_enfant, qte_adulte) VALUES (%s, %s, %s, %s, %s)" % (id_plat, id_ing, regime, QteEnfantEntry, QteAdulteEntry)
        setSQL(query)

    # for widget in platFrame.winfo_children():    #Reconstruction de tout
    #     widget.destroy()
    # makeplatFrame()
    addIngToPlatWin.destroy()
    platRegimeUpdate(platName, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes)


    return None

def addIngToPlatDone(platName, regimeBools, wIngName, wQteEnfantEntry, wQteAdulteEntry, addIngToPlatWin, platIngList, platIngSelectFrame, platAllergenes):

    ingName = wIngName.get()
    QteEnfantEntry = wQteEnfantEntry.get()
    QteAdulteEntry = wQteAdulteEntry.get()
    platRegimesVal = ""
    platRegimesValList = []
    for avRegime in regimeBools.keys():
        if regimeBools[avRegime].get() == 1:
            platRegimesVal += str(getRegimeVal(avRegime))
            platRegimesValList.append(getRegimeVal(avRegime))
    # print(platRegimesVal)

    checkPlatExistsPayload = askSQL("SELECT id_plat FROM plats WHERE nom = '%s'" % (platName.lower()))
    checkIngExistsPayload = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingName.lower()))
    if platName == "":
        makeErrorWindow("Erreur système : Nom du plat vide.")
    elif checkPlatExistsPayload == []:
        makeErrorWindow("Erreur système : Nom du plat inconnu.")
    elif checkIngExistsPayload == []:
        makeErrorWindow("Erreur : Ingrédient inconnu : " + ingName)
    elif not QteEnfantEntry.replace('.','',1).isdigit():
        makeErrorWindow("Erreur : Valeur invalide pour la portion enfant : '" + QteEnfantEntry + "'")
    elif not QteAdulteEntry.replace('.','',1).isdigit():
        makeErrorWindow("Erreur : Valeur invalide pour la portion adulte : '" + QteAdulteEntry + "'")
    elif platRegimesVal == "":
        makeErrorWindow("Erreur : Vous devez sélectionner un moins une variante (Viande, végétarien, etc...).")
    else:
        #Check de si l'ingrédient correspond au régime
        ingMaxRegime = askSQL("SELECT regime FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]
        # print(ingMaxRegime)
        operationMaxRegime = max(platRegimesValList)
        # print(operationMaxRegime)
        if ingMaxRegime in [0,1,2,3] and operationMaxRegime > ingMaxRegime:
            # print("warn")
            #WARN d'un ingrédient potentiellement pas adapté à un régime
            warnWin= Toplevel(addIngToPlatWin)
            warnWin.grab_set()
            warnWin.title("Conflit de régimes alimentaires")
            # warnWin.grid_columnconfigure(0, weight=1)
            warn = "Avertissement : Votre ingrédient '" + ingName + "' convient au maximum au régime '" + getRegimeName(ingMaxRegime) + "'.\nCependant, vous demandez à l'ajouter à l'option '" + getRegimeName(operationMaxRegime) + "' du plat '" + platName + "'.\n\nSouhaitez-vous vraiment continuer ?\n"
            warnLbl = Label(warnWin, text=warn, justify="left", bd = 5, font="Verdana 10 bold",bg = "orange")
            warnLbl.grid(row=0, column=0, columnspan=2, sticky='news')

            confirmButton = Button(warnWin,
                text="Je sais ce que je fais !",
                font = "Verdana 10 bold",
                bd = 2,
                relief = "groove",
                command= lambda:addIngToPlatDoneConfirm(platName, platRegimesVal, ingName, QteEnfantEntry, QteAdulteEntry, addIngToPlatWin, warnWin, platIngList, platIngSelectFrame, platAllergenes)
                )
            confirmButton.grid(row=1, column=0, sticky='news')

            cancelButton = Button(warnWin,
                text="Annuler",
                font = "Verdana 10 bold",
                bd = 2,
                relief = "groove",
                command= warnWin.destroy
                )
            cancelButton.grid(row=1, column=1, sticky='news')

            warnWin.bind('<Escape>', lambda event: warnWin.destroy())
            center(warnWin)
            warnWin.after(1, lambda: warnWin.focus_force())
            warnWin.mainloop()

        else:
            addIngToPlatDoneConfirm(platName, platRegimesVal, ingName, QteEnfantEntry, QteAdulteEntry, addIngToPlatWin, 0, platIngList, platIngSelectFrame, platAllergenes)

    return None

def updateUnitLbl(Lbl1, Lbl2, ingChoiceEntry):
    payload = askSQL("SELECT unit FROM ingredients WHERE nom = '%s'" % (ingChoiceEntry.get().lower()))
    if len(payload) != 0:
        unit = payload[0][0]
    else:
        unit = ""
    Lbl1.config(text=unit)
    Lbl2.config(text=unit)
    return None

def addIngToPlat(wPlatName, platIngList, platIngSelectFrame, platAllergenes):
    addIngToPlatWin= Toplevel(root)
    addIngToPlatWin.geometry("750x300")
    center(addIngToPlatWin)
    addIngToPlatWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie

    platName = wPlatName.cget("text")

    addIngToPlatWin.grid_columnconfigure(6, weight=1)
    addIngToPlatWin.grid_rowconfigure(5, weight=1)

    addIngToPlatWin.title("Ajouter un ingrédient à " + platName)
    label = Label(addIngToPlatWin, text="Ajouter un ingrédient à " + platName, bg="yellow", font = "8", bd=8)
    label.grid(row=0, column=0, columnspan = 7, sticky='nwe')

    ingNameLbl = Label(addIngToPlatWin, text="Choisissez un ingrédient : ", font = "Verdana 10 bold", relief=RAISED)
    ingNameLbl.grid(row=1, column=0, sticky='new')

    ingUnit = ""

    ingsPayload = askSQL("SELECT nom FROM ingredients ORDER BY nom")
    ingList = []
    for ing in ingsPayload:
        ingList.append(ing[0])

    ingChoiceEntry = AutocompleteEntryListbox(
        addIngToPlatWin,
        width=30,
        font=("Verdana 10"),
        completevalues=ingList,
        allow_other_values=True,
        )
    ingChoiceEntry.grid(row=2, column=0, rowspan = 4, sticky='nw')


    #Définition des régimes :
    addIngToPlatSelectRegimesLbl = Label(addIngToPlatWin, text="Ajouter pour les régimes : ", font = "Verdana 10 bold", relief=RAISED)
    addIngToPlatSelectRegimesLbl.grid(row=1, column=1, columnspan=6, sticky='news')

    request = "SELECT regimes from plats WHERE nom = '%s'" % (platName.lower())
    # print(request)
    allowedRegimesVal = askSQL(request)[0][0]
    allowedRegimesNames = [getRegimeName(int(i)) for i in allowedRegimesVal]


    addIngToPlatSelectRegimesFrame = Frame(addIngToPlatWin)
    addIngToPlatSelectRegimesFrame.grid(row=2, column=1, columnspan=6, sticky='n')

    regimeCheckButtons = {}
    regimeBools = {}
    for regime in allowedRegimesNames:
        regimeBools[regime] = IntVar(value=1)
        regimeCheckButtons[regime] = Checkbutton(addIngToPlatSelectRegimesFrame, text = regime, font = "Verdana 10", variable = regimeBools[regime], onvalue = 1, offvalue = 0)
        regimeCheckButtons[regime].pack(side=LEFT)

    #Définition des quantités
    addIngToPlatSetQuantitesLbl = Label(addIngToPlatWin, text="Quantités : ", font = "Verdana 10 bold", relief=RAISED)
    addIngToPlatSetQuantitesLbl.grid(row=3, column=1, columnspan=6, sticky='new')

    addIngToPlatSetQuantitesLblEnfant = Label(addIngToPlatWin, text="\nEnfant : \n")
    addIngToPlatSetQuantitesLblEnfant.grid(row=4, column=1, columnspan=1, sticky='w')

    addIngToPlatSetQuantitesEnfant = Entry(addIngToPlatWin, width = 5)
    addIngToPlatSetQuantitesEnfant.grid(row=4, column=2, columnspan=1, sticky='w')

    addIngToPlatSetQuantitesUnitLbl1 = Label(addIngToPlatWin, text=ingUnit)
    addIngToPlatSetQuantitesUnitLbl1.grid(row=4, column=3, columnspan=1, sticky='w')


    addIngToPlatSetQuantitesLblAdulte = Label(addIngToPlatWin, text="\nAdulte : \n")
    addIngToPlatSetQuantitesLblAdulte.grid(row=4, column=4, columnspan=1, sticky='w')

    addIngToPlatSetQuantitesAdulte = Entry(addIngToPlatWin, width = 5)
    addIngToPlatSetQuantitesAdulte.grid(row=4, column=5, columnspan=1, sticky='w')

    addIngToPlatSetQuantitesUnitLbl2 = Label(addIngToPlatWin, text=ingUnit)
    addIngToPlatSetQuantitesUnitLbl2.grid(row=4, column=6, columnspan=1, sticky='w')

    addIngToPlatSetQuantitesDesc = Label(addIngToPlatWin, text="Entrez les quantités de cet ingrédient pour\nUNE personne, adulte et enfant.", justify="left")
    addIngToPlatSetQuantitesDesc.grid(row=5, column=1, columnspan=6, sticky='new')



    #SAVE/DISCARD
    finishButtonsFrame= Frame(addIngToPlatWin)
    finishButtonsFrame.grid(row=5, column=1, columnspan=6, sticky='')

    addIngToPlatEditSaveButton = Button(finishButtonsFrame,
        text="Confirmer",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:addIngToPlatDone(platName, regimeBools, ingChoiceEntry, addIngToPlatSetQuantitesEnfant, addIngToPlatSetQuantitesAdulte, addIngToPlatWin, platIngList, platIngSelectFrame, platAllergenes)
        )
    addIngToPlatEditSaveButton.grid(row=0, column=0, sticky='n')

    addIngToPlatEditCancelButton = Button(finishButtonsFrame,
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= addIngToPlatWin.destroy
        )
    addIngToPlatEditCancelButton.grid(row=0, column=1, sticky='n')


    ingChoiceEntry.listbox.bind('<ButtonRelease-1>', lambda event:updateUnitLbl(addIngToPlatSetQuantitesUnitLbl1, addIngToPlatSetQuantitesUnitLbl2, ingChoiceEntry))
    ingChoiceEntry.listbox.bind('<KeyRelease>', lambda event:updateUnitLbl(addIngToPlatSetQuantitesUnitLbl1, addIngToPlatSetQuantitesUnitLbl2, ingChoiceEntry))
    ingChoiceEntry.entry.bind('<KeyRelease>', lambda event:updateUnitLbl(addIngToPlatSetQuantitesUnitLbl1, addIngToPlatSetQuantitesUnitLbl2, ingChoiceEntry))

    addIngToPlatWin.bind('<Return>', lambda event:addIngToPlatDone(platName, regimeBools, ingChoiceEntry, addIngToPlatSetQuantitesEnfant, addIngToPlatSetQuantitesAdulte, addIngToPlatWin, platIngList, platIngSelectFrame, platAllergenes))
    addIngToPlatWin.bind('<Escape>', lambda event:addIngToPlatWin.destroy())

    addIngToPlatWin.after(1, lambda: addIngToPlatWin.focus_force())
    addIngToPlatWin.mainloop()
    return None


def updatePlatList(platList):
    platList.delete(0,END)
    platpayload = askSQL("SELECT nom FROM plats ORDER BY nom")

    for i in range(len(platpayload)):
        platList.insert(i,platpayload[i][0].capitalize())

    return None

def platAddEditDone(wgNameEntry, wgOrdreEntry, regimeBools, platAddWin, editing, prevName, platList):
    platNameStr = wgNameEntry.get().lower()
    platOrdreStr = wgOrdreEntry.get()
    platOrdreVal = getOrdreVal(platOrdreStr)
    platRegimesVal = ""

    for regime in regimeList:
        if regimeBools[regime].get() == 1:
            platRegimesVal += str(getRegimeVal(regime))
    # print(platRegimesVal)


    if platNameStr == "":
        makeErrorWindow("Erreur : Vous devez donner un nom au plat.")
    elif platRegimesVal == "":
        makeErrorWindow("Erreur : Vous devez sélectionner un moins une variante (Viande, végétarien, etc...).")
    else:
        request = ("SELECT id_plat FROM plats WHERE nom = '%s'" % (platNameStr))
        existsCheck = askSQL(request)
        if existsCheck != []:
            makeErrorWindow("Erreur : Un plat avec ce nom existe déjà.")
        else:
            insertion = ("INSERT INTO plats (nom, ordre, regimes) VALUES ('%s', %s, '%s')" % (platNameStr, str(platOrdreVal), platRegimesVal))
            # print(insertion)
            setSQL(insertion)

    updatePlatList(platList)
    platAddWin.destroy()

    return None

def platAddEdit(platList, prevName):
    platAddWin= Toplevel(root)
    platAddWin.geometry("550x300")
    center(platAddWin)
    platAddWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie

    editing = 0

    platAddWin.grid_columnconfigure(3, weight=1)
    platAddWin.grid_rowconfigure(5, weight=2)

    if prevName != "":
        editing = 1
        platAddWin.title("Éditer les paramètres d'un plat")
        label = Label(platAddWin, text="Éditer les paramètres d'un plat\n", bg="yellow", font = "8", bd=8)
    else:
            platAddWin.title("Ajouter un plat dans la base de données")
            label = Label(platAddWin, text="Ajouter un plat dans la base de données\n", bg="yellow", font = "8", bd=8)

    label.grid(row=0, column=0, columnspan = 4, sticky='nwe')

    platNameLbl = Label(platAddWin, text="    Nom du plat : \n", font="Verdana 10 bold")
    platNameLbl.grid(row=1, column=0, sticky='nw')
    platNameEntry = Entry(platAddWin, width = 30)
    platNameEntry.grid(row=1, column=1, sticky='nw')

    platOrdreLbl = Label(platAddWin, text="        Type : ", font="Verdana 10 bold")
    platOrdreLbl.grid(row=1, column=2, sticky='nw')
    platOrdreEntry = ttk.Combobox(platAddWin, values = ordreList, state="readonly")
    platOrdreEntry.set("Autre")
    platOrdreEntry.grid(row=1, column=3, sticky='nw')

    #Définition des régimes :
    platAddSelectRegimesLbl = Label(platAddWin, text="Variantes du plat : ", font = "Verdana 15 bold", relief=RAISED)
    platAddSelectRegimesLbl.grid(row=2, column=0, columnspan=4, sticky='news')

    platAddSelectRegimesFrame = Frame(platAddWin)
    platAddSelectRegimesFrame.grid(row=3, column=0, columnspan=4, sticky='news')

    regimeCheckButtons = {}
    regimeBools2 = {}
    for regime in regimeList:
        regimeBools2[regime] = IntVar(value=1)
        regimeCheckButtons[regime] = Checkbutton(platAddSelectRegimesFrame, text = regime, font = "Verdana 10 bold", variable = regimeBools2[regime], onvalue = 1, offvalue = 0)
        regimeCheckButtons[regime].pack(side=LEFT)
    # print(regimeBools2)

    platAddSelectRegimesDesc = Label(platAddWin, text="""\nSélectionnez au moins une variante du plat.\nNote : si la recette est la même pour deux régimes, ne sélectionner pas les deux !\nPar exemple, pas besoin d'une option "Viande" pour une salade de fruits : \nla variante "Végétalien" suffira pour tous les régimes.""", justify="left")
    platAddSelectRegimesDesc.grid(row=4, column=0, columnspan=4, sticky='w')

    #SAVE/DISCARD
    platAddEditSaveButton = Button(platAddWin,
        text="Confirmer",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:platAddEditDone(platNameEntry, platOrdreEntry, regimeBools2, platAddWin, editing, prevName, platList)
        )
    platAddEditSaveButton.grid(row=5, column=1, sticky='e')

    platAddEditCancelButton = Button(platAddWin,
        # text="              Annuler              ",
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= platAddWin.destroy
        )
    platAddEditCancelButton.grid(row=5, column=2, columnspan=2, sticky='')



    platAddWin.bind('<Return>', lambda event:platAddEditDone(platNameEntry, platOrdreEntry, regimeBools2, platAddWin, editing, prevName, platList))
    platAddWin.bind('<Escape>', lambda event:platAddWin.destroy())

    platAddWin.after(1, lambda: platAddWin.focus_force())
    platAddWin.mainloop()
    return None

def platSelectIngUpdate(platName, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes):
    for widget in platIngSelectFrame.winfo_children():    #Clear de la frame
        widget.destroy()

    if platIngList.item(platIngList.selection())['values'] == "":
        return None
    ingName = platIngList.item(platIngList.selection())['values'][0]

    selectIngNameLbl = Label(platIngSelectFrame, text="Ingrédient sélectionné :   ", justify = "right")
    selectIngNameLbl.grid(row=0, column=0, sticky='nes')
    selectIngName = Label(platIngSelectFrame, text=ingName, font="Verdana 10 bold", justify = "left")
    selectIngName.grid(row=0, column=1, sticky='nws')
    selectIngAllergenesLbl = Label(platIngSelectFrame, text="Allergènes :   ", justify = "right")
    selectIngAllergenesLbl.grid(row=1, column=0, sticky='new')
    selectIngAllergenes = Label(platIngSelectFrame, text="", justify = "left")
    selectIngAllergenes.grid(row=1, column=1, sticky='news')


    ingInfoAllergenes = askSQL("SELECT allergenes FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]
    # print(ingInfoAllergenes)
    allergenes = ""
    if ingInfoAllergenes == None:
        allergenes = "Néant"
    else:
        ingInfoAllergenes = ingInfoAllergenes[1::]  #On yeet le 1 du début
        for pos in range(len(ingInfoAllergenes)//4):
            packet = int(ingInfoAllergenes[4*pos:4*pos+4])
            # print(packet)
            if packet >= 1000:
                allergenes += "Traces de " + allergeneList[packet-1000] + ",\n"
            else:
                allergenes += allergeneList[packet] + ",\n"
        allergenes = allergenes.strip(",\n") + "\n\n"

    selectIngAllergenes.config(text = allergenes)

    editIngQteButton = Button(
        platIngSelectFrame,
        text="Éditer les quantités",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "yellow",
        # relief = "groove",
        command= lambda:editQteIng(platName, ingName, platIngList, platIngSelectFrame, platAllergenes)
        )
    editIngQteButton.grid(row=0, column=2, sticky='new')

    remIngFromPlatButton = Button(
        platIngSelectFrame,
        text="Supprimer du plat",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "red",
        # relief = "groove",
        command= lambda:remIngFromPlat(platName, ingName, platIngList, platIngSelectFrame, platAllergenes)
        )
    remIngFromPlatButton.grid(row=1, column=2, sticky='new')


    return None

def platRegimeUpdate(platName, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes):
    # print(vRadioRegime.get())
    selectedRegime = int(vRadioRegime.get())
    # print(selectedRegime)
    # print(type(selectedRegime))

    query = "SELECT id_ing,qte_enfant,qte_adulte FROM plats_ing INNER JOIN plats ON plats_ing.id_plat = plats.id_plat WHERE (nom = '%s' AND regime = %s)" % (platName.lower(), selectedRegime)
    # print(query)
    infosJoin = askSQL(query)
    platAllergenesText = ""
    platAllergenesCodes = []
    # print(infosJoin)
    for item in platIngList.get_children():
        platIngList.delete(item)
    for payload in infosJoin:
        id_ing = payload[0]
        nomUnitIng = askSQL("SELECT nom, unit FROM ingredients WHERE id_ing = %s" % id_ing)
        platIngList.insert('', 'end', text="1", values=(nomUnitIng[0][0].capitalize(), str(payload[1]) + " " + nomUnitIng[0][1], str(payload[2]) + " " + nomUnitIng[0][1]))

        #Allergènes dans le plat
        ingInfoAllergenes = askSQL("SELECT allergenes FROM ingredients WHERE id_ing = %s" % (id_ing))[0][0]
        # print(ingInfoAllergenes)
        if ingInfoAllergenes != None:
            ingInfoAllergenes = ingInfoAllergenes[1::]  #On yeet le 1 du début
            for pos in range(len(ingInfoAllergenes)//4):
                packet = int(ingInfoAllergenes[4*pos:4*pos+4])
                if packet not in platAllergenesCodes:
        #         print(packet)
                    platAllergenesCodes.append(packet)
                    if packet >= 1000:
                        platAllergenesText += "traces de " + allergeneList[packet-1000] + ",\n"
                    else:
                        platAllergenesText += allergeneList[packet] + ",\n"
    platAllergenesText = platAllergenesText.strip(",\n").capitalize()
    # print(platAllergenesText)
    platAllergenes.config(text = platAllergenesText)

    platIngList.bind('<<TreeviewSelect>>', lambda event:platSelectIngUpdate(platName, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes))

    return None

def platSelect(event, platName, platOrdre, platAllergenes, platRegimeRadioFrame, platIngList, platIngSelectFrame):
    global vRadioRegime

    w = event.widget
    if w.curselection() == ():
        return None
    index = int(w.curselection()[0]) #Index dans la ListBox
    nom = w.get(index)  #Nom dans la liste
    # print(nom)
    # print('You selected item %d: "%s"' % (index, nom))

    infoPayload = askSQL("SELECT ordre,regimes FROM plats WHERE nom = '%s'" % (nom.lower()))[0]
    infoOrdre = getOrdreName(infoPayload[0])
    infoRegimes = infoPayload[1]

    platName.config(text=nom)
    platOrdre.config(text=infoOrdre)

    for widget in platRegimeRadioFrame.winfo_children():    #Destruction des radios précédentes
        widget.destroy()

    if len(infoRegimes) == 0:
        makeErrorWindow("Erreur système : ce plat n'est disponible pour aucun régime.")
    else:
        vRadioRegime = StringVar()
        vRadioRegime.set(getRegimeName(int(infoRegimes[-1])))
        radioRegimes = {}
        for j in infoRegimes:
            i = int(j)
            # print(getRegimeName(i))
            radioRegimes[i] = Radiobutton(platRegimeRadioFrame, text=getRegimeName(i), variable=vRadioRegime, value=i, tristatevalue=0, command=lambda:platRegimeUpdate(nom, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes))      #Création radioButton
            radioRegimes[i].pack(anchor = W, side=LEFT)

        # print(vRadioRegime.get())
        platFrame.after(1, lambda: radioRegimes[int(infoRegimes[-1])].select())
        platFrame.after(1, lambda: platRegimeUpdate(nom, vRadioRegime, platIngList, platIngSelectFrame, platAllergenes))     #Affichage des ingrédients du régime par défaut lors de la sélection

    return None

def makeplatFrame():
    global platFrame
    platFrame = Frame(master=container, borderwidth=5, relief=GROOVE, width=700, height=500)
    platFrame.grid(row=0, column=0, sticky='news')

    platFrame.grid_rowconfigure(9, weight=1)
    platFrame.grid_columnconfigure(0, weight=1, uniform="fred")
    # platFrame.grid_columnconfigure(2, weight=1, uniform="fred")
    platFrame.grid_columnconfigure(3, weight=1, uniform="fred")


    #LISTE des plats
    label = Label(platFrame, text="Gérer les plats de la base de données", bg="yellow", font = "10")
    label.grid(row=0, column=0, columnspan = 4, sticky='nwe')

    platListName = Label(platFrame, text="Liste des plats enregistrés", relief=RAISED)
    platListName.grid(row=1, column=0, sticky='new')

    platpayload = askSQL("SELECT nom FROM plats ORDER BY nom")

    scrollPlatList = Scrollbar(platFrame)
    scrollPlatList.grid(row=2, column=1, rowspan=8, sticky='nsw')
    platList = Listbox(platFrame, yscrollcommand = scrollPlatList.set, width=30)
    for i in range(len(platpayload)):
        platList.insert(i,platpayload[i][0].capitalize())
    platList.grid(row=2, column=0, rowspan=8, sticky='news')

    #INFOS sur un plat
    platSelectName = Label(platFrame, text="Infos sur le plat sélectionné", relief=RAISED)
    platSelectName.grid(row=1, column=2, columnspan=2, sticky='new')

    platNameLbl = Label(platFrame, text="Nom : ")
    platNameLbl.grid(row=2, column=2, sticky='nw')
    platName = Label(platFrame, text="")
    platName.grid(row=2, column=3, sticky='nw')

    platOrdreLbl = Label(platFrame, text="Type : ")
    platOrdreLbl.grid(row=3, column=2, sticky='nw')
    platOrdre = Label(platFrame, text="")
    platOrdre.grid(row=3, column=3, sticky='nw')

    platAllergenesLbl = Label(platFrame, text="Allergènes : \n\n\n\n\n")
    platAllergenesLbl.grid(row=4, column=2, sticky='nw')
    platAllergenes = Label(platFrame, text="", justify = "left")
    platAllergenes.grid(row=4, column=3, sticky='nw')

    platOptionsFrame = Frame(platFrame)
    platOptionsFrame.grid(row=5, column=2, columnspan=2, sticky='news')
    addPlatButton = Button(
        platOptionsFrame,
        text="Créer un plat",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:platAddEdit(platList, '')
        )
    addPlatButton.grid(row=0, column=0, sticky='n')

    addIngToPlatButton = Button(
        platOptionsFrame,
        text="Ajouter un ingrédient au plat",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "yellow",
        relief = "groove",
        command= lambda:addIngToPlat(platName, platIngList, platIngSelectFrame, platAllergenes)
        )
    addIngToPlatButton.grid(row=0, column=1, sticky='n')

    removePlatButton = Button(
        platOptionsFrame,
        text="Supprimer ce plat",
        font = "Verdana 10 underline",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= lambda:platRem(platList, platName)
        )
    removePlatButton.grid(row=0, column=2, sticky='n')

    platIngViewLbl = Label(platFrame, text="Régimes disponibles : ", relief=RAISED)
    platIngViewLbl.grid(row=6, column=2, columnspan=2, sticky='new')

    platRegimeRadioFrame = Frame(platFrame)
    platRegimeRadioFrame.grid(row=7, column=2, columnspan=2, sticky='news')

    platIngListFrame = Frame(platFrame)
    platIngListFrame.grid(row=8, column=2, columnspan=2, sticky='news')

    scrollPlatIngList = Scrollbar(platIngListFrame)
    scrollPlatIngList.grid(row=0, column=1, sticky='nsw')
    platIngList = ttk.Treeview(platIngListFrame, column=(0,1,2), show='headings', height=6, yscrollcommand = scrollPlatIngList.set)
    platIngList.column(0, anchor="e", width=300, stretch=NO)
    platIngList.heading(0, text="Ingrédient")
    platIngList.column(1, anchor="w", width=70, stretch=NO)
    platIngList.heading(1, text="Qté enfant")
    platIngList.column(2, anchor="w", width=70, stretch=NO)
    platIngList.heading(2, text="Qté adulte")

    platIngList.grid(row=0, column=0, sticky='news')

    platIngSelectFrame = Frame(platFrame, borderwidth=2)
    platIngSelectFrame.grid(row=9, column=2, columnspan=2, sticky='news')

    # wpf = platIngSelectFrame.winfo_children()
    # for w in wpf:
    #     print(w)

    platList.bind('<<ListboxSelect>>', lambda event:platSelect(event, platName, platOrdre, platAllergenes, platRegimeRadioFrame, platIngList, platIngSelectFrame))
    platList.select_set(0)
    platList.event_generate("<<ListboxSelect>>")
    platList.bind('<Delete>', lambda event:platRem(platList, platName))

    platFrame.after(10, lambda: platList.focus_force())
    return None

def raiseplat():
    platFrame.tkraise()

##Gérer les personnes
def saveVarsToBDD(valEntries, valsSaveStateLbl):

    for taille in tailleList:
        for regime in regimeList:
            # print(valEntries[taille + regime].get())
            val = valEntries[taille + regime].get()
            # print(val)
            if not val.isdigit():
                makeErrorWindow("Erreur : " + val + " n'est pas un nombre entier.")
                return None

    for taille in tailleList:
        for regime in regimeList:
            val = valEntries[taille + regime].get()
            payloadTest = askSQL("SELECT val FROM pers WHERE regime = %s AND taille = %s" % (getRegimeVal(regime), getTailleVal(taille)))
            # print(payloadTest)
            if payloadTest == []:
                request = "INSERT INTO pers (val, regime, taille) VALUES (%s, %s, %s)" % (val, getRegimeVal(regime), getTailleVal(taille))
            else:
                request = "UPDATE pers SET val = %s WHERE regime = %s AND taille = %s" % (val, getRegimeVal(regime), getTailleVal(taille))

            # print(request)
            setSQL(request)
    valsSaveStateLbl.config(text = "Aucun changement non sauvegardé")
    updateIngsInShopListList(ingsInShopListList)

    return None

def setAllEntriesTo0(valEntries, valsSaveStateLbl):
    for taille in tailleList:
        for regime in regimeList:
            valEntries[taille + regime].delete(0,END)
            valEntries[taille + regime].insert(0,"0")
    valsSaveStateLbl.config(text = "Attention : changements non sauvegardés")
    return None

def updatePersValsEntries(valEntries, valsSaveStateLbl, valEntriesVars):

    for taille in tailleList:
        for regime in regimeList:
            request = "SELECT val FROM pers WHERE regime = %s AND taille = %s" % (getRegimeVal(regime), getTailleVal(taille))
            # print(request)
            payload = askSQL(request)
            if payload == []:
                val = 0
            else:
                val = payload[0][0]
            valEntries[taille + regime].delete(0,END)
            valEntries[taille + regime].insert(0,val)
            valEntriesVars[taille + regime].trace_add('write', lambda a,b,c:valsSaveStateLbl.config(text="Attention : changements non sauvegardés"))

    valsSaveStateLbl.config(text = "Aucun changement non sauvegardé")
    return None

def makepersFrame():
    global persFrame
    persFrame = Frame(master=listeFrame, borderwidth=5, relief=GROOVE)
    persFrame.grid(row=2, column=1, columnspan=2, sticky='news')

    persFrame.grid_rowconfigure(4, weight=1)
    for c in [1,2,3,4]:
        persFrame.grid_columnconfigure(c, weight=1, uniform="fred")


    label = Label(persFrame, text="Modifier la liste des personnes", bg="yellow", font = "10")
    label.grid(row=0, column=0, columnspan = 5, sticky='nwe')

    #Labels des régimes et des tailles
    regimeLbls = {}
    for regime in regimeList:
        regimeLbls[regime] = Label(persFrame, text=regime)
        regimeLbls[regime].grid(row=2, column=1+getRegimeVal(regime), sticky='news')

    tailleLbls = {}
    for taille in tailleList:
        tailleLbls[taille] = Label(persFrame, text=taille)
        tailleLbls[taille].grid(row=3+getTailleVal(taille), column=0, sticky='news')

    valsSaveStateLbl = Label(persFrame, text="", font = "Verdana 7")
    valsSaveStateLbl.grid(row=5, column=0, columnspan=5, sticky="news")

    valEntries = {}
    valEntriesVars = {}
    for taille in tailleList:
        for regime in regimeList:
            valEntriesVars[taille + regime] = StringVar()
            valEntriesVars[taille + regime].trace_add('write', lambda a,b,c:valsSaveStateLbl.config(text="Attention : changements non sauvegardés"))
            valEntries[taille + regime] = Entry(persFrame, width = 5, textvariable=valEntriesVars[taille + regime])
            valEntries[taille + regime].grid(row=3+getTailleVal(taille), column=1+getRegimeVal(regime), sticky='news')

# valsSaveStateLbl.config(text="Attention : changements non sauvegardés")

    optionsButtonsFrame = Frame(persFrame)
    optionsButtonsFrame.grid(row=6, column=0, columnspan = 5, sticky='ns')

    saveInDBButton = Button(
        optionsButtonsFrame,
        text="Sauvegarder",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "green",
        relief = "groove",
        command= lambda:saveVarsToBDD(valEntries, valsSaveStateLbl)
        )
    saveInDBButton.grid(row=0, column=0, sticky='news')

    cancelChangesButton = Button(
        optionsButtonsFrame,
        text="Annuler changements",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= lambda:updatePersValsEntries(valEntries, valsSaveStateLbl, valEntriesVars)
        )
    cancelChangesButton.grid(row=0, column=1, sticky='news')

    setTo0Button = Button(
        optionsButtonsFrame,
        text="Mettre tout à 0",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "orange",
        relief = "groove",
        command= lambda:setAllEntriesTo0(valEntries, valsSaveStateLbl)
        )
    setTo0Button.grid(row=0, column=2, sticky='news')

    updatePersValsEntries(valEntries, valsSaveStateLbl, valEntriesVars)

    valsSaveStateLbl.config(text="Aucun changement non sauvegardé")
    return None

# def raisepers():
#     persFrame.tkraise()


##Assembler une liste de course
def exportListeCoursesConfirm(file_name, ingsInShopListList, exportShopListNameEntry, exportShopListSucces, warnWin, includeAllergenes):
    if warnWin != 0:
        warnWin.destroy()
    f = open(file_name, "w")
    f.write("----- Liste de courses -----\n\n")
    maxlen = 0
    maxlenUnit = 0
    for item in ingsInShopListList.get_children():
        # print(ingsInShopListList.item(item)["values"])
        ingName = str(ingsInShopListList.item(item)["values"][0])
        if len(ingName) > maxlen:
            maxlen = len(ingName)

        unitName = str(ingsInShopListList.item(item)["values"][0])
        if len(unitName) > maxlenUnit:
            maxlenUnit = len(unitName)

    maxlen += 2
    # maxlenUnit += 2

    for item in ingsInShopListList.get_children():
        ingName = str(ingsInShopListList.item(item)["values"][0])
        ingStr = ingName + (maxlen-len(ingName))*" "
        unitName = str(ingsInShopListList.item(item)["values"][1])
        unitStr = unitName + (maxlenUnit-len(unitName))*" "
        line = ""
        if includeAllergenes.get() == 1:
            allergenesStr = ""
            ingInfoAllergenes = askSQL("SELECT allergenes FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]
            # print(ingInfoAllergenes)
            if ingInfoAllergenes != None:
                ingInfoAllergenes = ingInfoAllergenes[1::]  #On yeet le 1 du début
                platAllergenesCodes = []
                for pos in range(len(ingInfoAllergenes)//4):
                    packet = int(ingInfoAllergenes[4*pos:4*pos+4])
                    if packet not in platAllergenesCodes:
            #         print(packet)
                        platAllergenesCodes.append(packet)
                        if packet >= 1000:
                            allergenesStr += "traces de " + allergeneList[packet-1000] + ", "
                        else:
                            allergenesStr += allergeneList[packet] + ", "
            allergenesStr = allergenesStr.strip(",\n").capitalize()
            # print(allergenesStr)
            line = ingStr + " " + unitStr + " " + allergenesStr.strip(", ") + "\n"
        else:
            line = ingStr + " " + unitStr.strip(" ") + "\n"


        f.write(line)

    f.close()

    exportShopListSucces.config(text="SUCCES.\nLa liste de courses a\nbien été exportée.")
    root.after(5000, lambda: exportShopListSucces.config(text=""))
    return None

def exportListeCourses(ingsInShopListList, exportShopListNameEntry, exportShopListSucces, includeAllergenes):
    if exportShopListNameEntry.get() == "":
        makeErrorWindow("Erreur : Nom de fichier vide.")
        return None
    file_name = exportShopListNameEntry.get() + exportExtension
    for c in file_name:
        if c in """<>:"/\\|?*""":
            makeErrorWindow("Erreur : Nom de fichier invalide.")
            return None
    # print(file_name)
    if os.path.isfile(file_name):
        # print("warn")
        #WARN override d'un fichier existant
        warnWin= Toplevel(listeFrame)
        warnWin.grab_set()
        warnWin.title("Fichier déjà existant")
        # warnWin.grid_columnconfigure(0, weight=1)
        warn = "Avertissement : Le fichier '" + file_name + "' existe déjà.\nVoulez-vous l'écraser ?"
        warnLbl = Label(warnWin, text=warn, justify="left", bd = 5, font="Verdana 10 bold",bg = "orange")
        warnLbl.grid(row=0, column=0, columnspan=2, sticky='news')

        confirmButton = Button(warnWin,
            text="Oui",
            font = "Verdana 10 bold",
            bd = 2,
            relief = "groove",
            command= lambda: exportListeCoursesConfirm(file_name, ingsInShopListList, exportShopListNameEntry, exportShopListSucces, warnWin, includeAllergenes)
            )
        confirmButton.grid(row=1, column=0, sticky='news')

        cancelButton = Button(warnWin,
            text="Annuler",
            font = "Verdana 10 bold",
            bd = 2,
            relief = "groove",
            command= warnWin.destroy
            )
        cancelButton.grid(row=1, column=1, sticky='news')

        warnWin.bind('<Escape>', warnWin.destroy)
        center(warnWin)
        warnWin.after(1, lambda: warnWin.focus_force())
        warnWin.mainloop()
    else:
        exportListeCoursesConfirm(file_name, ingsInShopListList, exportShopListNameEntry, exportShopListSucces, 0, includeAllergenes)

    return None

def updateIngsInShopListList(ingsInShopListList):
    selectedPlats = askSQL("SELECT * FROM listes WHERE is_ing = 0")
    # print(selectedPlats)
    selectedIngs = askSQL("SELECT * FROM listes WHERE is_ing = 1")
    # print(selectedIngs)

    for line in selectedPlats:
        id_plat = int(line[2])
        for regime in regimeList:
            regimeVal = getRegimeVal(regime)
            regimeForRegime = line[5 + regimeVal]
            # print(regimeForRegime)
            if regimeForRegime != -3:
                regimeCode = [0,0,0,0]
                regimeCode[regimeVal] = 1
                query = "SELECT id_ing,qte_enfant,qte_adulte FROM plats_ing INNER JOIN plats ON plats_ing.id_plat = plats.id_plat WHERE (plats.id_plat = '%s' AND regime = %s)" % (id_plat, regimeForRegime)
                platIngList = askSQL(query)
                # print(platIngList)
                for ingTuple in platIngList:
                    # print(ingTuple[0])
                    ingCode = (0, 1, ingTuple[0], ingTuple[1], ingTuple[2]) + tuple(regimeCode)
                    # print(ingCode)
                    selectedIngs.append(ingCode)

    # print(selectedIngs)

    #construction liste des gens
    payload = askSQL("SELECT * FROM pers")
    # print(payload)
    listePers = {}
    for i in payload:
        listePers[getTailleName(i[2]) + getRegimeName(i[1])] = int(i[0])
    # print(listePers)

    #Liste des ingrédients présents dans la liste de courses
    totalQtes = {}

    for line in selectedIngs:
        # print(line)
        id_ing = int(line[2])
        # print(id_ing)
        if id_ing not in list(totalQtes.keys()):
            request = "SELECT nom FROM ingredients WHERE id_ing = %s" % (id_ing)
            # print(request)

            ingName = askSQL(request)[0][0]
            # print(ingName)
            totalQtes[ingName] = 0

    # print(list(totalQtes.keys()))
    for ingName in list(totalQtes.keys()):
        id_ing = getIngVal(ingName)
        for line in selectedIngs:
            if id_ing == int(line[2]):
                qteEnfant = line[3]
                qteAdulte = line[4]
                totalQte = 0
                regimes = line[5:9]

                for regimeVal in range(len(regimes)):
                    # print(regimes[regimeVal])
                    if regimes[regimeVal] == 1:
                        totalQte += qteEnfant * listePers["Enfant" + getRegimeName(regimeVal)]
                        totalQte += qteAdulte * listePers["Adulte" + getRegimeName(regimeVal)]
                totalQtes[ingName] += totalQte
    # print(totalQtes)


    for item in ingsInShopListList.get_children():
        ingsInShopListList.delete(item)

    for ingName in list(totalQtes.keys()):
        unitIng = askSQL("SELECT unit FROM ingredients WHERE nom = '%s'" % ingName)[0][0]
        qte = totalQtes[ingName]
        ingsInShopListList.insert('', 'end', text="1", values=(ingName.capitalize(), str(qte) + " " + unitIng))

    #Allergènes dans la liste de courses
    platAllergenesCodes = []
    listeCoursesAllergenesText = ""
    for ingName in list(totalQtes.keys()):


        ingInfoAllergenes = askSQL("SELECT allergenes FROM ingredients WHERE nom = '%s'" % (ingName))[0][0]
        # print(ingInfoAllergenes)
        if ingInfoAllergenes != None:
            ingInfoAllergenes = ingInfoAllergenes[1::]  #On yeet le 1 du début
            for pos in range(len(ingInfoAllergenes)//4):
                packet = int(ingInfoAllergenes[4*pos:4*pos+4])
                if packet not in platAllergenesCodes:
        #         print(packet)
                    platAllergenesCodes.append(packet)
                    if packet >= 1000:
                        listeCoursesAllergenesText += "traces de " + allergeneList[packet-1000] + ",\n"
                    else:
                        listeCoursesAllergenesText += allergeneList[packet] + ",\n"
    listeCoursesAllergenesText = listeCoursesAllergenesText.strip(",\n").capitalize()
    # print(listeCoursesAllergenesText)
    allergenesInShopListList.config(text = listeCoursesAllergenesText)

    return None

def updateItemsInShopListList(itemsInShopListList, ingsInShopListList):
    itemsInShopListList.delete(0,END)

    # for i in range(len(ingpayload)):
    #     ingList.insert(i,ingpayload[i][0].capitalize())
    query = "SELECT id,is_ing FROM listes ORDER BY id_list"
    payload = askSQL(query)
    # print(payload)
    if payload == []:
        return None

    for packet in payload:
        if packet[1] == 1:
            query = "SELECT nom FROM ingredients WHERE id_ing = %s" % packet[0]
            # print(query)
            ingName = askSQL(query)
            if ingName == []:
                pass
            else:
                ingName = ingName[0][0].capitalize()
                # print(ingName)
                itemsInShopListList.insert("end",ingName)
                itemsInShopListList.itemconfig("end", {'bg':'light blue'})
        else:
            query = "SELECT nom FROM plats WHERE id_plat = %s" % packet[0]
            # print(query)
            platName = askSQL(query)
            if platName == []:
                pass
            else:
                platName = platName[0][0].capitalize()
                # print(platName)
                itemsInShopListList.insert("end",platName)
    updateIngsInShopListList(ingsInShopListList)
    return None

def remItemFromShopListDone(remItemFromShopListWin, itemsInShopListList, ingsInShopListList, all):
    if all:
        setSQL("DELETE FROM listes")
    else:
        line_number = itemsInShopListList.curselection()[0]
        print(line_number + 1)

        query = "SELECT id_list FROM listes ORDER BY id_list LIMIT %s" % str(line_number + 1)
        payload = askSQL(query)
        # print(payload)
        if payload != []:

            request = "DELETE FROM listes WHERE id_list = %s" % str(payload[-1][0])
            print(request)
            setSQL(request)

    updateItemsInShopListList(itemsInShopListList, ingsInShopListList)
    remItemFromShopListWin.destroy()
    return None

def remItemFromShopList(itemsInShopListList, ingsInShopListList, all=0):

    if not all:
        selectedPos = itemsInShopListList.curselection()
        if selectedPos == ():
            makeErrorWindow("Erreur : Aucun item sélectionné.")
            return None
    # nom = wnom.cget("text")
    remItemFromShopListWin= Toplevel(root)
    remItemFromShopListWin.geometry("650x100")
    center(remItemFromShopListWin)
    remItemFromShopListWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie


    remItemFromShopListWin.grid_columnconfigure(0, weight=1, uniform = "bbb")
    remItemFromShopListWin.grid_columnconfigure(1, weight=1, uniform = "bbb")
    remItemFromShopListWin.grid_rowconfigure(1, weight=1)

    if all:
        remItemFromShopListWin.title("Nettoyer la liste")
        label = Label(remItemFromShopListWin, text="Voulez-vous reset la liste de courses ?", bg="yellow", font = "6", bd=8)
        label.grid(row=0, column=0, columnspan = 2, sticky='nwes')
    else:
        itemName = itemsInShopListList.get(itemsInShopListList.curselection()[0])
        # print(itemName)

        remItemFromShopListWin.title("Retirer un item")
        label = Label(remItemFromShopListWin, text="Voulez-vous retirer " + itemName + " de la liste de courses ?", bg="yellow", font = "6", bd=8)
        label.grid(row=0, column=0, columnspan = 2, sticky='nwes')

    yesButton = Button(remItemFromShopListWin,
        text="Oui",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "light green",
        relief = "groove",
        command= lambda:remItemFromShopListDone(remItemFromShopListWin, itemsInShopListList, ingsInShopListList, all)
        )
    yesButton.grid(row=1, column=0, sticky='news')

    noButton = Button(remItemFromShopListWin,
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        # bg = "red",
        relief = "groove",
        command= remItemFromShopListWin.destroy
        )
    noButton.grid(row=1, column=1, sticky='news')

    remItemFromShopListWin.bind('<Return>', lambda event:remItemFromShopListDone(remItemFromShopListWin, itemsInShopListList, ingsInShopListList, all))
    remItemFromShopListWin.bind('<Escape>', lambda event:remItemFromShopListWin.destroy())

    remItemFromShopListWin.after(1, lambda: remItemFromShopListWin.focus_force())
    remItemFromShopListWin.mainloop()
    return None

def addIngToShopListDoneConfirm(ingName, QteEnfantEntry, QteAdulteEntry, regimesValList, warnWin, addIngToShopListWin, itemsInShopListList, ingsInShopListList):
    if warnWin != 0:
        warnWin.destroy()
    id_ing = askSQL("SELECT id_ing FROM ingredients WHERE nom = '%s'" % (ingName.lower()))

    # print(regimesValList)
    values = [1, id_ing[0][0], QteEnfantEntry, QteAdulteEntry, -3, -3, -3, -3]

    for i in regimesValList:
        values[4+i] = 1
    # print(values)
    request = "INSERT INTO listes (is_ing, id, qte_enfant, qte_adulte, '0', '1', '2', '3') VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" % tuple(values)
    # print(request)
    setSQL(request)

    updateItemsInShopListList(itemsInShopListList, ingsInShopListList)
    addIngToShopListWin.destroy()

    return None

def addIngToShopListDone(ingChoiceEntry, wQteEnfantEntry, wQteAdulteEntry, regimeBools, addIngToShopListWin, itemsInShopListList, ingsInShopListList):
    ingName = ingChoiceEntry.get()
    QteEnfantEntry = wQteEnfantEntry.get()
    QteAdulteEntry = wQteAdulteEntry.get()

    ingRegimesValList = []
    for regime in regimeList:
        if regimeBools[regime].get() == 1:
            ingRegimesValList.append(getRegimeVal(regime))
    # print(ingRegimesValList)

    payload = askSQL("SELECT regime FROM ingredients WHERE nom = '%s'" % (ingName.lower()))
    if payload == []:
        makeErrorWindow("Erreur : Nom d'ingrédient invalide : " + ingName)

    elif not QteEnfantEntry.replace('.','',1).isdigit():
        makeErrorWindow("Erreur : Valeur invalide pour la portion enfant : '" + QteEnfantEntry + "'")
    elif not QteAdulteEntry.replace('.','',1).isdigit():
        makeErrorWindow("Erreur : Valeur invalide pour la portion adulte : '" + QteAdulteEntry + "'")
    elif ingRegimesValList == []:
        makeErrorWindow("Erreur : Vous devez sélectionner un moins une variante (Viande, végétarien, etc...).")
    else:
        #Check de si l'ingrédient correspond au régime
        ingMaxRegime = askSQL("SELECT regime FROM ingredients WHERE nom = '%s'" % (ingName.lower()))[0][0]
        # print(ingMaxRegime)
        operationMaxRegime = max(ingRegimesValList)
        # print(operationMaxRegime)
        if ingMaxRegime in [0,1,2,3] and operationMaxRegime > ingMaxRegime:
            # print("warn")
            #WARN d'un ingrédient potentiellement pas adapté à un régime
            warnWin= Toplevel(addIngToShopListWin)
            warnWin.grab_set()
            warnWin.title("Conflit de régimes alimentaires")
            # warnWin.grid_columnconfigure(0, weight=1)
            warn = "Avertissement : Votre ingrédient '" + ingName + "' convient au maximum au régime '" + getRegimeName(ingMaxRegime) + "'.\nCependant, vous demandez à l'ajouter à la liste '" + getRegimeName(operationMaxRegime) + "'.\n\nSouhaitez-vous vraiment continuer ?\n"
            warnLbl = Label(warnWin, text=warn, justify="left", bd = 5, font="Verdana 10 bold",bg = "orange")
            warnLbl.grid(row=0, column=0, columnspan=2, sticky='news')

            confirmButton = Button(warnWin,
                text="Je sais ce que je fais !",
                font = "Verdana 10 bold",
                bd = 2,
                relief = "groove",
                command= lambda:addIngToShopListDoneConfirm(ingName, QteEnfantEntry, QteAdulteEntry, ingRegimesValList, warnWin, addIngToShopListWin, itemsInShopListList, ingsInShopListList)
                )
            confirmButton.grid(row=1, column=0, sticky='news')

            cancelButton = Button(warnWin,
                text="Annuler",
                font = "Verdana 10 bold",
                bd = 2,
                relief = "groove",
                command= warnWin.destroy
                )
            cancelButton.grid(row=1, column=1, sticky='news')

            warnWin.bind('<Escape>', warnWin.destroy)
            center(warnWin)
            warnWin.after(1, lambda: warnWin.focus_force())
            warnWin.mainloop()

        else:
            addIngToShopListDoneConfirm(ingName, QteEnfantEntry, QteAdulteEntry, ingRegimesValList, 0, addIngToShopListWin, itemsInShopListList, ingsInShopListList)


    return None

def addIngToShopList(itemsInShopListList, ingsInShopListList):

    addIngToShopListWin= Toplevel(root)
    addIngToShopListWin.geometry("570x270")
    center(addIngToShopListWin)
    addIngToShopListWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie

    addIngToShopListWin.grid_columnconfigure(1, weight=1)
    addIngToShopListWin.grid_rowconfigure(5, weight=1)

    addIngToShopListWin.title("Ajouter un ingrédient à la liste de courses")
    label = Label(addIngToShopListWin, text="Ajouter un ingrédient à la liste de courses", bg="yellow", font = "8", bd=8)
    label.grid(row=0, column=0, columnspan = 2, sticky='nwe')

    ingNameLbl = Label(addIngToShopListWin, text="Choisissez un ingrédient : ", font = "Verdana 10 bold", relief=RAISED)
    ingNameLbl.grid(row=1, column=0, sticky='new')


    ingsPayload = askSQL("SELECT nom FROM ingredients ORDER BY nom")
    ingList = []
    for ing in ingsPayload:
        ingList.append(ing[0])

    ingChoiceEntryFrame = Frame(addIngToShopListWin)
    ingChoiceEntryFrame.grid(row=2, column=0, rowspan = 4, sticky='news')

    # scrollIngChoiceEntry = Scrollbar(ingChoiceEntryFrame)
    # scrollIngChoiceEntry.grid(row=0, column=1, sticky='nsw')

    ingChoiceEntry = AutocompleteEntryListbox(
        ingChoiceEntryFrame,
        width=30,
        font=("Verdana 10"),
        completevalues=ingList,
        allow_other_values=True
        )
    ingChoiceEntry.grid(row=0, column=0, sticky='nw')
    # ingChoiceEntry.listbox.config(yscrollcommand = scrollIngChoiceEntry)

    #Définition des quantités
    ingUnit = ""

    addIngToShopListSetQuantitesLbl = Label(addIngToShopListWin, text="Quantités : ", font = "Verdana 10 bold", relief=RAISED)
    addIngToShopListSetQuantitesLbl.grid(row=1, column=1, columnspan=1, sticky='new')

    addIngToShopListSetQuantitesFrame = Frame(addIngToShopListWin)
    addIngToShopListSetQuantitesFrame.grid(row=2, column=1, columnspan = 1, sticky='')
    # addIngToShopListSetQuantitesFrame.grid_columnconfigure(0, weight=1)

    addIngToShopListSetQuantitesLblEnfant = Label(addIngToShopListSetQuantitesFrame, text="\nEnfant : \n")
    addIngToShopListSetQuantitesLblEnfant.grid(row=1, column=1, columnspan=1, sticky='w')

    addIngToShopListSetQuantitesEnfant = Entry(addIngToShopListSetQuantitesFrame, width = 5)
    addIngToShopListSetQuantitesEnfant.grid(row=1, column=2, columnspan=1, sticky='w')

    addIngToShopListSetQuantitesUnitLbl1 = Label(addIngToShopListSetQuantitesFrame, text=ingUnit)
    addIngToShopListSetQuantitesUnitLbl1.grid(row=1, column=3, columnspan=1, sticky='w')


    addIngToShopListSetQuantitesLblAdulte = Label(addIngToShopListSetQuantitesFrame, text="\nAdulte : \n")
    addIngToShopListSetQuantitesLblAdulte.grid(row=1, column=4, columnspan=1, sticky='w')

    addIngToShopListSetQuantitesAdulte = Entry(addIngToShopListSetQuantitesFrame, width = 5)
    addIngToShopListSetQuantitesAdulte.grid(row=1, column=5, columnspan=1, sticky='w')

    addIngToShopListSetQuantitesUnitLbl2 = Label(addIngToShopListSetQuantitesFrame, text=ingUnit)
    addIngToShopListSetQuantitesUnitLbl2.grid(row=1, column=6, columnspan=1, sticky='w')

    addIngToShopListSetQuantitesDesc = Label(addIngToShopListSetQuantitesFrame, text="Entrez les quantités de cet ingrédient pour\nUNE personne, adulte et enfant.\n", justify="left")
    addIngToShopListSetQuantitesDesc.grid(row=2, column=0, columnspan=6, sticky='new')

    #Définition des régimes affectés par l'ingrédient
    ingAddSelectRegimesLbl = Label(addIngToShopListWin, text="Ajouter aux régimes : ", font = "Verdana 10 bold", relief=RAISED)
    ingAddSelectRegimesLbl.grid(row=3, column=1, sticky='new')

    ingAddSelectRegimesFrame = Frame(addIngToShopListWin)
    ingAddSelectRegimesFrame.grid(row=4, column=1, columnspan=1, sticky='news')

    regimeCheckButtons = {}
    regimeBools = {}
    for regime in regimeList:
        regimeBools[regime] = IntVar(value=1)
        regimeCheckButtons[regime] = Checkbutton(ingAddSelectRegimesFrame, text = regime, variable = regimeBools[regime], onvalue = 1, offvalue = 0)
        regimeCheckButtons[regime].pack(side=LEFT)
    # print(regimeBools)

    #SAVE/DISCARD
    finishButtonsFrame= Frame(addIngToShopListWin)
    finishButtonsFrame.grid(row=5, column=1, columnspan=1, sticky='')

    addIngToShopListSaveButton = Button(finishButtonsFrame,
        text="Confirmer",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:addIngToShopListDone(ingChoiceEntry, addIngToShopListSetQuantitesEnfant, addIngToShopListSetQuantitesAdulte, regimeBools, addIngToShopListWin, itemsInShopListList, ingsInShopListList)
        )
    addIngToShopListSaveButton.grid(row=0, column=0, sticky='n')

    addIngToShopListCancelButton = Button(finishButtonsFrame,
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= addIngToShopListWin.destroy
        )
    addIngToShopListCancelButton.grid(row=0, column=1, sticky='n')


    ingChoiceEntry.listbox.bind('<ButtonRelease-1>', lambda event:updateUnitLbl(addIngToShopListSetQuantitesUnitLbl1, addIngToShopListSetQuantitesUnitLbl2, ingChoiceEntry))
    ingChoiceEntry.listbox.bind('<KeyRelease>', lambda event:updateUnitLbl(addIngToShopListSetQuantitesUnitLbl1, addIngToShopListSetQuantitesUnitLbl2, ingChoiceEntry))
    ingChoiceEntry.entry.bind('<KeyRelease>', lambda event:updateUnitLbl(addIngToShopListSetQuantitesUnitLbl1, addIngToShopListSetQuantitesUnitLbl2, ingChoiceEntry))

    addIngToShopListWin.bind('<Return>', lambda event:addIngToShopListDone(ingChoiceEntry, addIngToShopListSetQuantitesEnfant, addIngToShopListSetQuantitesAdulte, regimeBools, addIngToShopListWin, itemsInShopListList, ingsInShopListList))
    addIngToShopListWin.bind('<Escape>', lambda event:addIngToShopListWin.destroy())

    addIngToShopListWin.after(1, lambda: addIngToShopListWin.focus_force())
    addIngToShopListWin.mainloop()
    return None

def addPlatToShopListConfirm(platChoiceEntry, vRegimeEntries, addPlatToShopListWin, itemsInShopListList, ingsInShopListList):
    platName = platChoiceEntry.get()
    id_plat = askSQL("SELECT id_plat FROM plats WHERE nom = '%s'" % (platName.lower()))
    if id_plat == []:
        makeErrorWindow("Erreur : Nom de plat invalide : " + platName)
        return None
    else:
        values = [0, id_plat[0][0], 0, 0, -3, -3, -3, -3]

        for regime in regimeList:
            if regime in vRegimeEntries:
                # print(vRegimeEntries[regime].get())
                values[getRegimeVal(regime)+4] = getRegimeVal(vRegimeEntries[regime].get())
        # print(values)

        request = "INSERT INTO listes (is_ing, id, qte_enfant, qte_adulte, '0', '1', '2', '3') VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" % tuple(values)
        # print(request)
        setSQL(request)

        updateItemsInShopListList(itemsInShopListList, ingsInShopListList)
        addPlatToShopListWin.destroy()
    return None


def addPlatToShopListUpdateSelectedPlat(regimeEntries, vRegimeEntries, platChoiceEntry):
    payload = askSQL("SELECT regimes FROM plats WHERE nom = '%s'" % (platChoiceEntry.get().lower()))
    # print(payload)
    for persRegime in regimeEntries.keys():
        for regime in regimeEntries[persRegime].keys():
            regimeEntries[persRegime][regime].grid_remove()
    if len(payload) != 0:
        platRegimes = []
        for regimeVal in payload[0][0]:
            platRegimes.append(getRegimeName(int(regimeVal)))
        platRegimes.append(regimeNot)
        for persRegime in regimeEntries.keys():
            regimeEntries[persRegime][regimeNot].grid()
            for regime in platRegimes[::-1]:
                regimeEntries[persRegime][regime].grid()
                # print(regimeEntries[persRegime][regime].cget("fg"))
                if regimeEntries[persRegime][regime].cget("fg") != "red": #red = pas compatible (ie viande dans végé par ex)
                    vRegimeEntries[persRegime].set(regime)
    return None

def addPlatToShopList(itemsInShopListList, ingsInShopListList):

    addPlatToShopListWin= Toplevel(root)
    addPlatToShopListWin.geometry("750x320")
    center(addPlatToShopListWin)
    addPlatToShopListWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie


    addPlatToShopListWin.grid_columnconfigure(1, weight=1)
    addPlatToShopListWin.grid_rowconfigure(5, weight=1)

    addPlatToShopListWin.title("Ajouter un plat à la liste de courses")
    label = Label(addPlatToShopListWin, text="Ajouter un plat à la liste de courses", bg="yellow", font = "8", bd=8)
    label.grid(row=0, column=0, columnspan = 7, sticky='nwe')

    ingNameLbl = Label(addPlatToShopListWin, text="\nChoisissez un plat : ", font = "Verdana 10 bold", relief=RAISED)
    ingNameLbl.grid(row=1, column=0, sticky='new')


    platsPayload = askSQL("SELECT nom FROM plats ORDER BY nom")
    platList = []
    for plat in platsPayload:
        platList.append(plat[0])

    platChoiceEntryFrame = Frame(addPlatToShopListWin)
    platChoiceEntryFrame.grid(row=2, column=0, rowspan = 4, sticky='news')

    # scrollPlatChoiceEntry = Scrollbar(platChoiceEntryFrame)
    # scrollPlatChoiceEntry.grid(row=0, column=1, sticky='nsw')

    platChoiceEntry = AutocompleteEntryListbox(
        platChoiceEntryFrame,
        width=30,
        font=("Verdana 10"),
        completevalues=platList,
        allow_other_values=True
        )
    platChoiceEntry.grid(row=0, column=0, sticky='nw')
    # platChoiceEntry.listbox.config(yscrollcommand = scrollPlatChoiceEntry)

    #Définition des régimes :
    platRegimeSettingsLbl = Label(addPlatToShopListWin, text="Sélectionnez la variante du plat\nutilisée pour chaque régime", font = "Verdana 10 bold", relief=RAISED, justify="left")
    platRegimeSettingsLbl.grid(row=1, column=1, sticky='news')

    platRegimeSettingsFrame = Frame(addPlatToShopListWin)
    platRegimeSettingsFrame.grid(row=2, column=1, sticky='new')

    persListPerRegime = {}
    for regime in regimeList:
        request = "SELECT val FROM pers WHERE regime = %s" % (getRegimeVal(regime))
        payload = askSQL(request)
        # print(payload)
        if payload == [0]:
            persListPerRegime[regime] = 0
        else:
            add = 0
            for tupleVal in payload:
                add += int(tupleVal[0])
            persListPerRegime[regime] = add

    regimeEntries = {}
    vRegimeEntries = {}
    regimeLbls = {}
    for regime in regimeList:
        if persListPerRegime[regime] != 0:
            regimeLbls[regime] = Label(platRegimeSettingsFrame, text = regime + " : ", justify = "right", font="Verdana 9 bold")
            regimeLbls[regime].grid(row=getRegimeVal(regime), column=0, sticky='nes')
            regimeEntries[regime] = {}

    for regimeInPers in regimeEntries.keys():
        vRegimeEntries[regimeInPers] = StringVar()
        for regime in regimeList:
            if getRegimeVal(regime) < getRegimeVal(regimeInPers):
                regimeEntries[regimeInPers][regime] = Radiobutton(platRegimeSettingsFrame, text=regime, variable=vRegimeEntries[regimeInPers], value=regime, tristatevalue=0, fg = "red")      #Création radioButton
            else:
                regimeEntries[regimeInPers][regime] = Radiobutton(platRegimeSettingsFrame, text=regime, variable=vRegimeEntries[regimeInPers], value=regime, tristatevalue=0)      #Création radioButton

            regimeEntries[regimeInPers][regime].grid(row=getRegimeVal(regimeInPers), column=1+getRegimeVal(regime), sticky='news')

            regimeEntries[regimeInPers][regime].grid_remove()   #Caché tant que pas de plat

        regimeEntries[regimeInPers][regimeNot] = Radiobutton(platRegimeSettingsFrame, text=regimeNot, variable=vRegimeEntries[regimeInPers], value=regimeNot, tristatevalue=0)      #Création radioButton
        regimeEntries[regimeInPers][regimeNot].grid(row=getRegimeVal(regimeInPers), column=6, sticky='news')
        regimeEntries[regimeInPers][regimeNot].grid_remove()   #Caché tant que pas de plat

    platRegimeSettingsDesc = Label(addPlatToShopListWin, text="Les variantes en rouges sont celles qui à priori ne\nconviennent pas au régime correspondant.\nVous n'avez normalement pas besoin de les choisir.\n\n\nSi aucun régime n'apparaît, ça veut dire que votre\nliste de personnes présentes est vide :)", relief=SUNKEN, justify="left", anchor="w")
    platRegimeSettingsDesc.grid(row=3, column=1, sticky='news')

    #SAVE/DISCARD
    finishButtonsFrame= Frame(addPlatToShopListWin)
    finishButtonsFrame.grid(row=5, column=1, columnspan=6, sticky='')

    addIngToPlatEditSaveButton = Button(finishButtonsFrame,
        text="Confirmer",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:addPlatToShopListConfirm(platChoiceEntry, vRegimeEntries, addPlatToShopListWin, itemsInShopListList, ingsInShopListList)
        )
    addIngToPlatEditSaveButton.grid(row=0, column=0, sticky='n')

    addIngToPlatEditCancelButton = Button(finishButtonsFrame,
        text="Annuler",
        font = "Verdana 10 bold",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= addPlatToShopListWin.destroy
        )
    addIngToPlatEditCancelButton.grid(row=0, column=1, sticky='n')


    platChoiceEntry.listbox.bind('<ButtonRelease-1>', lambda event:addPlatToShopListUpdateSelectedPlat(regimeEntries, vRegimeEntries, platChoiceEntry))
    platChoiceEntry.listbox.bind('<KeyRelease>', lambda event:addPlatToShopListUpdateSelectedPlat(regimeEntries, vRegimeEntries, platChoiceEntry))
    platChoiceEntry.entry.bind('<KeyRelease>', lambda event:addPlatToShopListUpdateSelectedPlat(regimeEntries, vRegimeEntries, platChoiceEntry))

    addPlatToShopListWin.bind('<Return>', lambda event:addPlatToShopListConfirm(platChoiceEntry, vRegimeEntries, addPlatToShopListWin, itemsInShopListList, ingsInShopListList))
    addPlatToShopListWin.bind('<Escape>', lambda event:addPlatToShopListWin.destroy())

    addPlatToShopListWin.after(1, lambda: addPlatToShopListWin.focus_force())
    addPlatToShopListWin.mainloop()
    return None


def makelistecoursesFrame():
    global listeFrame
    global ingsInShopListList
    global allergenesInShopListList
    listeFrame = Frame(master=container, borderwidth=5, relief=GROOVE, width=100, height=100)
    listeFrame.grid(row=0, column=0, sticky='news')
    listeFrame.grid_rowconfigure(1, weight=1)
    listeFrame.grid_columnconfigure(0, weight=1)

    itemsInShopListFrame = Frame(listeFrame, borderwidth=1, relief=SUNKEN)
    itemsInShopListFrame.grid(row=1, column=0, rowspan = 2, sticky='news')
    ingsInShopListFrame = Frame(listeFrame, borderwidth=1, relief=SUNKEN)
    ingsInShopListFrame.grid(row=1, column=1, sticky='news')
    exportShopListFrame = Frame(listeFrame, borderwidth=1, relief=SUNKEN)
    exportShopListFrame.grid(row=1, column=2, sticky='news')

    #Top label
    label = Label(listeFrame, text="Générer une liste de courses", bg="yellow", font = "10")
    label.grid(row=0, column=0, columnspan = 3, sticky='nwe')

    #Colonne 0 : liste des items dans la liste, boutons pour ajouter/enlever
    itemsInShopListName = Label(itemsInShopListFrame, text="Items à prendre en compte : ", relief=RAISED)
    itemsInShopListName.grid(row=0, column=0, columnspan=2, sticky='news')

    scrollItemsInShopListList = Scrollbar(itemsInShopListFrame)
    scrollItemsInShopListList.grid(row=1, column=1, sticky='nsw')

    itemsInShopListList = Listbox(itemsInShopListFrame, yscrollcommand = scrollItemsInShopListList.set, width=45)
    itemsInShopListList.grid(row=1, column=0, sticky='news')

    optionsButtonsFrame = Frame(itemsInShopListFrame)
    optionsButtonsFrame.grid(row=2, column=0, columnspan = 2, sticky='news')
    optionsButtonsFrame.grid_columnconfigure(0, weight=1)
    optionsButtonsFrame.grid_columnconfigure(1, weight=1)

    addPlatToShopListButton = Button(
        optionsButtonsFrame,
        text="Ajouter un plat",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "green",
        relief = "groove",
        command= lambda:addPlatToShopList(itemsInShopListList, ingsInShopListList)
        )
    addPlatToShopListButton.grid(row=0, column=0, sticky='news')

    addIngToShopListButton = Button(
        optionsButtonsFrame,
        text="Ajouter un ingrédient",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "green",
        relief = "groove",
        command= lambda:addIngToShopList(itemsInShopListList, ingsInShopListList)
        )
    addIngToShopListButton.grid(row=0, column=1, sticky='news')

    suppItemFromShopList = Button(
        optionsButtonsFrame,
        text="Retirer la sélection",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= lambda:remItemFromShopList(itemsInShopListList, ingsInShopListList)
        )
    suppItemFromShopList.grid(row=1, column=0, sticky='news')

    clearShopList = Button(
        optionsButtonsFrame,
        text="Tout retirer",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "red",
        relief = "groove",
        command= lambda:remItemFromShopList(itemsInShopListList, ingsInShopListList, 1)
        )
    clearShopList.grid(row=1, column=1, sticky='news')

    itemsInShopListDesc = Label(itemsInShopListFrame, text="""\nVous pouvez ajouter des plats à la liste,\nmais également directement des ingrédients\nen spécifiant les quantités pour une personne.\n(notamment, si vous voulez acheter des pommes\npour le dessert pas besoin de créer un plat\n"Pommes", sélectionnez juste "Pomme" dans les\ningrédients et mettez une quantité de 1 par\npersonne)""", justify="left")
    itemsInShopListDesc.grid(row=3, column=0, columnspan=2, sticky='news')

    #Colonne 1 : Ingrédients dans la sélection
    ingsInShopListName = Label(ingsInShopListFrame, text="Contenu actuel de la liste de courses : ", relief=RAISED)
    ingsInShopListName.grid(row=0, column=0, columnspan=2, sticky='news')

    scrollIngsInShopListList = Scrollbar(ingsInShopListFrame)
    scrollIngsInShopListList.grid(row=1, column=1, sticky='nsw')

    ingsInShopListList = ttk.Treeview(ingsInShopListFrame, column=(0,1), show='headings', height=16, yscrollcommand = scrollIngsInShopListList.set)
    ingsInShopListList.column(0, anchor="e", width=200, stretch=NO)
    ingsInShopListList.heading(0, text="Ingrédient")
    ingsInShopListList.column(1, anchor="w", width=80, stretch=NO)
    ingsInShopListList.heading(1, text="Qté à acheter")
    ingsInShopListList.grid(row=1, column=0, sticky='nsw')

    #Colonne 2 : Exporter la liste et settings
    exportShopListLbl = Label(exportShopListFrame, text="Exporter dans un fichier", relief=RAISED)
    exportShopListLbl.grid(row=0, column=0, columnspan=2, sticky='news')

    exportShopListDesc1 = Label(exportShopListFrame, text="Entrez le nom de la liste de courses :")
    exportShopListDesc1.grid(row=1, column=0, columnspan=2, sticky='news')

    exportShopListNameEntry = Entry(exportShopListFrame, width = 25)
    exportShopListNameEntry.grid(row=2, column=0, sticky='news')
    exportShopListNameEntry.insert(0,"liste_de_courses")
    exportShopListNameExtenstionLbl = Label(exportShopListFrame, text=".txt")
    exportShopListNameExtenstionLbl.grid(row=2, column=1, sticky='news')

    exportShopListDesc2 = Label(exportShopListFrame, text="Le fichier sera créé dans le dossier\nde l'application.",justify="left")
    exportShopListDesc2.grid(row=3, column=0, columnspan=2, sticky='nws')

    includeAllergenes = IntVar()
    includeAllergenesCheck = Checkbutton(exportShopListFrame, text = "Écrire les allergènes", variable = includeAllergenes, onvalue = 1, offvalue = 0)
    includeAllergenesCheck.grid(row=4, column=0, sticky='nws')

    exportListButton = Button(
        exportShopListFrame,
        text="\nExporter\n",
        font = "Verdana 8 underline",
        bd = 2,
        bg = "light green",
        relief = "groove",
        command= lambda:exportListeCourses(ingsInShopListList, exportShopListNameEntry, exportShopListSucces, includeAllergenes)
        )
    exportListButton.grid(row=5, column=0, columnspan=2, sticky='news')

    sep = Label(exportShopListFrame, text = "")
    sep.grid(row=6, column=0, columnspan = 2, rowspan = 1, sticky='news')

    allergenesInShopListListLbl = Label(exportShopListFrame, text="Allergènes dans la liste :", relief = RAISED)
    allergenesInShopListListLbl.grid(row=7, column=0, columnspan=2, sticky='news')
    allergenesInShopListList = Label(exportShopListFrame, text="", justify="left")
    allergenesInShopListList.grid(row=8, column=0, columnspan=2, sticky='nws')

    exportShopListSucces = Label(exportShopListFrame, text="",justify="left", font = "Verdana 8 bold", fg = "green")
    exportShopListSucces.grid(row=9, column=0, columnspan=2, sticky='ws')

    #Chargement des données
    makepersFrame()
    updateItemsInShopListList(itemsInShopListList, ingsInShopListList)
    return None

def raiselistecourses():
    listeFrame.tkraise()

##Autres fonctions tkinter
def showAppInfos():
    showAppInfosWin= Toplevel(root)
    showAppInfosWin.geometry("620x350")
    center(showAppInfosWin)
    showAppInfosWin.grab_set()        #Pour ne pas pouvoir accéder à la main window pendant la saisie

    showAppInfosWin.grid_columnconfigure(0, weight=1)
    showAppInfosWin.grid_rowconfigure(2, weight=1)

    showAppInfosWin.title("Informations de l'application")
    label = Label(showAppInfosWin, text="Application %s version %s" % (APP_NAME, APP_VERSION), font = "Verdana 12 bold", bd=8, relief=RAISED)
    label.grid(row=0, column=0, columnspan = 2, sticky='nwe')

    infosApp = "UTILISATION : " + "\n"
    infosApp += "Le but de cette application est d'aider les intendants à composer leurs listes de courses." + "\n"
    infosApp += "Vous pouvez ajouter des ingrédients, puis les utiliser pour composer des plats." + "\n"
    infosApp += "Ensuite, entrez la liste des personnes présentes et choisissez quels éléments vous voulez dans votre liste de courses." + "\n"
    infosApp += "Le programme calculera les quantités nécessaire en fonction des quantités par personne que vous avez entrées." + "\n"
    infosApp += "Vous pouvez ensuite exporter la liste de courses sous format .txt" + "\n\n"
    infosApp += "Vous pouvez notifier de la présence d'allergènes dans les ingrédients," + "\n"
    infosApp += "qui seront ensuite reportés dans les plats utilisant ces ingrédients, puis dans la liste de courses" + "\n"
    infosApp += "ATTENTION : les allergènes sont là purement à titre indicatif, " + APP_NAME + " ne fera aucun calcul avec !" + "\n"
    infosApp += "Si vous avez des personnes allergiques dans votre groupe, n'utilisez pas " + APP_NAME + " pour faire leurs menus !" + "\n\n\n"
    infosApp += "DÉVELOPPEMENT : " + "\n"
    infosApp += "Application développée par Titouan, responsable EEDF au groupe de Meudon" + "\n"
    infosApp += "Téléchargement : github.com/Titouan-Stl/Denethor" + "\n"
    infosApp += "Code fait en Python, et probablement très moche. Le code source est disponible sur Github" + "\n"
    infosApp += "Contact : titouanthetitan sur Discord (oui je sais c'est pas terrible)"

    infosLbl = Label(showAppInfosWin, text=infosApp, bg="yellow", justify = "left")
    infosLbl.grid(row=1, column=0, sticky='news')

    closeButton = Button(showAppInfosWin,
        text="    Fermer    ",
        font = "Verdana 10 bold",
        bd = 2,
        relief = "groove",
        command= showAppInfosWin.destroy
        )
    closeButton.grid(row=2, column=0, sticky='ns')

    showAppInfosWin.bind('<Return>', lambda event:showAppInfosWin.destroy())
    showAppInfosWin.bind('<Escape>', lambda event:showAppInfosWin.destroy())

    showAppInfosWin.after(1, lambda: showAppInfosWin.focus_force())
    showAppInfosWin.mainloop()
    return None


##Ouverture/création de la BDD

if os.path.isfile(BDD_path):
    connection = sqlite3.connect(BDD_path)
    BDD = connection.cursor()
else:
        print("Aucune BDD trouvée : nouvelle BDD créée")
        formatBDD()

##Root window (menu)
root = Tk()
root.geometry("800x540")
center(root)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

container = Frame(root, width=700, height=500)
container.grid(row=0, column=0, sticky='news')
container.grid_rowconfigure(0, weight = 1)
container.grid_columnconfigure(0, weight = 1)


root.title(APP_NAME + ", l'aide de camp de l'intendant")
icon = PhotoImage(file = get_path("icon.png"))
root.iconphoto(False, icon)

# makeingFrame()
# makeplatFrame()
makelistecoursesFrame()


mainmenu = Menu(container)
mainmenu.add_command(label = "Gérer les ingrédients", command= makeingFrame)
mainmenu.add_command(label = "Gérer les plats", command= makeplatFrame)
# mainmenu.add_command(label = "Gérer les personnes", command= raisepers)
mainmenu.add_command(label = "Générer une liste de courses", command= makelistecoursesFrame)
mainmenu.add_command(label = "À propos", command= showAppInfos)
mainmenu.add_command(label = "Quitter", command= root.destroy)

# root.hover = HoverInfo(root, 'while hovering press return \n for an exciting msg')


root.config(menu = mainmenu)

root.after(1, lambda: root.focus_force())
root.mainloop()
connection.close()