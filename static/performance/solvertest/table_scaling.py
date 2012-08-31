#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# Tabulate parallel scalability performance.
#
# Uses subdirectory 'logs' with python log summaries.

logsDir = 'logs_lonestar'
cells = 'hex8'

# ======================================================================
import os
import sys
import numpy
import re

style = "latex"
if len(sys.argv) > 2:
    raise ValueError("usage: table_scalability.py [text | latex (default)]")
if len(sys.argv) == 2:
    style = sys.argv[1]

if not style in ["text", 
               "latex", 
               ]:
    raise ValueError("Unknown format (%s) requested." % style)


sys.path.append(logsDir)


# ----------------------------------------------------------------------
def eval_memory():
    #nprocs = [1,2,4,8,16,32,64]
    nprocs = [1,2,4,6,12,24,48,96]
    events = ["VecMDot", "VecAXPY", "VecMAXPY"]
            
    # Allocate storage for stats
    flops = {}
    imbalance = {}
    for e in events:
        flops[e] = numpy.zeros((len(nprocs),), dtype=numpy.float32)
        imbalance[e] = numpy.zeros((len(nprocs),), dtype=numpy.float32)

    # Get stats
    ip = 0
    for p in nprocs:
        modname = "%s_amg_np%03d" % (cells.lower(), nprocs[ip])
        if not os.path.exists("%s/%s.py" % (logsDir, modname)):
            print "Skipping stats for %d procs (%s). Log not found." % (p, modname)
            for e in events:
                flops[e][ip] = None
                imbalance[e][ip] = None
            continue

        # Get timing info from Python log
        log = __import__(modname)
        for e in events:
            elog = log.__getattribute__('Solve').event[e]
            eflops = elog.Flops
            etime = elog.Time
            flops[e][ip] = 1.0e-6*numpy.sum(eflops)/numpy.max(etime)
            imbalance[e][ip] = numpy.max(eflops)/numpy.min(eflops)

        ip += 1

    if style == "text":
        print "Event     #Cores  Load Imbalance  MFlops/s"
        for e in events:
            ip = 0
            line = "%-10s" % e
            while ip < len(nprocs):
                line += "%6d  %14.1f  %8.0f" % (nprocs[ip], imbalance[e][ip], flops[e][ip])
                print line
                line = " "*10
                ip += 1

    else:
        print "\\begin{tabular}{lrrr}"
        print "  \hline"
        print "  Event & \# Cores & Load Imbalance & MFlops/s \\\\"
        for e in events:
            print "  \hline"
            ip = 0
            line = e
            while ip < len(nprocs):
                line += " & %4d & %3.1f & %6.0f" % (nprocs[ip], imbalance[e][ip], flops[e][ip])
                print line + " \\\\"
                line = "    "
                ip += 1
        print "  \hline"
        print "\\end{tabular}"


# ----------------------------------------------------------------------
def eval_solver():
    #nprocs = [8,16,32,64]
    nprocs = [12,24,48,96]
    events = ["MatMult", "PCSetUp", "PCApply", "KSPSolve"]

    # Allocate storage for stats
    flops = {}
    time = {}
    calls = {}
    for e in events:
        flops[e] = numpy.zeros((len(nprocs),), dtype=numpy.float32)
        time[e] = numpy.zeros((len(nprocs),), dtype=numpy.float32)
        calls[e] = numpy.zeros((len(nprocs),), dtype=numpy.float32)

    # Get stats
    ip = 0
    for p in nprocs:
        modname = "%s_amg_np%03d" % (cells.lower(), nprocs[ip])
        if not os.path.exists("%s/%s.py" % (logsDir, modname)):
            print "Skipping stats for %d procs (%s). Log not found." % (p, modname)
            for e in events:
                flops[e][ip] = None
                time[e][ip] = None
                calls[e][ip] = None
            continue

        # Get timing info from Python log
        log = __import__(modname)
        for e in events:
            elog = log.__getattribute__('Solve').event[e]
            eflops = elog.Flops
            etime = elog.Time
            ecalls = elog.Count
            flops[e][ip] = 1.0e-6*numpy.sum(eflops)/numpy.max(etime)
            time[e][ip] = numpy.max(etime)
            calls[e][ip] = numpy.mean(ecalls)

        ip += 1

    if style == "text":
        print "\n\n"
        print "Event         Calls  Time (s)  MFlops/s"

        ip = 0
        while ip < len(nprocs):
            print "p = %d" % nprocs[ip]
            for e in events:
                line = "  %-10s  %5d  %8.1f  %8.0f" % (e, calls[e][ip], time[e][ip], flops[e][ip])
                print line
            ip += 1

    else:
        print "\\begin{tabular}{lrrr}"
        print "  \hline"
        print "  Event & \# Calls & Time (s) & MFlops/s \\\\"
        print "  \hline"

        ip = 0
        while ip < len(nprocs):
            print "\multicolumn{4}{c}{p = %d} \\\\" % nprocs[ip]
            for e in events:
                line = "  %s & %3d & %8.1f & %8.0f \\\\" % (e, calls[e][ip], time[e][ip], flops[e][ip])
                print line
            print "\hline"
            ip += 1
        print "\\end{tabular}"


            
# ----------------------------------------------------------------------
eval_memory()
eval_solver()
