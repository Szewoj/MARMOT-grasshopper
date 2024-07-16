clear;

% Prepare result table
Nsize = 100000;

% Prepare figures

% Figure 1
f1 = figure(1);
clf(f1)
subplot(2,1,1);
ax11 = gca;
subplot(2,1,2);
ax12 = gca;

title(ax11, 'Gyroscope readings')
title(ax12, 'Accelerometer readings')

GyroXLine = animatedline(ax11, "Color", 'red');
GyroYLine = animatedline(ax11, "Color", 'blue');
GyroZLine = animatedline(ax11, "Color", 'green');

AccXLine = animatedline(ax12, "Color", 'red');
AccYLine = animatedline(ax12, "Color", 'blue');
AccZLine = animatedline(ax12, "Color", 'green');

grid(ax11, "on")
grid(ax12, "on")

legend(ax11, ["gyro x", "gyro y", "gyro Z"], 'Location','northwest')
legend(ax12, ["acc x", "acc y", "acc Z"], 'Location','northwest')

% Figure 2

f2 = figure(2);
clf(f2)
posePlot = poseplot(quaternion([1 0 0 0]));
ax2 = gca;
ax2.XDir = "normal";
ax2.ZDir = "normal";
ax2.YDir = "normal";
ax2.CameraPosition = ax2.CameraPosition.*[-1 -1 1];
xlabel("X");
ylabel("Y");
zlabel("Z");

% Figure 3

f3 = figure(3);
clf(f3)
ax3 = gca;

title(ax3, 'Rotation')

RotXLine = animatedline(ax3, "Color", 'red');
RotYLine = animatedline(ax3, "Color", 'blue');

grid(ax3, "on")

legend(ax3, ["Rotation X", "Rotation Y"], 'Location','northwest')

readings = LogIMUloop(Nsize, ...
    posePlot, GyroXLine, GyroYLine, GyroZLine, AccXLine, AccYLine, AccZLine, RotXLine, RotYLine);


