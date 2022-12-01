import cv2
import os, glob

def take_picture():

    #Selects which camera to use
    cam_port = 0

    #Variable for video capture                                    
    cam = cv2.VideoCapture(cam_port)                

    while True:

        #ret checks if video capt is available, frame is the frame captured
        ret,frame = cam.read()                      
        if ret == True:
       
            key = cv2.waitKey(1)

            #shows frames that are captured by camera real time
            cv2.imshow("frame",frame)              

            #If Escape button pressed
            if key%265 == 27:                      
                print('Escape hit, closing app')
                print('No photo taken')
                break                               #Closes app
           
            #If space button pressed
            elif key%256 == 32:                    
                img_name = 'opencv_img.png'         #Captures a frame
                cv2.imwrite(img_name,frame)         #Saves image in the same directory
                break                               #After one picture, it closes the app

    cam.release()
    cv2.destroyAllWindows()
    return

def detect_face(filename):
    # Load the cascade file which is used to detect faces
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Read the input image
    img = cv2.imread(filename)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detects faces using the cascade
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
   
    i=0
    for i in range(0,len(faces)):           #This for loop crops all found faces and
                                            #creates a file with them
        factor = int((faces[i][2])*0.4)     #Factor to adjust size of crop

        #x, y, h and w are used for finding the face in the photo and the cropping it
        #I've manually adjusted these values a little to get a larger crop.
        #Can be adjusted with factor
        x=faces[i][0]-factor
        y=faces[i][1]-int(factor*1.5)
        h=faces[i][3]+(factor*2)
        w=faces[i][2]+(factor*2)
        crop = img[y:(y+w), x:(x+h)]        #Creates the cropped images of the faces

        #Saves each file with new name if there are multiple
        img_name = (f'face_{i+1}.png')
        cv2.imwrite(img_name,crop)

    #This prints the number of faces that were found in the photo
    print(f'{i+1} face(s) detected in that photo.')
    if i>0:
        print('Pictures of individual faces were created.')
       
    cv2.waitKey()

#Removes all previous pictures when starting the program
def remove_files():
    for filename in glob.glob('C:/Users/Arttu/OneDrive/Tiedostot/1/School/OneDrive - LUT University/.Lahti-Lut/Year 2/Smart systems/assingment 3/FaceDetectionApp/face_*'):
        os.remove(filename)  
    if os.path.isfile('opencv_img.png'):
        os.remove('opencv_img.png')  

#Menu
while True:
    remove_files()
    user = input('Do you want to 1.Take a photo or 2.Use existing photo? (1 or 2)')
    if user == '1':
        take_picture()
        if os.path.isfile('opencv_img.png'):
            detect_face('opencv_img.png')
        break

    elif user == '2':
        img_name = cv2.imread('threepeople.jpg')
        cv2.imshow('example', img_name)
        detect_face('threepeople.jpg')
        break