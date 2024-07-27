clear;

load("Data\lambdaResponse.mat")

PVx = (readings{:, "angleX"})';
PVy = (readings{:, "angleY"})';

OPx = (readings{:, "PID_X"} * 10)';
OPy = (readings{:, "PID_Y"} * 10)';

t = 1:length(PVx);

% full scale experiment

figure(1)
clf
ax11 = subplot(2,1,1);
ax12 = subplot(2,1,2);

title(ax11, "X axis step response experiment. \Deltat=0,01s")
title(ax12, "Y axis step response experiment. \Deltat=0,01s")

grid(ax11, "on")
grid(ax12, "on")

hold(ax11,"on")
hold(ax12,"on")

stairs(ax11, t, OPx)
plot(ax11, t, PVx)

stairs(ax12, t, OPy)
plot(ax12, t, PVy)

% X detailed plots

xlr = 480:600;
ylr = 180:300;

figure(2)
clf
ax21 = subplot(2,1,1);
ax22 = subplot(2,1,2);


title(ax21, "X axis lambda test. \Deltat=0,01s")
title(ax22, "Y axis lambda test. \Deltat=0,01s")

grid(ax21, "on")
grid(ax22, "on")

hold(ax21,"on")
hold(ax22,"on")


stairs(ax21, xlr, OPx(xlr))
plot(ax21, xlr, PVx(xlr))

stairs(ax22, ylr, OPy(ylr))
plot(ax22, ylr, PVy(ylr))


% Calculation parameters:
dT = 0.01; %s

deltaOUT = 4 - (-1);


% X axis lambda test results:
xInitSlope = (PVx(540) - PVx(520)) / (20 * dT)
xFinalSlope = (PVx(580) - PVx(550)) / (30 * dT)

xDeadTime = 2*dT;
xLagTime = 7*dT;

xKpi = (xFinalSlope - xInitSlope) / deltaOUT

% Y axis lambda test results:
yInitSlope = (PVy(240) - PVy(220)) / (20 * dT)
yFinalSlope = (PVy(280) - PVy(255)) / (25 * dT)

yDeadTime = 4*dT;
yLagTime = 4*dT;

yKpi = (yFinalSlope - yInitSlope) / deltaOUT

% Calculate lambda pid parameters:

disp("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
xLmbd = 1.5 * xLagTime
yLmbd = 1.5 * yLagTime

disp("X parameters:")

xT_I = (2*xLmbd + xDeadTime);
xK_P = xT_I / xKpi / (xLmbd  + xDeadTime)

xK_I = 1 / xT_I
xT_D = xLagTime

disp("Y parameters:")

yT_I = (2*yLmbd + yDeadTime);
yK_P = yT_I / yKpi / (yLmbd  + yDeadTime)

yK_I = 1 / yT_I
yT_D = yLagTime