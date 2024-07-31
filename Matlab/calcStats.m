clear;

% Load data:
file = "dryRun\a2.mat";

load("Data\" + file);

% Constants:

trailLen = 5.48; % m
dataLen = length(data{:,"angleX"});

timestamps = posixtime(data{:,"Time"});
timestamps = timestamps - timestamps(1);

speed = trailLen / timestamps(end);

% Figure 1 - system measured values:

f1 = figure(1);
clf(f1)
subplot(3,1,1);
ax11 = gca;
subplot(3,1,2);
ax12 = gca;
subplot(3,1,3);
ax13 = gca;

title(ax11, 'Angular position around X axis (roll)  [mrad]')
title(ax12, 'Angular position around Y axis (pitch) [mrad]')
title(ax13, 'Onboard Z axis velocity [m/s]')

grid(ax11, "on")
grid(ax12, "on")
grid(ax13, "on")

hold(ax11, "on")
hold(ax12, "on")
hold(ax13, "on")

stairs(ax11, timestamps, data{:,"angleX"}, "Color", "#0072BD");
stairs(ax11, timestamps, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");

stairs(ax12, timestamps, data{:,"angleY"}, "Color", "#D95319");
stairs(ax12, timestamps, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");

stairs(ax13, timestamps, data{:,"velZ"}, "Color", "#77AC30");

% Calc stats

%   MSE: (x, y, vZ)

%   MSD: (x, y, vZ)

%   mean and std: (x, y, vZ)

%   x and y derivative:

%       MSE: (dx, dy)

%       MSD: (dx, dy)

%       mean and std: (dx, dy)

