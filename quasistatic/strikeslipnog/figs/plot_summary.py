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

# Hydra (2.2 GHz Opteron)
data = {
    "Tet4 1000m": {
        'ncells': 79756,
        'nvertices': 15625,
        'nflops': 1.01e+09,
        'run_time': 35.8,
        'error': 1.41e-03,
        'niterations': 60,
        'memory': 313},

    "Hex8 1000m": {
        'ncells': 13824,
        'nvertices': 15625,
        'nflops': 1.95e+09,
        'run_time': 15.9,
        'error': 6.58e-04,
        'niterations': 37,
        'memory': 185},

    "Tet4 500m": {
        'ncells': 661929,
        'nvertices': 117649,
        'nflops': 1.28e+10,
        'run_time': 377.0,
        'error': 4.79e-04,
        'niterations': 106,
        'memory': 2400.0},

    "Hex8 500m": {
        'ncells': 110592,
        'nvertices': 117649,
        'nflops': 2.12e+10,
        'run_time': 154.0,
        'error': 1.94e-04,
        'niterations': 68,
        'memory': 2100.0},


    "Tet4 250m": {
        'ncells': 5244768,
        'nvertices': 912673,
        'nflops': 0.0,
        'run_time': 0.0,
        'error': 1.30e-04,
        'niterations': 0,
        'memory': 0.0},

    "Hex8 250m" : {
        'ncells': 884736,
        'nvertices': 912673,
        'nflops': 0.0,
        'run_time': 0.0,
        'error': 0.0,
        'niterations': 0,
        'memory': 0.0}
    }


class PlotSummary(object):

    def __init__(self):
        return

    def main(self):

        self._setup()

        plots = [{'value': "nvertices",
                  'title': "# Vertices",
                  'log': True,
                  'range': None},
                 {'value': "ncells",
                  'title': "# Cells",
                  'log': True,
                  'range': None},
                 {'value': "memory",
                  'title': "Peak Memory Usage (MB)",
                  'log': True,
                  'range': (1e+1, 1e+4)},
                 {'value': "niterations",
                  'title': "# Iterations in Solve",
                  'log': False,
                  'range': None},
                 {'value': "run_time",
                  'title': "Run Time (s)",
                  'log': True,
                  'range': (1e+1, 1e+3)},
                 {'value': "nflops",
                  'title': "# FLOPS",
                  'log': True,
                  'range': (1e+8, 1e+11)},
                 {'value': "error",
                  'title': "Average Error (m)",
                  'log': True,
                  'range': (1e-5, 1e-2)}]
        iplot = 1
        for plot in plots:
            pylab.subplot(self.nrows, self.ncols, iplot)
            offset = 0
            handles = []
            for shape in self.shapes:
                format = shape + " " + "%dm"
                keys = [format % res for res in self.resolutions]
                d = [data[key][plot['value']] for key in keys]
                h = pylab.bar(self.loc0+offset*self.width, d,
                              self.width,
                              log=plot['log'],
                              color=self.colorShapes[shape])
                handles.append(h)
                offset += 1
            pylab.title(plot['title'],
                        fontsize=self.titleFontSize)
            pylab.xticks(self.locs, ["%sm" % res for res in self.resolutions],
                         fontsize=self.labelFontSize)
            pylab.yticks(fontsize=self.labelFontSize)
            if not plot['range'] is None:
                pylab.ylim(plot['range'])
            iplot += 1

        pylab.subplot(self.nrows, self.ncols, iplot)
        pylab.axis('off')
        pylab.legend((handles[0][0], handles[1][0]), self.shapes,
                     shadow=True,
                     loc='center')

        pylab.show()
        #pylab.savefig('benchmark_summary')
        return

    def _setup(self):
        figWidth = 9.25
        figHeight = 8.5
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

        self.nrows = 3
        self.ncols = 3

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
        pylab.subplots_adjust(left=0.04,
                              right=0.96,
                              bottom=0.03,
                              top=0.96,
                              wspace=0.22,
                              hspace=0.35)
        return


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotSummary()
  app.main()


# End of file

