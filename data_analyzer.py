#! /bin/env/python2.7
import subprocess
import time
import datetime

def printTimeStatement(start_time):
    print("Current Time : {0}    Time Elapsed : {1} minutes".\
          format(datetime.datetime.now().time(), \
                 (time.time()-start_time)/60))
    
def data_analyzer(bench,processor, l1_size, l1_assoc, line_size):
    Storefile = [
        line for line in open("/home/chettyharish/Downloads/Storetemp.txt")]
    Cachefile = [
        line for line in open("/home/chettyharish/Downloads/Cachetemp.txt")]

    silent_stores = 0.0
    silent_bytes = []
    total_stores = 0.0
    i = 1
    j = 1
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

    opstring = (str(bench) + "_" +str(processor) + "_" + str(l1_size) + "KB_"
                + str(l1_assoc) + "_" + str(line_size) 
                + "\t" +str(total_stores) + "\t" + str(silent_stores) 
                +"\t" + str(silent_stores / total_stores) 
                + "\t"+ str(float(sum(zip(*silent_bytes)[2])))
                + "\t"+ str(float(sum(zip(*silent_bytes)[1])))
                + "\t"+ str(float(sum(zip(*silent_bytes)[2])) / float(sum(zip(*silent_bytes)[1])))) + "\n"
    outputfile = open("/home/chettyharish/Downloads/op.txt", "a")
    outputfile.write(opstring)
    outputfile.close()


def script_runner():
    bench, processor, l1_size, l1_assoc, line_size = ("soplex","X86", "32", "1", "64")
    start_time = time.time()
    
    command1 = "cat /dev/null > /home/chettyharish/Downloads/op.txt"
    command2 = "cat /dev/null > /home/chettyharish/Downloads/Cache.txt"
    command3 = "cat /dev/null > /home/chettyharish/Downloads/Store.txt"
    command4 = "echo \"Config\t\t\tTotal\tSilent\tRatio\tSilentB\tTotalB\tRatio\" > /home/chettyharish/Downloads/op.txt"
    printTimeStatement(start_time)
    p = subprocess.Popen(command1 , shell=True)
    p.wait()
    printTimeStatement(start_time)
    p = subprocess.Popen(command2, shell=True)
    p.wait()
    printTimeStatement(start_time)
    p = subprocess.Popen(command3, shell=True)
    p.wait()
    printTimeStatement(start_time)
    p = subprocess.Popen(command4, shell=True)
    p.wait()
    printTimeStatement(start_time)
    
    
    
    cmd1 = ("time build/X86/gem5.debug configs/example/se.py --cpu-type=detailed" +
            "--bench=soplex  --l1d_size=32kB --l1d_assoc=1 --cacheline_size=64 ")
    data_analyzer(bench, processor, l1_size, l1_assoc, line_size)

if __name__ == "__main__":
    script_runner()
#     data_analyzer("soplex","X86", 32, 1, 64)
