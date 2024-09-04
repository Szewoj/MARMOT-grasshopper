clear;

file = "lambdaV1\b1.mat";

load("Data\" + file);

dataLen = length(data{:,"angleX"});

timestamps = posixtime(data{:,"Time"});
timestamps = timestamps - timestamps(1);

% Figure - system measured values:

f1 = figure(1);
clf(f1)
f1.Position = [941,103,943,842];

subplot(3,2,1);
ax11 = gca;
subplot(3,2,3);
ax12 = gca;
subplot(3,2,5);
ax13 = gca;

subplot(4,2,2);
ax14 = gca;
subplot(4,2,4);
ax15 = gca;
subplot(4,4,11);
ax16 = gca;
subplot(4,4,12);
ax17 = gca;
subplot(4,4,15);
ax18 = gca;
subplot(4,4,16);
ax19 = gca;


title(ax11, '$\varphi_x$ (roll)', 'Interpreter','latex')
title(ax12, '$\varphi_y$ (pitch)', 'Interpreter','latex')
title(ax13, '$v_z$', 'Interpreter','latex')

title(ax14, '$\Delta u_x$', 'Interpreter','latex')
title(ax15, '$\Delta u_y$', 'Interpreter','latex')

title(ax16, '$u_{FL}$', 'Interpreter','latex')
title(ax17, '$u_{FR}$', 'Interpreter','latex')
title(ax18, '$u_{BL}$', 'Interpreter','latex')
title(ax19, '$u_{BR}$', 'Interpreter','latex')

xlabel(ax11, '$t$ [s]', 'Interpreter','latex')
xlabel(ax12, '$t$ [s]', 'Interpreter','latex')
xlabel(ax13, '$t$ [s]', 'Interpreter','latex')
xlabel(ax14, '$t$ [s]', 'Interpreter','latex')
xlabel(ax15, '$t$ [s]', 'Interpreter','latex')
xlabel(ax16, '$t$ [s]', 'Interpreter','latex')
xlabel(ax17, '$t$ [s]', 'Interpreter','latex')
xlabel(ax18, '$t$ [s]', 'Interpreter','latex')
xlabel(ax19, '$t$ [s]', 'Interpreter','latex')

ylabel(ax11, '$\varphi$ [mrad]', 'Interpreter','latex')
ylabel(ax12, '$\varphi$ [mrad]', 'Interpreter','latex')
ylabel(ax13, '$v$ [m/s]', 'Interpreter','latex')
ylabel(ax14, '$\Delta u$ [\%]', 'Interpreter','latex')
ylabel(ax15, '$\Delta u$ [\%]', 'Interpreter','latex')
ylabel(ax16, '$u$ [\%]', 'Interpreter','latex')
ylabel(ax17, '$u$ [\%]', 'Interpreter','latex')
ylabel(ax18, '$u$ [\%]', 'Interpreter','latex')
ylabel(ax19, '$u$ [\%]', 'Interpreter','latex')

grid(ax11, "on")
grid(ax12, "on")
grid(ax13, "on")

grid(ax14, "on")
grid(ax15, "on")

grid(ax16, "on")
grid(ax17, "on")
grid(ax18, "on")
grid(ax19, "on")

hold(ax11, "on")
hold(ax12, "on")
hold(ax13, "on")

hold(ax14, "on")
hold(ax15, "on")

hold(ax16, "on")
hold(ax17, "on")
hold(ax18, "on")
hold(ax19, "on")


stairs(ax11, timestamps, data{:,"angleX"}, "Color", "#0072BD");
stairs(ax11, timestamps, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");

stairs(ax12, timestamps, data{:,"angleY"}, "Color", "#D95319");
stairs(ax12, timestamps, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");

stairs(ax13, timestamps, data{:,"velZ"}, "Color", "#77AC30");
stairs(ax13, timestamps, zeros(dataLen,1), "Color", "#7E2F8E", "LineStyle","--");

stairs(ax14, timestamps, data{:,"PID_X"});
stairs(ax15, timestamps, data{:,"PID_Y"}, "Color", "#D95319");

stairs(ax16, timestamps, data{:,"uFL"}, "Color", "#7E2F8E");
stairs(ax17, timestamps, data{:,"uFR"}, "Color", "#7E2F8E");
stairs(ax18, timestamps, data{:,"uBL"}, "Color", "#7E2F8E");
stairs(ax19, timestamps, data{:,"uBR"}, "Color", "#7E2F8E");


axis(ax11, [timestamps(1), timestamps(end), min(data{:,"angleX"}) - 5, max(data{:,"angleX"}) + 5])
axis(ax12, [timestamps(1), timestamps(end), min(data{:,"angleY"}) - 5, max(data{:,"angleY"}) + 5])
axis(ax13, [timestamps(1), timestamps(end), min(data{:,"velZ"}) - 0.01, max(data{:,"velZ"}) + 0.01])
axis(ax14, [timestamps(1), timestamps(end), min(data{:,"PID_X"}) - 5, max(data{:,"PID_X"}) + 5])
axis(ax15, [timestamps(1), timestamps(end), min(data{:,"PID_Y"}) - 5, max(data{:,"PID_Y"}) + 5])
axis(ax16, [timestamps(1), timestamps(end), 0, 100])
axis(ax17, [timestamps(1), timestamps(end), 0, 100])
axis(ax18, [timestamps(1), timestamps(end), 0, 100])
axis(ax19, [timestamps(1), timestamps(end), 0, 100])

