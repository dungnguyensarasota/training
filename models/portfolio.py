from models.economics import Economics


class Portfolio(Economics):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def compute(self, econ_lst):
        pass
    # def __init__(self, econ_lst):
    #     self.eco_lst = econ_lst
    # def calc


if __name__ == '__main__':
    # params = {
    #     "econ_list":{
    #         "E1":{e1_pa}
    #     }
    # }
    e1 = Economics()
    e2 = Economics()
    # p = Portfolio()
    p = Portfolio('my_portfolio 2 wells')
    p.calculate([e1, e2])
    print(p.name)
    print(p.present_value)
