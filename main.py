import RPi.GPIO as GPIO
from time import sleep
import socket

GPIO.setmode(GPIO.BCM) # notation des pin du Raspberry pi type BOARD existe aussi BCM
#GPIO.setwarnings(False)

##initialisation
moteur1 = 13  # moteur 1
GPIO.setup(moteur1, GPIO.OUT)
moteur2 = 18  # moteur 2
GPIO.setup(moteur2, GPIO.OUT)

## remettre au démarage
pwmVitesseRobot = GPIO.PWM(moteur1,50)   # pwm 16 frequence de 50 Hz
pwmDirectionRobot = GPIO.PWM(moteur2,50)   # pwm 18 frequence de 50 Hz


#valeur borne moteur 1 moteur vitesse
minPWMMoteur1 = 5 #cela nous donne 1 ms et donc tourne à droite
maxPWMMoteur1 = 9 #cela nous donne 1.8 ms et donc tourne à gauche
initPWMMoteur1 = 7 #cela nous donne 1.4 ms et donc arrete
limitBasReculeMoteur1 = 0
limitHautReculeMoteur1 = 42
limitBasAvanceMoteur1 = 58
limitHautAvanceMoteur1 = 100

#valeur borne moteur 2 servo moteur direction
minPWMMoteur2 = 5 #cela nous donne 1 ms et donc recule max
maxPWMMoteur2 = 9 #cela nus donne 1.8 ms et donc avance max
initPWMMoteur2 = 7 #cela nous donne 1.4 ms reste centrer

#pourcentage vitesse
vitessePourcentActuel = 0 ## 50 Arret (sup 50 avance)(inf 50 recule)

directionPourcentageActuel = 50
directionPourcentageInit = 50

verifHautVitesse = 40 # vitesse max d'avancement
verifBasVitesse = -40 # vitesse max recule

def calculPourcentageMoteur1(pourcentageMoteur):
    print("pourcentage voulu", pourcentageMoteur)
    pourcentageMoteurConvertie = (((maxPWMMoteur1 - minPWMMoteur1) / 100) * pourcentageMoteur) + minPWMMoteur1
    print("=", pourcentageMoteurConvertie)
    return pourcentageMoteurConvertie

def calculPourcentageMoteur2(pourcentageMoteur):
    print("pourcentage voulu", pourcentageMoteur)
    pourcentageMoteurConvertie = (((maxPWMMoteur2 - minPWMMoteur2) / 100) * pourcentageMoteur) + minPWMMoteur2
    print("=", pourcentageMoteurConvertie)
    return pourcentageMoteurConvertie

def startRobot():
    print("startRobot")
    print("Init Direction")
    pwmDirectionRobot.start(initPWMMoteur2) # tout droit
    sleep(1)
    print("Init Vitesse null")
    #pwmVitesseRobot.start(initPWMMoteur1)  # Arret
    pwmVitesseRobot.start(0)  # Arret
    sleep(1)
    print("Fin Init Start robot")

def pauseRobot():
    pwmDirectionRobot.ChangeDutyCycle(initPWMMoteur2)  # tout droit
    sleep(1)
    print("Init Vitesse null")
    #pwmVitesseRobot.ChangeDutyCycle(initPWMMoteur1)
    pwmVitesseRobot.ChangeDutyCycle(0)
    pwmVitesseRobot.start(0)  # Arret

def stopRobot():
    print("stopRobot")
    pwmDirectionRobot.stop()  ## interruption du pwm direction robot
    pwmVitesseRobot.stop()  ## interruption du pwm vitesse robot

