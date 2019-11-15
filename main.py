import cv2

video = cv2.VideoCapture('video.mp4')
first_frame = None

a = 0
while True:
    a = a+1
    flag, frame = video.read()

    gray_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (15, 15), 0)

    if first_frame is None:
        first_frame = gray_frame
        continue

    delta_frame = cv2.absdiff(first_frame, gray_frame)
    threshold_frame = cv2.threshold(delta_frame , 30 , 255 , cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame , None , iterations = 2)

    (cnts , _ ) = cv2.findContours(threshold_frame.copy() , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame , (x,y) , (x+w , y+h) , (0, 255, 255) , 1)


    cv2.imshow('DETECTOR  ', frame)
    cv2.imshow('DELTA FRAME ', delta_frame)
    cv2.imshow('THRESHOLD FRAME ', threshold_frame)
    cv2.imshow('GRAYSCALE FRAME ', gray_frame)

    key = cv2.waitKey(30)
    if key == ord('q'):
        break

print ('total loops were ' + str(a))
cv2.destroyAllWindows