#!/usr/bin/env python
# -*- encoding: utf-8 -#-

'''
Script to send a command list to EBB

'''



import sys
import time

from pyaxidraw import axidraw
from plotink import ebb_motion
from plotink import ebb_serial
# print("hello")

def query(port_name, cmd):
    if port_name is not None and cmd is not None:
        response = ''
        try:
#             port_name.write(cmd.encode('ascii'))
            port_name.write(cmd.encode('ascii'))
            response = port_name.readline()
            n_retry_count = 0
            while len(response) == 0 and n_retry_count < 100:
                # get new response to replace null response if necessary
                response = port_name.readline()
                n_retry_count += 1
        except:
            print("Error reading serial data.")
        return response

def block(ad_ref, timeout_ms=None):
    '''
    Interactive context: Wait until all motion control commands have finished, or an
    an optional timeout occurs.

    Polls the EBB immediately and then every 10 ms thereafter until (1) Neither motor is
    currently in motion and (2) there is no queued motion control command.

    A value for timeout_ms, gives the maximum duration to wait in milliseconds.

    Returns True if the motion queue is empty, and False if timed out.

    Requires EBB version v2.6.2 or newer
    '''

    if timeout_ms is None:
        time_left = 60000 # Default 60 second timeout.
    else:
        time_left = timeout_ms

    while True:
        qg_val = bytes.fromhex(ebb_serial.query(ad_ref.plot_status.port, 'QG\r').strip())
        motion = qg_val[0] & (15).to_bytes(1, byteorder='big')[0] # Motion queue bits
        if motion == 0:
            return True
        if time_left <= 0:
            return False    # Timed out
        if time_left < 10:
            time.sleep(time_left / 1000) # Use up remaining time
            time_left = 0
        else:
            time.sleep(0.01) # Sleep 10 ms
            if timeout_ms is not None:
                time_left -= 10


ad = axidraw.AxiDraw() # Initialize class

ad.interactive()

if not ad.connect():                # Open serial port to AxiDraw;
    print("failed to connect")
    quit()   

the_port = ad.plot_status.port
if the_port is None:
    print("failed to connect")
    sys.exit() # end script

the_port.reset_input_buffer()


