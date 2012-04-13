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
import matplotlib.ticker as pyticker
import numpy
import sys
import os

sys.path.append("../../../figures")
import matplotlibext

header = 0.4 

symdict = {'Hex8': 's',
           'Tet4': '^',
           }
styledict = {'asm': ('orange', (3,1,1,1)),
             'fieldsplit_add': ('blue', (3,1.5)),
             'fieldsplit_mult': ('purple', (6,1.5)),
             'fieldsplit_mult_custompc': ('red', (None, None)),
             }
             
preconditioners = ['asm',
                   'fieldsplit_add',
                   'fieldsplit_mult',
                   'fieldsplit_mult_custompc',
                   ]
pclabels = ['ASM',
                   'AMG_add',
                   'AMG_mult',
                   'AMG_mult_custom',
                   ]
cells = ['Tet4',
         'Hex8',
         ]
problems = ['np001',
            'np002',
            'np004',
            ]
            
            

# Allocate storage for stats
niters = {}
for pc in preconditioners:
    niters[pc] = {}
    for c in cells:
        niters[pc][c] = numpy.zeros(len(problems), dtype=numpy.int32)

# Get stats
for pc in preconditioners:
    for c in cells:
        ip = 0
        for p in problems:
            sys.path.append("logs_output")
            log = __import__("%s_%s_%s" % (c.lower(), pc, p))
            niters[pc][c][ip] = log.Solve.event['VecMDot'].Count[0]
            ip += 1

problemsize = {'Tet4': numpy.array([178402, 352240, 701797]),
               'Hex8': numpy.array([178470, 351030, 690868])}


figure = matplotlibext.Figure()
figure.open(3.0, 3.25, margins=[[0.45, 0, 0.15], [0.42, 0, 0.05]], dpi=150)

ax = figure.axes(1.0+header, 1, 1.0+header, 1)

for pc in preconditioners:
    for c in cells:

        ax.semilogx(problemsize[c], niters[pc][c], 
                    marker=symdict[c], 
                    color=styledict[pc][0], 
                    linewidth=1,
                    dashes=styledict[pc][1])
        ax.hold(True)

ax.set_xlabel("Problem Size (# DOF)")

ax.set_ylim((0, 600))
ax.set_ylabel("# Iterations")

import matplotlib.lines as lines
proxies = []
for c in cells:
    proxies.append(lines.Line2D((0,0),(1,1), 
                                marker=symdict[c], 
                                color=styledict['asm'][0],
                                linewidth=0))
l1 = ax.legend(proxies, cells, 
          loc='lower left', bbox_to_anchor=(0,1.05), borderaxespad=0)

proxies = []
for pc in preconditioners:
    proxies.append(lines.Line2D((0,0),(1,1), 
                                marker=None, 
                                color=styledict[pc][0],
                                dashes=styledict[pc][1]))
ax.legend(proxies, pclabels, 
          loc='lower right', bbox_to_anchor=(1,1.05), borderaxespad=0)
ax.add_artist(l1)


pyplot.show()
pyplot.savefig('solvertest_pctest.eps')
