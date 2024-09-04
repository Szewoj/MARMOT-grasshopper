clear;

load("Raw\lambdaResponse.mat")

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

% detailed plots

xlr = 480:600;
ylr = 180:300;

Txlr = xlr * 0.01;
Tylr = ylr * 0.01;

figure(2)
clf
ax21 = subplot(2,1,1);
ax22 = subplot(2,1,2);


title(ax21, "Test lambda osi X. $\Delta t=0.01$s", 'Interpreter','latex')
title(ax22, "Test lambda osi Y. $\Delta t=0.01$s", 'Interpreter','latex')

grid(ax21, "on")
grid(ax22, "on")

hold(ax21,"on")
hold(ax22,"on")

stairs(ax21, Txlr, OPx(xlr))
stairs(ax21, Txlr, PVx(xlr))

stairs(ax22, Tylr, OPy(ylr))
stairs(ax22, Tylr, PVy(ylr))

xlabel(ax21, '$t$ $[s]$', 'Interpreter','latex');
xlabel(ax22, '$t$ $[s]$', 'Interpreter','latex');

ylabel(ax21, '$\varphi_x$ [mrad],\quad $\Delta u_x$ [\%]', 'Interpreter','latex')
ylabel(ax22, '$\varphi_y$ [mrad],\quad $\Delta u_y$ [\%]', 'Interpreter','latex');

axis(ax21, [Txlr(1), Txlr(end), min(PVx(xlr)) - 5, max(PVx(xlr)) + 5])
axis(ax22, [Tylr(1), Tylr(end), min(PVy(ylr)) - 5, max(PVy(ylr)) + 5])

legend(ax21, ["$\Delta u_x$", "$\varphi_x$"], 'Location','northwest', 'Interpreter','latex')
legend(ax22, ["$\Delta u_y$", "$\varphi_y$"], 'Location','northwest', 'Interpreter','latex')


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

xK_I = xK_P / xT_I
xT_D = xK_P * xLagTime

disp("Y parameters:")

yT_I = (2*yLmbd + yDeadTime);
yK_P = yT_I / yKpi / (yLmbd  + yDeadTime)

yK_I = yK_P / yT_I
yT_D = yK_P * yLagTime