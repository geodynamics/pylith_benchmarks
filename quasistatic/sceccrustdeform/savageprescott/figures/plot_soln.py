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

shape = "hex8"
scaleFactor = 5.0/40.0
t = 1900
pngfile = "savageprescott_soln.png"

style = {'colors': "lightbg",
         }

from enthought.mayavi.app import Mayavi
import vtk_geometry
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.mayavi.filters.warp_vector import WarpVector
from enthought.mayavi.filters.extract_vector_norm import ExtractVectorNorm
from enthought.mayavi.modules.surface import Surface
from enthought.mayavi.modules.outline import Outline
from enthought.mayavi.modules.axes import Axes
from enthought.mayavi.modules.surface import Surface

class PlotSoln(Mayavi):

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def run(self):    

    self._setup()

    self._renderScene()
    self._annotateScene()
    self._setCamera()
    scene = self.script.engine.current_scene.scene
    scene.disable_render = False
    scene.render()
    scene.save_png(pngfile)
    
    return

  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _setup(self):
    """
    Plot axes, fault surface, and materials.
    """

    dkslate = (47/255.0, 53/255.0, 72/255.0)
    ltblue = (51/255.0, 187/255.0, 255/255.0)
    ltred = (1.0, 0.25, 0.25)
    red = (1.0, 0.40, 0.40)
    ltyellow = (1.0, 1.0, 0.45)

    if style['colors'] == "darkbg":
      dkslate = (47/255.0, 53/255.0, 72/255.0)
      ltblue = (51/255.0, 187/255.0, 255/255.0)
      ltred = (1.0, 0.25, 0.25)
      self.colorFg = (1,1,1)
      self.colorBg = dkslate
      self.colorSurfTrace = red
      self.colorCities = ltyellow
    else:
      self.colorFg = (0,0,0)
      self.colorBg = (1,1,1)
      self.colorSurfTrace = (0,0,1)
      self.lut = "hot"
      self.lutReverse = True

    self.windowSize = (1600+16, 675+120)
    self.aaframes = 4

    return


  def _renderScene(self):

    script = self.script
    w = script.get_active_window()
    w.size = self.windowSize
    script.new_scene()
    scene = script.engine.current_scene.scene
    scene.disable_render = True
    scene.anti_aliasing_frames = self.aaframes
    scene.background = self.colorBg
    scene.foreground = self.colorFg


    script = self.script
    script.add_source(VTKDataSource(data=self._readData()))
    script.engine.current_object.name = "Solution"

    warp = WarpVector()
    warp.filter.scale_factor = scaleFactor
    script.add_filter(warp)

    norm = ExtractVectorNorm()
    script.add_filter(norm)
    
    surf = Surface()
    script.add_module(surf)

    wire = Surface()
    script.add_module(wire)
    wire.actor.actor.property.representation = "wireframe"
    wire.actor.actor.property.color = (0.0, 0.0, 0.0)
    wire.actor.mapper.scalar_visibility = False

    colorbar = script.engine.current_object.module_manager.scalar_lut_manager
    colorbar.scalar_bar.label_format = "%3.1f"
    colorbar.scalar_bar.label_text_property.font_size = 18
    colorbar.scalar_bar.label_text_property.shadow = True
    colorbar.scalar_bar.label_text_property.italic = False
    colorbar.scalar_bar.title_text_property.italic = False
    colorbar.scalar_bar.title_text_property.shadow = True
    colorbar.show_scalar_bar = True
    colorbar.data_range = (0.0, 18.0)
    colorbar.number_of_labels = 7
    w,h = colorbar.scalar_bar.position2
    colorbar.scalar_bar.position2 = (0.4, 0.11)
    colorbar.scalar_bar.position = (0.25, 0.02)
    colorbar.data_name = "Displacement [m]"

    return
    
  def _annotateScene(self):

    script = self.script
    
    # Domain (axes and outline)
    script.add_source(VTKDataSource(data=vtk_geometry.domain()))
    script.engine.current_object.name = "Domain"
    outline = Outline()
    script.add_module(outline)
    outline.actor.property.opacity = 0.2
    axes = Axes()
    axes.axes.x_label = "X"
    axes.axes.y_label = "Y"
    axes.axes.z_label = "Z"
    axes.axes.label_format = "%-0.1f"
    script.add_module(axes)

    return


  def _setCamera(self):
    script = self.script
    vtk_geometry.setCamera(script.engine.current_scene.scene.camera)
    return


  def _readData(self):
    from enthought.tvtk.api import tvtk
    import tables
    import numpy

    filename = "../results/spbm_%s_graded3_20km/spbm_%s_graded3_20km_t%04d.h5" % (shape, shape, t)
    h5 = tables.openFile(filename, 'r')

    cells = h5.root.topology.cells[:]
    (ncells, ncorners) = cells.shape
    vertices = h5.root.geometry.vertices[:] / (1e+3 * 40.0)
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

