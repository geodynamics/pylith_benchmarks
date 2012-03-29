#!/usr/bin/env python
#
# Python script to facilitate running scaling benchmarks using cluster
# with PBS scheduler.
#
# REQUIRES: $HOME/.pyre/pylithapp/pylithapp_pbs.cfg file with PBS options.

import os
import sys
import subprocess

if len(sys.argv) != 3:
    raise ValueError("usage: run_scaling.py CELL NPROCS")
cell = sys.argv[1]
nprocs = int(sys.argv[2])

if not cell in ["hex8", "tet4"]:
    raise ValueError("Cell type (%s) must be 'hex8' or 'tet4'." % cell)
if nprocs != 1 and (nprocs % 2) != 0:
    raise ValueError("Number of processors (%d) must be a power of 2." % nprocs)


for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)

job = "%s_np%03d" % (cell, nprocs)

pbsfile = os.environ['HOME'] + "/.pyre/pylithapp/pylithapp_pbs.cfg"
pcfiles = "fieldsplit_mult.cfg custompc.cfg"
args = pbsfile + " --job.name=%s --job.stdout=logs/%s.log" % (job, job)

if nprocs < 8:
    ppn = nprocs
else:
    ppn = 8

cmd = "pylith %s.cfg %s.cfg " % (cell, job) + \
    pcfiles + \
    " --nodes=%d --scheduler.ppn=%d " % (nprocs, ppn) + \
    args

print cmd
subprocess.call(cmd, shell=True)
