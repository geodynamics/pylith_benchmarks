#!/usr/bin/env python
#
# Python script to facilitate running fieldsplit convergence
# benchmarks. All runs are done on a single processor.

import os
import sys
import subprocess

if len(sys.argv) != 1:
    raise ValueError("usage: run_convtest.py")

for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)

# ----------------------------------------------------------------------
def runPyLith(args, logFilename):
    log = open("logs/logFilename", "w")
    subprocess.call("pylith " + args, stdout=log, stderr=log, shell=True)
    log.close()
    return


# ----------------------------------------------------------------------
for cell in ["hex8","tet4"]:

  print "ASM w/small tolerance"
  args = "%s.cfg asm.cfg" % cell
  runPyLith(args + " --petsc.ksp_rtol=1.0e-18", "%s_asm_tol18.log" % cell)

  print "Field split w/custom PC, rtol=1.0e-6"
  args = "%s.cfg fieldsplit_mult.cfg custompc.cfg" % cell
  runPyLith(args + " --petsc.ksp_rtol=1.0e-6", "%s_fs_tol06.log" % cell)

  print "Field split w/custom PC, rtol=1.0e-7"
  args = "%s.cfg fieldsplit_mult.cfg custompc.cfg" % cell
  runPyLith(args + " --petsc.ksp_rtol=1.0e-7", "%s_fs_tol07.log" % cell)

  print "Field split w/custom PC, rtol=1.0e-8"
  args = "%s.cfg fieldsplit_mult.cfg custompc.cfg" % cell
  runPyLith(args + " --petsc.ksp_rtol=1.0e-8", "%s_fs_tol08.log" % cell)
