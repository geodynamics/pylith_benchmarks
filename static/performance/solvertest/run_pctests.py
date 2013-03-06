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
               "fieldsplit_gamg",
               "schur",
               ]:
    raise ValueError("Unknown preconditioner (%s) requested." % sim)

for d in ["output", "logs_pctest"]:
  if not os.path.isdir(d):
      os.mkdir(d)

# ----------------------------------------------------------------------
def runPyLith(args, pcname):
    for cell in ["tet4","hex8"]:
        for nprocs in [1,2,4]:
            job = "%s_%s_np%03d" % (cell, pcname, nprocs)
            jargs = args + " bc_full.cfg faults.cfg %s.cfg %s_faults.cfg %s_np%03d.cfg --nodes=%d" % (cell, cell, cell, nprocs, 1)
            jargs += " --petsc.log_summary_python=logs_pctest/%s.py" % job
            logFilename = "logs_pctest/" + job + ".log"
            log = open(logFilename, "w")
            print "  pylith "+jargs
            subprocess.call("pylith "+jargs, stdout=log, stderr=log, shell=True)
            log.close()
    return

# ----------------------------------------------------------------------
if sim == "all" or sim == "asm":
  print "ASM preconditioner"
  runPyLith("pc_asm.cfg", "asm")

# ----------------------------------------------------------------------
if sim == "all" or sim == "fieldsplit":

  # field split, additive
  print  "field split, additive"
  runPyLith("pc_fieldsplit_add.cfg", "fieldsplit_add")

  # field split, multiplicative
  print "field split, multiplicative"
  runPyLith("pc_fieldsplit_mult.cfg", "fieldsplit_mult")

  # field split, multiplicative w/custom fault preconditioner
  print "field split, multiplicative w/custom pc"
  runPyLith("pc_fieldsplit_mult.cfg pc_custom.cfg", "fieldsplit_mult_custom")

# ----------------------------------------------------------------------
if sim == "all" or sim == "fieldsplit_gamg":

  # field split, multiplicative w/custom fault preconditioner
  print "field split, gamg, multiplicative w/custom pc"
  runPyLith("pc_fieldsplit_mult_gamg.cfg pc_custom.cfg", "fieldsplit_mult_gamg_custom")

# ----------------------------------------------------------------------
if sim == "all" or sim == "schur":

  # Schur complement, full
  print "schur, full"
  runPyLith("pc_schur_full.cfg", "schur_full")

  # Schur complement, upper
  print "schur, upper"
  runPyLith("pc_schur_upper.cfg", "schur_upper")


  # Schur complement, full w/custom fault preconditioner
  print "schur, full"
  runPyLith("pc_schur_full_custom.cfg", "schur_full_custom")

  # Schur complement, upper w/custom fault preconditioner
  print "schur, upper"
  runPyLith("pc_schur_upper_custom.cfg", "pc_schur_upper_custom")


# End of file
