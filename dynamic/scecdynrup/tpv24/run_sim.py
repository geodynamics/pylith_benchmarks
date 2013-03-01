#!/usr/bin/env python
#
# Python script to facilitate running benchmarks.
#
# Use QUEUE == None if not using batch system.

import os
import sys
import subprocess

if len(sys.argv) != 7:
    raise ValueError("usage: run_sim.py TPV CELL RES PPN NNODES QUEUE")
tpv = sys.argv[1]
cell = sys.argv[2]
res = sys.argv[3]
ppn = int(sys.argv[4])
nnodes = int(sys.argv[5])
queue = sys.argv[6]

if not tpv in ["tpv24", "tpv25"]:
    raise ValueError("TPV (%s) must be 'tpv24' or 'tpv25'." % pc)
if not cell in ["hex8", "tet4"]:
    raise ValueError("Cell type (%s) must be 'hex8' or 'tet4'." % cell)
if not res in ["200m", "100m"]:
    raise ValueError("Resolution (%s) must be '200c' or '100m'." % res)

nprocs = ppn*nnodes
for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)

job = "%s_%s_%s" % (tpv, cell, res)

if queue.lower() != "none":
    batchfile = os.environ['HOME'] + "/.pyre/pylithapp/pylithapp_%s.cfg" % queue
else:
    batchfile = ""

cfgfiles = " %s.cfg %s.cfg %s.cfg" % (tpv, cell, job)

args = batchfile + " --job.name=%s --job.stdout=logs/%s.log --job.stderr=logs/%s.err " % (job, job, job)

if queue.lower() == "none":
    cmd = "pylith " + cfgfiles + \
        " --nodes=%d " % (ppn*nnodes) + \
        args

elif queue == "pbs":
    cmd = "pylith " + cfgfiles + \
        " --nodes=%d --scheduler.ppn=%d " % (nprocs, ppn) + \
        args

elif queue == "lonestar":
    cmd = "pylith " + cfgfiles + \
        " --nodes=%d --scheduler.pe-name=%dway --scheduler.pe-number=%s " % (nprocs, ppn, max(12, ppn)*nnodes) + \
        args


print cmd
#subprocess.call(cmd, shell=True)
