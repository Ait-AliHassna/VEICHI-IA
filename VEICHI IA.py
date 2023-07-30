import cv2
from mymodule import handsFinder,findPosition
import numpy as np
import math
import time
import serial
L=0
S=0
R=0
hnd=None
progBar=20
calibration_time=30
TIMER = int(5)
frame_elapsed=0
font=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
prevTime=0
task=""
task1=""
sens=""
cmd=""
speed=0
count=0
list_task=[S,L,R]
font=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
path=r'C:\Users\HASSNA AIT-ALI\Desktop\Formation IOT\Heliantha robotics\Moteur IA\Codes\Designe\MOTOR.jpg'
path2=r'C:\Users\HASSNA AIT-ALI\Desktop\Formation IOT\Heliantha robotics\Moteur IA\Codes\Designe\\right.png'
imag_motor=cv2.imread(path)
imag_sens=cv2.imread(path2)
imag_motor=cv2.resize(imag_motor,(100,100))
imag_sens=cv2.resize(imag_sens,(40,40))
#configuration de la comunication Serial 

arduino = serial.Serial(port='COM13', baudrate=9600, timeout=.1)
#'/dev/ttyACM0'
#arduino.flush()
def write_read(list_task):
    arduino.flush()
    y=list_task[1]
    z=list_task[2]
    x=list_task[0]
    if(y>0):
        val=int(y)
    else:
        val=""
    result=str(z)+","+str(x)+","+str(val)
    print("value",result)
    arduino.write(bytes(result, 'utf-8'))
    time.sleep(2)
    data = arduino.readline()
    return data
#defined speed of motor
def change_speed(listfinger,count)-> int :
    L=0
    print("list",listfinger)
    x1,y1=listfinger[4][1],listfinger[4][2]
    #get the x,y of the second finger 
    x2,y2=listfinger[8][1],listfinger[8][2]
    #cv2.circle(image,(x1,y1),10,(255,255,255),cv2.FILLED)
    #cv2.circle(image,(x2,y2),10,(255,255,255),cv2.FILLED)
    if(count>0):
        cv2.circle(image_principal,(x1,y1),10,(255,255,255),cv2.FILLED)
        cv2.circle(image_principal,(x2,y2),10,(255,255,255),cv2.FILLED)
        cv2.line(image_principal,(x1,y1),(x2,y2),(0,0,0),3)
        #cv2.rectangle(image, (20, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(image, (20, 260), (85, 450), (0, 0, 0), 3)
        L=math.hypot(x2-x1,y2-y1)
        mL=L
        progBar=np.interp(int(mL),[20,250],[450,260])
        cv2.rectangle(image, (20, int(progBar)), (85, 450), (255, 0, 0), cv2.FILLED)
    #print("lenght ", L)
    #print("L",mL)
    #print(progBar,mL)
    L=(L/250)*100
    if(L>100):
        L=100
    val=(L/100)*(50)

    val=int(val)*100
    #print("pourcentage,val,",L,val)
    return val
# defined direction of motor 
def motor_direction(listfinger) -> int:
    S=0
    if(listfinger[0][1]>listfinger[17][1] and listfinger[0][1]>listfinger[18][1] and listfinger[0][1]>listfinger[19][1] and listfinger[0][1]>listfinger[20][1]):
           S=1 
    if(listfinger[0][1]<listfinger[17][1] and listfinger[0][1]<listfinger[18][1] and listfinger[0][1]<listfinger[19][1] and 
           listfinger[0][1]<listfinger[20][1]):
           S=2
    return S
#defined the state of motor 
def motor_demarrage(listfinger) -> int:
      Result=0
      MyId=[4,8,12,16,20]
      Fingers=[]
      if(listfinger[4][1]<listfinger[3][1]):
          Fingers.append('o')
      else:
          Fingers.append('c')
      for i in range(1,5):
        if(listfinger[MyId[i]][2]<listfinger[MyId[i]-2][2]):
            Fingers.append('o')
        else:
            Fingers.append('c')
      if(Fingers.count('o')==5):
          Result=1
      if(Fingers.count('c')==5):
          Result=2  
      if(Fingers.count('o')==2 or ((Fingers.count('o')==1 and listfinger[4][1]>listfinger[3][1]))):
          Result=3
      return Result   
