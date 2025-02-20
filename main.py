import flet as ft
import sympy as sp  # Biblioteca para cálculos matemáticos avançados

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

# Classe para botões de operações (+, -, *, /, =)
class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

# Classe para botões de ações extras (AC, CE, ⬅️, √, x², %)
class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        super().__init__(text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK

# Classe principal da calculadora
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=32)
        self.expression = ""  # Armazena a expressão atual para avaliação

        # Layout da calculadora com botões básicos, extras, avançados e o botão "="
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
                ]
            ),
        )

    # Manipular cliques nos botões
    def button_clicked(self, e):
        if e.control.data == "AC":  # Limpar tudo
            self.result.value = "0"
            self.expression = ""
        elif e.control.data == "CE":  # Limpar a entrada atual
            self.result.value = "0"
        elif e.control.data == "⬅️":  # Remover o último caractere
            self.result.value = self.result.value[:-1] if self.result.value else "0"
            if not self.result.value:
                self.result.value = "0"
        elif e.control.data == "=":  # Avaliar a expressão
            try:
                # Avaliar a expressão usando sympy
                self.expression += self.result.value
                resultado = sp.N(sp.sympify(self.expression))
                self.result.value = str(resultado)
                self.expression = ""
            except Exception:
                self.result.value = "Erro"
        elif e.control.data == "√":  # Calcular raiz quadrada
            try:
                valor = float(self.result.value)
                if valor >= 0:
                    self.result.value = str(sp.N(sp.sqrt(valor)))
                else:
                    self.result.value = "Erro"
            except Exception:
                self.result.value = "Erro"
        elif e.control.data == "x²":  # Calcular o quadrado do número
            try:
                valor = float(self.result.value)
                self.result.value = str(valor ** 2)
            except Exception:
                self.result.value = "Erro"
        elif e.control.data == "%":  # Calcular a porcentagem
            try:
                valor = float(self.result.value)
                self.result.value = str(valor / 100)
            except Exception:
                self.result.value = "Erro"
        else:
            # Adicionar números e operadores
            if self.result.value == "0" or self.result.value == "Erro":
                self.result.value = e.control.data
            else:
                self.result.value += e.control.data
        self.update()

# Função principal para rodar a calculadora
def main(page: ft.Page):
    page.title = "Calculadora Avançada"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=3000)
