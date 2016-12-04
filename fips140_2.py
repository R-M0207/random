#!/usr/bin/python3
#-*-coding;utf-8-*-


"""
The length of one sample tested should be 20000 bits@FIPS140-2.
The argument 'bitstream' for each test function is string made of '1' or '0'.
need python3.4+ to run.
"""

import os


BIN = lambda x,keta: '0' * (keta - len(bin(x)[2:])) + bin(x)[2:]
HEX = lambda x,keta: '0' * (keta - len(hex(x)[2:])) + hex(x)[2:]



def bitcountby32bit(num):
    num = (num & 0x55555555) + (num >> 1 & 0x55555555)
    num = (num & 0x33333333) + (num >> 2 & 0x33333333)
    num = (num & 0x0f0f0f0f) + (num >> 4 & 0x0f0f0f0f)
    num = (num & 0x00ff00ff) + (num >> 8 & 0x00ff00ff)
    return (num & 0x0000ffff) + (num >> 16 & 0x0000ffff)

def theMonobitTest(bitstream):
    if len(bitstream) != 20000:
        raise IndexError
    onecnt = 0
    for i in range(625):#20000 / 32 = 625
        onecnt += bitcountby32bit(int(bitstream[(i * 32):(i*32)+32],2))
    result = True if 9725 < onecnt < 10275 else False 
    return result,onecnt

def thePokerTest(bitstream):
    if len(bitstream) != 20000:
        raise IndexError
    g = [0 for _ in range(16)]
    for i in range(0,20000,4):
        g[int(bitstream[i:i+4],2)] += 1
    x = (16. / 5000.) * sum([pow(g[i],2)  for i in range(16)] )- 5000
    result = True if 2.16 < x < 46.17 else False 
    return result,x


def theRunsTest(bitstream):
    if len(bitstream) != 20000:
        raise IndexError
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
    if len(bitstream) != 20000:
        raise IndexError
    return (2315 <= rundict[1] <= 2685) and (1114 <= rundict[2] <= 1386) and \
        (527 <= rundict[3] <= 723) and (240 <= rundict[4] <= 384) and \
        (103 <= rundict[5] <= 209) and (103 <= rundict[6] <= 209)

def theLongrunsTest(bitstream):
    if len(bitstream) != 20000:
        raise IndexError
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



def sample():
    A_sample = BIN(int.from_bytes(os.urandom(2500),"little"),20000)
    print("The Monobit Test:{0}".format(theMonobitTest(A_sample)))
    print("The Poker Test:{0}".format(theRunsTest(A_sample)))
    print("The Runs Test:{0}".format(theRunsTest(A_sample)))
    print("The Longruns:{0}".format(theLongrunsTest(A_sample)))

if __name__ == '__main__':
    sample()
    
        
    
    


