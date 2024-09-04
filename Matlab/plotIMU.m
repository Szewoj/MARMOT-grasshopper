
load('IMU\imuTest.mat')

timestamps = posixtime(readings{:,"Time"});
timestamps = timestamps - timestamps(1);

qmat = [readings{:,"Q_w"}, readings{:,"Q_i"}, readings{:,"Q_j"}, readings{:,"Q_k"}];
qs = quaternion(qmat);
rpys = quat2eul(qs,"ZYX");

roll = rpys(:,3);
pitch = rpys(:,2);

% Figure 1
f1 = figure(1);
clf(f1)

subplot(2,1,1);
ax11 = gca;
subplot(2,1,2);
ax12 = gca;

hold(ax11, 'on')
hold(ax12, 'on')
grid(ax11, 'on')
grid(ax12, 'on')


title(ax11, 'Pomiar prędkości obrotowej')
title(ax12, 'Pomiar przyspieszenia')

stairs(ax11, timestamps, readings{:,"GyroX"}, "Color", 'red');
stairs(ax11, timestamps, readings{:,"GyroY"}, "Color", 'blue');
stairs(ax11, timestamps, readings{:,"GyroZ"}, "Color", 'green');

stairs(ax12, timestamps, readings{:,"AccX"}, "Color", 'red');
stairs(ax12, timestamps, readings{:,"AccY"}, "Color", 'blue');
stairs(ax12, timestamps, readings{:,"AccZ"}, "Color", 'green');

grid(ax11, "on")
grid(ax12, "on")

legend(ax11, ["$\dot{\varphi}_X$", "$\dot{\varphi}_Y$", "$\dot{\varphi}_Z$"], 'Location','southwest', 'Interpreter','latex')
legend(ax12, ["$a_X$", "$a_Y$", "$a_Z$"], 'Location','southwest', 'Interpreter','latex')

xlabel(ax11, '$t$ $[s]$', 'Interpreter','latex');
xlabel(ax12, '$t$ $[s]$', 'Interpreter','latex');

ylabel(ax11,'$\dot{\varphi}$ $[^o/s]$', 'Interpreter','latex')
ylabel(ax12, '$a [g]$', 'Interpreter','latex');
% Figure 3

f3 = figure(3);
clf(f3)
ax3 = gca;

hold(ax3, 'on')
grid(ax3, 'on')

title(ax3, 'Obliczona orientacja')

stairs(ax3, timestamps, roll, "Color", 'red');
stairs(ax3, timestamps, pitch, "Color", 'blue');

grid(ax3, "on")

legend(ax3, ["roll", "pitch"], 'Location','northwest')

xlabel(ax3, '$t$ $[s]$', 'Interpreter','latex');
ylabel(ax3,'$\varphi$ $[rad]$', 'Interpreter','latex')