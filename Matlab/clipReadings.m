%% Plot readings
clear;
file = "lambdaV1\b1.mat";

load("Raw\" + file);

dataLen = length(readings{:,"angleX"});

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

stairs(ax11, 1:dataLen, readings{:,"angleX"}, "Color", "#0072BD");
stairs(ax11, 1:dataLen, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");

stairs(ax12, 1:dataLen, readings{:,"angleY"}, "Color", "#D95319");
stairs(ax12, 1:dataLen, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");

stairs(ax13, 1:dataLen, readings{:,"velZ"}, "Color", "#77AC30");



%% Clip for save processed data

clipRange = 28:170;

data = readings(clipRange,:);

save("Data\" + file, "data");