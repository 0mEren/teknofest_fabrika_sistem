import cv2
import numpy as np
#r_alt = np.array(
#r_ust = np.array(

#kirmizi hue spektrumunu arkadan sariyor, iki aralik
r_dusukh_alt = np.array([0,120,70])
r_dusukh_ust = np.array([10,255,255])
r_yuksekh_alt = np.array([170,120,70])
r_yuksekh_ust = np.array([180,255,255])
b_alt = np.array([100, 50, 50])
b_ust = np.array([140, 255, 255])
g_alt = np.array([40, 50, 50])
g_ust = np.array([80, 255, 255])


class HSV_Algila:
    def __init__(self):
        self.kare = None
        self.kamera = cv2.VideoCapture(0) # kamera icin
        #self.testresim = cv2.imread("./gorev3_renk/testfile.jpg")

    def kare_yakala(self):
        global r_alt, r_ust, b_alt, b_ust, g_alt, g_ust
        cv2.namedWindow("HSV_algila")
        ret, kare = self.kamera.read()
        if not ret:
           return 0
        #kare = self.testresim.copy() #test ederken
        
        k = cv2.waitKey(1)
        if k%256 == 27:
            return 0
        hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)

        gmask = cv2.inRange(hsv, g_alt, g_ust)
        bmask = cv2.inRange(hsv, b_alt, b_ust)
        rmaskd = cv2.inRange(hsv, r_dusukh_alt, r_dusukh_ust)
        rmasky = cv2.inRange(hsv, r_yuksekh_alt, r_yuksekh_ust)
        rmask = cv2.bitwise_or(rmaskd, rmasky)
        rkontur, r_ = cv2.findContours(rmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        gkontur, g_ = cv2.findContours(gmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bkontur, b_ = cv2.findContours(bmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cikti = kare.copy()

        for contour in rkontur:
            x, y, w, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 500: 
                #merkez bulma
                print(f"RED at {x+(w/2)}, {y+(h/2)}")
                cv2.putText(cikti, "RED", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.rectangle(cikti, (x, y), (x + w, y + h), (0, 255, 0), 2) 

        for contour in gkontur:
            x, y, w, h = cv2.boundingRect(contour)
            
            if cv2.contourArea(contour) > 500: 
                #merkez bulma
                print(f"GREEN at {x+(w/2)}, {y+(h/2)}")
                cv2.putText(cikti, "GREEN", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.rectangle(cikti, (x, y), (x + w, y + h), (0, 255, 0), 2) 

        for contour in bkontur:
            x, y, w, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour) > 500: 
                print(f"BLUE at {x+(w/2)}, {y+(h/2)}")
                cv2.putText(cikti, "BLUE", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.rectangle(cikti, (x, y), (x + w, y + h), (0, 255, 0), 2) 

        cv2.imshow("HSV",cikti)
        return 1



if __name__ == '__main__':
    algila = HSV_Algila()
    while True:
        durum = algila.kare_yakala()
        if not durum:
            break
    algila.kamera.release()
    cv2.destroyAllWindows()