#pourcentage allant de -100 à 100
def changementVitesse(pourcentageAChanger):
    vitessePourcentActuel = pourcentageAChanger
    print('changement de vitesse')
    if pourcentageAChanger == 0:
        pwmVitesseRobot.ChangeDutyCycle(initPWMMoteur1)
    elif pourcentageAChanger >= -100 and pourcentageAChanger < 0:
        print("vitesse marche arrière")
        pourcentageAChangerConvertie = ((limitHautReculeMoteur1 - limitBasReculeMoteur1) * (pourcentageAChanger / 100)) + limitBasAvanceMoteur1
        print(pourcentageAChanger," -->",pourcentageAChangerConvertie)
        pwmVitesseRobot.ChangeDutyCycle(calculPourcentageMoteur1(pourcentageAChangerConvertie))
    elif pourcentageAChanger <= 100 and pourcentageAChanger > 0:
        print("vitesse marche Avant")
        pourcentageAChangerConvertie = ((limitHautAvanceMoteur1 - limitBasAvanceMoteur1) * (pourcentageAChanger / 100)) + limitBasAvanceMoteur1
        print(pourcentageAChanger," -->",pourcentageAChangerConvertie)
        pwmVitesseRobot.ChangeDutyCycle(calculPourcentageMoteur1(pourcentageAChangerConvertie))  # débute rapport cyclique de 75% donc a l'arret celon la doc


# permet de limiter la vitesse max arrière er avant
def verifLimiter(vitesseAVerif):
    vitesseLimiterRenvoi = 0
    if (vitesseAVerif <= verifHautVitesse and vitesseAVerif >= verifBasVitesse):
        print("-vitesse Acceptable-")
        vitesseLimiterRenvoi = vitesseAVerif
    elif (vitesseAVerif < verifBasVitesse):
        print("-vitesse Limiter Bas-")
        vitesseLimiterRenvoi = verifBasVitesse
    elif (vitesseAVerif > verifHautVitesse):
        print("-vitesse Limiter Bas-")
        vitesseLimiterRenvoi = verifHautVitesse
    else:
        print("-limite inaccepatable problème-")
    return vitesseLimiterRenvoi

#par default acceleration carré pic d'un coup 1
def typeAcceleration(vitesseAFinal, type):
    if(type == 1):
        changementVitesse(vitesseAFinal)
    else:
        print("type d\'accelerration : ", type, " inexistant ")

# accelaration par exemple de 10 pour augmenter de 10
def accelere(augmentation):
    global vitessePourcentActuel
    vitessePourcentVoulu = vitessePourcentActuel + augmentation
    #passage limiter max
    print("demande acceleration de", vitessePourcentActuel, " a ", vitessePourcentVoulu)
    vitessePourcentActuel = verifLimiter(vitessePourcentVoulu)
    print("acceleration en pourcentage réel après limiter", vitessePourcentActuel)
    typeAcceleration(vitessePourcentVoulu,1)
    print("acceleration terminer")

# decelaration par exemple de 10 pour baisser de 10
def decelere(deceleration):
    global vitessePourcentActuel
    vitessePourcentVoulu = vitessePourcentActuel - deceleration
    print("demande deceleration de", vitessePourcentActuel, " a ", vitessePourcentVoulu)
    if (vitessePourcentVoulu >=0 and vitessePourcentVoulu <verifHautVitesse):
        typeAcceleration(vitessePourcentVoulu, 1)
        vitessePourcentActuel = vitessePourcentVoulu
    elif (vitessePourcentVoulu < 0):
        print("!!! demande deceleration en dehors des limite  ou en dessous de 0 !!!")
        print("-- vitesse robot 0 --")
        typeAcceleration(0, 1)

# tourne a gauche pour 0.2 seconde
def gauche():
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(directionPourcentageActuel+30))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(directionPourcentageActuel))

def droite():
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(directionPourcentageActuel-30))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(directionPourcentageActuel))


###fonction de test
def testDroiteGauche():
    print("début testDroiteGauche")
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(0))
    sleep(1)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(100))
    sleep(1)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(50))
    sleep(1)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(10))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(20))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(30))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(40))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(50))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(60))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(70))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(80))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(90))
    sleep(0.2)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(100))
    sleep(1)
    pwmDirectionRobot.ChangeDutyCycle(calculPourcentageMoteur2(50))
    print("fin testDroiteGauche")

