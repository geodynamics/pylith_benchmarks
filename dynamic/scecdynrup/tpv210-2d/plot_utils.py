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

from pylith.utils.VTKDataReader import VTKDataReader

from enthought.tvtk.api import tvtk
import numpy

# ----------------------------------------------------------------------
class SurfaceData(object):

  def __init__(self):
    return


  def read(self, filename):

    reader = VTKDataReader()
    data = reader.read(filename)

    cells = data['cells']
    vertices = data['vertices']

    (ncells, ncorners) = cells.shape
    (nvertices, spaceDim) = vertices.shape
    
    vtkData = tvtk.UnstructuredGrid()
    vtkData.points = vertices
    assert(spaceDim == 3)
    assert(ncorners == 3)
    cellType = tvtk.Triangle().cell_type

    vtkData.set_cells(cellType, cells)


    # Displacement vector
    displacement = data['vertex_fields']['displacement']
    array = tvtk.FloatArray()
    array.from_array(displacement.squeeze())
    array.name = "Displacement (m)"
    vtkData.point_data.vectors = array
    vtkData.point_data.vectors.name = "Displacement (m)"

    # Compute velocity magnitude
    velocity = data['vertex_fields']['velocity']
    velocityLog = ((velocity[:,0]**2 + 
                    velocity[:,1]**2 + 
                    velocity[:,2]**2)**0.5)
    array = tvtk.FloatArray()
    array.from_array(velocityLog.squeeze())
    array.name = "Velocity (m/s)"
    vtkData.point_data.scalars = array
    vtkData.point_data.scalars.name = "Velocity (m/s)"

    return vtkData


# End of file
