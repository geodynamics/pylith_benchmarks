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

class PlotMesh(PlotScene):

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def run(self):    
    from enthought.mayavi.sources.vtk_data_source import VTKDataSource
    from enthought.mayavi.modules.surface import Surface

    self._setupScene(showFault=False, showMaterials=False)
    mesh = self._readMesh()

    script = self.script
    script.add_source(VTKDataSource(data=mesh))
    script.engine.current_object.name = "Mesh"

    surf = Surface()
    script.add_module(surf)
    
    surf = Surface()
    script.add_module(surf)
    
    import vtk_geometry
    vtk_geometry.setCamera(script.engine.current_scene.scene.camera)
    return


  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _readMesh(self):
    from enthought.tvtk.api import tvtk
    import tables
    import numpy

    filename = "../meshes/reverseslip_%s_%04dm.h5" % (shape, res)
    h5 = tables.openFile(filename, 'r')

    cells = h5.root.topology.cells[:]
    (ncells, ncorners) = cells.shape
    vertices = h5.root.geometry.vertices[:] / 1e+3
    (nvertices, spaceDim) = vertices.shape
    h5.close()
    
    if shape == "tet4":
        assert(spaceDim == 3)
        assert(ncorners == 4)
        cellType = tvtk.Tetra().cell_type
    else:
        raise ValueError("Unknown shape '%s'." % shape)

    data = tvtk.UnstructuredGrid()
    data.points = vertices
    data.set_cells(cellType, cells)
    return data


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotMesh()
  app.main()


# End of file

