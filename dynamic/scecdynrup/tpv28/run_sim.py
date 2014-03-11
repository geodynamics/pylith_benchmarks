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
#
# Use QUEUE == None if not using batch system.

import os
import sys
import subprocess

if len(sys.argv) != 6:
    raise ValueError("usage: run_sim.py CELL RES PPN NNODES QUEUE")
cell = sys.argv[1]
res = sys.argv[2]
ppn = int(sys.argv[3])
nnodes = int(sys.argv[4])
queue = sys.argv[5]

tpv = "tpv28"
if not cell in ["hex8", "tet4"]:
    raise ValueError("Cell type (%s) must be 'hex8' or 'tet4'." % cell)
if not res in ["200m", "100m"]:
    raise ValueError("Resolution (%s) must be '200m' or '100m'." % res)

nprocs = ppn*nnodes
for d in ["output", "logs"]:
  if not os.path.isdir(d):
      os.mkdir(d)

job = "%s_%s" % (cell, res)

if queue.lower() != "none":
    batchfile = os.environ['HOME'] + "/.pyre/pylithapp/pylithapp_%s.cfg" % queue
else:
    batchfile = ""

cfgfiles = " %s.cfg %s.cfg" % (cell, job)

args = batchfile + " --job.name=%s --job.stdout=logs/%s.log --job.stderr=logs/%s.err " % (job, job, job)

if queue.lower() == "none":
    cmd = "pylith " + cfgfiles + \
        " --nodes=%d " % (ppn*nnodes) + \
        args

elif queue == "pbs":
    #cfgfiles += " mem12bg.cfg"
    cmd = "pylith " + cfgfiles + \
        " --nodes=%d --scheduler.ppn=%d " % (nprocs, ppn) + \
        args

elif queue == "lonestar":
    cmd = "pylith " + cfgfiles + \
        " --nodes=%d --scheduler.pe-name=%dway --scheduler.pe-number=%s " % (nprocs, ppn, max(12, ppn)*nnodes) + \
        args

else:
    raise ValueError("Unknown queue '%s'." % queue)

print cmd
#subprocess.call(cmd, shell=True)
