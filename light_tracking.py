import cv2
import time

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('source/prosvet_cut.mp4')


def wagon_tracker(camera_capture):
    wagon = 1
    line = 250

    # for tracking
    first_pos = 0
    last_pos = 0

    # coordinates
    x1 = 500
    y1 = 200
    width = 900
    height = 500
    while True:
        # Camera
        _, frame = camera_capture.read()

        #             y1:y2         x1:x2
        belt = frame[y1:y1+height, x1: x1+width]
        #gray_belt = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_belt = cv2.cvtColor(belt, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray_belt, 110, 255, cv2.THRESH_BINARY)

        # Detection
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            # return coordinates for each found contour
            (x, y, w, h) = cv2.boundingRect(cnt)

            # Get the area
            area = int(cv2.contourArea(cnt))
            if area>18000:# > 20000 and area < 30000:
                #if aspect_ratio >= 0.80 and aspect_ratio <= 1.20:
                if w>80 and w<250 and h>270 and h<320:
                    # text      where     what    coord  font,size,color   AREA
                    cv2.putText(belt, str(area), (x,y+50), 0, 1, (0,255,0))

                    # Width
                    #cv2.putText(belt, f"Width: {str(w)}", (x, y+100), 0, 1, (255, 0, 0))

                    # Height
                    #cv2.putText(belt, f"Height: {str(h)}", (x, y+150), 0, 1, (255, 0, 0))

                    # Draw a rectange,                        green color, 3 thickness           
                    cv2.rectangle(belt, (x, y), (x+w, y+h), (0, 255, 0), (3))

                    # If we're already tracking
                    if first_pos != 0:    
                        last_pos = x

                    # If this is the first time
                    else:
                        # start of light, also record the time
                        first_pos = x
                        time_start = time.time()

            # Check if light tracking has been going 
            if first_pos != 0:
                #if 10 seconds have passed
                if int(time.time()-time_start) >= 5:
                    distance = last_pos-first_pos

                    # if certain distance has passed
                    if distance < -500:
                        # TODO save wagon and bag number into database
                        wagon += 1

                        # reset the light
                        first_pos = 0
                    
            # Draw the count of wagons
            cv2.putText(belt, str(wagon), (0, 25), 0, 1, (0,255,0))




        #cv2.imshow("Frame", frame)
        #cv2.imshow("Frame gray", gray_frame)
        #cv2.imshow("Threshhold", threshold)
        cv2.imshow("Belt", belt)

        key = cv2.waitKey(1)
        if key == 27:
            break

    camera_capture.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    wagon_tracker(cap)