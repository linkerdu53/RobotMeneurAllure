# coding: utf-8
import time
import sys
from PyQt5 import QtWidgets,uic,QtCore
from PyQt5.QtCore import QTimer,QDateTime
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout,QLabel
import socket

### ouverture socket
hote = "raspberrypi.local"
#hote = "Linker-portable-noir"
port = 15555

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((hote, port))
print ("Connection on {}".format(port))

def encodeUTF8(tosend):
    tosendutf = tosend.encode("utf-8")
    return tosendutf

def envoiRobot(argAenvoyer):
    #tosend = encodeUTF8("start")
    tosend = encodeUTF8(argAenvoyer)
    try:
        socket.send(tosend)
    except:
        print("erreur d'envoie re essayer")
    #print ("Close")
    #socket.close()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        print("début géneration des button")
        # button Start
        self.buttonStart = self.findChild(QtWidgets.QPushButton, 'btnstart')
        self.buttonStart.clicked.connect(self.ClicBtnStart)

        # button Pause
        self.buttonPause = self.findChild(QtWidgets.QPushButton, 'btnpause')
        self.buttonPause.clicked.connect(self.ClicBtnPause)

        # button Stop
        self.buttonStop = self.findChild(QtWidgets.QPushButton, 'btnstop')
        self.buttonStop.clicked.connect(self.ClicBtnStop)

        # button Plus
        self.buttonPlus = self.findChild(QtWidgets.QPushButton, 'btnplus')
        self.buttonPlus.clicked.connect(self.ClicBtnPlus)

        # button Moins
        self.buttonMoins = self.findChild(QtWidgets.QPushButton, 'btnmoins')
        self.buttonMoins.clicked.connect(self.ClicBtnMoins)

        # button Gauche
        self.buttonGauche = self.findChild(QtWidgets.QPushButton, 'btngauche')
        self.buttonGauche.clicked.connect(self.ClicBtnGauche)

        # button Droite
        self.buttonDroite = self.findChild(QtWidgets.QPushButton, 'btndroite')
        self.buttonDroite.clicked.connect(self.ClicBtnDroite)
        print("fin géneration des button")


        # affichage de l'interface
        self.show()


    ### Fonctions de CLIC Boutton

    def ClicBtnStart(self):
        print("envoie clic -start-")
        envoiRobot("start")
        print("fin envoie")

    def ClicBtnPause(self):
        print("envoie clic -pause-")
        envoiRobot("pause")
        print("fin envoie")

    def ClicBtnStop(self):
        print("envoie clic -stop-")
        envoiRobot("stop")
        print("fin envoie")

    def ClicBtnPlus(self):
        print("envoie clic -plus-")
        envoiRobot("plus")
        print("fin envoie")

    def ClicBtnMoins(self):
        print("envoie clic -moins-")
        envoiRobot("moins")
        print("fin envoie")

    def ClicBtnGauche(self):
        print("envoie clic -gauche-")
        envoiRobot("gauche")
        print("fin envoie")

    def ClicBtnDroite(self):
        print("envoie clic -droite-")
        envoiRobot("droite")
        print("fin envoie")

def main():
    print("main Start")
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()




main()
#envoiRobot("start")
#time.sleep(1)

#envoiRobot("accelere")
#time.sleep(5)
#envoiRobot("decelere")
#time.sleep(1)
#envoiRobot("pause")