#get command
def get_command(listfinger):
      Result=0
      task=""
      MyId=[4,8,12,16,20]
      Fingers=[]
      time.sleep(0.05)
      if(listfinger[4][1]<listfinger[3][1]):
        Fingers.append('o')
      else:
          Fingers.append('c')
      for i in range(1,5):
          if(listfinger[MyId[i]][2]<listfinger[MyId[i]-2][2]):
              Fingers.append('o')
          else:
              Fingers.append('c')
     # if(Fingers.count('o')==3):
          #task="Direction Motor"
      if(Fingers.count('o')==2):
          task="Speed Motor"
      else:
          if((listfinger[0][1]>listfinger[3][1] and listfinger[0][1]>listfinger[5][1] and listfinger[0][1]>listfinger[7][1]) 
         or (listfinger[0][1]<listfinger[3][1] and listfinger[0][1]<listfinger[5][1] and listfinger[0][1]<listfinger[7][1])):
              task="Direction Motor"
          if(listfinger[0][1]>listfinger[3][1] and listfinger[0][2]>listfinger[3][2] and listfinger[0][1]>listfinger[7][1] and listfinger[0][2]>listfinger[7][2]):
              task="motor_demarrage"
      #if(Fingers.count('o')==1):
          #task="motor_demarrage"
      return task     
# command Cancelled (Non utlisé) --- function de teste
def canceled_act(listfinger) -> int:
      Result=0
      MyId=[4,8,12,16,20]
      Fingers=[]
      time.sleep(0.05)
      if(listfinger[4][1]<listfinger[3][1]):
        Fingers.append('o')
      else:
          Fingers.append('c')
      for i in range(1,5):
          if(listfinger[MyId[i]][2]<listfinger[MyId[i]-2][2]):
              Fingers.append('o')
          else:
              Fingers.append('c')
      if(Fingers.count('o')==1 and listfinger[4][1]>listfinger[3][1]):
        #print("Canceld")
        Result= 1
      return Result  
   
