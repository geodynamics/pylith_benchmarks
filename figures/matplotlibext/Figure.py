#!/usr/bin/env python
#
# ======================================================================
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ======================================================================
#

import matplotlib
import matplotlib.pyplot as pyplot

# ----------------------------------------------------------------------
class Figure:

  def __init__(self,
               color="lightbg",
               fontsize=8):
    """
    Constructor.
    """
    self.handle = None
    self.colorstyle = color
    self.defaults = {'figure.facecolor': 'bg',
                     'figure.edgecolor': 'fg',
                     'axes.facecolor': 'bg',
                     'axes.edgecolor': 'fg',
                     'axes.labelcolor': 'fg',
                     'axes.labelsize': fontsize,
                     'axes.titlesize': fontsize,
                     'font.size': fontsize,
                     'text.color': 'fg',
                     'legend.fontsize': fontsize,
                     'grid.color': 'fg',
                     'xtick.labelsize': fontsize,
                     'xtick.color': 'fg',
                     'ytick.labelsize': fontsize,
                     'ytick.color': 'fg',
                     'savefig.facecolor': 'bg',
                     'savefig.edgecolor': 'bg',
                     }
    return


  def open(self, width, height, margins=((0.5,0.5,0.1),(0.5,0.5,0.1)), dpi=90):
    """
    Open figure.
    """
    self._setup()
    for setting in self.defaults.items():
      matplotlib.rcParams[setting[0]] = setting[1]
    self.handle = pyplot.figure(figsize=(width, height),
                                facecolor='bg',
                                dpi=dpi)
    self.handle.set_facecolor('bg')
    self.margins = margins
    return


  def close(self):
    """
    Close figure.
    """
    self.handle.close()
    self.handle = None
    return


  def axes(self, nrows, ncols, row, col, hide=False):
    """
    Create subplot in figure.
    """
    h = self.handle.get_figheight()
    w = self.handle.get_figwidth()
    margins = self.margins
    marginLeft = margins[0][0]
    hsep = margins[0][1]
    marginRight = margins[0][2]
    marginBottom = margins[1][0]
    vsep = margins[1][1]
    marginTop = margins[1][2]
    plotW = (w-marginRight-marginLeft-hsep*(ncols-1))/float(ncols)
    plotH = (h-marginTop-marginBottom-vsep*(nrows-1))/float(nrows)

    left = (marginLeft+(col-1)*(plotW+hsep)) / w
    right = left + plotW/w
    bottom = (marginBottom+(nrows-row)*(plotH+vsep)) / h
    top = bottom + plotH / h
    #print "left: %.4f, right: %.4f, top: %.4f, bottom: %.4f, width: %.4f, height: %.4f" % \
    #      (left, right, top, bottom, plotW/w, plotH/h)
    axes = self.handle.add_axes([left, bottom, plotW/w, plotH/h])

    if hide:
      axes.set_frame_on(False)
      axes.set_axis_bgcolor(None)
      axes.set_xticks([])
      axes.set_yticks([])
      
    self._colorticks(axes)
    return axes


  def _setup(self):
    if self.colorstyle == "lightbg":
      fg = (0.0001, 0.0001, 0.0001)
      bg = (0.9999, 0.9999, 0.9999)
    elif self.colorstyle == "darkbg":
      fg = (0.9999, 0.9999, 0.9999)
      bg = (0.18, 0.21, 0.28)
    elif self.colorstyle == "blackbg":
      fg = (0.9999, 0.9999, 0.9999)
      bg = (0.0001, 0.0001, 0.0001)

      
    colors = {'fg': fg,
              'bg': bg,
              'dkgray': (0.25, 0.25, 0.25),
              'mdgray': (0.5, 0.5, 0.5),
              'ltgray': (0.75, 0.75, 0.75),
              'dkslate': (0.18, 0.21, 0.28),
              'slate': (0.45, 0.50, 0.68),
              'ltorange': (1.0, 0.74, 0.41),
              'orange': (0.96, 0.50, 0.0),
              'ltred': (1.0, 0.25, 0.25),
              'red': (0.79, 0.00, 0.01),
              'ltblue': (0.2, 0.73, 1.0),
              'blue': (0.12, 0.43, 0.59),
              'ltgreen': (0.37, 0.80, 0.05),
              'green': (0.23, 0.49, 0.03),
              'ltpurple': (0.81, 0.57, 1.0),
              'purple': (0.38, 0.00, 0.68)}
    from matplotlib.colors import colorConverter
    for key in colors.keys():
      colorConverter.colors[key] = colors[key]
    return


  def _colorticks(self, axes):
    ticklines = axes.get_xticklines()
    for tickline in ticklines:
      tickline.set_color('fg')
      ticklines = axes.get_yticklines()
    for tickline in ticklines:
      tickline.set_color('fg')
    return


# End of file
