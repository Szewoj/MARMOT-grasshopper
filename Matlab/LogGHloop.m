function readingTable = LogGHloop(maxLoop, posePlot, ...
    angXstpt, angXstpLine, angXLine, ...
    angYstpt, angYstpLine, angYLine, ...
    accZLine, ...
    pidXLine, pidXPLine, pidXILine, pidXDLine, ...
    pidYLine, pidYPLine, pidYILine, pidYDLine, ...
    uFLLine, uFRLine, uBLLine, uBRLine)
%LOGGHLOOP Loop connection to suspension system and poll readings
    arguments
        maxLoop (1,1) {mustBeInteger}
        posePlot (1,1) {mustBeA(posePlot, "positioning.graphics.chart.PosePatch")}

        angXstpt (1,1) {mustBeNumeric}
        angXstpLine (1,1) {mustBeA(angXstpLine, "matlab.graphics.animation.AnimatedLine")}
        angXLine (1,1) {mustBeA(angXLine, "matlab.graphics.animation.AnimatedLine")}
        angYstpt (1,1) {mustBeNumeric}
        angYstpLine (1,1) {mustBeA(angYstpLine, "matlab.graphics.animation.AnimatedLine")}
        angYLine (1,1) {mustBeA(angYLine, "matlab.graphics.animation.AnimatedLine")}
        accZLine (1,1) {mustBeA(accZLine, "matlab.graphics.animation.AnimatedLine")}

        pidXLine (1,1) {mustBeA(pidXLine, "matlab.graphics.animation.AnimatedLine")}
        pidXPLine (1,1) {mustBeA(pidXPLine, "matlab.graphics.animation.AnimatedLine")}
        pidXILine (1,1) {mustBeA(pidXILine, "matlab.graphics.animation.AnimatedLine")}
        pidXDLine (1,1) {mustBeA(pidXDLine, "matlab.graphics.animation.AnimatedLine")}
        
        pidYLine (1,1) {mustBeA(pidYLine, "matlab.graphics.animation.AnimatedLine")}
        pidYPLine (1,1) {mustBeA(pidYPLine, "matlab.graphics.animation.AnimatedLine")}
        pidYILine (1,1) {mustBeA(pidYILine, "matlab.graphics.animation.AnimatedLine")}
        pidYDLine (1,1) {mustBeA(pidYDLine, "matlab.graphics.animation.AnimatedLine")}

        uFLLine (1,1) {mustBeA(uFLLine, "matlab.graphics.animation.AnimatedLine")}
        uFRLine (1,1) {mustBeA(uFRLine, "matlab.graphics.animation.AnimatedLine")}
        uBLLine (1,1) {mustBeA(uBLLine, "matlab.graphics.animation.AnimatedLine")}
        uBRLine (1,1) {mustBeA(uBRLine, "matlab.graphics.animation.AnimatedLine")}
    end

    startTime = posixtime(datetime('now'));

    readingTable = initGhTable();
    
    
    % Create tcp socket
    s = tcpclient("192.168.1.101",6000,"ByteOrder","big-endian","Timeout",10);
    
    for i = 1:maxLoop
        
        try
            data = read(s,16,"double");
        catch e
            disp("Connection timed out! Closing script...")
            break
        end
    
        timestamp = data(1) - startTime;

        % Calculate time difference
        while timestamp < 0
            startTime = startTime - 3600;
            timestamp = data(1) - startTime;
        end

        S.Time = datetime(data(1),'convertfrom','posixtime', 'Format', 'yyyy-MM-dd HH:mm:ss.SSS');
        S.angleX = data(2);
        S.angleY = data(3);
        S.velZ   = data(4);
        S.PID_X  = data(5);
        S.PID_Y  = data(6);
        S.PID_X_P= data(7);
        S.PID_Y_P= data(8);
        S.PID_X_I= data(9);
        S.PID_Y_I= data(10);
        S.PID_X_D= data(11);
        S.PID_Y_D= data(12);
        S.uFL    = data(13);
        S.uFR    = data(14);
        S.uBL    = data(15);
        S.uBR    = data(16);


        addpoints(angXstpLine, timestamp, angXstpt);
        addpoints(angXLine, timestamp, S.angleX);

        addpoints(angYstpLine, timestamp, angYstpt);
        addpoints(angYLine, timestamp, S.angleY);

        addpoints(accZLine, timestamp, S.velZ);

        addpoints(pidXLine, timestamp, S.PID_X);
        addpoints(pidXPLine, timestamp, S.PID_X_P);
        addpoints(pidXILine, timestamp, S.PID_X_I);
        addpoints(pidXDLine, timestamp, S.PID_X_D);

        addpoints(pidYLine, timestamp, S.PID_Y);
        addpoints(pidYPLine, timestamp, S.PID_Y_P);
        addpoints(pidYILine, timestamp, S.PID_Y_I);
        addpoints(pidYDLine, timestamp, S.PID_Y_D);

        addpoints(uFLLine, timestamp, S.uFL);
        addpoints(uFRLine, timestamp, S.uFR);
        addpoints(uBLLine, timestamp, S.uBL);
        addpoints(uBRLine, timestamp, S.uBR);
    

        ypr = [0, S.angleY/1000, S.angleX/1000];
        q = quaternion(eul2quat(ypr,"ZYX"));
        set(posePlot,Orientation=q);


        tableRow = struct2table(S);
  
        readingTable(i,:) = tableRow;
    end
end

