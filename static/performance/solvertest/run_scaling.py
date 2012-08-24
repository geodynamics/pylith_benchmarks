#!/usr/bin/env python
#
# Python script to facilitate running scaling benchmarks.
#
# Use QUEUE == None if not using batch system.

import os
import sys
import subprocess

if len(sys.argv) != 7:
    raise ValueError("usage: run_scaling.py PC CELL DOMAIN PPN NNODES QUEUE")
pc = sys.argv[1]
cell = sys.argv[2]
domain = sys.argv[3]
ppn = int(sys.argv[4])
nnodes = int(sys.argv[5])
queue = sys.argv[6]

if not pc in ["asm_reduced", "asm", "amg", "schur"]:
    raise ValueError("PC type (%s) must be 'asm_reduced', 'asm', 'amg', or 'schur'." % pc)
if not cell in ["hex8", "tet4"]:
    raise ValueError("Cell type (%s) must be 'hex8' or 'tet4'." % cell)
if not domain in ["original", "cube"]:
    raise ValueError("Domain (%s) must be 'original' or 'cube'." % domain)

nprocs = ppn*nnodes
for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)


if domain == "cube":
    job = "%s_%s_%s_np%03d" % (cell, domain, pc, nprocs)
    mesh = "%s_%s_np%03d" % (cell, domain, nprocs)
else:
    job = "%s_%s_np%03d" % (cell, pc, nprocs)
    mesh = "%s_np%03d" % (cell, nprocs)

if queue.lower() != "none":
    batchfile = os.environ['HOME'] + "/.pyre/pylithapp/pylithapp_%s.cfg" % queue
else:
    batchfile = ""

if pc == "asm_reduced" or pc =="asm":
    pcfiles = " pc_asm.cfg"
elif pc == "amg":
    pcfiles = " pc_fieldsplit_mult.cfg pc_custom.cfg --petsc.fs_fieldsplit_0_pc_mg_log"
elif pc == "schur":
    pcfiles = " pc_schur_full_custom.cfg --petsc.fs_fieldsplit_0_pc_mg_log"

if not "reduced" in pc:
    bcfiles = " bc_full.cfg faults.cfg nooutput.cfg nooutput_faults.cfg %s.cfg %s_faults.cfg" % (cell, cell)
else:
    bcfiles = " bc_reduced.cfg nooutput.cfg %s.cfg"

args = batchfile + " --job.name=%s --job.stdout=logs/%s.log --job.stderr=logs/%s.err --petsc.log_summary_python=logs/%s.py" % (job, job, job, job)

if queue.lower() == "none":
    cmd = "pylith " + bcfiles + pcfiles + \
        " %s.cfg " % (mesh,) + \
        " --nodes=%d " % (ppn*nnodes) + \
        args

elif queue == "pbs":
    cmd = "pylith " + bcfiles + pcfiles + \
        " %s.cfg " % (mesh,) + \
        " --nodes=%d --scheduler.ppn=%d " % (nprocs, ppn) + \
        args

elif queue == "lonestar":
    cmd = "pylith " + bcfiles + pcfiles + \
        " %s.cfg " % (mesh,) + \
        " --nodes=%d --scheduler.pe-name=%dway --scheduler.pe-number=%s " % (nprocs, ppn, max(12, ppn)*nnodes) + \
        args


print cmd
#subprocess.call(cmd, shell=True)
