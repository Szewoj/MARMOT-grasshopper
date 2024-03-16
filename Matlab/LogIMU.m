clear;

% init time start
startTime = posixtime(datetime('now')) - 3600;

% Prepare result table
Nsize = 100;

readings = initIMUTable();

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

f2 = figure(2);
posePlot = poseplot(quaternion([1 0 0 0]));
xlabel("X");
ylabel("Y");
zlabel("Z");


% Create tcp socket
server = tcpclient("192.168.1.101",6000,"ByteOrder","big-endian");

for i = 1:10000
    
    data = read(server,11,"double");

    timestamp = data(1) - startTime;

    addpoints(GyroXLine, timestamp, data(2));
    addpoints(GyroYLine, timestamp, data(3));
    addpoints(GyroZLine, timestamp, data(4));

    addpoints(AccXLine, timestamp, data(5));
    addpoints(AccYLine, timestamp, data(6));
    addpoints(AccZLine, timestamp, data(7));

    q = quaternion(data(8:11));
    set(posePlot,Orientation=q);
    drawnow

    
    S.Time = datetime(data(1),'convertfrom','posixtime', 'Format', 'yyyy-MM-dd HH:mm:ss.SSS');
    S.GyroX = data(2);
    S.GyroY = data(3);
    S.GyroZ = data(4);
    S.AccX = data(5);
    S.AccY = data(6);
    S.AccZ = data(7);
    S.Q_w = data(8);
    S.Q_i = data(9);
    S.Q_j = data(10);
    S.Q_k = data(11);

    tableRow = struct2table(S);

    readings(i,:) = tableRow;

end


delete(server)
