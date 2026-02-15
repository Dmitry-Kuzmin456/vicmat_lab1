from calculations import Calculations
from gui import MatrixWindow
from models import Result
import FreeSimpleGUI as sg


def main():
    data = MatrixWindow.start()
    if not data:
        return

    calc = Calculations(data)

    if not calc.find_diagonally_dominant():
        sg.popup_error(
            "Диагональное преобладание не достигнуто и не может быть получено перестановкой"
        )
        return

    try:
        res: Result = calc.solve()

        output = [
            f"Норма матрицы преобразования: {res.norm:.4f}",
            f"Количество итераций: {res.iterations}",
            "\nВектор неизвестных:",
        ]
        for i, val in enumerate(res.x):
            output.append(f"x{i + 1} = {val:.6f}")

        output.append("\nВектор погрешностей:")
        for i, err in enumerate(res.errors):
            output.append(f"e{i + 1} = {err:.10f}")

        sg.popup_scrolled("\n".join(output), title="Результаты")

    except Exception as e:
        sg.popup_error(f"Ошибка вычислений: {e}")


if __name__ == "__main__":
    main()
