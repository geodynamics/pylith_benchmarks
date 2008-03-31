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

from runstats import data

class PlotSummary(object):

    def __init__(self):
        return

    def main(self):

        self._setup()

        iplot = 1
        pylab.subplot(self.nrows, self.ncols, iplot)
        offset = 0
        handles = []
        for shape in self.shapes:
            format = shape + " " + "%dm"
            keys = [format % res for res in self.resolutions]
            err = [data[key]['error'] for key in keys]
            h = pylab.loglog(self.resolutions, err,
                             color=self.colorShapes[shape],
                             marker='+')
            handles.append(h)
            offset += 1
            pylab.title("Global Error versus Discretization Size",
                        fontsize=self.titleFontSize)
            pylab.xlabel("Discretization Size (m)",
                         fontsize=self.labelFontSize)
            pylab.ylabel("Global Error (m)",
                         fontsize=self.labelFontSize)
            pylab.xticks(fontsize=self.labelFontSize)
            pylab.yticks(fontsize=self.labelFontSize)
            pylab.xlim(1.0e+2, 2.0e+3)
            pylab.ylim(2.0e-5, 2.0e-3)
            iplot += 1

        pylab.legend((handles[0][0], handles[1][0]),
                     self.shapes,
                     shadow=True,
                     loc='upper left')

        pylab.show()
        pylab.savefig('benchmark_convergence')
        return

    def _setup(self):
        figWidth = 5.5
        figHeight = 5.0
        colors = {'fg': (0,0,0),
                  'bg': (1,1,1),
                  'dkgray': 0.25,
                  'mdgray': 0.5,
                  'ltgray': 0.75,
                  'dkslate': (0.18, 0.21, 0.28),
                  'slate': (0.45, 0.50, 0.68),
                  'ltorange': (1.0, 0.74, 0.41),
                  'orange': (0.96, 0.50, 0.0),
                  'ltred': (1.0, 0.25, 0.25),
                  'red': (0.79, 0.00, 0.01),
                  'ltblue': (0.2, 0.73, 1.0),
                  'blue': (0.12, 0.43, 0.59),
                  'green': (0.37, 0.80, 0.05),
                  'green': (0.23, 0.49, 0.03)}
        from matplotlib.colors import colorConverter
        for key in colors.keys():
            colorConverter.colors[key] = colors[key]
        self.titleFontSize = 18
        self.labelFontSize = 14

        self.nrows = 1
        self.ncols = 1

        self.resolutions = [1000, 500, 250]
        self.shapes = ["Tet4", "Hex8"]

        self.width = 1.0/(len(self.shapes)+1)
        self.locs = pylab.arange(len(self.resolutions))
        self.loc0 = self.locs - 0.5*len(self.shapes)*self.width

        self.colorShapes = {'Tet4': 'orange',
                            'Hex8': 'blue'}

        pylab.figure(figsize=(figWidth, figHeight),
                     facecolor='bg',
                     dpi=90)
        pylab.subplots_adjust(left=0.14,
                              right=0.96,
                              bottom=0.10,
                              top=0.91,
                              wspace=0.22,
                              hspace=0.35)
        return


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotSummary()
  app.main()


# End of file

