import cv2
import sys
import gc
from face_train import Model

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage:%s camera_id\r\n" % (sys.argv[0]))
        sys.exit(0)

    # 加载模型
    model = Model()
    model.load_model(file_path = 'D:/model/ZCM.face.model.h5')

    # 框住人脸的边框颜色
    color = (0, 255, 0)

    # 捕获指定摄像头的实时视频流
    cap = cv2.VideoCapture(0)

    # 人脸识别分类器本地存储路径
    cascade_path = 'C:\\projects\\opencv-python\\opencv\modules\\objdetect\\src\\cascadedetect\\haarcascade_frontalface_default.xml'

    # 循环识别人脸
    while True:
        ret, frame = cap.read() # 读取一帧视频

        if ret is True:
            # 图像灰度化，降低计算复杂度
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            continue
        # 使用人脸识别分类器，读入分类器
        cascade = cv2.CascadeClassifier(cascade_path)

        # 利用分类器识别出人脸区域
        faceRects = cascade.detectMultiScale(frame_gray, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
        if len(faceRects) > 0:
            for faceRect in faceRects:
                x, y, w, h = faceRect
                # 截取脸部图像提交给模型识别
                image = frame[y - 10: y + h + 10, x - 10: x + w +10]
                faceID = model.face_predict(image)

                # 如果是'我'
                if faceID == 0:
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, thickness = 2)
                    #文字提示是谁                    
                    cv2.putText(frame,'ZCM',
                                (x + 30, y + 30),           #坐标
                                cv2.FONT_HERSHEY_SIMPLEX,   #字体
                                1,                          #字号
                                (255,0,255),                #颜色
                                2)                          #字的线宽
                else:
                    pass

        cv2.namedWindow('识别我')
        cv2.imshow('识别我', frame) 

        # 等待10ms看是否有按键输入
        k = cv2.waitKey(10)
        # 按'q'退出
        if k & 0xFF == ord('q'):
            break

    # 释放摄像头并销毁所有接口
    cap.release()
    cv2.destroyAllWindows()