cap=cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
while True :
    #count=0
    ret, image_principal= cap.read()
    ret,image=cap.read()

   # image=cv2.resize(image)
    image_principal=cv2.resize(image_principal,(480, 480))

    image_principal=cv2.flip(image_principal,1)
    image=cv2.flip(image,1)
    image=cv2.resize(image,(480, 480))
    if(list_task[1]<0):
        speed=0
    else:
        speed=int(list_task[1]/100)
    cv2.putText(image,"Task :"+(str(task1)),(40,80),font,1,(0,0,0),2,cv2.LINE_AA)
    text = "Variation \n de vitesse "
    y0, dy = 130,30
    for i, line in enumerate(text.split('\n')):
        y = y0 + i*dy
        cv2.putText(image, line, (5, y ), font,1,(0,0,0),2,cv2.LINE_AA)
        #cv2.putText(image,"Variation \n de vitesse :",(5,200),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(image,"Vitesse :"+(str(speed)+"Hz"),(5,200),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(image,"Attente : "+(str(int(TIMER)))+" s",(5,250),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.rectangle(image, (20, 260), (85, 450), (0, 0, 0), 3)
    cv2.rectangle(image, (240, 150), (245, 450), (255, 255, 255), 3,cv2.FILLED)
        # sens de rotation
    text = "Variation \n de Rotation "
    y0, dy = 130,30
    for i, line in enumerate(text.split('\n')):
        y = y0 + i*dy
        cv2.putText(image, line, (245, y ), font,1,(0,0,0),2,cv2.LINE_AA)
        #cv2.putText(image,"Variation \n de vitesse :",(5,200),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(image,"Sens :"+(str(sens)),(255,200),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(image,"Attente :"+(str(int(TIMER)))+" s",(255,250),font,1,(0,0,0),2,cv2.LINE_AA)
    image[310:350,255:295]=imag_sens
    image[310:350,320:360]=imag_sens
    image[360:460,255:355]=imag_motor
    #cv2.rectangle(image, (20, 150), (85, 400), (0, 0, 0), 3)
    #cv2.putText(image," Speed :"+(str(speed)+"Hz"),(20,100),font,1,(0,0,0),2,cv2.LINE_AA)
    #cv2.putText(image," Sens :"+(str(sens)),(90,300),font,1,(0,0,0),2,cv2.LINE_AA)
    #cv2.putText(image," cmd :"+(str(cmd)),(90,400),font,1,(0,0,0),2,cv2.LINE_AA)
    #cv2.putText(image," Waiting ... :"+(str(int(TIMER)))+" s",(90,200),font,1,(0,0,0),2,cv2.LINE_AA)
    #cv2.putText(image,"     Task :"+(str(task1)),(90,450),font,1,(0,0,0),2,cv2.LINE_AA)
    #frame_elapsed+=1
    image_principal=handsFinder(image_principal)
    listfinger=findPosition(image_principal)
    if(len(listfinger)!=0):
        if(count==0):
            task=get_command(listfinger)
            task1="?"
            mtime=time.time()
            #cur=time.time()
            if(mtime-prevTime>=1):
                prevTime=mtime
                TIMER=TIMER-1
                if(TIMER==0):
                    print("task",task)
                    TIMER=5
                    prevTime=0
                    count=1
        #print("count",count)
        elif(count==1):
            print("voila task",task)
            if( task == "Speed Motor"):
                L=change_speed(listfinger,1)
                list_task[1]=L
                list_task[0]=0
                list_task[2]=2
                task1="Speed Motor........."
            if( task == "Direction Motor"):
                S=motor_direction(listfinger)
                list_task[0]=S
                if(S==2):
                    sens="Right"
                if(S==1):
                    sens="Left"
                if(S==0):
                    sens="Error"
                list_task[1]=-1
                list_task[2]=0
                task1="Direction Motor........."
            if( task== "motor_demarrage"):
                R=motor_demarrage(listfinger)
                if(R==1):
                    cmd="OFF"
                if(R==2):
                    cmd="ON"
                list_task[2]=R
                list_task[1]=-1
                list_task[0]=0
                task1="motor_demarrage ........."
            mtime=time.time()
            #cur=time.time()
            print("HEUR",mtime-prevTime)
            if(mtime-prevTime>=1):
                print("TIMER",TIMER)
                prevTime=mtime
                TIMER=TIMER-1
                #=TIMER
                if(TIMER<=3):
                    cv2.putText(image,(str(int(TIMER)))+" s",(200,300),font,10,(0,0,255),4,cv2.LINE_AA)
                if(TIMER==0):
                    print("HI",TIMER)
                    TIMER=5
                    write_read(list_task)
                    time.sleep(2)
                    write_read(list_task)
                    count=0





        '''
        #print("I_P",listfinger[0][1],listfinger[17][1] , listfinger[0][1],listfinger[18][1] , listfinger[0][1],listfinger[19][1] , listfinger[0][1],listfinger[20][1])
        #print("I",listfinger[0][1],listfinger[17][1] , listfinger[0][1],listfinger[18][1] , listfinger[0][1],listfinger[19][1] , listfinger[0][1],listfinger[20][1])
        # GET THE SENS OF THE MOTOR 
        #get the command
        #cv2.putText(image," Commande ? 1:ON/OFF 2: Speed 3: Sens ",(80,200),font,1,(0,255,255),2,cv2.LINE_AA)
        
            print("phaseteste")
            L=change_speed(listfinger,0)
            S=motor_direction(listfinger)
            R=motor_demarrage(listfinger)
           # print("change_speed",L,"motor_direction",S,"motor_demarrage",R)

            if ((R==2 and S==2 ) or (R==1 and S==2 ) ):
                task="motor_demarrage"
                task1="?"
            if((R==0 and S==2) or (R==0 and S==1)):
                task="Direction Motor"
                task1="?"
            if(R==3 ):
                task="Speed Motor"
                task1="?"
            
        if(count==0):
            task=get_command(listfinger)
        if(len(task)>0):
            count+=1
            print("task",task,len(task))
            if( task == "Direction Motor"):
              
                S=motor_direction(listfinger)
                list_task[0]=S
                if(S==2):
                    sens="Right"
                if(S==1):
                    sens="Left"
                if(S==0):
                    sens="Error"
            if( task == "Speed Motor"):
                L=change_speed(listfinger)
                list_task[1]=L
            if( task== "motor_demarrage"):
                R=motor_demarrage(listfinger)
                if(R==1):
                    cmd="OFF"
                if(R==2):
                    cmd="ON"
                list_task[2]=R
            print("T",task,count)
            #list_task.append()
            #listfinger=take_instance_photo()
            mtime=time.time()
            #cur=time.time()
            if(mtime-prevTime>=1):
                prevTime=mtime
                TIMER=TIMER-1
                #=TIMER
                if(TIMER<4):
                    cv2.putText(image,(str(int(TIMER)))+" s",(200,300),font,10,(0,0,255),4,cv2.LINE_AA)
                if(TIMER==0):
                    TIMER=5
                    write_read(list_task)
                    count=0
                    #get_command(listfinger)


                    count+=1
                
                    if(count==1):
                        task="Speed Motor"
                        TIMER=5
                    if( count==2):
                        task="motor_demarrage"
                        TIMER=5
                if(count==3):
                    print ("done")
                    write_read(list_task)
                    TIMER=int(5)
                    task="Direction Motor"
                    count=0
                '''
    #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    image_result = np.concatenate((image, image_principal), axis=1)
    cv2.imshow("two images",image_result)
   # cv2.imshow("window",image_principal)
    if(cv2.waitKey(1) & 0xFF == ord('x')):
        print("Speed",list_task[1],"direction",list_task[0])
        break
    #cv2.rectangle(image, (20, 500), (300, 150), (255, 0, 0), 3)
    #cv2.waitKey(1)
cap.release()

cv2.destroyAllWindows()