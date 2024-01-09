import cv2
import time
import threading


class USBCamera:
    def __init__(self, device=-1, resolution=(640, 480)):

        self.device = device
        self.width = resolution[0]
        self.height = resolution[1]

        self.cap = None
        self.frame = None
        self.opened = False

        self.th = None
        self.th = threading.Thread(target=self.camera_task, args=(), daemon=True)
        self.th.start()

    def camera_open(self):
        try:
            self.cap = cv2.VideoCapture(self.device)
            # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
            # self.cap.set(cv2.CAP_PROP_FPS, 30)
            # self.cap.set(cv2.CAP_PROP_SATURATION, 40)
            self.opened = True
        except Exception as e:
            print('打开摄像头失败:', e)

    def camera_close(self):
        try:
            self.opened = False
            time.sleep(0.2)
            if self.cap is not None:
                self.cap.release()
                time.sleep(0.05)
            self.cap = None
        except Exception as e:
            print('关闭摄像头失败:', e)

    def camera_task(self):
        while True:
            try:
                if self.opened and self.cap.isOpened():
                    ret, frame_tmp = self.cap.read()
                    if ret:
                        frame_resize = cv2.resize(frame_tmp, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
                        self.frame = frame_resize
                    else:
                        print(1)
                        self.frame = None
                        cap = cv2.VideoCapture(self.device)
                        ret, _ = cap.read()
                        if ret:
                            self.cap = cap
                elif self.opened:
                    print(2)
                    cap = cv2.VideoCapture(self.device)
                    ret, _ = cap.read()
                    if ret:
                        self.cap = cap
                else:
                    time.sleep(0.01)
            except Exception as e:
                print('获取摄像头画面出错:', e)
                time.sleep(0.01)


if __name__ == '__main__':
    camera = USBCamera()
    camera.camera_open()
    while True:
        img1 = camera.frame
        if img1 is not None:
            cv2.imshow('img', img1)
            key1 = cv2.waitKey(1)
            if key1 == 27:
                break
    camera.camera_close()
    cv2.destroyAllWindows()
