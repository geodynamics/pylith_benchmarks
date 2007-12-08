addpath('../../okada');
scenario = 'tet4_0250m';

in = sprintf('../analytic/output/%s_points.in', scenario);
out = sprintf('../analytic/output/%s_points.disp', scenario);

StrikeSlip_ng(in, out);
