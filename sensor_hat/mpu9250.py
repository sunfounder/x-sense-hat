# mpu9250.py MicroPython driver for the InvenSense MPU9250 inertial measurement unit
# Authors Peter Hinch, Sebastian Plamauer
# V0.5 17th June 2015

'''
mpu9250 is a micropython module for the InvenSense MPU9250 sensor.
It measures acceleration, turn rate and the magnetic field in three axis.

The MIT License (MIT)
Copyright (c) 2014 Sebastian Plamauer, oeplse@gmail.com, Peter Hinch
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from ezblock import delay as sleep_ms
from sensor_hat.imu import MPU6050, bytes_toint, MPUException
from sensor_hat.vector3d import Vector3d
import math
import threading
from math import sqrt, degrees, acos, atan2

def default_wait():
    '''
    delay of 50 ms
    '''
    sleep_ms(50)

compass_quadrant_list = ["N","NE","E","SE","S","SW","W","NW"]

class MPU9250(MPU6050):
    '''
    MPU9250 constructor arguments
    1. side_str 'X' or 'Y' depending on the Pyboard I2C interface being used
    2. optional device_addr 0, 1 depending on the voltage applied to pin AD0 (Drotek default is 1)
       if None driver will scan for a device (if one device only is on bus)
    3, 4. transposition, scaling optional 3-tuples allowing for outputs to be based on vehicle
          coordinates rather than those of the sensor itself. See readme.
    '''

    _mag_addr = 12          # Magnetometer address
    _chip_id = 113

    def __init__(self, side_str, device_addr=None, transposition=(0, 1, 2), scaling=(1, 1, 1)):

        super().__init__(side_str, device_addr, transposition, scaling)
        self._mag = Vector3d(transposition, scaling, self._mag_callback)
        self.accel_filter_range = 0             # fast filtered response
        self.gyro_filter_range = 0
        self._mag_stale_count = 0               # MPU9250 count of consecutive reads where old data was returned
        self.mag_correction = self._magsetup()  # 16 bit, 100Hz update.Return correction factors.
        self._mag_callback()  # Seems neccessary to kick the mag off else 1st reading is zero (?)
        self.imu_timer = threading.Thread(target=self.imu_thread, name="Thread1")
        self.accel_data = [0,0,0]
        self.gyro_data = [0,0,0]
        self.mag_data = [0,0,0]
        self.roll = 0
        self.pitch = 0


    def start_imu(self):
        self.imu_timer.setDaemon(True)
        self.imu_timer.start()

    @property
    def sensors(self):
        '''
        returns sensor objects accel, gyro and mag
        '''
        return self._accel, self._gyro, self._mag

    # get temperature
    @property
    def temperature(self):
        '''
        Returns the temperature in degree C.
        '''
        try:
            self.buf2 = self._read(self.buf2, 0x41, self.mpu_addr)
        except OSError:
            raise MPUException(self._I2Cerror)
        return bytes_toint(self.buf2[0], self.buf2[1])/333.87 + 21  # I think

    # Low pass filters
    @property
    def gyro_filter_range(self):
        '''
        Returns the gyro and temperature sensor low pass filter cutoff frequency
        Pass:               0   1   2   3   4   5   6   7
        Cutoff (Hz):        250 184 92  41  20  10  5   3600
        Sample rate (KHz):  8   1   1   1   1   1   1   8
        '''
        try:
            self.buf1 = self._read(self.buf1, 0x1A, self.mpu_addr)
            res = self.buf1[0] & 7
        except OSError:
            raise MPUException(self._I2Cerror)
        return res

    @gyro_filter_range.setter
    def gyro_filter_range(self, filt):
        '''
        Sets the gyro and temperature sensor low pass filter cutoff frequency
        Pass:               0   1   2   3   4   5   6   7
        Cutoff (Hz):        250 184 92  41  20  10  5   3600
        Sample rate (KHz):  8   1   1   1   1   1   1   8
        '''
        if filt in range(8):
            try:
                self._write(filt, 0x1A, self.mpu_addr)
            except OSError:
                raise MPUException(self._I2Cerror)
        else:
            raise ValueError('Filter coefficient must be between 0 and 7')

    @property
    def accel_filter_range(self):
        '''
        Returns the accel low pass filter cutoff frequency
        Pass:               0   1   2   3   4   5   6   7 BEWARE 7 doesn't work on device I tried.
        Cutoff (Hz):        460 184 92  41  20  10  5   460
        Sample rate (KHz):  1   1   1   1   1   1   1   1
        '''
        try:
            self.buf1 = self._read(self.buf1, 0x1D, self.mpu_addr)
            res = self.buf1[0] & 7
        except OSError:
            raise MPUException(self._I2Cerror)
        return res

    @accel_filter_range.setter
    def accel_filter_range(self, filt):
        '''
        Sets the accel low pass filter cutoff frequency
        Pass:               0   1   2   3   4   5   6   7 BEWARE 7 doesn't work on device I tried.
        Cutoff (Hz):        460 184 92  41  20  10  5   460
        Sample rate (KHz):  1   1   1   1   1   1   1   1
        '''
        if filt in range(8):
            try:
                self._write(filt, 0x1D, self.mpu_addr)
            except OSError:
                raise MPUException(self._I2Cerror)
        else:
            raise ValueError('Filter coefficient must be between 0 and 7')

    def _magsetup(self):                        # mode 2 100Hz continuous reads, 16 bit
        '''
        Magnetometer initialisation: use 16 bit continuous mode.
        Mode 1 is 8Hz mode 2 is 100Hz repetition
        returns correction values
        '''
        try:
            self._write(0x0F, 0x0A, self._mag_addr)      # fuse ROM access mode
            self.buf3 = self._read(self.buf3, 0x10, self._mag_addr)  # Correction values
            self._write(0, 0x0A, self._mag_addr)         # Power down mode (AK8963 manual 6.4.6)
            self._write(0x16, 0x0A, self._mag_addr)      # 16 bit (0.15uT/LSB not 0.015), mode 2
        except OSError:
            raise MPUException(self._I2Cerror)
        mag_x = (0.5*(self.buf3[0] - 128))/128 + 1
        mag_y = (0.5*(self.buf3[1] - 128))/128 + 1
        mag_z = (0.5*(self.buf3[2] - 128))/128 + 1
        return (mag_x, mag_y, mag_z)


    def mag_calibrate(self):
        self.mag.calibrate()

        
    @property
    def mag(self):
        '''
        Magnetomerte object
        '''
        return self._mag

    def _mag_callback(self):
        '''
        Update magnetometer Vector3d object (if data available)
        '''
        try:                                    # If read fails, returns last valid data and
            self.buf1 = self._read(self.buf1, 0x02, self._mag_addr)  # increments mag_stale_count
            if self.buf1[0] & 1 == 0:
                return self._mag                # Data not ready: return last value
            self.buf6 = self._read(self.buf6, 0x03, self._mag_addr)
            self.buf1 = self._read(self.buf1, 0x09, self._mag_addr)
        except OSError:
            raise MPUException(self._I2Cerror)
        if self.buf1[0] & 0x08 > 0:             # An overflow has occurred
            self._mag_stale_count += 1          # Error conditions retain last good value
            return                              # user should check for ever increasing stale_counts
        self._mag._ivector[1] = bytes_toint(self.buf6[1], self.buf6[0])  # Note axis twiddling and little endian
        self._mag._ivector[0] = bytes_toint(self.buf6[3], self.buf6[2])
        self._mag._ivector[2] = -bytes_toint(self.buf6[5], self.buf6[4])
        scale = 0.15                            # scale is 0.15uT/LSB
        self._mag._vector[0] = self._mag._ivector[0]*self.mag_correction[0]*scale
        self._mag._vector[1] = self._mag._ivector[1]*self.mag_correction[1]*scale
        self._mag._vector[2] = self._mag._ivector[2]*self.mag_correction[2]*scale
        self._mag_stale_count = 0

    @property
    def mag_stale_count(self):
        '''
        Number of consecutive times where old data was returned
        '''
        return self._mag_stale_count

    def get_mag_irq(self):
        '''
        Uncorrected values because floating point uses heap
        '''
        self.buf1 = self._read(self.buf1, 0x02, self._mag_addr)
        if self.buf1[0] == 1:                   # Data is ready
            self.buf6 = self._read(self.buf6, 0x03, self._mag_addr)
            self.buf1 = self._read(self.buf1, 0x09, self._mag_addr)    # Mandatory status2 read
            self._mag._ivector[1] = 0
            if self.buf1[0] & 0x08 == 0:        # No overflow has occurred
                self._mag._ivector[1] = bytes_toint(self.buf6[1], self.buf6[0])
                self._mag._ivector[0] = bytes_toint(self.buf6[3], self.buf6[2])
                self._mag._ivector[2] = -bytes_toint(self.buf6[5], self.buf6[4])


    def imu_thread(self):
        import time
        while True:
            self.get_imu_data()
            self.posture_angle()
            time.sleep(0.01)

    def read(self,sensor_type="accel",axis="x"):
        sensor_type =str(sensor_type)
        axis =str(axis)
        if sensor_type == "accel":
            if axis == 'x':
                return self.accel_data[0]
                # self.accel_data =-1*self.accel.x
            elif axis == 'y':
                return self.accel_data[1]
            elif axis == 'z':
                return self.accel_data[2]
            elif axis == 'all':
                return self.accel_data
        elif sensor_type == "gyro":
            if axis == 'x':
                return self.gyro_data[0] * -1
            elif axis == 'y':
                return self.gyro_data[1] * -1
            elif axis == 'z':
                return self.gyro_data[2] * -1
            elif axis == 'all':
                return self.gyro_data * -1
        elif sensor_type == "mag":
            if axis == 'x':
                return self.mag_data[0] * -1
            elif axis == 'y':
                return self.mag_data[1] * -1
            elif axis == 'z':
                return self.mag_data[2] * -1
            elif axis == 'all':
                 return self.mag_data * -1
        # time.sleep(0.001)


    def get_imu_data(self):
        
        self.accel_data = [x * -1 for x in self.accel.xyz]
        self.gyro_data = [x * -1 for x in self.gyro.xyz]
        self.mag_data = [x for x in self.mag.xyz]


    # def magnetic_angle(self):

    #     # print(self.read(sensor_type="mag",axis="x"),self.read(sensor_type="mag",axis="y"))
    #     angle = math.atan2(self.read(sensor_type="mag",axis="x"),self.read(sensor_type="mag",axis="y"))
    #     angle = (angle)*180.0/math.pi
    #     if angle < 0:
    #         angle += 360
    #     angle = int(360 - angle)
    #     return angle
        # print(angle)

    def magnetic_angle(self,param = "azimuth"):
        # angle = math.atan2(self.read(sensor_type="mag",axis="x"),self.read(sensor_type="mag",axis="y"))
        angle = math.atan2(self.mag_data[0],self.mag_data[1])
        angle = (angle)*180.0/math.pi
        # angle = new_angle
        # print(angle)
        if angle < 0:
            angle += 360
        angle = int(360 - angle)
        if param == "azimuth":
            return angle
        elif  param == "quadrant":
            angle = angle + 22.5 
            if angle >= 360:
                angle = 0
            return compass_quadrant_list[int(angle/45)]


        # print(angle)

    def posture_angle(self):
        # accel_data_list = self.read(sensor_type="accel",axis="all")

        forceMagnitudeApprox = self.read(sensor_type="accel",axis="all")
        # forceMagnitudeApprox = [x if abs(x) < 1 else x / abs(x) for x in forceMagnitudeApprox]
        # forceMagnitudeApprox = [0 if abs(x) < 0.1 else x for x in forceMagnitudeApprox]
        forceMagnitudeApprox = [round(x,1)  for x in forceMagnitudeApprox]
        pitchAcc = -1*atan2(forceMagnitudeApprox[1],forceMagnitudeApprox[2]) * 180 / math.pi
        rollAcc = atan2(forceMagnitudeApprox[0],forceMagnitudeApprox[2]) * 180 / math.pi

        if  pitchAcc > 0:
            pitchAcc = pitchAcc - 180
        elif  pitchAcc < 0:  
            pitchAcc = pitchAcc + 180

        if  rollAcc > 0:
            rollAcc = rollAcc - 180
        elif  rollAcc < 0:  
            rollAcc = rollAcc + 180



        self.pitch = 0.98 * (self.pitch + self.read("gyro","x") * 0.01) + 0.02 * pitchAcc
        self.roll =  0.98 * (self.roll + self.read("gyro","y") * 0.01) + 0.02 * rollAcc
        # self.pitch = -1 * self.pitch
        # self.roll  = -1 * self.roll 
        # print(self.pitch,self.roll)
        # print("  ")
        # return self.pitch,self.roll 

    def get_posture_angle(self,aram = "pitch"):
        if aram == "pitch":
            return int(-1 * self.pitch)
        elif aram == "roll":
            return int(-1 * self.roll)
        elif aram == "all":
            return [int(-1 * self.pitch),int(-1 * self.roll)]


    def accel_gyro_calibrate(self, waitfunc=default_wait):
        '''
        calibration routine, sets cal
        '''
        from ezblock import Pin
        sw = Pin("D14", Pin.IN)

        self.accel.cal = (0, 0, 0)
        self.gyro.cal = (0, 0, 0)
        self.accel.update()
        self.gyro.update()
        accel_maxvec = self.accel._vector[:]                # Initialise max and min lists with current values
        accel_minvec = self.accel._vector[:]
        gyro_maxvec = self.gyro._vector[:]                # Initialise max and min lists with current values
        gyro_minvec = self.gyro._vector[:]

        while not sw.value() != 1:
            waitfunc()
            self.accel.update()
            self.gyro.update()
            accel_maxvec = list(map(max,accel_maxvec, self.accel._vector))
            accel_minvec = list(map(min, accel_minvec, self.accel._vector))
            gyro_maxvec = list(map(max, gyro_maxvec, self.gyro._vector))
            gyro_minvec = list(map(min, gyro_minvec, self.gyro._vector))
        self.accel.cal = tuple(map(lambda a, b: (a + b)/2, accel_maxvec, accel_minvec))
        self.gyro.cal = tuple(map(lambda a, b: (a + b)/2, gyro_maxvec, gyro_minvec))
        self.accel.set_offset(self.accel.cal)
        self.accel.set_offset(self.gyro.cal)

    # def calibrate_accel_gyro(self):
    #     self.

    # def calibrate_accel_sensor(self):
    #     imu_m.accel.calibrate()

    # def calibrate_gyro_sensor(self):
    #     imu_m.gyro.calibrate()
if __name__ == "__main__":
    
    from ezblock import I2C
    from sensor_hat import RGB_Matrix,Bme280
    import time

    rr = RGB_Matrix(0X74)
    i2c = I2C()
    imu_m = MPU9250(i2c)
    test_sensor = Bme280()
    imu_m.start_imu()

    CALLIBRATE = False
    rectangle_coor_2 = [2,2,5,5]
    if CALLIBRATE:
        print("Start acc calibration")
        imu_m.accel.calibrate()
        # imu_m.gyro.calibrate()
        print(imu_m.accel.cal)
        print("Finished!")
        time.sleep(2)
    if CALLIBRATE:
        print("Start gyro calibration")
        # imu_m.accel.calibrate()
        imu_m.gyro.calibrate()
        print(imu_m.gyro.cal)
        print("Finished!")
        time.sleep(2)
    # else:
    #     pass
    # print(atan2(-0.02197265625,-0.041259765625)
    while True:
        # pass
        # print(imu_m.read("gyro","all"))
        # print(imu_m.get_posture_angle("all"))
        print(imu_m.magnetic_angle("azimuth"))
        print(imu_m.magnetic_angle("quadrant"))

        time.sleep(0.1)

        