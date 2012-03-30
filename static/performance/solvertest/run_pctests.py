#!/usr/bin/env python
#
# Python script to facilitate running preconditioner benchmarks. All
# runs are done on a single processor.

import os
import sys
import subprocess

if len(sys.argv) != 2:
    raise ValueError("usage: run_scaling.py SIM")
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
def runPyLith(args, logFilename):
    log = open("logs/logFilename", "w")
    subprocess.call("pylith " + args, stdout=log, stderr=log, shell=True)
    log.close()
    return

# ----------------------------------------------------------------------
if sim == "all" or sim == "asm":
  # ASM
  #
  # STATUS: OK
  print "ASM preconditioner"
  runPyLith("tet4.cfg asm.cfg", "tet4_asm.log")
  runPyLith("hex8.cfg asm.cfg", "hex8_asm.log")

# ----------------------------------------------------------------------
if sim == "all" or sim == "fieldsplit":

  # field split, additive
  #
  # STATUS: OK
  print  "field split, additive"
  runPyLith("tet4.cfg fieldsplit_add.cfg", "tet4_fieldsplit_add.log")
  runPyLith("hex8.cfg fieldsplit_add.cfg", "hex8_fieldsplit_add.log")

  # field split, multiplicative
  #
  # STATUS: OK
  print "field split, multiplicative"
  runPyLith("tet4.cfg fieldsplit_mult.cfg", "tet4_fieldsplit_mult.log")
  runPyLith("hex8.cfg fieldsplit_mult.cfg", "hex8_fieldsplit_mult.log")

  # field split, multiplicative w/custom fault preconditioner
  #
  # STATUS: OK
  print "field split, multiplicative w/custom pc"
  runPyLith("tet4.cfg fieldsplit_mult.cfg custompc.cfg", "tet4_fieldsplit_mult_custompc.log")
  runPyLith("hex8.cfg fieldsplit_mult.cfg custompc.cfg", "hex8_fieldsplit_mult_custompc.log")

# ----------------------------------------------------------------------
if sim == "all" or sim == "schur":

  # Schur complement, diagonal
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              true residual does not decrease for hex8
  print "schur, diag"
  runPyLith("tet4.cfg schur_diag.cfg", "tet4_schur_diag.log")
  runPyLith("hex8.cfg schur_diag.cfg", "hex8_schur_diag.log")

  # Schur complement, lower
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              hangs at iteration 8 for hex8
  print "schur, lower"
  runPyLith("tet4.cfg schur_lower.cfg", "tet4_schur_lower.log")
  runPyLith("hex8.cfg schur_lower.cfg", "hex8_schur_lower.log")

  # Schur complement, upper
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              works for hex8
  print "schur, upper"
  runPyLith("tet4.cfg schur_upper.cfg", "tet4_schur_upper.log")
  runPyLith("hex8.cfg schur_upper.cfg", "hex8_schur_upper.log")

  # Schur complement, full
  #
  # STATUS: BUG, hangs at very beginning of solve for tet4 
  #              works for hex8
  print "schur, full"
  runPyLith("tet4.cfg schur_full.cfg", "tet4_schur_full.log")
  runPyLith("hex8.cfg schur_full.cfg", "hex8_schur_full.log")


# End of file
