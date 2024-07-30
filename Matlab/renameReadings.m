clear;
files = ["Data\dryRun\a1", "Data\dryRun\a2", "Data\dryRun\a3", "Data\dryRun\a4", "Data\dryRun\a5", ...
        "Data\dryRun\b1", "Data\dryRun\b2", "Data\dryRun\b3", "Data\dryRun\b4", "Data\dryRun\b5", ...
        "Data\dryRun\y1", "Data\dryRun\y2", "Data\dryRun\y3", "Data\dryRun\y4", "Data\dryRun\y5", ...
        "Data\lambdaV1\a1", "Data\lambdaV1\b1", "Data\lambdaV1\y1", ...
        "Data\lambdaV2\a1", "Data\lambdaV2\b1", ...
        ];


for i = 1:length(files)

    load(files(i))

    data.Properties.VariableNames{'accZ'} = 'velZ';

    save(files(i), "data")

end
        