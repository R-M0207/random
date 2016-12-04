#!/usr/bin/python3
#-*-codig;utf-8-*-

import os
import binascii
import argparse
import threading


BIN = lambda x,keta: '0' * (keta - len(bin(x)[2:])) + bin(x)[2:]
HEX = lambda x,keta: '0' * (keta - len(hex(x)[2:])) + hex(x)[2:]




def bitcountby32bit(num):
    num = (num & 0x55555555) + (num >> 1 & 0x55555555)
    num = (num & 0x33333333) + (num >> 2 & 0x33333333)
    num = (num & 0x0f0f0f0f) + (num >> 4 & 0x0f0f0f0f)
    num = (num & 0x00ff00ff) + (num >> 8 & 0x00ff00ff)
    return (num & 0x0000ffff) + (num >> 16 & 0x0000ffff)

def theMonobitTest(bitstream):
    onecnt = 0
    if len(bitstream) < 20000:
        print(len(bitstream))
        raise ValueError
    for i in range(625):#20000 / 32 = 625
        onecnt += bitcountby32bit(int(bitstream[(i * 32):(i*32)+32],2))
    result = True if 9725 < onecnt < 10275 else False 
    return result,onecnt

def thePokerTest(bitstream):
    g = [0 for _ in range(16)]
    for i in range(0,20000,4):
        g[int(bitstream[i:i+4],2)] += 1
    x = (16. / 5000.) * sum([pow(g[i],2)  for i in range(16)] )- 5000
    result = True if 2.16 < x < 46.17 else False 
    return result,x


def theRunsTest(bitstream):
    bitlen = len(bitstream)
    idx = 0;run = 0;
    runlength0 = {1:0,2:0,3:0,4:0,5:0,6:0}
    runlength1 = {1:0,2:0,3:0,4:0,5:0,6:0}
    while idx < bitlen:
        x = bitstream[idx]
        offset = 0
        while idx + offset < bitlen:
            if x == bitstream[idx + offset]:
                offset += 1
            else:
                run = offset if offset <= 6 else 6  
                if run > 0:
                    if x == "0": runlength0[run] += 1
                    else:runlength1[run] += 1
                break
        idx += offset
    result0 = parseRunsTest(runlength0)
    result1 = parseRunsTest(runlength1)
    return result0,runlength0,result1,runlength1

def parseRunsTest(rundict):
    return (2315 <= rundict[1] <= 2685) and (1114 <= rundict[2] <= 1386) and \
        (527 <= rundict[3] <= 723) and (240 <= rundict[4] <= 384) and \
        (103 <= rundict[5] <= 209) and (103 <= rundict[6] <= 209)

def theLongrunsTest(bitstream):
    bitlen = len(bitstream)
    idx = 0;longrun = 0;runchar = None
    while idx < bitlen:
        x = bitstream[idx]
        offset = 0
        while idx + offset < bitlen:
            if x == bitstream[idx + offset]:
                offset += 1
            else:
                break
        if longrun < offset:
            longrun = offset;runchar = x;
        idx += offset
    result = True if longrun < 26 else False
    return x,longrun,result

def s_mono(files):     
    results = []
    for df in files:
        dataf = open(df,"rb")
        data = dataf.read()
        dataf.close()
        bits = BIN(int.from_bytes(data,"big"),20000)
        results.append(theMonobitTest(bits))
        
    return results

def s_poker(files):
    results = []
    for df in files:
        datfile = open(df,"rb")
        data = datfile.read(2500)
        datfile.close()
        bits = BIN(int.from_bytes(data,"big"),20000)
        results.append(thePokerTest(bits))
    return results

def s_runs(files):
    results = []
    for df in files:
        datfile = open(df,"rb")
        data = datfile.read(2500)
        datfile.close()
        bits = BIN(int.from_bytes(data,"big"),20000)
        results.append(theRunsTest(bits))
    return results

def s_long(files):
    results = []
    for df in files:
        datfile = open(df,"rb")
        data = datfile.read(2500)
        datfile.close()
        bits = BIN(int.from_bytes(data,"big"),20000)
        results.append(theLongrunTest(bits))
    return results
    
def testall(bitseq):
    print("[*] Running: The Monobit Test..",end="")
    monores,v = theMonobitTest(bitseq)
    print("Result:{0},{1}".format(monores,v))

    print("[*] Running: The Poker Test..",end="")
    pokerres,w = thePokerTest(bitseq)
    print("Result:{0},{1}".format(pokerres,w))

    print("[*] Running: The Runs Test..")
    run0res,x,run1res,y = theRunsTest(bitseq)
    print("[+] Result:{0},{1},{2},{3}".format(run0res,x,run1res,y))

    print("[*] Running: The Longruns Test..",end="")
    z,lrun,lrunres = theLongrunsTest(bitseq)
    print("Result:{0},{1},{2}".format(z,lrun,lrunres))

def main(srcfile,isbinary,testlist,outfile):
    data = ""
    if isbinary:
        f = open(srcfile,"rb")
        data = BIN(int.from_bytes(f.read(2500),"little"),20000)
    else:
        f = open(srcfie,"r")
        while True:
            line = f.readline().rstrip()
            if not line:break
            data += line.encode()
        if len(data) > 20000 / 8:
            raise ValueError
        data = BIN(int.from_bytes(data,"little"),20000)
    f.close()
    result = testall(data)
    if outfile:
        with open(outfile+".txt","w") as of:
            of.write(result)
            
    
        
    
    

if __name__ == '__main__':
    print("[*] Runnig {}".format(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--src",type=str,help="[+]")
    parser.add_argument("-b","--bin",action="store_action",help="[*]")
    parser.add_argument("-t","--test",type=list,default=[0])
    parser.add_argument("-o","--out",type=str,default="stdout")
    args = parser.parse_args()
    main(args.src,args.bin,args.test,args.out)
