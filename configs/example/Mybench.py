#Mybench.py
import optparse
import sys
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.util import addToPath, fatal

addToPath('../common')
addToPath('../ruby')

import Options
import Ruby
import Simulation
import CacheConfig
import MemConfig
from Caches import *
from cpu2000 import *

cpu2006_dir = os.environ["M5_HOME"] + "/CPU2006v1.0.1/benchspec/CPU2006/"
benchmarks = {}

#400.perlbench
perlbench = LiveProcess()
perlbench.executable =  cpu2006_dir+'400.perlbench/exe/perlbench_base.i386-m32-gcc42-nn'
perlbench.cmd = [perlbench.executable] + ['-I./lib', cpu2006_dir + '400.perlbench/data/test/input/attrs.pl']
#perlbench.output = 'attrs.out'
benchmarks['perlbench'] = perlbench

#401.bzip2
#1 0m 1s
#2 40m
bzip2 = LiveProcess()
bzip2.executable =  cpu2006_dir+'401.bzip2/exe/bzip2_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'401.bzip2/data/all/input/input.program'
bzip2.cmd = [bzip2.executable] + [data, '1']
#bzip2.output = 'input.program.out'
benchmarks['bzip2'] = bzip2

#403.gcc
gcc = LiveProcess()
gcc.executable =  cpu2006_dir+'403.gcc/exe/gcc_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'403.gcc/data/test/input/cccp.i'
output= cpu2006_dir + '403.gcc/exe/cccp.s'
gcc.cmd = [gcc.executable] + [data]+['-o',output]
#gcc.output = 'ccc.out'
benchmarks['gcc'] = gcc

#410.bwaves
#no
bwaves = LiveProcess()
bwaves.executable =  cpu2006_dir+'410.bwaves/exe/bwaves_base.i386-m32-gcc42-nn'
bwaves.cmd = [bwaves.executable]
benchmarks['bwaves'] = bwaves

#416.gamess
#no
gamess=LiveProcess()
gamess.executable =  cpu2006_dir+'416.gamess/exe/gamess_base.i386-m32-gcc42-nn'
gamess.cmd = [gamess.executable]
gamess.input='CPU2006v1.0.1/benchspec/CPU2006/416.gamess/data/test/input/exam29.config'
#gamess.output='exam29.output'
benchmarks['gamess'] = gamess

#429.mcf
# yes
#0 0m 4s
mcf = LiveProcess()
mcf.executable =  cpu2006_dir+'429.mcf/exe/mcf_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'429.mcf/data/test/input/inp.in'
mcf.cmd = [mcf.executable] + [data]
#mcf.output = 'inp.out'
benchmarks['mcf'] = mcf

#433.milc
#toolong
#0 0m 16s
milc=LiveProcess()
milc.executable = cpu2006_dir+'433.milc/exe/milc_base.i386-m32-gcc42-nn'
stdin=cpu2006_dir+'433.milc/data/test/input/su3imp.in'
milc.cmd = [milc.executable]
milc.input=stdin
#milc.output='su3imp.out'
benchmarks['milc'] = milc

#434.zeusmp
#fortran
#no
zeusmp=LiveProcess()
zeusmp.executable =  cpu2006_dir+'434.zeusmp/exe/zeusmp_base.i386-m32-gcc42-nn'
zeusmp.cmd = [zeusmp.executable]
#zeusmp.output = 'zeusmp.stdout'
#benchmarks['zeusmp'] = zeusmp

#435.gromacs
#fortran
# no
gromacs = LiveProcess()
gromacs.executable =  cpu2006_dir+'435.gromacs/exe/gromacs_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'435.gromacs/data/test/input/gromacs.tpr'
gromacs.cmd = [gromacs.executable] + ['-silent','-deffnm',data,'-nice','0']
#benchmarks['gromacs'] = gromacs

#436.cactusADM
#fortran
cactusADM = LiveProcess()
cactusADM.executable =  cpu2006_dir+'436.cactusADM/exe/cactusADM_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'436.cactusADM/data/test/input/benchADM.par'
cactusADM.cmd = [cactusADM.executable] + [data]
#cactusADM.output = 'benchADM.out'
#benchmarks['cactusADM'] = cactusADM

