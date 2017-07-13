import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "RTIMULib"
ROUND_DECIMALS = 2
print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(False)

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

dataFile = open(str(int(time.time())),'w')
dataFile.write("#\tTime\tAcc[x]\tAcc[y]\tAcc[z]\tGyro[x]\tGyro[y]\tGyro[z]\n")
dataCount = 0
summ = 0
startTime = time.time()
while True:
  if imu.IMURead():
    currTime = time.time() - startTime
    data = imu.getIMUData()
##    summ += math.degrees(data['gyro'][1])
##    print summ / 100
    print currTime
    dataCount += 1
    dataFile.write(str(dataCount) + "\t" + str(round(currTime,5)) + "\t" + str(round(data["accel"][0],ROUND_DECIMALS)) + "\t" + str(round(data["accel"][1],ROUND_DECIMALS)) + "\t" + str(round(data["accel"][2],ROUND_DECIMALS)) + "\t" + str(round(math.degrees(data["gyro"][0]),ROUND_DECIMALS)) + "\t" + str(round(math.degrees(data["gyro"][1]),ROUND_DECIMALS)) + "\t" + str(round(math.degrees(data["gyro"][2]),ROUND_DECIMALS)) + "\n")
    time.sleep(poll_interval*1.0/1000.0)
    
