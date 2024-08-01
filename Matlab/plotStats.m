% Data sets to plot:

load("Stats\batch.mat");

toPlot = {"dryRun", "xyV2"};


% Ready figures:
%   Figure 1 - x y vZ - MAE and MAD
f1 = figure(1);
clf(f1)

subplot(2,3,1); ax11 = gca;
subplot(2,3,2); ax12 = gca;
subplot(2,3,3); ax13 = gca;
subplot(2,3,4); ax14 = gca;
subplot(2,3,5); ax15 = gca;
subplot(2,3,6); ax16 = gca;

hold(ax11, 'on'); grid(ax11, 'on'); title(ax11, 'X axis MAE')
hold(ax12, 'on'); grid(ax12, 'on'); title(ax12, 'Y axis MAE')
hold(ax13, 'on'); grid(ax13, 'on'); title(ax13, 'Z velocity MAE')
hold(ax14, 'on'); grid(ax14, 'on'); title(ax14, 'X axis MAD')
hold(ax15, 'on'); grid(ax15, 'on'); title(ax15, 'Y axis MAD')
hold(ax16, 'on'); grid(ax16, 'on'); title(ax16, 'Z velocity MAD')

xlabel(ax11, "v [m/s]"); ylabel(ax11, "\phi_x [mrad]"); 
xlabel(ax12, "v [m/s]"); ylabel(ax12, "\phi_y [mrad]"); 
xlabel(ax13, "v [m/s]"); ylabel(ax13, "v_z [m/s]"); 
xlabel(ax14, "v [m/s]"); ylabel(ax14, "\phi_x [mrad]"); 
xlabel(ax15, "v [m/s]"); ylabel(ax15, "\phi_y [mrad]"); 
xlabel(ax16, "v [m/s]"); ylabel(ax16, "v_z [m/s]"); 



%   Figure 2 - x y vZ - gaussian distribution 
f2 = figure(2);
clf(f2)

subplot(3,1,1); ax21 = gca;
subplot(3,1,2); ax22 = gca;
subplot(3,1,3); ax23 = gca;

hold(ax21, 'on'); grid(ax21, 'on'); title(ax21, 'X axis error distribution')
hold(ax22, 'on'); grid(ax22, 'on'); title(ax22, 'Y axis error distribution')
hold(ax23, 'on'); grid(ax23, 'on'); title(ax23, 'Z velocity error distribution')

xlabel(ax21, "v [m/s]"); ylabel(ax21, "\phi_x [mrad]"); 
xlabel(ax22, "v [m/s]"); ylabel(ax22, "\phi_y [mrad]"); 
xlabel(ax23, "v [m/s]"); ylabel(ax23, "v_z [m/s]"); 


%   Figure 3 - dx dy - MAE and MAD



% Plot data:
sorted = sortrows(stats, "Speed", "ascend");

for i = 1:length(toPlot)
    Label = toPlot{i};

    selectRows = sorted{:,"Label"} == Label;

    % F1:
    plot(ax11, sorted{selectRows,"Speed"}, sorted{selectRows,"x_MAE"}, 'v:')
    plot(ax12, sorted{selectRows,"Speed"}, sorted{selectRows,"y_MAE"}, 'v:')
    plot(ax13, sorted{selectRows,"Speed"}, sorted{selectRows,"vZ_MAE"}, 'v:')
    plot(ax14, sorted{selectRows,"Speed"}, sorted{selectRows,"x_MAD"}, 'v:')
    plot(ax15, sorted{selectRows,"Speed"}, sorted{selectRows,"y_MAD"}, 'v:')
    plot(ax16, sorted{selectRows,"Speed"}, sorted{selectRows,"vZ_MAD"}, 'v:')

    % F2:
    errorbar(ax21, sorted{selectRows,"Speed"}, sorted{selectRows,"x_m"}, sorted{selectRows,"x_std"}, 'o:')
    errorbar(ax22, sorted{selectRows,"Speed"}, sorted{selectRows,"y_m"}, sorted{selectRows,"y_std"}, 'o:')
    errorbar(ax23, sorted{selectRows,"Speed"}, sorted{selectRows,"vZ_m"}, sorted{selectRows,"vZ_std"}, 'o:')


end


% Legends:

legend(ax11, toPlot,'Location','northwest');
legend(ax12, toPlot,'Location','northwest');
legend(ax13, toPlot,'Location','northwest');
legend(ax14, toPlot,'Location','northwest');
legend(ax15, toPlot,'Location','northwest');
legend(ax16, toPlot,'Location','northwest');