#437.leslie3d
#fortran
leslie3d=LiveProcess()
leslie3d.executable =  cpu2006_dir+'437.leslie3d/exe/leslie3d_base.i386-m32-gcc42-nn'
stdin=cpu2006_dir+'437.leslie3d/data/test/input/leslie3d.in'
leslie3d.cmd = [leslie3d.executable]
leslie3d.input=stdin
#leslie3d.output='leslie3d.stdout'
#benchmarks['leslie3d'] = leslie3d

#444.namd
#1 0m 37s
namd = LiveProcess()
namd.executable =  cpu2006_dir+'444.namd/exe/namd_base.i386-m32-gcc42-nn'
input=cpu2006_dir+'444.namd/data/all/input/namd.input'
namd.cmd = [namd.executable] + ['--input',input,'--iterations','1','--output','namd.out']
#namd.output='namd.stdout'
benchmarks['namd'] = namd

#445.gobmk
gobmk=LiveProcess()
gobmk.executable =  cpu2006_dir+'445.gobmk/exe/gobmk_base.i386-m32-gcc42-nn'
stdin=cpu2006_dir+'445.gobmk/data/test/input/capture.tst'
gobmk.cmd = [gobmk.executable]+['--quiet','--mode','gtp']
gobmk.input=stdin
#gobmk.output='capture.out'
benchmarks['gobmk'] = gobmk

#447.dealII
#no
dealII=LiveProcess()
dealII.executable =  cpu2006_dir+'447.dealII/exe/dealII_base.i386-m32-gcc42-nn'
dealII.cmd = [gobmk.executable]+['8']
#dealII.output='log'
#benchmarks['dealII'] = dealII


#450.soplex
#1 0m 0s
#2 1m 21s
soplex=LiveProcess()
soplex.executable =  cpu2006_dir+'450.soplex/exe/soplex_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'450.soplex/data/test/input/test.mps'
soplex.cmd = [soplex.executable]+['-m10000',data]
#soplex.output = 'test.out'
benchmarks['soplex'] = soplex

#453.povray
povray=LiveProcess()
povray.executable =  cpu2006_dir+'453.povray/exe/povray_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'453.povray/data/test/input/SPEC-benchmark-test.ini'
#povray.cmd = [povray.executable]+['SPEC-benchmark-test.ini']
povray.cmd = [povray.executable]+[data]
#povray.output = 'SPEC-benchmark-test.stdout'
benchmarks['povray'] = povray

#454.calculix
calculix=LiveProcess()
calculix.executable =  cpu2006_dir+'454.calculix/exe/calculix_base.i386-m32-gcc42-nn'
data='/import/RaidHome/mjwu/work_spec2006/454.calculix/m5/beampic'
calculix.cmd = [calculix.executable]+['-i',data]
#calculix.output = 'beampic.log'
#benchmarks['calculix'] = calculix

#456.hmmer
#0 0m 0s
#1 20m
hmmer=LiveProcess()
hmmer.executable =  cpu2006_dir+'456.hmmer/exe/hmmer_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'456.hmmer/data/test/input/bombesin.hmm'
hmmer.cmd = [hmmer.executable]+['--fixed', '0', '--mean', '325', '--num', '5000', '--sd', '200', '--seed', '0', data]
#hmmer.output = 'bombesin.out'
benchmarks['hmmer'] = hmmer

#458.sjeng
#1 0m 5s
sjeng=LiveProcess()
sjeng.executable =  cpu2006_dir+'458.sjeng/exe/sjeng_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'458.sjeng/data/test/input/test.txt'
sjeng.cmd = [sjeng.executable]+[data]
#sjeng.output = 'test.out'
benchmarks['sjeng'] = sjeng

#459.GemsFDTD
#fortran
GemsFDTD=LiveProcess()
GemsFDTD.executable =  cpu2006_dir+'459.GemsFDTD/exe/GemsFDTD_base.i386-m32-gcc42-nn'
GemsFDTD.cmd = [GemsFDTD.executable]
#GemsFDTD.output = 'test.log'
#benchmarks['GemsFDTD'] = GemsFDTD

