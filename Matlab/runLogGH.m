clear;

% Prepare result table
Nsize = 600;

% Angular position setpoints:
ANG_X_STPT = 0;
ANG_Y_STPT = 0;

% Prepare figures

% Figure 1 - live pose representation:

f1 = figure(1);
clf(f1)
posePlot = poseplot(quaternion([1 0 0 0]));
ax1 = gca;
ax1.XDir = "normal";
ax1.ZDir = "normal";
ax1.YDir = "normal";
ax1.CameraPosition = ax1.CameraPosition.*[-1 -1 1];
xlabel("X");
ylabel("Y");
zlabel("Z");

% Figure 2 - system measured values:

f2 = figure(2);
clf(f2)
subplot(3,1,1);
ax21 = gca;
subplot(3,1,2);
ax22 = gca;
subplot(3,1,3);
ax23 = gca;

title(ax21, 'Angular position around X axis (roll)  [mrad]')
title(ax22, 'Angular position around Y axis (pitch) [mrad]')
title(ax23, 'Onboard Z axis acceleration [m/s^2]')

angXLine = animatedline(ax21, "Color", "#0072BD");
angXstptLine = animatedline(ax21, "Color", "#7E2F8E", "LineStyle","--");

angYLine = animatedline(ax22, "Color", "#D95319");
angYstptLine = animatedline(ax22, "Color", "#7E2F8E", "LineStyle","--");

accZLine = animatedline(ax23, "Color", "#77AC30");

grid(ax21, "on")
grid(ax22, "on")
grid(ax23, "on")


% Figure 3 - system outputs

f3 = figure(3);
clf(f3)

if f3.Position(4) ~= 924
    f3.Position = [f3.Position(1), f3.Position(2) - round(f3.Position(4)), 1.2 * f3.Position(3), 2.2 * f3.Position(4)];
end

subplot(4,1,1);
ax31 = gca;
subplot(4,1,2);
ax32 = gca;
subplot(4,2,5);
ax33 = gca;
subplot(4,2,6);
ax34 = gca;
subplot(4,2,7);
ax35 = gca;
subplot(4,2,8);
ax36 = gca;

title(ax31, 'Inner PID X axis output (\Deltau_x) [%]')
title(ax32, 'Inner PID Y axis output (\Deltau_y) [%]')

title(ax33, 'Front left wheel u_F_L [%]')
title(ax34, 'Front right wheel u_F_R [%]')
title(ax35, 'Back left wheel u_B_L [%]')
title(ax36, 'Back right wheel u_B_R [%]')


pidXLine = animatedline(ax31, "Color", "#0072BD");
pidXPLine = animatedline(ax31, "Color", "#7E2F8E", "LineStyle","--");
pidXILine = animatedline(ax31, "Color", "#77AC30", "LineStyle","-.");
pidXDLine = animatedline(ax31, "Color", "#A2142F", "LineStyle",":");

legend(ax31, {'u_{PID}', 'u_P', 'u_I', 'u_D'},"Location","southwest")

pidYLine = animatedline(ax32, "Color", "#D95319");
pidYPLine = animatedline(ax32, "Color", "#7E2F8E", "LineStyle","--");
pidYILine = animatedline(ax32, "Color", "#77AC30", "LineStyle","-.");
pidYDLine = animatedline(ax32, "Color", "#A2142F", "LineStyle",":");

legend(ax32, {'u_{PID}', 'u_P', 'u_I', 'u_D'},"Location","southwest")

uFLLine = animatedline(ax33, "Color", "#D95319");
uFRLine = animatedline(ax34, "Color", "#D95319");
uBLLine = animatedline(ax35, "Color", "#D95319");
uBRLine = animatedline(ax36, "Color", "#77AC30");

grid(ax31, "on")
grid(ax32, "on")
grid(ax33, "on")
grid(ax34, "on")
grid(ax35, "on")
grid(ax36, "on")


% Start data collection loop:

readings = LogGHloop(Nsize, posePlot, ...
    ANG_X_STPT, angXstptLine, angXLine, ...
    ANG_Y_STPT, angYstptLine, angYLine, ...
    accZLine, ...
    pidXLine, pidXPLine, pidXILine, pidXDLine, ...
    pidYLine, pidYPLine, pidYILine, pidYDLine, ...
    uFLLine, uFRLine, uBLLine, uBRLine);