from day7_calibSys import CalibrationSystem
from day7_equation import Equation
from command_line_parser import get_arguments_from_command_line

if __name__ == "__main__":
  filename, part = get_arguments_from_command_line()
  calibSys = CalibrationSystem(filename)
  if part == 1 or part == 2:
    pass
    calibResult = calibSys.totalCalibrationResult
    print("Total calibration result:", calibResult)
