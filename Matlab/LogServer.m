clear;

% Prepare result table
Nsize = 100;

readings = array2table( zeros(Nsize,6) ...
                       , 'VariableNames' ...
                       , {'GyroX','GyroY','GyroZ','AccX', 'AccY','AccZ'} ...
                       );

% Prepare figures

f1 = figure(1);
clf(f1)
subplot(2,1,1);
ax11 = gca;
subplot(2,1,2);
ax21 = gca;

title(ax11, 'Gyroscope readings')
title(ax21, 'Accelerometer readings')

GyroXLine = animatedline(ax11, "Color", 'red');
GyroYLine = animatedline(ax11, "Color", 'blue');
GyroZLine = animatedline(ax11, "Color", 'green');

AccXLine = animatedline(ax21, "Color", 'red');
AccYLine = animatedline(ax21, "Color", 'blue');
AccZLine = animatedline(ax21, "Color", 'green');


% Create tcp socket
server = tcpserver("0.0.0.0",6000,"Timeout",60);
server.ByteOrder = "big-endian";

for i = 1:100
    
    data = read(server,6,"double");

    addpoints(GyroXLine, i, data(1));
    addpoints(GyroYLine, i, data(2));
    addpoints(GyroZLine, i, data(3));

    addpoints(AccXLine, i, data(4));
    addpoints(AccYLine, i, data(5));
    addpoints(AccZLine, i, data(6));

    data = array2table(data, ...
                       'VariableNames', ...
                       {'GyroX','GyroY','GyroZ','AccX', 'AccY','AccZ'} ...
                       );
    readings(i,:) = data;

end


delete(server)
