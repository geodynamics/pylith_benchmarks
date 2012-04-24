#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# Plot initial stress and slip profiles.
#
# PREREQUISITES: matplotlib, numpy, gmt

sim = "tpv13"
griddata = False
showAB = True

# ----------------------------------------------------------------------
import tables
import numpy
import matplotlib.pyplot as pyplot
import sys
import subprocess

sys.path.append("../../../figures")
import matplotlibext

header = 0.55
lineStyle = [("red", 'dashed'),
             ("blue", 'dashdot'), 
             ("orange", 'dotted'), 
             ("black", 'solid'),
             ]

labelsAB = 'ab'

# ----------------------------------------------------------------------
def getval(v):
    try:
        d = float(v)
    except ValueError:
        d = None
    return d

# ----------------------------------------------------------------------
figure = matplotlibext.Figure()
figure.open(6.0, 2.5, margins=[[0.4, 0.3, 0.1], [0.35, 0, 0.1]], dpi=150)

nrows = 1
ncols = 2

for icol in xrange(ncols):

    simdirs = []
    if icol == 0:
        labels = ["Tet4, 200m",
                  "Tet4 100m",
                  ]
        for dx in [200,100]:
            for cell in ["tet4"]:
                label = "%s, %dm" % (cell.capitalize(), dx)
                d = "scecfiles/%s_%s_%03dm" % (sim,cell,dx)
                simdirs.append((label, d))
    else:
        cell = "tri3"
        dx = 100
        modelers = [('Barall', "barall"),
                    ('Kaneko', "kaneko"),
                    ('Ma', "ma"),
                    ('PyLith', "tet4"),
                    ]
        for (label,modeler) in modelers:
            d = "scecfiles/%s_%s_%03dm" % (sim,modeler,dx)
            simdirs.append((label, d))
    
    for irow in xrange(nrows):
        ax = figure.axes(nrows+header, ncols, irow+1+header, icol+1)
    
        isim = 0
        labels = []
        lines = []
        for (label, simdir) in simdirs:
            if griddata:
                cmd = "awk '/^j/ {next}; { print $0 }' %s/ruptime.dat | triangulate -G%s/ruptime.grd -I100.0/100.0 -R-15.0e+3/+15.0e+3/0.0/15.0e+3 -Jx1.0 > /dev/null " % (simdir, simdir)
                subprocess.call(cmd, shell=True)
                cmd = "grd2xyz %s/ruptime.grd > %s/ruptime.txtgrd" % \
                (simdir, simdir)
                subprocess.call(cmd, shell=True)
            filename = "%s/ruptime.txtgrd" % (simdir)
            data = numpy.loadtxt(filename)

            data = numpy.reshape(data, (151, 301, 3))

            if isim != len(simdirs)-1:
                style = lineStyle[isim]
            else:
                style = lineStyle[len(lineStyle)-1]
            contours = ax.contour(data[:,:,0]/1.0e+3, data[:,:,1]/1e+3, data[:,:,2],
                                  levels=numpy.arange(0.0, 8.01, 0.5),
                                  colors=style[0],
                                  linewidths=1.0,
                                  linestyles=style[1])
            lines.append(contours.collections[0])
            ax.hold(True)
            labels.append(label)
            isim += 1

        ax.set_xlim((-15.0, +15.0))
        ax.set_xlabel("Dist. Along Strike (km)")
        ax.set_ylim((15.0, 0.0))
        ax.set_yticks(numpy.arange(0, 15.01, 5.0))
        ax.set_ylabel("Dist. Down Dip (km)")
        ax.set_aspect('equal')

        if irow == 0:
            ax.legend(lines, labels, loc="lower right",
                      bbox_to_anchor=(1,1.1), 
                      borderaxespad=0)

        if irow+1 < nrows:
            ax.set_xticklabels([])
            ax.set_xlabel("")
        if icol > 0:
            ax.set_title("")
            ax.set_yticklabels([])
            ax.set_ylabel("")

        if showAB:
            ilabel = icol
            ax.text(-15, -1, "(%s)" % labelsAB[ilabel],
                     fontweight='bold')

pyplot.show()
pyplot.savefig("%s_ruptime" % (sim))


# End of file