# Motor 1 only
command_list = [
"LT,40,268435456,0,0,0",
"LT,22,490123456,0,0,0",
"LT,22,-490123456,0,0,0",
"LT,2,1073741824,0,0,0",
"LT,2,-1073741824,0,0,0",
"LT,20,490123456,0,0,0,1073741823",
"LT,20,-490123456,0,0,0,1073741823",
"LT,85,8589934,17353403,0,0",
"LT,85,-8589934,-17353403,0,0",
"LT,83,8589934,17353403,0,0,2047483648",
"LT,83,-8589934,17353403,0,0,2047483648",
"LT,69,1800095000,-26012345,0,0",
"LT,69,-1800095000,26012345,0,0",
"LT,30,0,50353403,0,0",
"LT,30,0,-50353403,0,0",
"LT,69,1800095000,-54567890,0,0",
"LT,69,-1800095000,54567890,0,0",
"LT,20,10,-35111222,0,0",
"LT,20,-10,-35111222,0,0",
"LT,20,-10,35111222,0,0",
"LT,19,80000000,-35000000,0,0",
"LT,27,388300000,-35111222,0,0",
"LT,27,390000000,-35111222,0,0",
"LT,27,-390000000,35111222,0,0",
"LT,11,1204481500,-77012345,0,0",
"LT,17,395851877,-77012345,0,0,115030",
"LT,11,1204481500,-77012345,0,0",
"LT,15,-395851877,77012345,0,0,115030",
"LT,471,-1050109930,5099123,0,0",
"LT,14,-79000000,10015000,0,0,128535542",
"LT,471,-1050109930,5099123,0,0",
"LT,23,79000000,10015000,0,0,128535542",
"LT,8842,-388686102,70433,0,0,623903050",
"LT,6884,505377802,-143537,0,0,1498912166",
"LT,10818,332897914,-30231,0,0,1616956732",
"LT,367,540353247,-102800,0,0",
"LT,4419,969802237,-278607,0,0,29315105",
"LT,577969,978847345,-654,0,0,455082516",
"LT,578247,978847345,-655,0,0,455082516",
"LT,577692,978847345,-653,0,0,455082516",
"LT,7667213,1223372258,-217,0,0,1528960515",
"LT,2549531,942132454,-175,0,0",
"LT,651,1579676895,-2431086,0,0,27145044",
"LT,115,-640499386,19406038,0,0,1979182198",
"LT,61,1135557706,-18994490,0,0,416382676",
"LT,2030,1833381763,0,0,0,1657564855",
"LT,2030,1833381763,0,0,0,1657564856",
"LT,2029,1833381763,0,0,0,1657564857",
"LT,2029,1833381763,0,0,0,1657564858",
"LT,2030,-1833381763,0,0,0,489918792",
"LT,2030,-1833381763,0,0,0,489918791",
"LT,2029,-1833381763,0,0,0,489918790",
"LT,40,268435456,0,0,0,0",
"LT,40,268435456,0,0,0,1",
"LT,40,268435456,0,0,0,2",
"LT,33,268435456,0,0,0,2147483647",
"LT,33,268435456,0,0,0,2147483646",
"LT,33,268435456,0,0,0,2147483645",
"LT,18,-490123456,0,0,0,0",
"LT,18,-490123456,0,0,0,1",
"LT,18,-490123456,0,0,0,2",
"LT,22,-490123456,0,0,0,2147483647",
"LT,22,-490123456,0,0,0,2147483646",
"LT,22,-490123456,0,0,0,2147483645",
"LT,2,1073741824,0,0,0,0",
"LT,2,1073741824,0,0,0,1",
"LT,2,1073741824,0,0,0,2",
"LT,1,1073741824,0,0,0,2147483647",
"LT,1,1073741824,0,0,0,2147483646",
"LT,1,1073741824,0,0,0,2147483645",
"LT,1,-1073741824,0,0,0,0",
"LT,1,-1073741824,0,0,0,1",
"LT,1,-1073741824,0,0,0,2",
"LT,2,-1073741824,0,0,0,2147483647",
"LT,2,-1073741824,0,0,0,2147483646",
"LT,2,-1073741824,0,0,0,2147483645",
"LT,10,500000,-1000000,0,0",
"LT,10,-500000,1000000,0,0",
"LT,1000,500000,-1000000,0,0",
"LT,1000,-500000,1000000,0,0",
]



print("connected")

response = query(the_port, 'V\r')
print(response)



last_command = ""

for command in command_list:
    block(ad)
    response = str(query(the_port, command + '\r'))
    print(last_command + " :: " + response.strip())
    last_command = command
    
print(last_command + " :: ")


ad.disconnect()             # Close serial port to AxiDraw

