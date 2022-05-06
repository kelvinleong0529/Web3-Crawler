class operation:

    def __init__(self) -> None:
        pass


class add(operation):

    def __init__(self) -> None:
        super().__init__()
        self.__ans = 0

    def add(self, x, y):
        self.__ans = x + y
        return self.__ans


class minus(operation):

    def __init__(self) -> None:
        super().__init__()

    def minus(self, x, y):
        return x - y


class final(add, minus):

    def __init__(self) -> None:
        super().__init__()

    def combine(self, x, y):
        print(super().add(x, y))
        print(super().minus(x, y))


temp = final()
temp.combine(30, 20)
