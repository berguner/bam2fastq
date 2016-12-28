# Coded by Bekir Erguner
# Usage:
# samtools view your.bam | python bam2fastq.py

import sys
import time


def reverse_comp(s):
    r = ''
    l = len(s)
    for i in range(l-1,-1,-1):
        if s[i] == 'A':
            r += 'T'
        elif s[i] == 'T':
            r += 'A'
        elif s[i] == 'G':
            r += 'C'
        elif s[i] == 'C':
            r += 'G'
        else:
            r += 'N'
    return r


def reverse(s):
    q = ''
    l = len(s)
    for i in range(l-1,-1,-1):
        q += s[i]
    return q


if __name__ == '__main__':
    cached_reads = {}
    f1 = open("R1.fq",'w')
    f2 = open("R2.fq",'w')
    count = 0
    line = sys.stdin.readline()
    start = time.time()
    begin = time.time()
    while line:
        count += 1
        if count % 1000000 == 0:
            sys.stderr.write(str(count) + " reads processed in " + str((time.time() - start)) + " seconds\n")
            start = time.time()
        read = line.split('\t')
        tt = read[0]
        sq = read[9]
        qs = read[10]
        flag = int(read[1])
        if flag & 2304 != 0:
            line = sys.stdin.readline()
            #print tt, sq, qs, flag
            continue
        if tt in cached_reads:
            tmp = cached_reads.pop(tt)
            r1 = ''
            r2 = ''
            if tmp[3] & 16 == 16:
                r1 = '@' + tmp[0] + '\n' + reverse_comp(tmp[1]) + '\n+\n' + reverse(tmp[2]) + '\n'
            else:
                r1 = '@' + tmp[0] + '\n' + tmp[1] + '\n+\n' + tmp[2] + '\n'
            if flag & 16 == 16:
                r2 = '@' + tt + '\n' + reverse_comp(sq) + '\n+\n' + reverse(qs) + '\n'
            else:
                r2 = '@' + tt + '\n' + sq + '\n+\n' + qs + '\n'
            if tmp[3] & 64 == 64:
                f1.write(r1)
                f2.write(r2)
            else:
                f1.write(r2)
                f2.write(r1)
        else:
            cached_reads[tt] = (tt,sq,qs,flag)
        line = sys.stdin.readline()
    fs = open("single_ends.fq","w")
    single_count = 0
    for k in cached_reads:
        single_count += 1
        tmp = cached_reads[k]
        r1 = ''
        if tmp[3] & 16 == 16:
            r1 = '@' + tmp[0] + '\n' + reverse_comp(tmp[1]) + '\n+\n' + reverse(tmp[2]) + '\n'
        else:
            r1 = '@' + tmp[0] + '\n' + tmp[1] + '\n+\n' + tmp[2] + '\n'
        fs.write(r1)
    sys.stderr.write(str(single_count) + " reads did not have pairs\n")
    sys.stderr.write(str(count) + " reads processed in " + str((time.time() - begin)) + " seconds\n")

