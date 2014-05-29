#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
# Charles A. Williams, GNS Science
# Matthew G. Knepley, University of Chicago
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2014 University of California, Davis
#
# See COPYING for license information.
#
# ----------------------------------------------------------------------
#
# Python script to facilitate running benchmarks.

import os
import sys
import subprocess

ppn = 8
batchfile = os.environ['HOME'] + "/.pyre/pylithapp/pylithapp_pbs.cfg"

if len(sys.argv) != 4:
    raise ValueError("usage: run_sim.py CELL RES NPROCS")
cell = sys.argv[1]
res = sys.argv[2]
nprocs = int(sys.argv[3])

if not cell in ["hex8", "tet4"]:
    raise ValueError("Cell type (%s) must be 'hex8' or 'tet4'." % cell)
if not res in ["200m", "100m"]:
    raise ValueError("Resolution (%s) must be '200m' or '100m'." % res)

for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)

job = "%s_%s" % (cell, res)

cfgfiles = " %s.cfg %s.cfg" % (cell, job)

args = batchfile + " --job.name=%s --job.stdout=logs/%s.log --job.stderr=logs/%s.err " % (job, job, job)

cmd = "pylith " + cfgfiles + \
    " --nodes=%d --scheduler.ppn=%d " % (nprocs, ppn) + \
        args

print cmd
#subprocess.call(cmd, shell=True)
