# vector3d.py 3D vector class for use in inertial measurement unit drivers
# Authors Peter Hinch, Sebastian Plamauer

# V0.7 17th May 2017 pyb replaced with utime
# V0.6 18th June 2015

'''
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
from math import sqrt, degrees, acos, atan2
from sensor_hat.filedb import FileDB



def default_wait():
    '''
    delay of 50 ms
    '''
    sleep_ms(50)


class Vector3d(object):
    '''
    Represents a vector in a 3D space using Cartesian coordinates.
    Internally uses sensor relative coordinates.
    Returns vehicle-relative x, y and z values.
    '''
    def __init__(self, transposition, scaling, update_function,sensor_type = 'mag'):
        db = '/home/pi/.mpu9250_config'
        self.db = FileDB(db=db)
        self.sensor_type = sensor_type
        if self.sensor_type == 'mag':
            db_val = self.db.get('mag_offset_list', default_value=str(self.new_list(0)))
        elif self.sensor_type == 'accel':
            db_val = self.db.get('accel_offset_list', default_value=str(self.new_list(0)))
        elif self.sensor_type == 'gyro':
            db_val = self.db.get('gyro_offset_list', default_value=str(self.new_list(0)))
        db_val = [float(i.strip()) for i in db_val.strip("[]").split(",")]
        self.cal = tuple(db_val)
        # print("self.cal: ",self.cal)
        self._vector = [0, 0, 0]
        self._ivector = [0, 0, 0]
        # self.cal = (0, 0, 0)
        self.argcheck(transposition, "Transposition")
        self.argcheck(scaling, "Scaling")
        if set(transposition) != {0, 1, 2}:
            raise ValueError('Transpose indices must be unique and in range 0-2')
        self._scale = scaling
        self._transpose = transposition
        self.update = update_function
        # self.timer = threading.Thread(target=self.update, name="Thread1")
        




    def new_list(self, default_value):
        _ = [0 for i in range(3)]
        return _


    def argcheck(self, arg, name):
        '''
        checks if arguments are of correct length
        '''
        if len(arg) != 3 or not (type(arg) is list or type(arg) is tuple):
            raise ValueError(name + ' must be a 3 element list or tuple')

    def calibrate(self, waitfunc=default_wait):
        '''
        calibration routine, sets cal
        '''
        from ezblock import Pin
        sw = Pin("D14", Pin.IN)

        self.cal = (0, 0, 0)
        self.update()
        maxvec = self._vector[:]                # Initialise max and min lists with current values
        minvec = self._vector[:]
        print("type: ",self.sensor_type)
        while not sw.value() != 1:
            waitfunc()
            self.update()
            maxvec = list(map(max, maxvec, self._vector))
            minvec = list(map(min, minvec, self._vector))
        self.cal = tuple(map(lambda a, b: (a + b)/2, maxvec, minvec))
        self.set_offset(self.cal)

    # def accel_gyro_calibrate(self, waitfunc=default_wait):
    #     '''
    #     calibration routine, sets cal
    #     '''
    #     from ezblock import Pin
    #     sw = Pin("D14", Pin.IN)

    #     self.cal = (0, 0, 0)
    #     self.update()
    #     maxvec = self._vector[:]                # Initialise max and min lists with current values
    #     minvec = self._vector[:]
    #     print("type: ",self.sensor_type)
    #     while not sw.value() != 1:
    #         waitfunc()
    #         self.update()
    #         maxvec = list(map(max, maxvec, self._vector))
    #         minvec = list(map(min, minvec, self._vector))
    #     self.cal = tuple(map(lambda a, b: (a + b)/2, maxvec, minvec))
    #     self.set_offset(self.cal)

    def set_offset(self,offset_list):
        
        if self.sensor_type == 'mag':
            temp = str(list(offset_list))
            self.cal = offset_list
            self.db.set('mag_offset_list',temp)
        elif self.sensor_type == 'accel':
            offset_list = list(offset_list)
            offset_list[2] = offset_list[2] - 1
            temp = str(list(offset_list))
            self.cal = offset_list
            self.db.set('accel_offset_list',temp)
        elif self.sensor_type == 'gyro':
            temp = str(list(offset_list))
            self.cal = offset_list
            self.db.set('gyro_offset_list',temp)


    # def accel_set_offset(self,offset_list):
    #     temp = str(list(offset_list))
    #     self.db.set('accel_offset_list',temp)

    @property
    def _calvector(self):
        '''
        Vector adjusted for calibration offsets
        '''
        return list(map(lambda val, offset: val - offset, self._vector, self.cal))

    @property
    def x(self):                                # Corrected, vehicle relative floating point values
        self.update()
        return self._calvector[self._transpose[0]] * self._scale[0]

    @property
    def y(self):
        self.update()
        return self._calvector[self._transpose[1]] * self._scale[1]

    @property
    def z(self):
        self.update()
        return self._calvector[self._transpose[2]] * self._scale[2]

    @property
    def xyz(self):
        self.update()
        return (self._calvector[self._transpose[0]] * self._scale[0],
                self._calvector[self._transpose[1]] * self._scale[1],
                self._calvector[self._transpose[2]] * self._scale[2])

    @property
    def magnitude(self):
        x, y, z = self.xyz  # All measurements must correspond to the same instant
        return sqrt(x**2 + y**2 + z**2)

    @property
    def inclination(self):
        x, y, z = self.xyz
        return degrees(acos(z / sqrt(x**2 + y**2 + z**2)))

    @property
    def elevation(self):
        return 90 - self.inclination

    @property
    def azimuth(self):
        x, y, z = self.xyz
        return degrees(atan2(y, x))

    # Raw uncorrected integer values from sensor
    @property
    def ix(self):
        return self._ivector[0]

    @property
    def iy(self):
        return self._ivector[1]

    @property
    def iz(self):
        return self._ivector[2]

    @property
    def ixyz(self):
        return self._ivector

    @property
    def transpose(self):
        return tuple(self._transpose)

    @property
    def scale(self):
        return tuple(self._scale)