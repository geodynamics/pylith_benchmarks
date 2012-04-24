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

sim = "tpv13"
showAB = True

# ----------------------------------------------------------------------
import tables
import numpy
import matplotlib.pyplot as pyplot
import sys

sys.path.append("../../../figures")
import matplotlibext

header = 0.95 
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
figure.open(6.0, 6.25, margins=[[0.45, 0.2, 0.1], [0.35, 0.3, 0.1]], dpi=150)

locs = [0, 3.0, 7.5, 12.0]

nrows = len(locs)
ncols = 2
labelsAB = 'abcdefgh'


for icol in xrange(ncols):

    simdirs = []
    if icol == 0:
        labels = ["Quad4, 200m",
                  "Tri3, 200m",
                  "Quad4, 100m",
                  "Tri3 100m",
                  "Quad4, 50m",
                  "Tri3, 50m",
                  ]
        for dx in [200,100,50]:
            for cell in ["quad4", "tri3"]:
                label = "%s, %dm" % (cell.capitalize(), dx)
                d = "scecfiles/%s_%s_%03dm" % (sim,cell,dx)
                simdirs.append((label, d))
    else:
        cell = "tri3"
        dx = 100
        modelers = [('Andrews', "andrews"),
                    ('Barall', "barall"),
                    ('Dunham', "dunham"),
                    ('Ma', "ma"),
                    ('PyLith (Tri3)', "tri3"),
                    ]
        for (label,modeler) in modelers:
            d = "scecfiles/%s_%s_%03dm" % (sim,modeler,dx)
            simdirs.append((label, d))
    
    for irow in xrange(nrows):
        ax = figure.axes(nrows+header, ncols, irow+1+header, icol+1)
    
        isim = 0
        for (label, simdir) in simdirs:
            filename = "%s/faultst000dp%03d.dat" % (simdir, int(locs[irow]*10))
            data = numpy.loadtxt(filename, comments="#", usecols=(0,5),
                                 converters={0: getval,
                                             5: getval})
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

        ax.set_xlim((0.0, 8.0))
        ax.set_xlabel("Time (s)")
        ax.set_ylim((0, 16.0))
        ax.set_ylabel("Slip Rate (m/s)")
        if icol == 0:
            ax.text(0, 17, "%3.1f km Down Dip" % locs[irow],
                    fontweight='bold')

        if irow == 0:
            ax.legend(loc="lower right",
                      bbox_to_anchor=(1,1.25), 
                      borderaxespad=0)

        if irow+1 < nrows:
            ax.set_xticklabels([])
            ax.set_xlabel("")
        if icol > 0:
            ax.set_title("")
            ax.set_yticklabels([])
            ax.set_ylabel("")

        if showAB:
            ilabel = icol*nrows + irow
            ax.text(0.2, 14, "(%s)" % labelsAB[ilabel],
                    fontweight='bold')
            

pyplot.show()
pyplot.savefig("%s-2d_sliprate" % (sim))


# End of file
