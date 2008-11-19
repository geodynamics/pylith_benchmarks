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
        'nflops': 1.012e+09,
        'run_time': 24.44,
        'error': 1.41e-03,
        'niterations': 60,
        'memory': 233.9},

    "Hex8 1000m": {
        'ncells': 13824,
        'nvertices': 15625,
        'nflops': 1.977e+09,
        'run_time': 12.98,
        'error': 6.58e-04,
        'niterations': 38,
        'memory': 229.1},

    "Tet4 500m": {
        'ncells': 661929,
        'nvertices': 117649,
        'nflops': 1.342e+10,
        'run_time': 216.8,
        'error': 4.79e-04,
        'niterations': 111,
        'memory': 1709.0},

    "Hex8 500m": {
        'ncells': 110592,
        'nvertices': 117649,
        'nflops': 2.165e+10,
        'run_time': 113.5,
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
    [{'nprocs': 1, 'total': 216.77, 'compute': 73.91},
     {'nprocs': 2, 'total': 330.35, 'compute': 48.58},
     {'nprocs': 4, 'total': 262.85, 'compute': 29.16},
     {'nprocs': 8, 'total': 229.57, 'compute': 17.78},
     {'nprocs': 16, 'total': 222.19, 'compute': 11.89},
     ],
    
    "Hex8":
     [{'nprocs': 1, 'total': 113.39, 'compute': 54.12},
      {'nprocs': 2, 'total': 124.16, 'compute': 49.21},
      {'nprocs': 4, 'total': 93.54, 'compute': 28.17},
      {'nprocs': 8, 'total': 80.62, 'compute': 16.69},
      {'nprocs': 16, 'total': 71.31, 'compute': 10.41},
      ]
    }
