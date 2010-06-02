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

style = {'colors': "lightbg"}

warpScale = 250.0

# ======================================================================
from enthought.mayavi.scripts.mayavi2 import MayaviApp as Mayavi
from enthought.tvtk.api import tvtk
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.mayavi.filters.warp_vector import WarpVector
from enthought.mayavi.filters.extract_vector_norm import ExtractVectorNorm
from enthought.mayavi.modules.surface import Surface
from enthought.mayavi.modules.glyph import Glyph
from enthought.mayavi.modules.text import Text


import numpy

import plot_utils

class PlotScene(Mayavi):

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def run(self):
    self._setup()

    surface = plot_utils.SurfaceData()
    data = surface.read("output/tri3_100m_refine_t04000.vtk")

    pngfile = "solution.png"

    self._renderScene(data)
    self._setCamera()
    scene = self.script.engine.current_scene.scene
    scene.disable_render = False
    scene.render()
    scene.save_png(pngfile)
    return
    

  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _setup(self):

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

    self.windowSize = (1024+15, 768+117)
    self.aaframes = 4

    return


  def _renderScene(self, data):

    script = self.script
    w = script.get_active_window()
    w.size = self.windowSize
    script.new_scene()
    scene = script.engine.current_scene.scene
    scene.disable_render = True
    scene.anti_aliasing_frames = self.aaframes
    scene.background = self.colorBg
    scene.foreground = self.colorFg

    script.add_source(VTKDataSource(data=data))
    objTop = script.engine.current_object
    script.engine.current_object.name = "fault"

    warp = WarpVector()
    warp.filter.scale_factor = warpScale
    script.add_filter(warp)

    surf = Surface()
    script.add_module(surf)

    colorbar = script.engine.current_object.module_manager.scalar_lut_manager
    colorbar.data_name = "Velocity (m/s)"
    colorbar.lut_mode = self.lut
    colorbar.reverse_lut = self.lutReverse
    colorbar.scalar_bar.label_format = "%4.2f"
    colorbar.scalar_bar.label_text_property.font_size = 18
    colorbar.scalar_bar.label_text_property.shadow = True
    colorbar.scalar_bar.label_text_property.italic = False
    colorbar.scalar_bar.title_text_property.italic = False
    colorbar.scalar_bar.title_text_property.shadow = True
    colorbar.show_scalar_bar = False
    colorbar.data_range = (0.0, 1.0)
    #colorbar.number_of_labels = 0

    colorbar.scalar_bar.orientation = "horizontal"
    scalar_bar = colorbar.scalar_bar_widget.representation
    scalar_bar.position2 = (0.33, 0.12)
    scalar_bar.position = (0.01, 0.02)

    surf = Surface()
    script.add_module(surf)

    

    return

  def _setCamera(self):
    import math

    script = self.script
    camera = self.script.engine.current_scene.scene.camera

    dist = 32.0e+3
    angle = 60.0

    clipRange = numpy.array( [5e+2, 500e+3] )
    ptTo = numpy.array( [-12e+3*math.cos(60/180.0*math.pi), -dist/2.0, 0] )
    ptFrom = ptTo + numpy.array( [0.0, 0.0, dist])      

    camera.view_up = (0.0, 1.0, 0.0)
    camera.view_angle = angle
    camera.focal_point = ptTo
    camera.position = ptFrom
    camera.clipping_range = clipRange
    #camera.parallel_projection = True
    #camera.parallel_scale = 0.5*118.125e+3

    camera.view_angle = angle
    camera.parallel_projection = False

    return


# ======================================================================
if __name__ == "__main__":

  app = PlotScene()
  app.main()


# End of file
