import flet as ft
import sympy as sp
import datetime
import json


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
    def __init__(self):
        super().__init__()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=32)
        self.expression = ""  
        self.history = self.load_history()  
        self.history_list = ft.Column(visible=False)  

        
        self.content = ft.Container(
            width=400,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                    ft.Row(
                        controls=[
                            ExtraActionButton("AC", self.button_clicked),
                            ExtraActionButton("CE", self.button_clicked),
                            ExtraActionButton("⬅️", self.button_clicked),
                            ActionButton("/", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("7", self.button_clicked),
                            DigitButton("8", self.button_clicked),
                            DigitButton("9", self.button_clicked),
                            ActionButton("*", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("4", self.button_clicked),
                            DigitButton("5", self.button_clicked),
                            DigitButton("6", self.button_clicked),
                            ActionButton("-", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("1", self.button_clicked),
                            DigitButton("2", self.button_clicked),
                            DigitButton("3", self.button_clicked),
                            ActionButton("+", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("0", self.button_clicked, expand=2),
                            DigitButton(".", self.button_clicked),
                            ActionButton("=", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ExtraActionButton("√", self.button_clicked),
                            ExtraActionButton("x²", self.button_clicked),
                            ExtraActionButton("%", self.button_clicked),
                        ]
                    ),
                    ft.ElevatedButton("Mostrar Histórico", on_click=self.toggle_history),
                    ft.ElevatedButton("Limpar Histórico", on_click=self.clear_history),
                    self.history_list,
                ]
            ),
        )

    
    def button_clicked(self, e):
        if e.control.data == "AC":
            self.result.value = "0"
            self.expression = ""
        elif e.control.data == "CE":
            self.result.value = "0"
        elif e.control.data == "⬅️":
            self.result.value = self.result.value[:-1] if self.result.value else "0"
            if not self.result.value:
                self.result.value = "0"
        elif e.control.data == "=":
            try:
                self.expression += self.result.value
                resultado = sp.N(sp.sympify(self.expression))
                self.add_to_history(self.expression, resultado)
                self.result.value = str(resultado)
                self.expression = ""
            except Exception:
                self.result.value = "Erro"
        elif e.control.data == "√":
            try:
                valor = float(self.result.value)
                if valor >= 0:
                    resultado = sp.N(sp.sqrt(valor))
                    self.add_to_history(f"√({valor})", resultado)
                    self.result.value = str(resultado)
                else:
                    self.result.value = "Erro"
            except Exception:
                self.result.value = "Erro"
        elif e.control.data == "x²":
            try:
                valor = float(self.result.value)
                resultado = valor ** 2
                self.add_to_history(f"({valor})²", resultado)
                self.result.value = str(resultado)
            except Exception:
                self.result.value = "Erro"
        elif e.control.data == "%":
            try:
                valor = float(self.result.value)
                resultado = valor / 100
                self.add_to_history(f"{valor}%", resultado)
                self.result.value = str(resultado)
            except Exception:
                self.result.value = "Erro"
        else:
            if self.result.value == "0" or self.result.value == "Erro":
                self.result.value = e.control.data
            else:
                self.result.value += e.control.data
        self.update()

    
    def add_to_history(self, expression, result):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.insert(0, {"expression": expression, "result": str(result), "time": timestamp})
        if len(self.history) > 10:
            self.history.pop()  
        self.save_history()

    
    def save_history(self):
        with open("calc_history.json", "w") as f:
            json.dump(self.history, f)

    
    def load_history(self):
        try:
            with open("calc_history.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    
    def toggle_history(self, e):
        if self.history_list.visible:
            self.history_list.visible = False
        else:
            self.history_list.controls = [
                ft.Text(f"{item['time']} - {item['expression']} = {item['result']}")
                for item in self.history
            ]
            self.history_list.visible = True
        self.update()

    
    def clear_history(self, e):
        self.history = []
        self.save_history()
        self.toggle_history(None)


def main(page: ft.Page):
    page.title = "Calculadora Avançada"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=3000)
