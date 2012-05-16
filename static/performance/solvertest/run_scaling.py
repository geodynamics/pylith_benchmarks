#!/usr/bin/env python
#
# Python script to facilitate running scaling benchmarks using cluster
# with PBS scheduler.
#
# REQUIRES: $HOME/.pyre/pylithapp/pylithapp_pbs.cfg file with PBS options.

import os
import sys
import subprocess

if len(sys.argv) != 4:
    raise ValueError("usage: run_scaling.py PC CELL NPROCS")
pc = sys.argv[1]
cell = sys.argv[2]
nprocs = int(sys.argv[3])

if not pc in ["asm_reduced", "asm", "amg", "schur"]:
    raise ValueError("PC type (%s) must be 'asm_reduced', 'asm', 'amg', or 'schur'." % pc)
if not cell in ["hex8", "tet4"]:
    raise ValueError("Cell type (%s) must be 'hex8' or 'tet4'." % cell)
if nprocs != 1 and (nprocs % 2) != 0:
    raise ValueError("Number of processors (%d) must be a power of 2." % nprocs)


for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)

job = "%s_%s_np%03d" % (cell, pc, nprocs)
mesh = "%s_np%03d" % (cell, nprocs)

pbsfile = os.environ['HOME'] + "/.pyre/pylithapp/pylithapp_pbs.cfg"
if pc == "asm_reduced" or pc =="asm":
    pcfiles = " pc_asm.cfg"
elif pc == "amg":
    pcfiles = " pc_fieldsplit_mult.cfg pc_custom.cfg --petsc.fs_fieldsplit_0_pc_mg_log"
elif pc == "schur":
    pcfiles = " pc_schur_full_custom.cfg --petsc.fs_fieldsplit_0_pc_mg_log"

if not "reduced" in pc:
    bcfiles = " bc_full.cfg faults.cfg nooutput.cfg nooutput_faults.cfg"
else:
    bcfiles = " bc_reduced.cfg nooutput.cfg "

args = pbsfile + " --job.name=%s --job.stdout=logs/%s.log --job.stdout=logs/%s.err" % (job, job, job)

if nprocs < 8:
    ppn = nprocs
else:
    ppn = 8

cmd = "pylith " + bcfiles + pcfiles + \
    " %s.cfg %s.cfg " % (cell, mesh) + \
    " --nodes=%d --scheduler.ppn=%d " % (nprocs, ppn) + \
    args

print cmd
#subprocess.call(cmd, shell=True)
