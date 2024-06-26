#!/usr/bin/env python
# -*- encoding: utf-8 -#-

'''
python_send_cmds3.py

Run this demo by calling: python3 python_send_cmds3.py

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


# This is for v3.0.0 EBB firmwares and above (i.e. ones that have the L3 command and
# the ability to change it's FIFO depth)

# At first this will just send the command.

# Eventually this code can capture and analyze the result from the Saleae to generate
# the answers fully automatically.

SM_command_list = [
"SM,10,250,250",
]



# CU,4 sets new FIFO length
# QU,2 reads back max FIFO length

print("connected")

response = query(the_port, 'V\r')
print(response)
response = query(the_port, 'CU,250,1\r')    # Turn on ISR GPIO debug bits
print(response)
response = query(the_port, 'CU,4,32\r')     # Set FIFO to max size
print(response)

last_command = ""

time.sleep(0.5)

for command in SM_command_list:
    #block(ad)
    for i in range(100):
        response = str(query(the_port, command + '\r'))
        print(last_command + " :: " + response.strip())
        last_command = command
    
    time.sleep(.25)

print(last_command + " :: ")

response = query(the_port, 'CU,254,1\r')    # Switch to lock up mode
print(response)

# Now watch Saleae traces to see how much time is actually used by ISR (empty) and 
# how much time main() gets to process incoming USB packets.
# EBB will need to be reset to get out of this mode.

time.sleep(5.0)

ad.disconnect()             # Close serial port to AxiDraw
