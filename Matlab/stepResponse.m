clear;

load("Data\StepResponse.mat")

PVx = (readings{:, "angleX"})';
PVy = (readings{:, "angleY"})';

OPx = (readings{:, "PID_X"}*10)';
OPy = (readings{:, "PID_Y"}*10)';

t = 1:length(PVx);

% full scale experiment

figure(1)
ax11 = subplot(2,1,1);
ax12 = subplot(2,1,2);

title(ax11, "X axis step response experiment. \Deltat=0,04s")
title(ax12, "Y axis step response experiment. \Deltat=0,04s")

grid(ax11, "on")
grid(ax12, "on")

hold(ax11,"on")
hold(ax12,"on")

stairs(ax11, t, OPx)
plot(ax11, t, PVx)

stairs(ax12, t, OPy)
plot(ax12, t, PVy)

% X detailed plots



% Y detailed plots