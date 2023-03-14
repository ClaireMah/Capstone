calibration=load('C:\Users\mabel\OneDrive\Desktop\Year 4\ENGO 500\calibration\cameraParameters.mat');
iops_struct=calibration.cameraParams.Intrinsics;
%disp(iops_struct);

errors=load('C:\Users\mabel\OneDrive\Desktop\Year 4\ENGO 500\calibration\cameraErrors.mat');
errors_struct=errors.estimationErrors.IntrinsicsErrors;
%disp(errors_struct);

width_mm=22.6*10;
height_mm=16.9*10;

px=width_mm/iops_struct.ImageSize(2);
py=height_mm/iops_struct.ImageSize(1);

F1=iops_struct.FocalLength(1)*px;
F2=iops_struct.FocalLength(2)*py;

disp(['Principal Point x (pixels): ' num2str(iops_struct.PrincipalPoint(1)) ' +/- ' num2str(errors_struct.PrincipalPointError(1))]);
disp(['Principal Point y (pixels): ' num2str(iops_struct.PrincipalPoint(2)) ' +/- ' num2str(errors_struct.PrincipalPointError(2))]);
disp(['Focal Length (mm): ' num2str(F1)]);