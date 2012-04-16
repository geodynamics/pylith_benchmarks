#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# Plot initial stress and slip profiles.
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

header = 0.45
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
figure.open(6.75, 4.5, margins=[[0.45, 0.2, 0.1], [0.35, 0.6, 0.1]], dpi=150)

locs = [(-9.0, 0.0), (0.0, 0.0), (9.0, 0.0),
        (-9.0, 9.0), (0.0, 9.0), (9.0, 9.0)]

nrows = 2
ncols = 3

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
    
iloc = 0
for irow in xrange(nrows):
    for icol in xrange(ncols):
        ax = figure.axes(nrows+header, ncols, irow+1+header, icol+1)
    
        isim = 0
        for (label, simdir) in simdirs:
            filename = "%s/faultst%+04ddp%03d.dat" % \
                (simdir, int(locs[iloc][0]*10), int(locs[iloc][1]*10))
            data = numpy.loadtxt(filename, comments="#", usecols=(0,2),
                                 converters={0: getval,
                                             2: getval})
            if isim != len(simdirs)-1:
                style = lineStyle[isim]
            else:
                style = lineStyle[len(lineStyle)-1]
            ax.plot(data[:,0], data[:,1], color=style[0],
                    linewidth=1,
                    dashes=style[1],
                    label=label)
            ax.hold(True)
            isim += 1
    
        ax.set_xlim((0.0, 10.5))
        ax.set_xlabel("Time (s)")
        if irow == 0:
            ax.set_ylim((0.0, 10.0))
            ymin0, ymax0 = ax.get_ylim()
        else:
            ax.set_ylim((0.0, 5.0))

        if icol == 0:
            ymin, ymax = ax.get_ylim()
            ax.text(-1.5, (ymax0+2.2)/ymax0*ymax, 
                     "%3.1f km Down Dip" % locs[iloc][1],
                     fontweight='bold', 
                     horizontalalignment='left')
            

        ax.set_ylabel("Slip Rate (m/s)")

        ax.set_title("%3.1f km Along Strike" % locs[iloc][0],
                 fontweight='bold', 
                 horizontalalignment='center')
    
        if irow == 0 and icol == ncols-1:
            ax.legend(loc="lower right",
                      bbox_to_anchor=(1,1.3), 
                      borderaxespad=0)
    
        if irow+1 < nrows:
            ax.set_xticklabels([])
            ax.set_xlabel("")
        if icol > 0:
            ax.set_yticklabels([])
            ax.set_ylabel("")
    
        iloc += 1

pyplot.show()
pyplot.savefig("%s_sliprate" % (sim))


# End of file
