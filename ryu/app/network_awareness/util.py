#!/usr/bin/env python
# coding: utf-8
import random

def bit_reverse(bit):
    return 1 - int(bit)

# 192.168.1.1  =》 1110111101010101010101010101001
def ip_to_bin(ip_str):
    return ''.join([bin(int(x))[2:].rjust(8, '0')
                    for x in ip_str.split('.')])

# 192.168.1.1  《= 1110111101010101010101010101001
def bin_to_ip(bin_str):
    return '.'.join([str(int(bin_str[0:8], 2)),
                     str(int(bin_str[8:16], 2)),
                     str(int(bin_str[16:24], 2)),
                     str(int(bin_str[24:32], 2))])

# 随机生成 192.1.2.2
def ip_list_generator():
    return ('.'.join([str(a), str(b), str(c), str(d)])
            for a in xrange(1, 255)
            for b in xrange(1, 255)
            for c in xrange(1, 255)
            for d in xrange(1, 255))

def another_ip_list_generator():
    return ('.'.join([str(202), str(117), str(c), str(d)])
            for c in xrange(1, 255)
            for d in xrange(1, 255))

def take(generator, count):
    result = []
    for _ in range(count):
        result.append(next(generator))
    return result

if __name__ == '__main__':
    ip_list = take(another_ip_list_generator(), 5000)
    sampled_ip_list = random.sample(ip_list, 2000)
    for ip in sampled_ip_list:
        print ip
        print ip_to_bin(ip)
