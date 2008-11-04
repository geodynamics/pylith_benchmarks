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

# ----------------------------------------------------------------------
# Version 1.1
# ----------------------------------------------------------------------
# Hydra (2.2 GHz Opteron)
data_v1_1 = {
    "Tet4 1000m": {
        'ncells': 79756,
        'nvertices': 15625,
        'nflops': 9.911e+08,
        'run_time': 42.0,
        'error': 1.41e-03,
        'niterations': 59,
        'memory': 340},

    "Hex8 1000m": {
        'ncells': 13824,
        'nvertices': 15625,
        'nflops': 1.97e+09,
        'run_time': 18.9,
        'error': 6.58e-04,
        'niterations': 38,
        'memory': 293},

    "Tet4 500m": {
        'ncells': 661929,
        'nvertices': 117649,
        'nflops': 1.293e+10,
        'run_time': 380.6,
        'error': 4.79e-04,
        'niterations': 107,
        'memory': 2514.6},

    "Hex8 500m": {
        'ncells': 110592,
        'nvertices': 117649,
        'nflops': 2.16e+10,
        'run_time': 165.5,
        'error': 1.94e-04,
        'niterations': 70,
        'memory': 2205.9},


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
        'error': 7.70e-05,
        'niterations': 0,
        'memory': 0.0}
    }

# Hydra (2.2 GHz Opteron)
dataScaling_v1_1 = {
    "Tet4":
    [{'nprocs': 1,
      'total': 380.6,
      'distribute': 0.0},
     {'nprocs': 2,
      'total': 613.0,
      'distribute': 339.4},
     {'nprocs': 4,
      'total': 523.4,
      'distribute': 316.3},
     {'nprocs': 8,
      'total': 508.4,
      'distribute': 317.5},
     {'nprocs': 16,
      'total': 487.8,
      'distribute': 310.0},
     ],
    "Hex8":
     [{'nprocs': 1,
       'total': 165.4,
       'distribute': 0.0},
      {'nprocs': 2,
       'total': 206.4,
       'distribute': 50.4},
      {'nprocs': 4,
       'total': 181.22,
       'distribute': 49.8},
      {'nprocs': 8,
       'total': 181.8,
       'distribute': 52.5},
      {'nprocs': 16,
       'total': 188.0,
       'distribute': 52.2},
      ]
    }

# ----------------------------------------------------------------------
# Version 1.3.1
# ----------------------------------------------------------------------
# Hydra (2.2 GHz Opteron)
data_v1_3 = {
    "Tet4 1000m": {
        'ncells': 79756,
        'nvertices': 15625,
        'nflops': 9.958e+08,
        'run_time': 26.51,
        'error': 1.41e-03,
        'niterations': 59,
        'memory': 234.1},

    "Hex8 1000m": {
        'ncells': 13824,
        'nvertices': 15625,
        'nflops': 1.977e+09,
        'run_time': 13.45,
        'error': 6.58e-04,
        'niterations': 38,
        'memory': 229},

    "Tet4 500m": {
        'ncells': 661929,
        'nvertices': 117649,
        'nflops': 1.297e+10,
        'run_time': 237.4,
        'error': 4.79e-04,
        'niterations': 107,
        'memory': 1709.0},

    "Hex8 500m": {
        'ncells': 110592,
        'nvertices': 117649,
        'nflops': 2.165e+10,
        'run_time': 120.7,
        'error': 1.94e-04,
        'niterations': 70,
        'memory': 1710.6},


    "Tet4 250m": {
        'ncells': 5244768,
        'nvertices': 912673,
        'nflops': 2.093e+11,
        'run_time': 2.355e+03,
        'error': 1.30e-04,
        'niterations': 228,
        'memory': 12000.0},

    "Hex8 250m" : {
        'ncells': 884736,
        'nvertices': 912673,
        'nflops': 2.521e+11,
        'run_time': 1.268e+03,
        'error': 7.70e-05,
        'niterations': 134,
        'memory': 12000.0}
    }

# Hydra (2.2 GHz Opteron)
dataScaling_v1_3 = {
    "Tet4":
    [{'nprocs': 1, 'total': 237.2, 'compute': 75.88},
     {'nprocs': 2, 'total': 398.2, 'compute': 56.14},
     {'nprocs': 4, 'total': 307.3, 'compute': 39.93},
     {'nprocs': 8, 'total': 252.9, 'compute': 16.50},
     {'nprocs': 16, 'total': 234.8, 'compute': 10.70},
     ],
    
    "Hex8":
     [{'nprocs': 1, 'total': 117.5, 'compute': 56.08},
      {'nprocs': 2, 'total': 174.5, 'compute': 46.63},
      {'nprocs': 4, 'total': 111.9, 'compute': 29.41},
      {'nprocs': 8, 'total': 86.3, 'compute': 16.01},
      {'nprocs': 16, 'total': 78.7, 'compute': 10.46},
      ]
    }
