#!/usr/bin/env python
#
# Python script to facilitate running Savage and Prescott benchmark.

import os
import sys
import subprocess

if len(sys.argv) >= 3:
    cell = sys.argv[1]
    nprocs = int(sys.argv[2])
    batch = None
    if len(sys.argv) == 4:
        batch = sys.argv[3].upper()
else:
    raise ValueError("usage: run_sims.py CELL NPROCS [BATCH_SYSTEM]")

if not cell in ["hex8", "tet4"]:
    raise ValueError("Cell type (%s) must be 'hex8' or 'tet4'." % cell)

if not batch is None and not batch in ["PBS"]:
    raise ValueError("Unknown batch system '%s'." % batch)

for d in ["output"]:
  if not os.path.isdir(d):
      os.mkdir(d)

args = "%s.cfg fieldsplit.cfg --nodes=%d" % (cell, nprocs)
if batch == "PBS":
    pbsfile = os.environ['HOME'] + "/.pyre/pylithapp/pylithapp_pbs.cfg"
    args += " " + pbsfile + " --job.name=savageprescott_%s --job.stdout=%s.log" % (cell, cell)

    if nprocs < 8:
        ppn = nprocs
    else:
        ppn = 8
    args += " --scheduler.ppn=%d" % ppn


cmd = "pylith " + args
print cmd
subprocess.call(cmd, shell=True)
