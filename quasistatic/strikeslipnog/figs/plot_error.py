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
res = 500
showSlice = True

class PlotError(PlotScene):

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def run(self):    
    from enthought.mayavi.sources.vtk_data_source import VTKDataSource
    from enthought.mayavi.filters.threshold import Threshold
    from enthought.mayavi.modules.surface import Surface
    from enthought.mayavi.modules.scalar_cut_plane import ScalarCutPlane

    self._setupScene()
    data = self._readData()

    script = self.script
    script.add_source(VTKDataSource(data=data))
    script.engine.current_object.name = "Error"

    threshold = Threshold()
    script.add_filter(threshold)
    threshold.lower_threshold = -3.5
    
    surf = Surface()
    script.add_filter(surf)
    if showSlice:
      surf.actor.property.opacity = 0.2
      slice = ScalarCutPlane()
      script.add_module(slice)
      slice.implicit_plane.origin = (12.0, 12.0, -12.0)
      slice.implicit_plane.normal = (0, -1.0, 0.0)

    colorbar = script.engine.current_object.module_manager.scalar_lut_manager
    colorbar.show_scalar_bar = True
    colorbar.data_range = (-3.5, -2.0)
    colorbar.number_of_labels = 7
    colorbar.scalar_bar.label_format = "%-4.2f"

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
