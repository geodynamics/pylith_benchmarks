#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
# Charles A. Williams, GNS Science
# Matthew G. Knepley, University of Chicago
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2014 University of California, Davis
#
# See COPYING for license information.
#
# ----------------------------------------------------------------------
#
# PREREQUISITES: numpy, spatialdata
#
# Create spatial variation of initial fault tractions for TPV28.

filename = "initial_tration.spatialdb"

# ----------------------------------------------------------------------
import numpy
from spatialdata.spatialdb.SimpleIOAscii import SimpleIOAscii
from spatialdata.geocoords.CSCart import CSCart

radiusOuter = 2.0e+3
radiusInner = 1.4e+3
dx = 100.0

y = numpy.arange(-radiusOuter, +radiusOuter+0.5*dx, dx)
numY = y.shape[0]

z = numpy.arange(-7500.0-radiusOuter, -7500+radiusOuter+0.5*dx, dx)
numZ = z.shape[0]

points = numpy.zeros((numY*numZ, 3), dtype=numpy.float64)
for iY in xrange(numY):
    points[:,0] = 0.0
    points[iY*numZ:(iY+1)*numZ,1] = y[iY]
    points[iY*numZ:(iY+1)*numZ,2] = z

r = (points[:,1]**2+(points[:,2]+7500.0)**2)**0.5
maskO = numpy.bitwise_and(r > radiusInner, r <= radiusOuter)
maskI = r <= radiusInner
tractionShearLL = maskO*-5.80*(1.0+numpy.cos(numpy.pi*(r-1400.0)/600.0)) + maskI*-11.60
tractionShearUD = 0*tractionShearLL
tractionNormal = 0*tractionShearLL

cs = CSCart()
cs._configure()
cs.initialize()

dataOut = {'points': points,
           'coordsys': cs,
           'data_dim': 1,
           'values': [{'name': 'traction-shear-leftlateral', 
                       'units': 'MPa',
                       'data': tractionShearLL},
                      {'name': 'traction-shear-updip', 
                       'units': 'MPa',
                       'data': tractionShearUD},
                      {'name': 'traction-normal', 
                       'units': 'MPa',
                       'data': tractionNormal},
                      ],
           }

writer = SimpleIOAscii()
writer.inventory.filename = "initial_traction.spatialdb"
writer._configure()
writer.write(dataOut)


# End of file
