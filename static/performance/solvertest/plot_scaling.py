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

header = 0.25 

nprocs = [1,2,4,8,16,32,64]
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
    for s in stages:
        data[c][s] = numpy.zeros(len(nprocs), dtype=numpy.float32)

# Get stats
niters = {}
for c in cells:
    niters[c] = numpy.zeros(len(nprocs), dtype=numpy.float32)
    for ip in xrange(len(nprocs)):
        sys.path.append("logs")
        log = __import__("%s_np%03d" % (c.lower(), nprocs[ip]))
        niters[c][ip] = log.Solve.event['VecMDot'].Count[0]
        for s in stages:
            
            total = 0.0
            sattr = s.replace(' ','_')
            assert(nprocs[ip] == log.__getattribute__('Nproc'))
            data[c][s][ip] = log.__getattribute__(sattr).time / nprocs[ip]

figure = matplotlibext.Figure()
figure.open(3.0, 5.25, margins=[[0.6, 0, 0.1], [0.5, 0.4, 0.05]], dpi=150)

ax = figure.axes(2.0+header, 1, 1.0+header, 1)

for c in cells:
    for s in stages:
        ax.loglog(nprocs, data[c][s], 
                  marker=symdict[c], 
                  color=styledict[s][0], 
                  linewidth=1,
                  dashes=styledict[s][1])
        ax.hold(True)
        if s == 'Solve':
            ax.loglog(nprocs, data[c][s]/(niters[c]/niters[c][0]), 
                      marker=symdict[c], 
                      color='gray',
                      linewidth=1,
                      dashes=styledict[s][1])

ax.set_xlim((1, 128))
#ax.set_xlabel("# Processors", fontsize=10)

ax.set_ylim((0.01, 200))
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
for s in stages:
    proxies.append(lines.Line2D((0,0),(1,1), 
                                marker=None, 
                                color=styledict[s][0],
                                dashes=styledict[s][1]))
ax.legend(proxies, stages, 
          loc='lower right', bbox_to_anchor=(1,1.05), borderaxespad=0)
ax.add_artist(l1)

ax = figure.axes(2.0+header, 1, 2.0+header, 1)

for c in cells:
    ax.semilogx(nprocs, niters[c], 
            marker=symdict[c], 
            color='red', 
            linewidth=1)
    ax.hold(True)

ax.set_xlim((1, 128))
ax.set_xlabel("# Processors", fontsize=10)

ax.set_ylim((0, 150))
ax.set_ylabel("# Iterations", fontsize=10)


pyplot.show()
pyplot.savefig('scaling.pdf')
