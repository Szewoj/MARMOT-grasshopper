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

x_MSE  = data{:,"angleX"}' * data{:,"angleX"} / dataLen;
y_MSE  = data{:,"angleY"}' * data{:,"angleY"} / dataLen;
vZ_MSE = data{:,"velZ"}' * data{:,"velZ"} / dataLen;

%   median absolute deviation: (x, y, vZ)

x_MAD  = median(abs(data{:,"angleX"}));
y_MAD  = median(abs(data{:,"angleY"}));
vZ_MAD = median(abs(data{:,"velZ"}));

%   mean absolute error: (x, y, vZ)

x_MAE  = mean(abs(data{:,"angleX"}));
y_MAE  = mean(abs(data{:,"angleY"}));
vZ_MAE = mean(abs(data{:,"velZ"}));

%   mean and deviation: (x, y, vZ)

x_m = mean(data{:,"angleX"});
x_std = std(data{:,"angleX"});

y_m = mean(data{:,"angleY"});
y_std = std(data{:,"angleY"});

vZ_m = mean(data{:,"velZ"});
vZ_std = std(data{:,"velZ"});

%   x and y derivative:

dt = timestamps(2:end) - timestamps(1:end-1);

dx = (data{2:end,"angleX"} - data{1:end-1,"angleX"}) ./ dt;
dy = (data{2:end,"angleY"} - data{1:end-1,"angleY"}) ./ dt;

%       MSE: (dx, dy)

dx_MSE = dx'*dx / (dataLen-1);
dy_MSE = dy'*dy / (dataLen-1);

%       MAD: (dx, dy)

dx_MAD = median(abs(dx));
dy_MAD = median(abs(dy));

%       MAE: (dx, dy)

dx_MAE  = mean(abs(dx));
dy_MAE  = mean(abs(dy));

%       mean and std: (dx, dy)

dx_m = mean(dx);
dx_std = std(dx);

dy_m = mean(dy);
dy_std = std(dy);
