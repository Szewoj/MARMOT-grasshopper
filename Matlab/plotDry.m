clear;

file = "dryRun\a2.mat";

load("Data\" + file);

dataLen = length(data{:,"angleX"});

timestamps = posixtime(data{:,"Time"});
timestamps = timestamps - timestamps(1);

% Figure - system measured values:

f1 = figure(1);
clf(f1)
f1.Position = [941,103,729,842];

subplot(3,1,1);
ax11 = gca;
subplot(3,1,2);
ax12 = gca;
subplot(3,1,3);
ax13 = gca;


title(ax11, '$\varphi_x$ (roll)', 'Interpreter','latex')
title(ax12, '$\varphi_y$ (pitch)', 'Interpreter','latex')
title(ax13, '$v_z$', 'Interpreter','latex')


xlabel(ax11, '$t$ [s]', 'Interpreter','latex')
xlabel(ax12, '$t$ [s]', 'Interpreter','latex')
xlabel(ax13, '$t$ [s]', 'Interpreter','latex')


ylabel(ax11, '$\varphi$ [mrad]', 'Interpreter','latex')
ylabel(ax12, '$\varphi$ [mrad]', 'Interpreter','latex')
ylabel(ax13, '$v$ [m/s]', 'Interpreter','latex')


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
stairs(ax13, timestamps, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");


axis(ax11, [timestamps(1), timestamps(end), min(data{:,"angleX"}) - 5, max(data{:,"angleX"}) + 5])
axis(ax12, [timestamps(1), timestamps(end), min(data{:,"angleY"}) - 5, max(data{:,"angleY"}) + 5])
axis(ax13, [timestamps(1), timestamps(end), min(data{:,"velZ"}) - 0.01, max(data{:,"velZ"}) + 0.01])
