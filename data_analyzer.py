#! /bin/env/python2.7
import subprocess
import time
import datetime
import matplotlib
matplotlib.use("Agg")
import linecache
import matplotlib.pyplot as plt
from operator import itemgetter
import itertools
from itertools import islice

def printTimeStatement(start_time):
    print("Current Time : {0}    Time Elapsed : {1} minutes".
          format(datetime.datetime.now().time(),
                 (time.time() - start_time) / 60))


def data_analyzer_smart(start_time, bench, processor, l1_size, l1_assoc, line_size):
    printTimeStatement(start_time)
    Storetxt = "/home/chettyharish/Downloads/Store.txt"
    Cachetxt = "/home/chettyharish/Downloads/Cache.txt"
    

    total_obs = 0.0
    p = subprocess.Popen(['wc', '-l', Storetxt], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    total_obs = int(result.strip().split()[0])

    total_obs = total_obs / 2
    sampling_obs = int(total_obs / 500.0)
    print(total_obs , sampling_obs)
    silent_stores = 0.0
    silent_bytes = 0.0
    total_stores = 0.0
    total_stores_byte = 0.0
    i = 0
    j = 0
    
    #For plots
    y1 = []
    y2 = []
    
    #For RLE
    rle_list = []
    curr = -1
    count = 0
    nt = 0
    with open(Storetxt, 'r') as infile , open(Cachetxt, 'r') as infile2:
        while True:
            nt += 1
            Storefile = list(islice(infile, 2))
            if not Storefile:
                break
            addr1 = Storefile[0].split(":")[1]
            while True:
                Cachefile = list(islice(infile2 , 4))
                addr2 = Cachefile[0].split(":")[1]
                if addr1 == addr2:
                    break

            cnt1 = 0
            size = int(Cachefile[1].split(":")[1])
            bfdata = Cachefile[2].split("\t")
            afdata = Cachefile[3].split("\t")
            for k in range(size):
                if int(bfdata[k]) == int(afdata[k]):
                    cnt1 += 1

            if cnt1 == size:
                silent_stores += 1
            silent_bytes += cnt1
            total_stores += 1
            total_stores_byte += size
            
            if i % sampling_obs == 0:
                if cnt1 == size:
                    y1.append(1)
                else:
                    y1.append(0)
                y2.append(float(float(cnt1)/float(size)))
            

            if (cnt1 == size) == curr:
                count += 1
            else:
                rle_list.append((i, str(curr), str(count)))
                rle_list = sorted(rle_list, key=itemgetter(2), reverse=True)[0:200]
                curr = cnt1 == size
                count = 1
            i += 1 
    print(nt)
    print(total_stores)
    if silent_bytes != 0:
        ##############################
        #    FINAL STATS HERE
        #
        ##############################
        printTimeStatement(start_time)
        config_string = (str(bench) + "_" + str(processor) + "_" + str(l1_size) + "KB_"
                         + str(l1_assoc) + "_" + str(line_size))
        opstring = (config_string + "\t" + str(total_stores) + "\t" + str(silent_stores)
                    + "\t" + str(silent_stores / total_stores)
                    + "\t" + str(float(silent_bytes))
                    + "\t" + str(float(total_stores_byte))
                    + "\t" + str(float(silent_bytes/total_stores_byte))) + "\n"
        outputfile = open("/home/chettyharish/Downloads/op.txt", "a")
        outputfile.write(opstring)
        outputfile.close()
    
        ##############################
        #    PLOTTING STARTS HERE
        #
        ##############################
        printTimeStatement(start_time)
        x1 = [i for i in range(len(y1))]
        print(len(x1) , len(y1) , len(y2))
        print(y1)
        print(y2)
        fig = plt.figure(figsize=(22, 12), dpi = 110)
        ax0 = plt.subplot(211)
        ax0.plot(x1, y1)
        ax0.set_title('Store number vs SilentStores')
        ax1 = plt.subplot(212)
        ax1.plot(x1, y2)
        ax1.set_title('Store number vs Bytes Stored')
        ax0.spines['right'].set_visible(False)
        ax0.spines['top'].set_visible(False)
        ax0.yaxis.set_ticks_position('left')
        ax0.xaxis.set_ticks_position('bottom')
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.yaxis.set_ticks_position('left')
        ax1.xaxis.set_ticks_position('bottom')
        plt.subplots_adjust(hspace=0.5)
        plt.savefig("/home/chettyharish/Downloads/" + config_string + ".png")
        
        
        opstring = "\n".join(
            [str(x[0])+"\t"+str(x[1])+"\t"+str(x[2]) 
             for x in sorted(rle_list, key=itemgetter(2), reverse=True)[0:200]])
        outputfile = open(
            "/home/chettyharish/Downloads/" + config_string + ".txt", "w")
        outputfile.write(
            "Total\t" + str(total_stores) + "\t" + str(silent_stores) + "\n")
        outputfile.write(opstring)
        outputfile.close()
    else:
        print("There was an EXCEPTION")
    return
        

def data_analyzer(start_time, bench, processor, l1_size, l1_assoc, line_size):
    printTimeStatement(start_time)
    Storefile = [
        line for line in open("/home/chettyharish/Downloads/Store.txt")]
    Cachefile = [
        line for line in open("/home/chettyharish/Downloads/Cache.txt")]

    silent_stores = 0.0
    silent_bytes = []
    total_stores = 0.0
    i = 0
    j = 0
    while i < len(Storefile):
        addr1 = Storefile[i].split(":")[1]
        while j < len(Cachefile):
            addr2 = Cachefile[j].split(":")[1]
            if addr1 == addr2:
                cnt1 = 0
                size = int(Cachefile[j + 1].split(":")[1])
                bfdata = Cachefile[j + 2].split("\t")
                afdata = Cachefile[j + 3].split("\t")

                for k in range(size):
                    if int(bfdata[k]) == int(afdata[k]):
                        cnt1 += 1

                if cnt1 == size:
                    silent_stores += 1
                    total_stores += 1
                    silent_bytes.append((j, size, cnt1))
                else:
                    total_stores += 1
                    silent_bytes.append((j, size, cnt1))

                j += 4
                break
            else:
                j += 4
        i += 2

    print(total_stores)
    if len(silent_bytes) != 0:
        ##############################
        #    FINAL STATS HERE
        #
        ##############################
        printTimeStatement(start_time)
        config_string = (str(bench) + "_" + str(processor) + "_" + str(l1_size) + "KB_"
                         + str(l1_assoc) + "_" + str(line_size))
        opstring = (config_string + "\t" + str(total_stores) + "\t" + str(silent_stores)
                    + "\t" + str(silent_stores / total_stores)
                    + "\t" + str(float(sum(zip(*silent_bytes)[2])))
                    + "\t" + str(float(sum(zip(*silent_bytes)[1])))
                    + "\t" + str(float(sum(zip(*silent_bytes)[2])) / float(sum(zip(*silent_bytes)[1])))) + "\n"
        outputfile = open("/home/chettyharish/Downloads/op.txt", "a")
        outputfile.write(opstring)
        outputfile.close()
    
        ##############################
        #    PLOTTING STARTS HERE
        #
        ##############################
        printTimeStatement(start_time)
        x1 = []
        y1 = []
        y2 = []
        i = 0
        total_obs = len(silent_bytes)
        sampling_obs = int(total_obs / 500.0)
    
        while i < total_obs:
            if silent_bytes[i][1] == silent_bytes[i][2]:
                y1.append(1)
            else:
                y1.append(0)
            y2.append(float(silent_bytes[i][2]) / float(silent_bytes[i][1]))
            i += sampling_obs
    
        x1 = [i for i in range(len(y1))]
        fig = plt.figure(figsize=(22, 12), dpi = 110)
        ax0 = plt.subplot(211)
        ax0.plot(x1, y1)
        ax0.set_title('Store number vs SilentStores')
        ax1 = plt.subplot(212)
        ax1.plot(x1, y2)
        ax1.set_title('Store number vs Bytes Stored')
        ax0.spines['right'].set_visible(False)
        ax0.spines['top'].set_visible(False)
        ax0.yaxis.set_ticks_position('left')
        ax0.xaxis.set_ticks_position('bottom')
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.yaxis.set_ticks_position('left')
        ax1.xaxis.set_ticks_position('bottom')
        plt.subplots_adjust(hspace=0.5)
        plt.savefig("/home/chettyharish/Downloads/" + config_string + ".png")
    
        ##############################
        #    RLE STARTS HERE
        #
        ##############################
        printTimeStatement(start_time)
        silent_store = [1 if ele[1] == ele[2] else 0 for ele in silent_bytes]
        rle_list = []
        curr = -1
        count = 0
        for i, ele in enumerate(silent_store):
            if ele == curr:
                count += 1
            else:
                rle_list.append((i, str(curr), str(count)))
                curr = ele
                count = 1
    
        opstring = "\n".join(
            [str(x[0])+"\t"+str(x[1])+"\t"+str(x[2]) 
             for x in sorted(rle_list, key=itemgetter(2), reverse=True)[0:200]])
        outputfile = open(
            "/home/chettyharish/Downloads/" + config_string + ".txt", "w")
        outputfile.write(
            "Total\t" + str(total_stores) + "\t" + str(silent_stores) + "\n")
        outputfile.write(opstring)
        outputfile.close()
    else:
        print("There was an EXCEPTION")
    return


def script_runner():
    processor = "X86"
    start_time = time.time()

    command2 = "echo \"Configuration\tTotal\tSilent\tRatio\tSilentB\tTotalB\tRatio\" > /home/chettyharish/Downloads/op.txt"
    command3 = "cat /dev/null > /home/chettyharish/Downloads/Cache.txt"
    command4 = "cat /dev/null > /home/chettyharish/Downloads/Store.txt"

    p = subprocess.Popen(command2, shell=True)
    p.wait()

    benchmarks = [
#                 "bzip2", 
#                 "namd",
#                 "libquantum",
#                 "gamess",
#                 "omnetpp",
#                 "mcf",
#                 "specrand_i",
#                 "sjeng",
#                 "gcc",
#                 "hmmer",
#                 "milc",
#                 "perlbench",
#                 "povray",
#                 "soplex",
#                 "lbm",
#                 "gobmk"
                ]

    for bench_mark in benchmarks: 
        for l1_size in [8]:
            for l1_assoc in [4]:
                for line_size in [64]:
                    printTimeStatement(start_time)
                    p = subprocess.Popen(command3, shell=True)
                    p.wait()
                    p = subprocess.Popen(command4, shell=True)
                    p.wait()
                    try:
                        build_cmd = ("build/X86/gem5.debug configs/example/se.py --cpu-type=detailed" +
                                     " --bench="+bench_mark+" --caches --l1d_size=" +
                                     str(l1_size) + "kB --l1d_assoc="
                                     + str(l1_assoc) + " --cacheline_size=" + str(line_size))
                        p = subprocess.Popen(build_cmd, shell=True)
                        p.wait()
                        print(build_cmd)
                        data_analyzer(
                            start_time, bench_mark, processor, l1_size, l1_assoc, line_size)
                        print()
                    except:
                        print("There was an EXCEPTION")
    return

if __name__ == "__main__":
#     script_runner()
#     data_analyzer(time.time(),"hmmrDumb","X86","8kB","4","64")
    data_analyzer_smart(time.time(),"hmmrSmar","X86","8kB","4","64")
