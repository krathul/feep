#!/usr/bin/env python3

from pysnmp.hlapi import *

import time

def getValue(prop):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData('private', mpModel=0),
        UdpTransportTarget(('192.168.149.114', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('GUDEADS-EPC1202-MIB', prop, 1)),
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    value = 0

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            value = varBind[1]

    return value



start = time.time()

for i in range(1, 20):

    current = getValue("epc1202Current")
    voltage = getValue("epc1202Voltage")
    powerFactor = getValue("epc1202PowerFactor")

    print("Current", current)
    print("Voltage", voltage)
    print("Power Factor", powerFactor)

    watts = float(int(voltage)*int(current)*int(powerFactor))/(1000*1000)

    print("Watts", watts)

    end = time.time()
    print("Time:", end-start)
    start = end

    time.sleep(0.1)

    print()
