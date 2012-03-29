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
# Create subdirectory 'logs' with python log summaries.

import matplotlib.pyplot as pyplot
import numpy
import sys

sys.path.append("../../../figures")
import matplotlibext

nprocs = [1,2,4,8,16,32]
events = ["Solve",
          "Reform Jacobian",
          "Reform Residual",
          ]
cells = ["Hex8",
         "Tet4",
         ]

symdict = {'Hex8': 's',
           'Tet4': '^',
           }
styledict = {'Setup': ('orange', (None,None)),
             'Prestep': ('green', (None, None)),
             'Reform Jacobian': ('blue', (3,1.5)),
             'Reform Residual': ('purple', (6,1.5)),
             'Solve': ('red', (None, None)),
             'Poststep': ('ltblue', (None, None)),
             }
             

# Allocate storage for stats
data = {}
for c in cells:
    data[c] = {}
    for e in events:
        data[c][e] = numpy.zeros(len(nprocs), dtype=numpy.float32)

# Get stats
for c in cells:
    for ip in xrange(len(nprocs)):
        sys.path.append("logs")
        log = __import__("%s_np%03d" % (c.lower(), nprocs[ip]))
        for e in events:
            total = 0.0
            eattr = e.replace(' ','_')
            for sube in log.__getattribute__(eattr).event.values():
                total += numpy.mean(sube.Time)
            data[c][e][ip] = total


figure = matplotlibext.Figure()
figure.open(3.0, 3.25, margins=[[0.6, 0, 0.1], [0.5, 0, 0.05]], dpi=150)
ax = figure.axes(1.35, 1, 1.35, 1)

for c in cells:
    for e in events:
        ax.loglog(nprocs, data[c][e], 
                  marker=symdict[c], 
                  color=styledict[e][0], 
                  linewidth=1,
                  dashes=styledict[e][1])
        ax.hold(True)

ax.set_xlim((1, 128))
ax.set_xlabel("# Processors", fontsize=10)

ax.set_ylim((0.01, 500))
ax.set_ylabel("Time (s)", fontsize=10)

import matplotlib.lines as lines
proxies = []
for c in cells:
    proxies.append(lines.Line2D((0,0),(1,1), 
                                marker=symdict[c], 
                                color=styledict['Solve'][0],
                                linewidth=0))
l1 = ax.legend(proxies, cells, 
          loc='lower left', bbox_to_anchor=(0,1.05), borderaxespad=0)

proxies = []
for e in events:
    proxies.append(lines.Line2D((0,0),(1,1), 
                                marker=None, 
                                color=styledict[e][0],
                                dashes=styledict[e][1]))
ax.legend(proxies, events, 
          loc='lower right', bbox_to_anchor=(1,1.05), borderaxespad=0)
ax.add_artist(l1)

pyplot.show()
pyplot.savefig('scaling.pdf')