def testAvanceRecul1():
    print("début testAvanceRecul 1 ")
    accelere(10)
    sleep(1)
    accelere(10)
    sleep(1)
    #pauseRobot()
    sleep(1)
    #accelere(-10)
    decelere(-10)
    sleep(1)
    #accelere(-10)
    decelere(-10)
    sleep(1)
    pauseRobot()
    sleep(1)
    print("fin testAvanceRecul 1 ")

def testAvanceRecul2():
    print("début testAvanceRecul 1 ")
    accelere(20)
    sleep(0.5)
    decelere(20)
    sleep(0.5)
    decelere(20)
    sleep(3)
    pauseRobot()
    print("fin testAvanceRecul 1 ")


#init vitesse null et direction devant tour droit
#startRobot()
#sleep(1)
#print("vitessePourcentActuel : ", vitessePourcentActuel)
#sleep(3)

#testDroiteGauche()
#print("vitessePourcentActuel : ", vitessePourcentActuel)
#sleep(1)
#testAvanceRecul2()
#print("vitessePourcentActuel : ", vitessePourcentActuel)



#sleep(3)
#accelere(1)

#pwmVitesseRobot.ChangeDutyCycle(7.4)
#decelere(-1)
#sleep(10)
#accelere(-1)
#sleep(1)
#pauseRobot()
#print("vitessePourcentActuel : ", vitessePourcentActuel)





#pwmVitesseRobot.ChangeDutyCycle(calculPourcentageMoteur1(60))
#sleep(3)
#pwmVitesseRobot.ChangeDutyCycle(calculPourcentageMoteur1(40))
#sleep(3)

def autreFonction():
    print("contenue de l'autre fonction")



# comminication avec le robot via wifi
def communicationWifi():
    import socket
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(('', 15555))

    while True:
        try:
            socket.listen(1)
            client, address = socket.accept()
            client.setblocking(False)
            print("{} connected".format(address))

            while(1):
                print("essaie reception données")
                try:
                    response = client.recv(255)

                except:
                    print("connexion perdu")
                    continue
                if response != "":
                    print(response)
                    responsedecode = response.decode("utf-8")
                    print(responsedecode)
                    if responsedecode == "start":
                        startRobot()
                        print("<-start robot")
                    if responsedecode == "pause":
                        pauseRobot()
                        print("<-pause robot")
                    if responsedecode == "stop":
                        stopRobot()
                        print("<-stop robot")
                    if responsedecode == "plus":
                        accelere(5)
                        print("<-accelere robot de 5% en plus")
                    if responsedecode == "moins":
                        accelere(-5)
                        print("<-decelere robot de 5% en moins")
                    if responsedecode == "gauche":
                        print("<-gauche de 10%")
                        gauche()
                        print("<-retour devant")
                    if responsedecode == "droite":
                        print("<-droite de 10%")
                        droite()
                        print("<-retour devant")
        except:
            print("autres fonction")
            autreFonction()
#print("Close")
#client.close()
#stock.close()

communicationWifi()
while (1):
    sleep(1)
    print("dans boucle principale passage")




print("Arret du programme")
stopRobot()
GPIO.cleanup()


#pwm.start(100)   # débute rapport cyclique de 100% donc a plein régime
#GPIO.output(moteur1,GPIO.HIGH) # commence la rotation
#pwmVitesseRobot.ChangeDutyCycle(40) # changment du rapport cyclique

#def startRobot():
#    pwmVitesseRobot.start(midPWMMoteur2)  # débute rapport cyclique de 75% donc a l'arret celon la doc
#    #GPIO.output(moteur1, GPIO.HIGH)  # commence la rotation

#def stopRobot():
#    #GPIO.output(moteur1, GPIO.LOW)  # arret du moteur
#    pwmVitesseRobot.stop()  ## interruption du pwm