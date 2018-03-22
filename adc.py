import smbus
import time


ADDRESS = 0x48


def main():
    for i in range(0, 10):
        bus = smbus.SMBus(1)
        data = bus.read_byte_data(ADDRESS, 4)
        print(data)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
