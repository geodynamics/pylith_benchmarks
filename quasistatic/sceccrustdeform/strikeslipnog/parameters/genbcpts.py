#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# <LicenseText>
#
# ----------------------------------------------------------------------
#

dx = 250.0
faces = [
    {'label': "ypos",
     'xrange': [0.0, 24.0e+3],
     'yrange': [24.0e+3, 24.0e+3],
     'zrange': [-24e+3, 0.0]},
    {'label': "xpos",
     'xrange': [24.0e+3, 24.0e+3],
     'yrange': [0.0, 24.0e+3],
     'zrange': [-24.0e+3, 0.0]},
    {'label': "xneg",
     'xrange': [0.0, 0.0],
     'yrange': [0.0, 24.0e+3],
     'zrange': [-24.0e+3, 0.0]},
    {'label': "zneg",
     'xrange': [0.0, 24.0e+3],
     'yrange': [0.0, 24.0e+3],
     'zrange': [-24.0e+3, -24.0e+3]}
    ]

for face in faces:
    fout = open("bcpts_%s.in" % face['label'], "w")
    numX = int(1 + (face['xrange'][1] - face['xrange'][0])/dx)
    numY = int(1 + (face['yrange'][1] - face['yrange'][0])/dx)
    numZ = int(1 + (face['zrange'][1] - face['zrange'][0])/dx)
    for iX in xrange(numX):
        x = face['xrange'][0] + iX*dx
        for iY in xrange(numY):
            y = face['yrange'][0] + iY*dx
            for iZ in xrange(numZ):
                z = face['zrange'][0] + iZ*dx
                fout.write("%12.4e %12.4e %12.4e\n" % (x, y, z))
    fout.close()
                           

# End of file 
