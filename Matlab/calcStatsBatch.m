% Data set definition:

clear;
dataSets = struct('Label', {"dryRun", "lambdaV1", "lambdaV2", "x", "y", "xyV1", "xyV2", "xyV2z", "xyV3"}, ...
                  'Range', {1:5,      1:1,        1:5,        1:1, 1:1, 1:5,    1:5,    1:5,     1:5},...
                  'Modes', {["a", "b", "y"], ["a", "b", "y"], ["a", "b", "y"], ["a", "b"], ["a", "b"], ...
                            ["a", "b", "y"], ["a", "b", "y"], ["a", "b", "y"], ["a", "b", "y"]});


% Constants:
trailLen = 5.48; % m

% init statistic table:
stats = initStatTable();

% loop calculating statistics

setsLen = length(dataSets);
r = 1;

for i = 1:setsLen

    for j = 1:length(dataSets(i).Modes)

        for k = dataSets(i).Range
            % calculate stat line:
            clear('data')
            statRow = struct();
            load("Data\" + dataSets(i).Label + "\" + dataSets(i).Modes(j)  + string(k) + ".mat");

            statRow.Label = dataSets(i).Label;
            statRow.Mode = dataSets(i).Modes(j);


            dataLen = length(data{:,"angleX"});
            timestamps = posixtime(data{:,"Time"});
            timestamps = timestamps - timestamps(1);

            statRow.Speed = trailLen / timestamps(end);

            statRow.x_MSE  = data{:,"angleX"}' * data{:,"angleX"} / dataLen;
            statRow.y_MSE  = data{:,"angleY"}' * data{:,"angleY"} / dataLen;
            statRow.vZ_MSE = data{:,"velZ"}' * data{:,"velZ"} / dataLen;
            
            %   median absolute deviation: (x, y, vZ)
            
            statRow.x_MAD  = median(abs(data{:,"angleX"}));
            statRow.y_MAD  = median(abs(data{:,"angleY"}));
            statRow.vZ_MAD = median(abs(data{:,"velZ"}));
            
            %   mean absolute error: (x, y, vZ)
            
            statRow.x_MAE  = mean(abs(data{:,"angleX"}));
            statRow.y_MAE  = mean(abs(data{:,"angleY"}));
            statRow.vZ_MAE = mean(abs(data{:,"velZ"}));
            
            %   mean and deviation: (x, y, vZ)
            
            statRow.x_m = mean(data{:,"angleX"});
            statRow.x_std = std(data{:,"angleX"});
            
            statRow.y_m = mean(data{:,"angleY"});
            statRow.y_std = std(data{:,"angleY"});
            
            statRow.vZ_m = mean(data{:,"velZ"});
            statRow.vZ_std = std(data{:,"velZ"});
            
            %   x and y derivative:
            
            dt = timestamps(2:end) - timestamps(1:end-1);
            
            dx = (data{2:end,"angleX"} - data{1:end-1,"angleX"}) ./ dt;
            dy = (data{2:end,"angleY"} - data{1:end-1,"angleY"}) ./ dt;
            
            %       MSE: (dx, dy)
            
            statRow.dx_MSE = dx'*dx / (dataLen-1);
            statRow.dy_MSE = dy'*dy / (dataLen-1);
            
            %       MAD: (dx, dy)
            
            statRow.dx_MAD = median(abs(dx));
            statRow.dy_MAD = median(abs(dy));
            
            %       MAE: (dx, dy)
            
            statRow.dx_MAE  = mean(abs(dx));
            statRow.dy_MAE  = mean(abs(dy));
            
            %       mean and std: (dx, dy)
            
            statRow.dx_m = mean(dx);
            statRow.dx_std = std(dx);
            
            statRow.dy_m = mean(dy);
            statRow.dy_std = std(dy);

            % save row
            stats(r,:) = struct2table(statRow);
            r = r+1;

        end

    end
end


save("Stats\batch.mat", "stats");