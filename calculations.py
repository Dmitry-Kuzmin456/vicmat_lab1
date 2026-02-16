from itertools import permutations
from models import Data, Result


class Calculations:
    def __init__(self, data: Data):
        self.n = data.n
        self.matrix = [row[:-1] for row in data.matrix]
        self.res = [row[-1] for row in data.matrix]
        self.accuracy = data.accuracy

    def find_diagonally_dominant(self) -> bool:
        if self.is_diagonally_dominant(self.n, self.matrix):
            return True

        indices = list(range(self.n))
        for p in permutations(indices):
            new_m = [self.matrix[i] for i in p]
            new_res = [self.res[i] for i in p]
            if self.is_diagonally_dominant(self.n, new_m):
                self.matrix = new_m
                self.res = new_res
                return True
        return False

    @staticmethod
    def is_diagonally_dominant(n: int, matrix: list[list[float]]) -> bool:
        strict_dominance = False
        for i in range(n):
            row_sum = sum(abs(matrix[i][j]) for j in range(n) if i != j)
            if abs(matrix[i][i]) < row_sum:
                return False
            if abs(matrix[i][i]) > row_sum:
                strict_dominance = True
        return strict_dominance

    def calculate(self) -> Result:
        C = []
        d = []
        for i in range(self.n):
            denom = self.matrix[i][i]
            d.append(self.res[i] / denom)
            row_c = []
            for j in range(self.n):
                if i == j:
                    row_c.append(0.0)
                else:
                    row_c.append(-self.matrix[i][j] / denom)
            C.append(row_c)

        norm = max(sum(abs(val) for val in row) for row in C)

        curr_x = d[:]
        iterations = 0
        max_iterations = 10000

        while iterations < max_iterations:
            prev_x = curr_x[:]
            new_x = []
            for i in range(self.n):
                val = d[i] + sum(C[i][j] * prev_x[j] for j in range(self.n))
                new_x.append(val)

            iterations += 1

            errors = [abs(new_x[i] - prev_x[i]) for i in range(self.n)]
            curr_x = new_x

            if max(errors) < self.accuracy:
                return Result(x=curr_x, iterations=iterations, errors=errors, norm=norm)

        raise Exception("Метод не сошелся за отведенное число итераций.")
