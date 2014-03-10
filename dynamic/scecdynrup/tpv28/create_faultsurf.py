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
# PREREQUISITES: numpy, netCDF4

# Python script to create Exodus II mapped mesh of fault geometry for
# import into CUBIT.

# Filename for ExodusII file (output)
filenameEXO = "fault.exo"

# Geometry of simulation domain
domainLength = 64.0e+3
domainHeight = 32.0e+3
buffer = 1.5e+3 # Extend fault plane beyond domain

# Geometry of bump
bumpRadius = 3.0e+3
bumpAmplitude = 6.0e+2
bumpY = 10.5e+3
bumpZ = -7.5e+3
bumpDx = 5.0e+2

# ======================================================================
import os
import numpy

from cubit_io import write_exodus_file
from netCDF4 import Dataset

# ----------------------------------------------------------------------
def bump(y, z):
    r1 = ((y+bumpY)**2 + (z-bumpZ)**2)**0.5
    r2 = ((y-bumpY)**2 + (z-bumpZ)**2)**0.5
    mask1 = r1 <= 3.0e+3
    mask2 = r2 <= 3.0e+3
    npts = yz.shape[0]
    x = mask1*+0.5*bumpAmplitude*(1.0+numpy.cos(numpy.pi*r1/3.0e+3)) + \
        mask2*+0.5*bumpAmplitude*(1.0+numpy.cos(numpy.pi*r2/3.0e+3))
    return x


# ----------------------------------------------------------------------
y0 = -0.5*domainLength-buffer; y1 = -bumpY-bumpRadius; ny = int(1+(y1-y0)/(8.0*bumpDx))
yA = numpy.linspace(y0, y1, ny)
y0 = y1 + bumpDx; y1 = -bumpY+bumpRadius
yB = numpy.arange(y0, y1, bumpDx)

y0 = y1+bumpDx; y1 = +bumpY-bumpRadius; ny = int(1+(y1-y0)/(8.0*bumpDx))
yC = numpy.linspace(y0, y1, ny)
y0 = y1 + bumpDx; y1 = +bumpY+bumpRadius
yD = numpy.arange(y0, y1, bumpDx)

y0 = y1+bumpDx; y1 = +0.5*domainLength+buffer; ny = int(1+(y1-y0)/(8.0*bumpDx))
yE = numpy.linspace(y0, y1, ny)
y = numpy.hstack((yA, yB, yC, yD, yE))
numY = y.shape[0]

z0 = -domainHeight-buffer; z1 = bumpZ-bumpRadius; nz = (1+(z1-z0)/(8.0*bumpDx))
zA = numpy.linspace(z0, z1, nz)
zB = numpy.arange(z1+bumpDx, bumpZ+bumpRadius, bumpDx)

z0 = bumpZ+bumpRadius+bumpDx; z1 = +buffer; nz = int(1+(z1-z0)/(8.0*bumpDx))
zC = numpy.linspace(z0, z1, nz)
z = numpy.hstack((zA, zB, zC))
numZ = z.shape[0]

yz = numpy.zeros((numY*numZ, 2), dtype=numpy.float64)

for iY in xrange(numY):
    yz[iY*numZ:(iY+1)*numZ,1] = z
    yz[iY*numZ:(iY+1)*numZ,0] = y[iY]

x = bump(yz[:,0],yz[:,1])
vertices = numpy.zeros((numY*numZ,3), dtype=numpy.float64)
vertices[:,0] = x
vertices[:,1] = yz[:,0]
vertices[:,2] = yz[:,1]

cells = numpy.zeros(((numY-1)*(numZ-1),4), dtype=numpy.int32)

for iY in xrange(numY-1):
    for iZ in xrange(numZ-1):
        v0 = iY*numZ+iZ
        v1 = v0+1
        v2 = v1+numZ
        v3 = v0+numZ
        cells[iY*(numZ-1)+iZ,:] = [v0,v1,v2,v3]

write_exodus_file(filenameEXO, cells, vertices)


# End of file
