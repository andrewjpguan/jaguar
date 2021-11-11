from BaseLibrary.Code.Server.Motor import*
from cv.faceDetect import Vision
from rpi_ws281x import *
import time

cv = Vision()
PWM = Motor()
led = Led()


try:
    idleCount = 0
    m1i = m2i = m3i = m4i = 0  # Forward/backwards values
    # Main robot loop goes here
    while True:
        (x, y, w, h) = cv.get_bounding_box()
        # print(f"{x}, {y}, {w}, {h}")
        relativeX = cv.get_x_center() - x - w / 2
        m1t = m2t = m3t = m4t = 0  # Turning Values
        if w != 0 and abs(relativeX) >= 75:
            if relativeX < 0:
                print("Turning right")
                m1t, m2t, m3t, m4t = 600, 600, -600, -600
            elif relativeX > 0:
                print("Turning left")
                m1t, m2t, m3t, m4t = -600, -600, 600, 600

        if w > 100 and h > 100:
            # Too close
            print("Going backwards")
            m1, m2, m3, m4 = m1 - 800, m2 - 800, m3 - 800, m4 - 800
            led.colorWipe(led.strip, Color(255, 0, 0))
            idleCount = 0
        elif 0 < w < 60 and 0 < h < 60:
            # Too far
            print("Going forwards")
            m1, m2, m3, m4 = m1 + 800, m2 + 800, m3 + 800, m4 + 800
            led.colorWipe(led.strip, Color(0, 255, 0))
            idleCount = 0
        elif idleCount < 5:
            print("Idling")
            idleCount += 1
            led.colorWipe(led.strip, Color(0, 0, 255))
        else:
            print("No f/b movement")
            m1i, m2i, m3i, m4i = 0, 0, 0, 0

        PWM.setMotorModel(m1t + m1i, m2t + m2i, m3t + m3i, m4t + m4i)

except KeyboardInterrupt:
    PWM.setMotorModel(0, 0, 0, 0)
    cv.destroy()
    led.colorWipe(led.strip, Color(0,0,0),10)
