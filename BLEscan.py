from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate
from bluepy.btle import BTLEDisconnectError
from bluepy.btle import BTLEGattError
import codecs
import signal
import sys
import os

# CHARACTERISTIC
WRITE_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

# COMMANDS
LOCK = "55aa032003700168ff"
UNLOCK = "55aa032003710167ff"

# CONSTANTS
TIMEOUT_LENGTH = 3
FILE_NAME = "scootersAddr.txt"
COMMAND = ""

if sys.argv[2] == "lock":
    COMMAND = LOCK
elif sys.argv[2] == "unlock":
    COMMAND = UNLOCK
else:
    raise Exception('Command not recognised')


def timeout_handler(signum, timeout_handler):
    raise TimeoutError


signal.signal(signal.SIGALRM, timeout_handler)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(2)


def add_addr_to_known(dev_addr):
    file_exists = os.path.exists('./' + FILE_NAME)

    if file_exists:
        with open(FILE_NAME) as file:
            addresses = [line.strip() for line in file]

        for addr in addresses:
            if addr == dev_addr:
                return None

    f = open(FILE_NAME, "a")
    print(dev_addr, file=f)
    f.close()


def write_command(dev, command):
    signal.alarm(TIMEOUT_LENGTH)
    peri = btle.Peripheral(dev)
    characteristics = peri.getCharacteristics(uuid=WRITE_UUID)[0]
    characteristics.write(codecs.decode(command, 'hex'))
    peri.disconnect()
    print("Success!")
    add_addr_to_known(dev.addr)


def write_devices(devs, command):
    for dev in devs:
        try:
            print("Attempting to send command to device ", dev.addr, dev.getScanData())
            write_command(dev, command)
        except (BTLEDisconnectError, BTLEGattError, TimeoutError):
            print("Couldn't connect")


def get_known_addr(devs):
    file_exists = os.path.exists('./' + FILE_NAME)
    known_devices = []

    if file_exists:
        print('file exists')
        with open(FILE_NAME) as file:
            known_addr = [line.strip() for line in file]

        print('[%s]' % ', '.join(map(str, known_addr)))

        for dev in devs:
            for addr in known_addr:
                if dev.addr == addr:
                    known_devices.append(dev)
    else:
        raise Exception('No saved addresses in file ' + FILE_NAME)

    return known_devices


if sys.argv[1] == "scan":
    print("Scanning ", len(devices), " device/s in bluetooth area")
    write_devices(devices, COMMAND)
elif sys.argv[1] == "saved":
    knownDevices = get_known_addr(devices)

    if knownDevices:
        print("Scanning ", len(knownDevices), " device/s in bluetooth area")
        write_devices(knownDevices, COMMAND)
    else:
        raise Exception('Could not find any known devices in area')
else:
    raise Exception('incorrect arguments')