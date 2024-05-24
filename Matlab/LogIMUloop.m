function readingTable = LogIMUloop(maxLoop, posePlot, ...
    GyroXLine, GyroYLine, GyroZLine, ...
    AccXLine, AccYLine, AccZLine, ...
    RotXLine, RotYLine)
%LOGIMULOP Loop connection to IMU device and poll readings
    arguments
        maxLoop (1,1) {mustBeInteger}
        posePlot (1,1) {mustBeA(posePlot, "positioning.graphics.chart.PosePatch")}
        GyroXLine (1,1) {mustBeA(GyroXLine, "matlab.graphics.animation.AnimatedLine")}
        GyroYLine (1,1) {mustBeA(GyroYLine, "matlab.graphics.animation.AnimatedLine")}
        GyroZLine (1,1) {mustBeA(GyroZLine, "matlab.graphics.animation.AnimatedLine")}
        AccXLine (1,1) {mustBeA(AccXLine, "matlab.graphics.animation.AnimatedLine")}
        AccYLine (1,1) {mustBeA(AccYLine, "matlab.graphics.animation.AnimatedLine")}
        AccZLine (1,1) {mustBeA(AccZLine, "matlab.graphics.animation.AnimatedLine")}
        RotXLine (1,1) {mustBeA(RotXLine, "matlab.graphics.animation.AnimatedLine")}
        RotYLine (1,1) {mustBeA(RotYLine, "matlab.graphics.animation.AnimatedLine")}
    end

    startTime = posixtime(datetime('now')) - 3600;

    readingTable = initIMUTable();
    
    
    % Create tcp socket
    s = tcpclient("192.168.1.101",6000,"ByteOrder","big-endian");
    
    for i = 1:maxLoop
        
        data = read(s,11,"double");
    
        timestamp = data(1) - startTime;
    
        addpoints(GyroXLine, timestamp, data(2));
        addpoints(GyroYLine, timestamp, data(3));
        addpoints(GyroZLine, timestamp, data(4));
    
        addpoints(AccXLine, timestamp, data(5));
        addpoints(AccYLine, timestamp, data(6));
        addpoints(AccZLine, timestamp, data(7));
    
        q = quaternion(data(8:11));
        rpy = quat2eul(q,"ZYX");
        rpy(1) = 0;
        q2 = quaternion(eul2quat(rpy,"ZYX"));
        set(posePlot,Orientation=q2);

        addpoints

        addpoints(RotXLine, timestamp, rpy(3));
        addpoints(RotYLine, timestamp, rpy(2));
        
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
    
        readingTable(i,:) = tableRow;
    
    end



end

