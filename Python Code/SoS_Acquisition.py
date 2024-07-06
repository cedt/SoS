'''
Program By Harsh Sharma at TI-CEPD, NSUT
This program is the accompanying program for a set of Physics experiments using Science on a Stick
for more information regarding the experiment, please refer to the Science on a Stick Article

Here, data is read over USB Serial communication from the experiment setup as described in the article
this data is processed and stored in a CSV file along with a graph
'''

#Necessary imports
import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import os
# Create directories if they don't exist
os.makedirs("data/X/", exist_ok=True)
os.makedirs("data/Y/", exist_ok=True


'''
COM Port, The first argument of function below needs to changed according
to which port the Arduino described in the experiment setup is plugged into
Please refer to device manager (or equivalent) in your system properties
after plugging in Arduino to find out the exact com port
'''
arduinoData=serial.Serial('COM3',115200)

date_string = time.strftime("%d-%m-%y-%H-%M")       #To store current date, used for file names


def is_Int(s):
    
    '''
    Returns True if the given argument is an instance of integer datatype
    False Otherwise
    '''

    try:
        int(s)
        return True
    except ValueError:
        return False


flag=True

def capture():
    
    '''
    Main method to capture and store sensor readings data coming over USB Serial from Arduino
    This function captures the data, scales it into actual physical values and stores the data in a CSV format

    Format of csv stored is <current_date_and_time>.csv

    Reads data from Arduino over USB Serial until End of Data Flag is encoutered
    '''

    a=[]
    count1=0
    myData1=0
    val1=0

    while True:

        while(arduinoData.inWaiting==0):    #Wait till data is received
            pass

        myData1=arduinoData.readline()
        myData1=myData1[:-2:]

        if(is_Int(myData1)):
            
            if(int(myData1)==3000):         #Read until End of Data flag is received
                break
            else:
                myData1=float(myData1)      #Scale data accroding to physcial values
                myData1=(myData1*5)/1023
                myData1=myData1-2.5
                #myData1=(myData1*1068)/68

                if(count1==0) :
                    val1=myData1
                    myData1=myData1-val1
                else:
                    myData1=myData1-val1

                a.append(myData1)           #append current reading into a list
                count1=count1+1


    n=0
    val1=[]
    while(n<2):
        while(arduinoData.inWaiting==0):    #Start and End time values are received after End of Data flag
            pass

        myData1=arduinoData.readline()
        myData1=myData1[:-2:]

        if(is_Int(myData1)) :
            val1.append(int(myData1))
            n=n+1

    print('End')                            #End of data read over USB Serial

    time1 = np.linspace(0,val1[1]-val1[0],count1)   #Timestamp array for each reading

    #Try add into CSV 
    saveX = np.asarray(time1)
    saveY = np.asarray(a)
    print(len(saveX))

    np.savetxt("data/X/" + date_string + '.csv', saveX, delimiter = ",")
    np.savetxt("data/Y/" + date_string + '.csv', saveY, delimiter = ",")
    plt.plot(time1,a)                       #Plot the data


    # plt.show()
    plt.pause(0.1)


print('Enter the number of plots you need')
counter = int(input())

plt.grid(True)
plt.ylabel('Voltage (in V)')
plt.xlabel('Time (in ms) ')
plt.title("Lenz Law demonstration")

for i in range(counter):
    print('plot number', i+1, )
    date_string = time.strftime("%d-%m-%y-%H-%M-%S")
    capture()

plt.show()

input("<Press any key to Exit>")
exit()
