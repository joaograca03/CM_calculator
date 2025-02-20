import flet as ft


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
                ]
            ),
        )

    
    def button_clicked(self, e):
        if e.control.data == "AC":  
            self.result.value = "0"
        elif e.control.data == "CE":  
            self.result.value = "0"
        elif e.control.data == "⬅️":  
            self.result.value = self.result.value[:-1] if self.result.value else "0"
            if not self.result.value:
                self.result.value = "0"
        else:
            
            if self.result.value == "0":
                self.result.value = e.control.data
            else:
                self.result.value += e.control.data
        self.update()

def main(page: ft.Page):
    page.title = "Calculadora Simples"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = CalculatorApp()
    page.add(calc)

ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=3000)
