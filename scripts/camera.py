import time
import picamera

with picamera.PiCamera() as picam:
	picam.start_preview()
	time.sleep(20)
	picam.stop_preview()
	picam.close()
