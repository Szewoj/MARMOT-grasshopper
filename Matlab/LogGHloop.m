function readingTable = LogGHloop(maxLoop, posePlot, ...
    angXstpt, angXstpLine, angXLine, ...
    angYstpt, angYstpLine, angYLine, ...
    accZLine, ...
    pidXLine, pidYLine, ...
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
        pidYLine (1,1) {mustBeA(pidYLine, "matlab.graphics.animation.AnimatedLine")}

        uFLLine (1,1) {mustBeA(uFLLine, "matlab.graphics.animation.AnimatedLine")}
        uFRLine (1,1) {mustBeA(uFRLine, "matlab.graphics.animation.AnimatedLine")}
        uBLLine (1,1) {mustBeA(uBLLine, "matlab.graphics.animation.AnimatedLine")}
        uBRLine (1,1) {mustBeA(uBRLine, "matlab.graphics.animation.AnimatedLine")}
    end

    startTime = posixtime(datetime('now'));

    readingTable = initIMUTable();
    
    
    % Create tcp socket
    s = tcpclient("192.168.1.101",6000,"ByteOrder","big-endian");
    
    for i = 1:maxLoop
        
        data = read(s,10,"double");
    
        timestamp = data(1) - startTime;

        % Calculate time difference
        while timestamp < 0
            startTime = startTime - 3600;
            timestamp = data(1) - startTime;
        end

        S.Time = datetime(data(1),'convertfrom','posixtime', 'Format', 'yyyy-MM-dd HH:mm:ss.SSS');
        S.angleX = data(2);
        S.angleY = data(3);
        S.accZ   = data(4);
        S.PID_X  = data(5);
        S.PID_Y  = data(6);
        S.uFL    = data(7);
        S.uFR    = data(8);
        S.uBL    = data(9);
        S.uBR    = data(10);


        addpoints(angXstpLine, timestamp, angXstpt);
        addpoints(angXLine, timestamp, S.angleX);

        addpoints(angYstpLine, timestamp, angYstpt);
        addpoints(angYLine, timestamp, S.angleY);

        addpoints(accZLine, timestamp, S.accZ);

        addpoints(pidXLine, timestamp, S.PID_X);
        addpoints(pidYLine, timestamp, S.PID_Y);

        addpoints(uFLLine, timestamp, S.uFL);
        addpoints(uFRLine, timestamp, S.uFR);
        addpoints(uBLLine, timestamp, S.uBL);
        addpoints(uBRLine, timestamp, S.uBR);
    

        ypr = [0, S.angleY/100, S.angleX/100];
        q = quaternion(eul2quat(ypr,"ZYX"));
        set(posePlot,Orientation=q);


        tableRow = struct2table(S);
  
        readingTable(i,:) = tableRow;
    end
end

