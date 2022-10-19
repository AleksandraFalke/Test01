import cv2
from vidgear.gears import CamGear
from vidgear.gears import WriteGear

#принятие-просмотр видео
def video (name):
    video = cv2.VideoCapture(name)
    file_count = 0
    while (video.isOpened()):
        ret, frames = video.read()
        if ret == True:
            cv2.imshow('Look', frames)
            file_count += 1
            print('Кадр {0:04d}'.format(file_count))

            key = cv2.waitKey(20)
            if (key == ord('q')) or key == 27:
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()

#отправка видео на сервер
def send_server (name):
#    g_source = 0
    stream = CamGear(source=name, logging=True).start()
#output_params = {"-f": "rtsp", '-pix_fmt': 'yuv420p', "-rtsp_transport": "tcp","-b:v":"150k", '-bufsize':'150k', '-maxrate':'150k'}
#"-vcodec":"libx264","-profile:v":"main","-preset:v":"medium","-g":60,"-keyint_min":60,"-sc_threshold":0,"-b:v":"2500k","-maxrate":"2500k","-bufsize":"2500k", "-f":"flv"'-r':
#-r частота кадров "-r":'24'
# что-то полезное,"-g":'0'
#размер '-s':'340x240'
    output_params = {"-f": "rtsp", '-pix_fmt': 'yuv420p', "-rtsp_transport": "tcp","-g":"0"}
    writer = WriteGear(output_filename='rtsp://192.168.1.102:8554/stream', logging=True, **output_params)

    while True:
        frame = stream.read()
        if frame is None:
            break
        writer.write(frame)
#        cv2.imshow("Output Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    stream.stop()
    writer.close()