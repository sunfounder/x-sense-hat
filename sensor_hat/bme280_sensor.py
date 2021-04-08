import smbus2
import bme280
import time


class Bme280(object):

    port = 1
    address = 0x76
    def __init__(self):
        self.bus = smbus2.SMBus(self.port)

        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

        # the sample method will take a single reading and return a
        # compensated_reading object
        # data = bme280.sample(bus, address, calibration_params)
        

# the compensated_reading class has the following attributes
# print(data.id)   celsius/fahrenheit
    def read(self,param):
        data = bme280.sample(self.bus, self.address,self.calibration_params)
        param = str(param)
        if param == 'celsius':
            return round(data.temperature,1)
        elif param == 'humidity':
            return round(data.humidity,1)
        elif param == 'pressure':
            return round(data.pressure)
        elif param == 'fahrenheit':
            return round(data.temperature * 1.8 + 32,1)
        else:
            raise ValueError('aram must be temperature, humidity or pressure')




def test():
    test_sensor = Bme280()
    while True:
        print(test_sensor.read('celsius'))
        print(test_sensor.read('fahrenheit'))
        print(test_sensor.read('humidity'))
        print(test_sensor.read('pressure'))
        print(" ")
        time.sleep(1)

if __name__=='__main__':
    test()

