clear;

load("Data\StepResponse.mat")

PVx = (readings{:, "angleX"})';
PVy = (readings{:, "angleY"})';

OPx = (readings{:, "PID_X"}*10)';
OPy = (readings{:, "PID_Y"}*10)';

t = 1:length(PVx);

% full scale experiment

figure(1)
clf
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

xsr1 = 240:290;
xsr2 = 280:340;
xsr3 = 330:390;
xsr4 = 380:440;

figure(2)
clf
ax21 = subplot(2,2,1);
ax22 = subplot(2,2,2);
ax23 = subplot(2,2,3);
ax24 = subplot(2,2,4);

title(ax21, "X axis step response 1. \Deltat=0,04s")
title(ax22, "X axis step response 2. \Deltat=0,04s")
title(ax23, "X axis step response 3. \Deltat=0,04s")
title(ax24, "X axis step response 4. \Deltat=0,04s")

grid(ax21, "on")
grid(ax22, "on")
grid(ax23, "on")
grid(ax24, "on")

hold(ax21,"on")
hold(ax22,"on")
hold(ax23,"on")
hold(ax24,"on")


stairs(ax21, xsr1, OPx(xsr1))
plot(ax21, xsr1, PVx(xsr1))

stairs(ax22, xsr2, OPx(xsr2))
plot(ax22, xsr2, PVx(xsr2))

stairs(ax23, xsr3, OPx(xsr3))
plot(ax23, xsr3, PVx(xsr3))

stairs(ax24, xsr4, OPx(xsr4))
plot(ax24, xsr4, PVx(xsr4))


% Y detailed plots

ysr1 = 25:85;
ysr2 = 75:145;
ysr3 = 135:190;
ysr4 = 170:250;

figure(3)
clf
ax31 = subplot(2,2,1);
ax32 = subplot(2,2,2);
ax33 = subplot(2,2,3);
ax34 = subplot(2,2,4);

title(ax31, "Y axis step response 1. \Deltat=0,04s")
title(ax32, "Y axis step response 2. \Deltat=0,04s")
title(ax33, "Y axis step response 3. \Deltat=0,04s")
title(ax34, "Y axis step response 4. \Deltat=0,04s")

grid(ax31, "on")
grid(ax32, "on")
grid(ax33, "on")
grid(ax34, "on")

hold(ax31,"on")
hold(ax32,"on")
hold(ax33,"on")
hold(ax34,"on")


stairs(ax31, ysr1, OPy(ysr1))
plot(ax31, ysr1, PVy(ysr1))

stairs(ax32, ysr2, OPy(ysr2))
plot(ax32, ysr2, PVy(ysr2))

stairs(ax33, ysr3, OPy(ysr3))
plot(ax33, ysr3, PVy(ysr3))

stairs(ax34, ysr4, OPy(ysr4))
plot(ax34, ysr4, PVy(ysr4))

% Calculate relevant values:

stepAmp = 100;

xsrRate = mean([ ...
    (PVx(257)-PVx(253))/(257-253)/0.04, ...
    (PVx(303)-PVx(307))/(307-303)/0.04, ...
    (PVx(353)-PVx(357))/(357-353)/0.04, ...
    (PVx(407)-PVx(403))/(407-403)/0.04 ...
    ]);
xsrLag = 2 * 0.04;

ysrRate = mean([ ...
    (PVy(58)-PVy(53))/(58-53)/0.04, ...
    (PVy(103)-PVy(108))/(108-103)/0.04, ...
    (PVy(154)-PVy(157))/(157-154)/0.04, ...
    (PVy(208)-PVy(203))/(208-203)/0.04 ...
    ]);
ysrLag = 2 * 0.04;

% Calculate Ziegler-Nichols parameters:
disp("PI parameters:")

Kp = [0.9*stepAmp/(xsrLag*xsrRate), 0.9*stepAmp/(ysrLag*ysrRate)]
Ti = [Kp(1)*3.3*xsrLag, Kp(2)*3.3*ysrLag]
Ki = 1./Ti

disp("PID parameters:")

Kp = [1.2*stepAmp/(xsrLag*xsrRate), 1.2*stepAmp/(ysrLag*ysrRate)]

Ti = [Kp(1)*2*xsrLag, Kp(2)*2*ysrLag]
Ki = 1./Ti

Td = [Kp(1)*0.5*xsrLag, Kp(2)*0.5*ysrLag]


% Calculate cross-disturbance between axes:

diffsX = mean([ ...
    mean(PVx(60:90)) - mean(PVx(10:50)), ...
    mean(PVx(60:90)) - mean(PVx(110:150)), ...
    mean(PVx(110:150)) - mean(PVx(160:200)), ...
    mean(PVx(210:250)) - mean(PVx(160:200)), ...
    ]);

diffsY = mean([ ...
    mean(PVy(280:300)) - mean(PVy(230:250)), ...
    mean(PVy(280:300)) - mean(PVy(330:350)), ...
    0, ...
    0, ...
    ]);

qx = -diffsX/100;
qy = -diffsY/100;

Kcross = [...
    qx/(1-qx),...
    qy/(1-qy)
    ]