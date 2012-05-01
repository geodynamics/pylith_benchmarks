#!/usr/bin/env python
#
# Python script to facilitate running preconditioner benchmarks. All
# runs are done on a single processor.

import os
import sys
import subprocess

if len(sys.argv) != 2:
    raise ValueError("usage: run_pctests.py PCTYPE")
sim = sys.argv[1]

if not sim in ["all", 
               "asm", 
               "fieldsplit",
               "schur",
               ]:
    raise ValueError("Unknown preconditioner (%s) requested." % sim)

for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)

# ----------------------------------------------------------------------
def runPyLith(args, pcname):
    for cell in ["tet4","hex8"]:
        for nprocs in [1,2,4]:
            job = "%s_%s_np%03d" % (cell, pcname, nprocs)
            jargs = args + " %s.cfg %s_np%03d.cfg --nodes=%d" % \
                (cell, cell, nprocs, 1)
            jargs += " --petsc.log_summary_python=logs/%s.py" % job
            logFilename = "logs/" + job + ".log"
            log = open(logFilename, "w")
            print "  pylith "+jargs
            subprocess.call("pylith "+jargs, stdout=log, stderr=log, shell=True)
            log.close()
    return

# ----------------------------------------------------------------------
if sim == "all" or sim == "asm":
  # ASM
  #
  # STATUS: OK
  print "ASM preconditioner"
  runPyLith("asm.cfg", "asm")

# ----------------------------------------------------------------------
if sim == "all" or sim == "fieldsplit":

  # field split, additive
  #
  # STATUS: OK
  print  "field split, additive"
  runPyLith("fieldsplit_add.cfg", "fieldsplit_add")

  # field split, multiplicative
  #
  # STATUS: OK
  print "field split, multiplicative"
  runPyLith("fieldsplit_mult.cfg", "fieldsplit_mult")

  # field split, multiplicative w/custom fault preconditioner
  #
  # STATUS: OK
  print "field split, multiplicative w/custom pc"
  runPyLith("fieldsplit_mult.cfg custompc.cfg", "fieldsplit_mult_custompc")

# ----------------------------------------------------------------------
if sim == "all" or sim == "schur":

  # Schur complement, diagonal
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              true residual does not decrease for hex8
  print "schur, diag"
  runPyLith("schur_diag.cfg", "schur_diag")

  # Schur complement, lower
  print "schur, lower"
  runPyLith("schur_lower.cfg", "schur_lower")

  # Schur complement, upper
  print "schur, upper"
  runPyLith("schur_upper.cfg", "schur_upper")

  # Schur complement, full
  print "schur, full"
  runPyLith("schur_full.cfg", "schur_full")


# End of file
