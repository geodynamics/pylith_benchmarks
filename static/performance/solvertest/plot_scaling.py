#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# Plot performance for weak scaling.
#
# PREREQUISITES: matplotlib, numpy
#
# Create subdirectory 'logs' with ASCII and python log summaries.

import matplotlib.pyplot as pyplot
import numpy
import sys
import os
import re

sys.path.append("../../../figures")
import matplotlibext

header = 0.3
logsDir = "logs_lonestar"

#nprocs = [1,2,4,8,16,32,64]
nprocs = [1,2,4,6,12,24,48,96]
stages = ["Solve",
          "Reform Jacobian",
          "Reform Residual",
          ]
cells = ["Hex8",
         "Tet4",
         ]

symdict = {'Hex8': 's',
           'Tet4': '^',
           }
styledict = {'Reform Jacobian': ('blue', (3,1.5)),
             'Reform Residual': ('purple', (6,1.5)),
             'Solve': ('red', (None, None)),
             'MG Apply': ('ltblue', (1.5, 1.5)),
             'Setup': ('orange', (None,None)),
             'Prestep': ('green', (None, None)),
             }
             

# Allocate storage for stats
data = {}
for c in cells:
    data[c] = {}
    for s in stages:
        data[c][s] = numpy.zeros(len(nprocs), dtype=numpy.float32)

# Get stats
niters = {}
sys.path.append(logsDir)
for c in cells:
    niters[c] = numpy.zeros(len(nprocs), dtype=numpy.float32)
    for ip in xrange(len(nprocs)):
        modname = "%s_amg_np%03d" % (c.lower(), nprocs[ip])
        if not os.path.exists("%s/%s.py" % (logsDir, modname)):
            print "Skipping stats for cell %s and %d procs (%s). Log not found." %\
                (c, nprocs[ip], modname)
            niters[c][ip] = None
            data[c][s][ip] = None
            continue

        # Get timing info from Python log
        log = __import__(modname)
        for s in stages:
            total = 0.0
            sattr = s.replace(' ','_')
            assert(nprocs[ip] == log.__getattribute__('Nproc'))
            try:
                data[c][s][ip] = log.__getattribute__(sattr).time / nprocs[ip]
            except AttributeError:
                data[c][s][ip] = 0

        # Get number of iterations from ASCII log
        logname = "%s/%s_amg_np%03d.log" % (logsDir, c.lower(), nprocs[ip])
        with open(logname, "r") as fin:
            for line in fin:
                refields = re.search("Linear solve converged due to \w+ iterations ([0-9]+)", line)
                if refields:
                    niters[c][ip] = refields.group(1)
                    break

figure = matplotlibext.Figure()
figure.open(3.0, 5.25, margins=[[0.5, 0.35, 0.15], [0.42, 0.4, 0.05]], dpi=150)

ncols = 1
nrows = 2

icol = 0
irow = 0

ax = figure.axes(nrows+header, ncols, irow+1+header, icol+1)

for c in cells:
    for s in stages:
        ax.loglog(nprocs, data[c][s], 
                  marker=symdict[c], 
                  color=styledict[s][0], 
                  linewidth=1,
                  dashes=styledict[s][1])
        ax.hold(True)
        if s == 'Solve' and False:
            ax.loglog(nprocs, data[c][s]/(niters[c]/niters[c][0]), 
                      marker=symdict[c], 
                      color='gray',
                      linewidth=1,
                      dashes=styledict[s][1])

ax.set_xlim((1, 100))
#ax.set_xlabel("# Processors")

ax.set_ylim((0.1, 100))
if icol == 0:
    ax.set_ylabel("Time (s)")
else:
    ax.set_yticklabels([])
    ax.set_ylabel("")

if icol == 0:
    import matplotlib.lines as lines
    proxies = []
    for c in cells:
        proxies.append(lines.Line2D((0,0),(1,1), 
                                    marker=symdict[c], 
                                    color=styledict['Solve'][0],
                                    linewidth=0))
    l1 = ax.legend(proxies, cells, 
                   loc='lower left', 
                   bbox_to_anchor=(0,1.05), 
                   borderaxespad=0)

    proxies = []
    for s in stages:
        proxies.append(lines.Line2D((0,0),(1,1), 
                                    marker=None, 
                                    color=styledict[s][0],
                                    dashes=styledict[s][1]))
    ax.legend(proxies, stages, 
              loc='lower right', 
              bbox_to_anchor=(1,1.05), 
              borderaxespad=0)
    ax.add_artist(l1)

irow += 1
ax = figure.axes(nrows+header, ncols, irow+1+header, icol+1)

for c in cells:
    ax.loglog(nprocs, niters[c], 
                marker=symdict[c], 
                color='red', 
                linewidth=1)
    ax.hold(True)

ax.set_xlim((1, 100))
ax.set_xlabel("# Processors")

ax.set_ylim((1, 100))
if icol == 0:
    ax.set_ylabel("# Iterations")
else:
    ax.set_yticklabels([])
    ax.set_ylabel("")

pyplot.show()
pyplot.savefig('solvertest_scaling.eps')
