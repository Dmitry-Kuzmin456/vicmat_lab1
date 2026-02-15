import FreeSimpleGUI as sg
from models import Data


class MatrixWindow:
    @classmethod
    def start(cls) -> Data | None:
        layout = [
            [sg.Text("Выберите способ ввода данных:")],
            [
                sg.Button("Ввести вручную", key="Klavatura"),
                sg.Button("Загрузить из файла", key="File"),
            ],
            [sg.Button("Выход")],
        ]
        window = sg.Window("Начало работы", layout)
        event, _ = window.read()
        window.close()

        if event == "Klavatura":
            return cls.manual_input()
        elif event == "File":
            return cls.file_input()
        return None

    @classmethod
    def manual_input(cls) -> Data | None:
        n = cls.choose_size()
        if not n:
            return None
        matrix = cls.choose_matrix(n)
        if not matrix:
            return None
        accuracy = cls.choose_accuracy()
        if not accuracy:
            return None
        return Data(n=n, matrix=matrix, accuracy=accuracy)

    @classmethod
    def file_input(cls) -> Data | None:
        file_path = sg.popup_get_file(
            "Выберите файл с данными", file_types=(("Text Files", "*.txt"),)
        )
        if not file_path:
            return None
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
                n = int(lines[0].strip())
                matrix = []
                for i in range(1, n + 1):
                    matrix.append([float(x) for x in lines[i].split()])
                accuracy = float(lines[n + 1].strip())
                return Data(n=n, matrix=matrix, accuracy=accuracy)
        except Exception as e:
            sg.popup_error(f"Ошибка при чтении файла: {e}")
            return None

    @staticmethod
    def choose_size() -> int | None:
        layout = [
            [sg.Text("Размер матрицы n (<=20):")],
            [sg.Input(key="n")],
            [sg.Button("OK")],
        ]
        window = sg.Window("Размер", layout)
        while True:
            event, values = window.read()
            if event in (None, sg.WIN_CLOSED):
                break
            try:
                n = int(values["n"])
                if 1 <= n <= 20:
                    window.close()
                    return n
                sg.popup("Размер должен быть от 1 до 20")
            except Exception:
                sg.popup("Введите число")
        window.close()
        return None

    @staticmethod
    def choose_matrix(n: int) -> list[list[float]] | None:
        grid = []
        for r in range(n):
            row = []
            for c in range(n):
                row.extend(
                    [
                        sg.Input(size=(5, 1), key=f"m_{r}_{c}"),
                        sg.Text(f"x{c + 1} + " if c < n - 1 else f"x{c + 1} = "),
                    ]
                )
            row.append(sg.Input(size=(5, 1), key=f"res_{r}"))
            grid.append(row)

        layout = [[sg.Text("Введите коэффициенты:")], *grid, [sg.Button("Подтвердить")]]
        window = sg.Window("Матрица", layout)
        while True:
            event, values = window.read()
            if event == "Подтвердить":
                try:
                    res_matrix = []
                    for r in range(n):
                        row = [float(values[f"m_{r}_{c}"]) for c in range(n)]
                        row.append(float(values[f"res_{r}"]))
                        res_matrix.append(row)
                    window.close()
                    return res_matrix
                except Exception:
                    sg.popup("Проверьте числа")
            if event is None:
                break
        window.close()
        return None

    @staticmethod
    def choose_accuracy() -> float | None:
        layout = [[sg.Text("Точность:")], [sg.Input(key="acc")], [sg.Button("OK")]]
        window = sg.Window("Точность", layout)
        event, values = window.read()
        window.close()
        return float(values["acc"]) if event == "OK" else None
