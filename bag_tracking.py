import cv2

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('source/conveyer.mpg')



bags = 0
found_over = False
line = 100
while True:
    # Camera
    _, frame = cap.read()

    #             y1:y2    x1:x2
    belt = frame[200:900, 390: 900]
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
        if area > 40000: # and area < 4500:
            # square will have ap of about 1
            aspect_ratio = w / float(h)
            
            if aspect_ratio >= 0.80 and aspect_ratio <= 1.20:
                # text      where     what    coord     font,size,color
                cv2.putText(belt, str(area), (x,y), 0, 1, (0,255,0))

                # Draw a rectange,                        green color, 3 thickness           
                cv2.rectangle(belt, (x, y), (x+w, y+h), (0, 255, 0), (3))
                
                if y>line and found_over:
                    found_over = False

                if y < line and found_over==False:
                    bags += 1
                    found_over = True
                
        # Draw the count of bags
        cv2.putText(belt, str(bags), (0, 25), 0, 1, (0,255,0))

        #Draw the line  x1  y1   x2   y2
        cv2.line(belt, (0, line), (510, line), (0, 0, 255), thickness=2)



    #cv2.imshow("Frame", frame)
    #cv2.imshow("Frame gray", gray_frame)
    #cv2.imshow("Threshhold", threshold)
    cv2.imshow("Belt", belt)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()