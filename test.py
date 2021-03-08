class Compute:

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2


    def total(self):
        total = self.num1 + self.num2
        return total

x=Compute(2,3)
y = x.total()
print(y)