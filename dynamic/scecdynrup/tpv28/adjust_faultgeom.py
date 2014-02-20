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

filenameEXO = "tet4_200m.exo"

# ======================================================================
import numpy
import netCDF4

from create_faultsurf import bump

exodus = netCDF4.Dataset(filenameEXO, 'a')
coordx = exodus.variables['coordx'][:]
coordy = exodus.variables['coordy'][:]
coordz = exodus.variables['coordz'][:]

nodesetNames = exodus.variables['ns_names']
for i in range(nodesetNames.shape[0]):
    if netCDF4.chartostring(nodesetNames[i,:]) == "fault":
        indices = exodus.variables['node_ns%d' % i][:]

faulty = coordy[indices]
faultz = coordz[indices]
faultx = bump(faulty, faultz)
coordx[indices] = faultx
exodus.variables['coordx'][:] = coordx

exodus.close()


# End of file
