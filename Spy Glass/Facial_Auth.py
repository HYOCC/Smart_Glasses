import os
import face_recognition
import cv2 
import time 

def first_time_auth(user_id:str, Name:str):
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Error: Unable to access the camera")
        return
    
    
    run = True 
    
    while run:
        
        if os.path.exists(f'Known_Face/{user_id}'):
            pass
        else:
            os.mkdir(f'Known_Face/{user_id}')
            print('Successfully made folder for new user_id') 
        
        #SLowing down taking picture for authentication and takes 15 picture of training usage for algorithm to recognize
        num_of_pics = 1
        slow_down_pic_frame = 1        
        
        #Finds the face 15 times and saves it as a image to be used for facial recoginition        
        while num_of_pics <= 15:
            if slow_down_pic_frame % 5 == 0: 
                #Check if there is existing frame, ret is a Boolean indicator for frame
                ret, frame = cam.read() 
                
                if not ret: 
                        print('Something went wrong getting the camera feed')
                        break
                    
                # Convert the frame from BGR (OpenCV format) to RGB (face_recognition format)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                
                
                # Detect face locations in the frame
                face_location = face_recognition.face_locations(rgb_frame, model="hog")  # Use "cnn" for GPU acceleration
                
                if face_location:
                    # Select only the first detected face
                    top, right, bottom, left = face_location[0]
                    
                    first_face = frame[top:bottom, left:right]
                    
                    cv2.imwrite(f'Known_Face/{user_id}/{Name + str(num_of_pics)}.jpg', first_face)
                    print(f'Added image Known_Face/{user_id}/{Name + str(num_of_pics)}')
        
                    num_of_pics += 1
                    
            slow_down_pic_frame += 1
            #Adds a delay for the next iteration
            time.sleep(0.15)
            
        run  = False 
    
    #Lets go all of resouces such as the cam etc
    cam.release()
    cv2.destroyAllWindows()





user_id = input("Choose your unique ID: ")
user_id_prefer_name = input('What would you like to be called?: ')
first_time_auth(user_id, user_id_prefer_name)
    
        
        
        
        
        
        
         
    
    