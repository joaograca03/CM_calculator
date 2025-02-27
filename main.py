import flet as ft
import sympy as sp
import datetime

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK

class CalculatorApp(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=32)
        self.expression = ft.Text(value="", color=ft.colors.GREY_500, size=24)
        self.history = self.load_history()  # Carrega o histórico do client storage
        self.history_list = ft.Column(visible=False)  # Coluna para exibir o histórico
        self.content = ft.Container(
            width=400,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[self.expression], alignment=ft.MainAxisAlignment.END),
                    ft.Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                            ExtraActionButton(text="CE", button_clicked=self.button_clicked),
                            ExtraActionButton(text="⬅️", button_clicked=self.button_clicked),
                            ActionButton(text="/", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="7", button_clicked=self.button_clicked),
                            DigitButton(text="8", button_clicked=self.button_clicked),
                            DigitButton(text="9", button_clicked=self.button_clicked),
                            ActionButton(text="*", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="4", button_clicked=self.button_clicked),
                            DigitButton(text="5", button_clicked=self.button_clicked),
                            DigitButton(text="6", button_clicked=self.button_clicked),
                            ActionButton(text="-", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="1", button_clicked=self.button_clicked),
                            DigitButton(text="2", button_clicked=self.button_clicked),
                            DigitButton(text="3", button_clicked=self.button_clicked),
                            ActionButton(text="+", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="0", button_clicked=self.button_clicked, expand=2),
                            DigitButton(text=".", button_clicked=self.button_clicked),
                            ActionButton(text="=", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="(", button_clicked=self.button_clicked),
                            ExtraActionButton(text=")", button_clicked=self.button_clicked),
                            ExtraActionButton(text="√", button_clicked=self.button_clicked),
                            ExtraActionButton(text="x²", button_clicked=self.button_clicked),
                            ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ]
                    ),
                    ft.ElevatedButton(text="Mostrar Histórico", on_click=self.toggle_history),
                    ft.ElevatedButton(text="Limpar Histórico", on_click=self.clear_history),
                    self.history_list
                ]
            ),
        )

    def format_number(self, value):
        try:
            num = float(str(value))
            return f"{num:,.10f}".replace(",", " ").rstrip("0").rstrip(".")
        except ValueError:
            return str(value)

    def button_clicked(self, e):
        if e.control.data == "AC":
            self.expression.value = ""
            self.result.value = "0"
        elif e.control.data == "CE":
            self.result.value = "0"
        elif e.control.data == "⬅️":
            self.result.value = self.result.value[:-1] if self.result.value else "0"
            if not self.result.value:
                self.result.value = "0"
        elif e.control.data == "=":
            try:
                full_expression = self.expression.value + self.result.value
                sympy_result = sp.N(sp.sympify(full_expression))
                formatted_result = self.format_number(sympy_result)
                self.add_to_history(full_expression, formatted_result)
                self.result.value = formatted_result
                self.expression.value = ""
            except Exception:
                self.result.value = "Erro"
        elif e.control.data == "+/-":
            if self.result.value.startswith("-"):
                self.result.value = self.result.value[1:]
            else:
                self.result.value = "-" + self.result.value
        elif e.control.data == "%":
            try:
                self.result.value = str(float(self.result.value) / 100)
            except:
                self.result.value = "Erro"
        elif e.control.data == "√":
            try:
                self.result.value = self.format_number(sp.N(sp.sqrt(float(self.result.value))))
            except:
                self.result.value = "Erro"
        elif e.control.data == "x²":
            try:
                self.result.value = self.format_number(float(self.result.value) ** 2)
            except:
                self.result.value = "Erro"
        else:
            if self.result.value == "0" or self.result.value == "Erro":
                self.result.value = e.control.data
            else:
                self.result.value += e.control.data
        self.update()

    def add_to_history(self, expression, result):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"expression": expression, "result": result, "time": timestamp}
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history.pop()
        self.save_history()

    def save_history(self):
        # Salva o histórico no client storage
        self.page.client_storage.set("calc_history", self.history)

    def load_history(self):
        # Carrega o histórico do client storage
        return self.page.client_storage.get("calc_history") or []

    def toggle_history(self, e):
        if self.history_list.visible:
            self.history_list.visible = False
        else:
            self.history_list.controls = [
                ft.Row(
                    [
                        ft.Text(f"{i+1}. {item['expression']} = {item['result']}"),
                        ft.IconButton(icon=ft.icons.COPY, on_click=lambda _, r=item['result']: self.copy_to_clipboard(r)),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda _, idx=i: self.delete_from_history(idx))
                    ]
                )
                for i, item in enumerate(self.history)
            ]
            self.history_list.visible = True
        self.update()

    def copy_to_clipboard(self, result):
        print(f"Copiado: {result}")

    def delete_from_history(self, idx):
        if 0 <= idx < len(self.history):
            self.history.pop(idx)
            self.save_history()
            self.toggle_history(None)

    def clear_history(self, e):
        self.history = []
        self.save_history()
        self.toggle_history(None)

def main(page: ft.Page):
    page.title = "Calculadora Avançada"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = CalculatorApp(page)
    page.add(calc, calc.history_list)

ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=3000, assets_dir="assets")