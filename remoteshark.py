# REMOTESHARK
# Kindly inspired by Win32 Wireshark named pipes example
# Requires Python for Windows and the Python for Windows Extensions:
# http://www.python.org
# http://sourceforge.net/projects/pywin32/

import win32pipe, win32file
import time
import subprocess
import getpass
import argparse
import atexit

print("""
.______       _______ .___  ___.   ______   .___________. _______ 
|   _  \     |   ____||   \/   |  /  __  \  |           ||   ____|
|  |_)  |    |  |__   |  \  /  | |  |  |  | `---|  |----`|  |__   
|      /     |   __|  |  |\/|  | |  |  |  |     |  |     |   __|  
|  |\  \----.|  |____ |  |  |  | |  `--'  |     |  |     |  |____ 
| _| `._____||_______||__|  |__|  \______/      |__|     |_______|
                                                                  
     _______. __    __       ___      .______       __  ___       
    /       ||  |  |  |     /   \     |   _  \     |  |/  /       
   |   (----`|  |__|  |    /  ^  \    |  |_)  |    |  '  /        
    \   \    |   __   |   /  /_\  \   |      /     |    <         
.----)   |   |  |  |  |  /  _____  \  |  |\  \----.|  .  \        
|_______/    |__|  |__| /__/     \__\ | _| `._____||__|\__\       
                                                                  """)


#parse arguments to receive password and/or a putty profile
parser = argparse.ArgumentParser(description="Connect wireshark to remote tcpdump!")
parser.add_argument('-l','--loadprofile',dest='profile',help='Putty profile name')
parser.add_argument('-p','--ask-password',action='store_true',help='Prompt for password')
parser.add_argument('-f','--custom-filter',help='Custom BPF filter for tcpdump')


args = parser.parse_args()
#print args
profile = args.profile
ask_password = args.ask_password
custom_filter = args.custom_filter

ssh_password = False
plink_command = ["plink",'-batch']

if ask_password:
	ssh_password = getpass.getpass()
	plink_command.append("-pw")
	plink_command.append(ssh_password)

if profile:
	plink_command.append("-load")
	plink_command.append(profile)

	
if custom_filter:
	plink_command.append("tcpdump -i -eth0 -w - '" + custom_filter + "'")
else:
	plink_command.append("tcpdump -i eth0 -w - 'not port 22'")

#tell the user how to exit
print "[+] Press Ctrl+C to exit."

#open Wireshark, configure pipe interface and start capture (not mandatory, you can also do this manually)
wireshark_cmd=['C:\Program Files\Wireshark\Wireshark.exe', r'-i\\.\pipe\wireshark','-k']
proc=subprocess.Popen(wireshark_cmd)

#create the named pipe \\.\pipe\wireshark
pipe = win32pipe.CreateNamedPipe(
    r'\\.\pipe\wireshark',
    win32pipe.PIPE_ACCESS_OUTBOUND,
	#win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536,
    300,
    None)

#connect to pipe
win32pipe.ConnectNamedPipe(pipe, None)

#register how close the pipe before leaving!																  
def quit_gracefully():
	print "Exiting..."
	win32file.CloseHandle(pipe)

atexit.register(quit_gracefully)
	
#open ssh connection with tcpdump command
plink = subprocess.Popen(
			plink_command,
			shell=False,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
#keep reading data and feeding it to the named pipe (\\.\pipe\wireshark)
while 1:
	time.sleep(0.2)
	for data in iter(plink.stdout.readline,""):
		win32file.WriteFile(pipe, data)
