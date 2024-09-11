
s1 = "dryRunSingle\b9.mat";
s2 = "xyV3zSingle\b3.mat";


% Figure frequency response:

f1 = figure(1);
clf(f1);

f1.Position = [941,103,729,842];

subplot(3,1,1);
ax11 = gca;
subplot(3,1,2);
ax12 = gca;
subplot(3,1,3);
ax13 = gca;


title(ax11, '$|\hat{\varphi_x}(f)|$', 'Interpreter','latex')
title(ax12, '$|\hat{\varphi_y}(f)|$', 'Interpreter','latex')
title(ax13, '$|\hat{v_z}(f)|$', 'Interpreter','latex')


xlabel(ax11, '$f$ [Hz]', 'Interpreter','latex')
xlabel(ax12, '$f$ [Hz]', 'Interpreter','latex')
xlabel(ax13, '$f$ [Hz]', 'Interpreter','latex')


ylabel(ax11, '$\hat{\varphi}$', 'Interpreter','latex')
ylabel(ax12, '$\hat{\varphi}$', 'Interpreter','latex')
ylabel(ax13, '$\hat{v}$', 'Interpreter','latex')

grid(ax11, "on")
grid(ax12, "on")
grid(ax13, "on")

hold(ax11, "on")
hold(ax12, "on")
hold(ax13, "on")

% Calculate first series

load("Data\" + s1);

Fs = 40;

timestamps = posixtime(data{:,"Time"});
timestamps = timestamps - timestamps(1);
n = length(timestamps);

yX = nufft(data{:,"angleX"}, timestamps*Fs);
yXP2 = abs(yX/n);
yXP1 = yXP2(1:n/2+1);
yXP1(2:end-1) = 2*yXP1(2:end-1);

yY = nufft(data{:,"angleY"}, timestamps*Fs);
yYP2 = abs(yY/n);
yYP1 = yYP2(1:n/2+1);
yYP1(2:end-1) = 2*yYP1(2:end-1);

yZ = nufft(data{:,"velZ"}, timestamps*Fs);
yZP2 = abs(yZ/n);
yZP1 = yZP2(1:n/2+1);
yZP1(2:end-1) = 2*yZP1(2:end-1);

f = Fs/n*(0:(n/2));

plot(ax11, f, abs(yXP1));
plot(ax12, f, abs(yYP1));
plot(ax13, f, abs(yZP1));

% Calculate second series

load("Data\" + s2);

Fs = 75/2;

timestamps = posixtime(data{:,"Time"});
timestamps = timestamps - timestamps(1);
n = length(timestamps);

yX = nufft(data{:,"angleX"}, timestamps*Fs);
yXP2 = abs(yX/n);
yXP1 = yXP2(1:n/2+1);
yXP1(2:end-1) = 2*yXP1(2:end-1);

yY = nufft(data{:,"angleY"}, timestamps*Fs);
yYP2 = abs(yY/n);
yYP1 = yYP2(1:n/2+1);
yYP1(2:end-1) = 2*yYP1(2:end-1);

yZ = nufft(data{:,"velZ"}, timestamps*Fs);
yZP2 = abs(yZ/n);
yZP1 = yZP2(1:n/2+1);
yZP1(2:end-1) = 2*yZP1(2:end-1);

f = Fs/n*(0:(n/2));

plot(ax11, f, abs(yXP1));
plot(ax12, f, abs(yYP1));
plot(ax13, f, abs(yZP1));

% legends

legend(ax11, ["dryRunSingle", "xyV3zSingle"],'Location','northeast');
legend(ax12, ["dryRunSingle", "xyV3zSingle"],'Location','northeast');
legend(ax13, ["dryRunSingle", "xyV3zSingle"],'Location','northeast');