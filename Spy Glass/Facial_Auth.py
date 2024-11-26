import os
from face_recognition import load_image_file, face_locations, face_encodings, compare_faces
import cv2 
from time import sleep

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
                face_location = face_locations(rgb_frame, model="hog")  # Use "cnn" for GPU acceleration
                
                if face_location:
                    # Select only the first detected face
                    top, right, bottom, left = face_location[0]
                    
                    first_face = frame[top:bottom, left:right]
                    
                    cv2.imwrite(f'Known_Face/{user_id}/{Name + str(num_of_pics)}.jpg', first_face)
                    print(f'Added image Known_Face/{user_id}/{Name + str(num_of_pics)}')
        
                    num_of_pics += 1
                    
            slow_down_pic_frame += 1
            #Adds a delay for the next iteration
            sleep(0.15)
            
        run  = False 
    
    #Lets go all of resouces such as the cam etc
    cam.release()
    cv2.destroyAllWindows()




def authenticate(user_id:str):
    #Loads in available images from given user id to load in data
    if os.path.exists(f'Known_Face/{user_id}'):
        user_id_dir = f'Known_Face/{user_id}'            
        user_id_with_face = {}

        for image_name in os.listdir(user_id_dir):
            image_path_file = os.path.join(user_id_dir, image_name)
            print(image_path_file)#Logging
            
            image = load_image_file(image_path_file)
            encodings = face_encodings(image)

            if encodings:
                if user_id_with_face:
                    user_id_with_face[user_id].append(encodings[0])
                else:
                    user_id_with_face[user_id] = [encodings[0]]
                #known_names.append(os.path.splitext(image_name)[0])  # Use filename as label
            print('known faces lodaded and encoded')
            print(user_id_with_face)
    else:
        print('Cant find user_id ' + user_id)
        print(f'Known_Face/{user_id}')
        return 
    
    run = True 
    #Starts cam
    cam = cv2.VideoCapture(0)
    #Starts authenticating User
    while run:
        ret, frame = cam.read() #Checks if frames was successfully captured then save the frame onto 'frame'
    
        if not ret:
            print('failed to grab ret')
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Changes the BGR to RGB which is required for facial recognization
        
        face_location = face_locations(rgb_frame, model='hog') #Detects faces 
        face_encoding = face_encodings(rgb_frame, face_location) #Encodes the faces 
        
        #Compares the seen face to known faces
        for (top, right, bottom, left), encoding in zip(face_location, face_encoding):
            matches = compare_faces(user_id_with_face[user_id], encoding)
            if True in matches:
                print('detected ' + user_id)
                run = False #breaks the finding person function once a detected person is found
    #Lets go all of resouces such as the cam etc
    cam.release()
    cv2.destroyAllWindows()
        
    
    
    

    
authenticate('HYO)C')