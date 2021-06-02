import KeyPressModule as kp
from djitellopy import tello
import cv2

#Crea una finestra nera che 'cattura' i tasti premuti
#Ricordati che è necessario cliccare sulla scheda per poter inviare i comandi
kp.init()

#Si connette al drone (il pc deve essere collegato al drone tramite wifi)
drone = tello.Tello()
drone.connect()
#Il drone inizia a trasferire le immagini della videocamera
drone.streamon()
#Stampa la percentuale di batteria rimanente
print(drone.get_battery())

#Funzione che fa variare la velocità e direzione del drone in base ai tasti premuti
def getKeyboardInput():
    lato, dritto, alto, rotaz = 0, 0, 0, 0
    speed = 100
    #Freccia sinistra/destra per far muovere il drone a sinistra/destra
    if kp.getKey("LEFT"): lato = -speed
    elif kp.getKey("RIGHT"): lato = speed

    #Freccia su/giù per far muovere il drone avanti/dietro
    if kp.getKey("UP"): dritto = speed
    elif kp.getKey("DOWN"): dritto = -speed

    #Tasto w/s per far muovere il drone in alto/basso
    if kp.getKey("w"): alto = speed
    elif kp.getKey("s"): alto = -speed

    #Tasto a/d per far ruotare il drone verso sinistra/destra
    if kp.getKey("a"): rotaz = -speed
    elif kp.getKey("d"): rotaz = speed

    #Tasto t per far partire il drone da terra
    if kp.getKey("t"): drone.takeoff()

    #Tasto l per far atterrare il drone
    if kp.getKey("l"): drone.land()

    return lato, dritto, alto, rotaz


while True:
    values = getKeyboardInput()
    #Invia un comando al drone in base ai tasti premuti
    drone.send_rc_control(values[0], values[1], values[2], values[3])
    #Il codice seguente serve per mostrare il video ripreso dal drone
    video = drone.get_frame_read().frame
    video = cv2.resize(video, (360, 240))
    cv2.imshow("Drone video", video)
    cv2.waitKey(1)
