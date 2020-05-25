# RemoteShark
Quick script to connect Wireshark on Windows to a remote tcpdump instance through named pipes.
This simple tool is meant to be used to display a packet capture running on a remote Linux server with Wireshark on your Windows client.
It connects to the SSH daemon using putty's utility "plink" and outputs the packet capture to an ad hoc created named pipe on the local Windows PC. Wireshark is automatically opened to capture the named pipe as interface.

## Requirements
On the client
 - Putty
 - Wireshark
 - python (tested with python2.7, should work with python3 as well)
On the server
 - Reachable SSH daemon
 - A user with permission to launch packet capture
 - tcpdump

## Tipps
Easiest way is to create a profile under Putty, so you have the option to set private key and proxy.

## Options
Following options are supported:
```
-l, --load-profile: Name of the saved Putty profile you want to load,
-p, --ask-password: If you didn't provide a private key in the profile, use this option to be prompted for password,
-f, --custom-filter: Default BPF filter is "not port 22" to avoid sniffing the ssh session itself. Use this option to override the filter.
```
## Future development
- Try to make the delay smaller
- Handle sudo password prompt
- Python3 testing
- Translation for Powershell to make it more universal
- Introduce exception handling
- Option for thsark
- Arpspoofing module? Why not..
...

## Sources and thanks
Wireshark documentation provided a very useful starting point for this script.
Various Stackoverflow answers, as usual :)

## Copyright
Use and modify this script as you wish.
