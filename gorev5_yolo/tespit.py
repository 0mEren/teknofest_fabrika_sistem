import cv2
from ultralytics import YOLO

class Detector:
    def __init__(self, model_yol):
        self.model = YOLO(model_yol)

    def detect(self, camera_i):
        capt = cv2.VideoCapture(camera_i)

        if capt.isOpened():
            capt.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            capt.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) 

            while True:
                ret, kare = capt.read()
                if not ret:
                    break
                sonuclar = self.model(kare, conf=0.5, stream=True)
                for sonuc in sonuclar:
                    label = sonuc.plot()

                cv2.imshow("ISARET", label)

                if cv2.waitKey(1) & 0xFF == 27:
                    break
        else:
            return
        capt.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    det = Detector(model_yol="best.pt")
    det.detect(camera_i = 0)