'''
Expected results log LT, 2023-05-07

T,40,S,5,C,0,R,268435456,P,5
T,22,S,5,C,45297792,R,490123456,P,5
T,22,S,5,C,2102185855,R,-490123456,P,-5
T,2,S,1,C,0,R,1073741824,P,1
T,2,S,1,C,2147483647,R,-1073741824,P,-1
T,20,S,5,C,138792703,R,490123456,P,5
T,20,S,5,C,2008690943,R,-490123456,P,-5
T,85,S,29,C,1142286978,R,1474952488,P,29
T,85,S,29,C,1005196669,R,-1474952488,P,-29
T,83,S,29,C,257219053,R,1440245682,P,29
T,83,S,28,C,978773657,R,1423065814,P,28
T,69,S,29,C,7141901,R,18249367,P,29
T,69,S,29,C,2140341746,R,-18249367,P,-29
T,30,S,10,C,1184194885,R,1485425389,P,10
T,30,S,10,C,963288762,R,-1485425389,P,-10
T,69,S,29,C,750143799,R,-1937805465,P,-3
T,69,S,29,C,1397339848,R,1937805465,P,3
T,20,S,3,C,1567690391,R,-684668819,P,-3
T,20,S,3,C,1567689991,R,-684668839,P,-3
T,20,S,3,C,579793256,R,684668819,P,3
T,19,S,3,C,1644950944,R,-567500000,P,-3
T,27,S,2,C,1981026877,R,-542147383,P,-2
T,27,S,4,C,2026926877,R,-540447383,P,-2
T,27,S,4,C,120556770,R,540447383,P,2
T,11,S,4,C,115030,R,395851877,P,4
T,17,S,3,C,2043764022,R,-874851816,P,-3
T,11,S,4,C,115030,R,395851877,P,4
T,15,S,3,C,578742047,R,720827126,P,1
T,471,S,134,C,128535542,R,1349027442,P,34
T,14,S,2,C,4005542,R,56202500,P,0
T,471,S,134,C,128535542,R,1349027442,P,34
T,23,S,2,C,299535746,R,304337500,P,2
T,8842,S,682,C,21112357,R,234047268,P,-318
T,6884,S,792,C,2140113428,R,-482659138,P,36
T,10818,S,854,C,1825761,R,5874071,P,854
T,367,S,89,C,260582377,R,502677047,P,89
T,4419,S,842,C,1959708691,R,-261222793,P,728
T,577969,S,212579,C,199874382,R,600855946,P,212579
T,578247,S,212579,C,27378968,R,600095887,P,212579
T,577692,S,212579,C,601512122,R,601614795,P,212579
T,7667213,S,1813937,C,2145511894,R,-440412855,P,1397709
T,2549531,S,853667,C,494970505,R,495964616,P,853667
T,651,S,240,C,2147356522,R,-1744548,P,238
T,115,S,36,C,809604235,R,1581491965,P,26
T,61,S,17,C,2133899377,R,-13608939,P,15
T,2030,S,1733,C,1833381761,R,1833381763,P,1733
T,2030,S,1733,C,1833381762,R,1833381763,P,1733
T,2029,S,1733,C,0,R,1833381763,P,1733
T,2029,S,1733,C,1,R,1833381763,P,1733
T,2030,S,1733,C,314101886,R,-1833381763,P,-1733
T,2030,S,1733,C,314101885,R,-1833381763,P,-1733
T,2029,S,1733,C,2147483647,R,-1833381763,P,-1733
T,40,S,5,C,0,R,268435456,P,5
T,40,S,5,C,1,R,268435456,P,5
T,40,S,5,C,2,R,268435456,P,5
T,33,S,5,C,268435455,R,268435456,P,5
T,33,S,5,C,268435454,R,268435456,P,5
T,33,S,5,C,268435453,R,268435456,P,5
T,18,S,5,C,1915196032,R,-490123456,P,-5
T,18,S,5,C,1915196033,R,-490123456,P,-5
T,18,S,5,C,1915196034,R,-490123456,P,-5
T,22,S,5,C,2102185855,R,-490123456,P,-5
T,22,S,5,C,2102185854,R,-490123456,P,-5
T,22,S,5,C,2102185853,R,-490123456,P,-5
T,2,S,1,C,0,R,1073741824,P,1
T,2,S,1,C,1,R,1073741824,P,1
T,2,S,1,C,2,R,1073741824,P,1
T,1,S,1,C,1073741823,R,1073741824,P,1
T,1,S,1,C,1073741822,R,1073741824,P,1
T,1,S,1,C,1073741821,R,1073741824,P,1
T,1,S,1,C,1073741824,R,-1073741824,P,-1
T,1,S,1,C,1073741825,R,-1073741824,P,-1
T,1,S,1,C,1073741826,R,-1073741824,P,-1
T,2,S,1,C,2147483647,R,-1073741824,P,-1
T,2,S,1,C,2147483646,R,-1073741824,P,-1
T,2,S,1,C,2147483645,R,-1073741824,P,-1
T,10,S,0,C,2102483647,R,-9000000,P,0
T,10,S,0,C,45000000,R,9000000,P,0
T,1000,S,232,C,863689983,R,-999000000,P,-232
T,1000,S,232,C,1283793664,R,999000000,P,232
'''








