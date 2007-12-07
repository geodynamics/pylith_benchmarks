#!/usr/bin/env python
#
# ======================================================================
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# {LicenseText}
#
# ======================================================================
#

from enthought.mayavi.sources.vtk_file_reader import VTKFileReader
import numpy
import tables

shape = "hex8"
res = 1000
t = 0.0
filenameIn = "strikeslip_%s_%04dm_t%0.6f.vtk" % (shape, res, t)
filenameOut = "strikeslip_%s_%04dm.h5" % (shape, res)

reader = VTKFileReader()
reader.initialize(filenameIn)
data = reader.outputs[0]
cellsVtk = data.get_cells().to_array()
if shape == "hex8":
    ncorners = 8
elif shape == "tet4":
    ncorners = 4
(size,) = cellsVtk.shape
ncells = size / (1+ncorners)
assert((1+ncorners)*ncells == size)
cellsVtk = numpy.reshape(cellsVtk, (ncells, 1+ncorners))[:,1:1+ncorners]
verticesVtk = data._get_points().to_array()
dispVtk = data._get_point_data()._get_vectors().to_array()

h5 = tables.openFile(filenameOut, "w")
h5.createGroup("/", "topology")
h5.createArray("/topology", "vertices", verticesVtk)
h5.createArray("/topology", "cells", cellsVtk)
h5.createGroup("/", "data")
h5.createArray("/data", "displacements", dispVtk)
h5.close()

# End of file

