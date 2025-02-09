from day7_equation import Equation


class CalibrationSystem:
  def __init__(self, inputFileName: str) -> None:
    self.inputFileName = inputFileName
    self.equations: list[Equation] = self.parseInput()

  def parseInput(self) -> list[Equation]:
    """
    Parse input file and fill the self.equations list
    """
    lines = self.getLinesFromInputFile()
    equations: list[Equation] = []

    for line in lines:
      parts = line.split(':')
      if len(parts) == 2:
        try:
          testValue = int(parts[0].strip())
          numbers_str = parts[1].strip()
          # Convert to list of integers
          numbers = [int(x) for x in numbers_str.split()]
          equation = Equation(testValue, numbers)
          equations.append(equation)
        except ValueError:
          print(f"Conversion error for line: {line}")
      else:
        print(f"Invalid line: {line}")

    return equations

  def getLinesFromInputFile(self) -> list[str]:
    lines = []
    with open(self.inputFileName, 'r', encoding='utf8') as file:
      for line in file:
        # do not keep '\n' end character in each line
        if line[-1] == "\n":
          lines.append(line[:-1])
        else:
          lines.append(line)
    return lines

  @property
  def totalCalibrationResult(self) -> int:
    return sum(equation.computeCalibrationResult() for equation in self.equations)

  def __str__(self) -> str:
    equations_str = "\n".join(str(equation) for equation in self.equations)
    return equations_str
