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

from plot_geometry import PlotScene

shape = "tet4"
res = 1000

class PlotError(PlotScene):

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def run(self):    
    from enthought.mayavi.sources.vtk_data_source import VTKDataSource
    from enthought.mayavi.filters.cell_to_point_data import CellToPointData
    from enthought.mayavi.modules.iso_surface import IsoSurface

    self._setupScene()
    data = self._readData()

    script = self.script
    script.add_source(VTKDataSource(data=data))
    script.engine.current_object.name = "Error"

    ptdata = CellToPointData()
    script.add_filter(ptdata)

    surf = IsoSurface()
    script.add_module(surf)
    
    return


  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _readData(self):
    from enthought.tvtk.api import tvtk
    import tables
    import numpy

    filename = "../projection/pylith_%s_%04dm.h5" % (shape, res)
    h5 = tables.openFile(filename, 'r')

    cells = h5.root.topology.cells[:]
    (ncells, ncorners) = cells.shape
    vertices = h5.root.geometry.vertices[:] / 1e+3
    (nvertices, spaceDim) = vertices.shape
    error = h5.root.difference.pylith_1_0_analytic.snapshot0.displacements[:]
    disp = h5.root.projection.data.pylith_1_0.snapshot0.displacements[:]
    dispE = h5.root.projection.data.analytic.snapshot0.displacements[:]
    h5.close()
    
    if shape == "tet4":
        assert(spaceDim == 3)
        assert(ncorners == 4)
        cellType = tvtk.Tetra().cell_type
    else:
        raise ValueError("Unknown shape '%s'." % shape)

    errorLog10 = numpy.log10(error)
    disp = numpy.reshape(disp, (ncells, spaceDim))

    data = tvtk.UnstructuredGrid()
    data.points = vertices
    data.set_cells(cellType, cells)
    data.cell_data.scalars = errorLog10
    data.cell_data.scalars.name = "log10(Error [m])"
    return data


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotError()
  app.main()


# End of file

