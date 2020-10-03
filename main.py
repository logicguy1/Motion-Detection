import time
import cv2

def get_diff(*numbers): #function to calculate the diffrence between two numbers will always return between 1 and 0
    if min(numbers) == 0:
        return 1-1
    try:
        out = (max(numbers) - min(numbers)) / min(numbers)
        return out
    except ZeroDivisionError:
        return 1-1


cv2.namedWindow("Motion Capture") # create the window
vc = cv2.VideoCapture(0) # setup the video capture

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

squres = 0 #get the ammount of squres that it is calculateing
for y in range(0, len(frame), 8):
    for x in range(0, len(frame[0]), 8):
        squres += 1

oldImg = None # the old imave is set
data = {} # data is used to manage all the dots and their respective values

while rval: # while the camera is active
    # time.sleep(.02)

    for i in range(5): # Update the camera 20 times to get fluid fps
        rval, frame = vc.read() # get the next frame from the camera

        for pos, val in data.items(): #loop through each dot and apply them
            pos = pos.split(",")

            frame[int(pos[0])+1, int(pos[1])] = [0,val,0]
            frame[int(pos[0])+2, int(pos[1])] = [0,val,0]
            frame[int(pos[0]), int(pos[1])+1] = [0,val,0]

        cv2.imshow("Motion Capture", frame) # Update the window

        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

    start = time.time() # Initialise the timer

    data = {} # clear the data in data lol

    sqAmount = 0 #this keeps track of the current lit squres

    for y in range(0, len(frame), 8): # loop throught the 2d array
        for x in range(0, len(frame[0]), 8):
            # print(frame[y, x])
            if oldImg is not None: # Make sure we calculated the first image before
                oldPix = oldImg[y, x] # get the rbg value of the old and new image
                newPix = frame[y, x]

                diff0 = get_diff(oldPix[0], newPix[0]) #get the diffrence between the old and new pixel values
                diff1 = get_diff(oldPix[1], newPix[1])
                diff2 = get_diff(oldPix[2], newPix[2])

                diffrence = (diff0 + diff1 + diff2) / 3 # calculate the avrige diffrance between the 3 color channels

                data[f"{y},{x}"] = diffrence * 255 # apply the recently created data in the data dictionery

                if diffrence > .8: #check if the diffrence in pixels is over 80%
                    sqAmount += 1 #increace the counter by 1

    oldImg = frame # update old image variable

    print(f"{sqAmount} / {squres} Squres detected movement") #tell the user how much "movement" there was in the image
    print(f"Calculations took {round((time.time() - start) * 1000)} ms") # Tell the user how long it took to calculate the data

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("Motion Capture") # close the window
