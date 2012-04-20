#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# Plot slip rate time histories.
#
# PREREQUISITES: matplotlib, numpy

sim = "tpv16"

# ----------------------------------------------------------------------
import tables
import numpy
import matplotlib.pyplot as pyplot
import sys

sys.path.append("../../../figures")
import matplotlibext

header = 0.38
lineStyle = [("red", (2.0, 1.0)),
             ("blue", (4.0, 1.0)),
             ("purple", (6.0, 1.0)),
             ("green", (3.0, 1.0, 1.5, 1.0)),
             ("orange", (6.0, 1.0, 1.5, 1.0)),
             ("black", (None, None)),
             ]

# ----------------------------------------------------------------------
def getval(v):
    try:
        d = float(v)
    except ValueError:
        d = None
    return d

# ----------------------------------------------------------------------
figure = matplotlibext.Figure()
figure.open(4.5, 4.5, margins=[[0.55, 0.2, 0.1], [0.35, 0.6, 0.1]], dpi=150)

locs = [(-6.0, -9.0), (+6.0, 0.0)]

nrows = 2
ncols = 2

cell = "tet4"
dx = 75
simdirs = []
modelers = [('Barall', "barall"),
            ('Kaneko', "kaneko"),
            ('PyLith', "tet4"),
            ]
for (label,modeler) in modelers:
    d = "scecfiles/%s_%s_%03dm" % (sim,modeler,dx)
    simdirs.append((label, d))

labels = ["Fault Parallel Component",
          "Fault Normal Component"]
    
for irow in xrange(nrows):
    iloc = irow

    isim = 0
    for (label, simdir) in simdirs:
        filename = "%s/body%+04dst%+04ddp000.dat" % \
            (simdir, int(locs[iloc][0]*10), int(locs[iloc][1]*10))
        data = numpy.loadtxt(filename, comments="#", usecols=(0,2,6),
                             converters={0: getval,
                                         2: getval,
                                         6: getval})

        for icol in xrange(ncols):
            ax = figure.axes(nrows+header, ncols, irow+1+header, icol+1)
            if isim != len(simdirs)-1:
                style = lineStyle[isim]
            else:
                style = lineStyle[len(lineStyle)-1]
            ax.plot(data[:,0], data[:,icol+1], color=style[0],
                        linewidth=1,
                        dashes=style[1],
                        label=label)
            ax.hold(True)
    
            ax.set_xlim((0.0, 15.0))
            ax.set_xlabel("Time (s)")
            ax.set_ylim((-0.4, 0.45))
            ax.set_ylabel("Velocity (m/s)")

            if irow == 0:
                ax.set_title(labels[icol])

            if icol == 0:
                ax.text(-4.0, 0.7, 
                         "%3.1f km From Fault, %3.1f Along Strike" % locs[iloc],
                         fontweight='bold', 
                         horizontalalignment='left')
    
            if irow == 0 and icol == ncols-1:
                ax.legend(loc="lower right",
                          bbox_to_anchor=(1,1.2), 
                          borderaxespad=0)
    
            if irow+1 < nrows:
                ax.set_xticklabels([])
                ax.set_xlabel("")
            if icol > 0:
                ax.set_yticklabels([])
                ax.set_ylabel("")

        isim += 1
    
pyplot.show()
pyplot.savefig("%s_velth" % (sim))


# End of file