#462.libquantum
#0 0m 0
#1 2m 18s
libquantum=LiveProcess()
libquantum.executable =  cpu2006_dir+'462.libquantum/exe/libquantum_base.i386-m32-gcc42-nn'
libquantum.cmd = [libquantum.executable],'33','5'
#libquantum.output = 'test.out'
benchmarks['libquantum'] = libquantum

#464.h264ref
#no
h264ref=LiveProcess()
h264ref.executable =  cpu2006_dir+'464.h264ref/exe/h264ref_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'464.h264ref/data/all/input/foreman_qcif.yuv'
h264ref.cmd = [h264ref.executable]+['-d',data]
#h264ref.output = 'foreman_test_encoder_baseline.out'
benchmarks['h264ref'] = h264ref

#470.lbm
#1 0m 2s
lbm=LiveProcess()
lbm.executable =  cpu2006_dir+'470.lbm/exe/lbm_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'470.lbm/data/test/input/100_100_130_cf_a.of'
lbm.cmd = [lbm.executable]+['20', 'reference.dat', '0', '1' ,data]
#lbm.output = 'lbm.out'
benchmarks['lbm'] = lbm

#471.omnetpp
# 0m 0s
# 20m
omnetpp=LiveProcess()
omnetpp.executable =  cpu2006_dir+'471.omnetpp/exe/omnetpp_base.i386-m32-gcc42-nn'
data=cpu2006_dir+'471.omnetpp/data/test/input/omnetpp.insdfssdfi'
omnetpp.cmd = [omnetpp.executable]+[data]
#omnetpp.output = 'omnetpp.log'
benchmarks['omnetpp'] = omnetpp

#473.astar
astar=LiveProcess()
astar.executable =  cpu2006_dir+'473.astar/exe/astar_base.i386-m32-gcc42-nn'
astar.cmd = [astar.executable]+['lake.cfg']
#astar.output = 'lake.out'
benchmarks['astar'] = astar

#481.wrf
#fortran
wrf=LiveProcess()
wrf.executable =  cpu2006_dir+'481.wrf/exe/wrf_base.i386-m32-gcc42-nn'
wrf.cmd = [wrf.executable]+['namelist.input']
#wrf.output = 'rsl.out.0000'
#benchmarks['wrf'] = wrf

#482.sphinx
#no
sphinx3=LiveProcess()
sphinx3.executable =  cpu2006_dir+'482.sphinx_livepretend/exe/sphinx_livepretend_base.i386-m32-gcc42-nn'
sphinx3.cmd = [sphinx3.executable]+['ctlfile', '.', 'args.an4']
#sphinx3.output = 'an4.out'
#benchmarks['sphinx3'] = sphinx3

#483.xalancbmk
#no
xalancbmk=LiveProcess()
xalancbmk.executable =  cpu2006_dir+'483.Xalan/exe/Xalan_base.i386-m32-gcc42-nn'
xalancbmk.cmd = [xalancbmk.executable]+['-v','test.xml','xalanc.xsl']
#xalancbmk.output = 'test.out'
#benchmarks['xalancbmk'] = xalancbmk

#998.specrand
#0 0m 1s
#1 0m 56s
specrand_i=LiveProcess()
specrand_i.executable = cpu2006_dir+'998.specrand/exe/specrand_base.i386-m32-gcc42-nn'
specrand_i.cmd = [specrand_i.executable] + ['324342','24239']
#specrand_i.output = 'rand.24239.out'
benchmarks['specrand_i'] = specrand_i

#999.specrand
specrand_f=LiveProcess()
specrand_f.executable = cpu2006_dir+'999.specrand/exe/specrand_base.i386-m32-gcc42-nn'
specrand_f.cmd = [specrand_i.executable] + ['324342','24239']
#specrand_f.output = 'rand.24239.out'
#benchmarks['specrand_f'] = specrand_f
