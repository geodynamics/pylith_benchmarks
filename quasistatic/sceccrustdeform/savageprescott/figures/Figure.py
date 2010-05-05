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

import pylab

# ----------------------------------------------------------------------
class Figure:

 def __init__(self,
              color="lightbg",
              style="hardcopy",
              fontsize=8,
              palette="blueorange"):
   """
   Constructor.
   """
   self.handle = None
   self.colorstyle = color
   self.defaults = {'figure.facecolor': 'bg',
                    'axes.facecolor': 'bg',
                    'axes.edgecolor': 'fg',
                    'axes.labelcolor': 'fg',
                    'axes.labelsize': fontsize,
                    'axes.titlesize': fontsize,
                    'xtick.color': 'fg',
                    'ytick.color': 'fg',
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


 def open(self, width, height, margins):
   """
   Open figure.
   """
   self._setup()
   for setting in self.defaults.items():
     pylab.rcParams[setting[0]] = setting[1]
   self.handle = pylab.figure(figsize=(width, height),
                              facecolor='bg',
                              dpi=90)
   self.handle.set_facecolor('bg')
   self.margins = margins
   return


 def close(self):
   """
   Close figure.
   """
   pylab.close(self.handle)
   self.handle = None
   return


 def subplot(self, nrows, ncols, row, col):
   """
   Create subplot in figure.
   """
   i = (row-1)*ncols+col
   h = pylab.subplot(nrows, ncols, (row-1)*ncols+col)
   return h


 def axes(self, nrows, ncols, row, col):
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
   axes = pylab.subplot(nrows, ncols, ncols*(row-1)+col)
   axes.set_position([left, bottom, plotW/w, plotH/h])
   return axes


 def _setup(self):
   if self.colorstyle == "lightbg":
     fg = (0.01, 0.01, 0.01)
     bg = (0.99, 0.99, 0.99)
   elif self.colorstyle == "darkbg":
     fg = (0.99, 0.99, 0.99)
     bg = (0.01, 0.01, 0.01)

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


# End of file
