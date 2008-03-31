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

shape = "hex8"
res = 1000
scaleFactor = 2.0

class PlotSoln(PlotScene):

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def run(self):    
    from enthought.mayavi.sources.vtk_data_source import VTKDataSource
    from enthought.mayavi.filters.warp_vector import WarpVector
    from enthought.mayavi.filters.extract_vector_norm import ExtractVectorNorm
    from enthought.mayavi.modules.surface import Surface
    from enthought.mayavi.modules.glyph import Glyph

    self._setupScene(showFault=False, showMaterials=False)
    data = self._readData()

    script = self.script
    script.add_source(VTKDataSource(data=data))
    script.engine.current_object.name = "Solution"

    warp = WarpVector()
    warp.filter.scale_factor = scaleFactor
    script.add_filter(warp)

    norm = ExtractVectorNorm()
    script.add_filter(norm)
    
    surf = Surface()
    script.add_module(surf)
    glyph = Glyph()
    script.add_module(glyph)
    glyph.actor.property.color = (1,1,1)
    glyph.actor.mapper.scalar_visibility = False
    glyph.glyph.glyph_position = 'tail'
    glyph.glyph.glyph.scale_factor = scaleFactor
    glyph.glyph.glyph_source = glyph.glyph.glyph_list[1]
    
    colorbar = script.engine.current_object.module_manager.scalar_lut_manager
    colorbar.show_scalar_bar = False
    colorbar.data_range = (0.0, 0.8)
    colorbar.number_of_labels = 5
    colorbar.scalar_bar.label_format = "%3.1f"
    w,h = colorbar.scalar_bar.position2
    colorbar.scalar_bar.position2 = (w, 0.1)
    colorbar.data_name = "Displacement [m]"
    
    import vtk_geometry
    vtk_geometry.setCamera(script.engine.current_scene.scene.camera)
    return


  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _readData(self):
    from enthought.tvtk.api import tvtk
    import tables
    import numpy

    filename = "../results/reverseslip_%s_%04dm.h5" % (shape, res)
    h5 = tables.openFile(filename, 'r')

    cells = h5.root.topology.cells[:]
    (ncells, ncorners) = cells.shape
    vertices = h5.root.geometry.vertices[:] / 1e+3
    (nvertices, spaceDim) = vertices.shape
    disp = h5.root.solution.snapshot0.displacements[:]
    h5.close()
    
    if shape == "tet4":
        assert(spaceDim == 3)
        assert(ncorners == 4)
        cellType = tvtk.Tetra().cell_type
    elif shape == "hex8":
        assert(spaceDim == 3)
        assert(ncorners == 8)
        cellType = tvtk.Hexahedron().cell_type
    else:
        raise ValueError("Unknown shape '%s'." % shape)

    data = tvtk.UnstructuredGrid()
    data.points = vertices
    data.set_cells(cellType, cells)
    data.point_data.vectors = disp
    data.point_data.vectors.name = "Displacement [m]"
    return data


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotSoln()
  app.main()


# End of file

