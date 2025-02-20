import flet as ft

# Classe base para os botões
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

# Classe para botões de dígitos (0-9)
class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__(text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

# Classe para botões de operações (+, -, *, /)
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

# Classe principal da calculadora
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=32)

        # Layout da calculadora com botões básicos
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
                            DigitButton("7", self.button_clicked),
                            DigitButton("8", self.button_clicked),
                            DigitButton("9", self.button_clicked),
                            ActionButton("/", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("4", self.button_clicked),
                            DigitButton("5", self.button_clicked),
                            DigitButton("6", self.button_clicked),
                            ActionButton("*", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("1", self.button_clicked),
                            DigitButton("2", self.button_clicked),
                            DigitButton("3", self.button_clicked),
                            ActionButton("-", self.button_clicked),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("0", self.button_clicked, expand=2),
                            DigitButton(".", self.button_clicked),
                            ActionButton("+", self.button_clicked),
                        ]
                    ),
                ]
            ),
        )

    # Manipular cliques nos botões
    def button_clicked(self, e):
        if self.result.value == "0":
            self.result.value = e.control.data
        else:
            self.result.value += e.control.data
        self.update()

# Função principal para rodar a calculadora
def main(page: ft.Page):
    page.title = "Calculadora Simples"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=3000)
