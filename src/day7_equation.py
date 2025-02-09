class Equation:

  operators = ('+', '*', '||')

  class Operation:
    """
    An operation is a list of an equation operands combined with operators.
    For example if the equation is '190: 10 19', an operation could be 10 * 19
    or 10 + 19.
    """

    def __init__(self, equation: "Equation", operators: list[str]):
      self.testValue = equation.testValue
      self.operands: list[int] = equation.operands
      self.operators: list[str] = operators

    def evaluate(self) -> int:
      """
      Evaluates the operation from left to right.
      """
      result = self.operands[0]
      for operator, operand in zip(self.operators, self.operands[1:]):
        if operator == '+':
          result += operand
        elif operator == '*':
          result *= operand
        elif operator == '||':
          result = int(str(result) + str(operand))

      return result

    def isCorrect(self) -> bool:
      return self.evaluate() == self.testValue

    def __str__(self) -> str:
      firstOperand = str(self.operands[0])
      nextOperands = map(str, self.operands[1:])
      displayedOperation = firstOperand
      for operand, operator in zip(nextOperands, self.operators):
        displayedOperation += f" {operator} {operand}"

      return displayedOperation

  def __init__(self, testValue: int, operands: list[int]):
    self.testValue = testValue
    self.operands = operands

  def _listOfOperatorsGenerator(self, numOperands):
    if numOperands < 2:
      raise ValueError("The number of operands cannot be less than 2")
    elif numOperands == 2:
      for op in self.operators:
        yield [op]
    else:
      for op in self.operators:
        for comb in self._listOfOperatorsGenerator(numOperands - 1):
          yield [op] + comb

  def operationGenerator(self):
    for op in self._listOfOperatorsGenerator(len(self.operands)):
      yield Equation.Operation(self, op)

  def computeCalibrationResult(self) -> int:
    """
    Returns the test value if an operation is equal to the test value
    returns 0 otherwise
    """
    for expr in self.operationGenerator():
      if expr.isCorrect():
        return expr.testValue
    return 0

  def __str__(self) -> str:
    operands_str = " ".join(map(str, self.operands))
    return f"{self.testValue}: {operands_str}"
