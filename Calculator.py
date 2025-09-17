import pygame
import UI as ui
import Constants as cts
pygame.init()


class UI:
    def __init__(self, sf, x, y, w, h, br):
        self.sf = sf
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.br = br
        self.layer = pygame.surface.Surface.subsurface(self.sf, (0, 20, self.w, self.h - 20))

        self.digits_buttons = [
            ["", "", ".", "C"],
            ["7", "8", "9", "+"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "*"],
            ["<", "0", "=", "/"]
        ]

        dbtn_w = int(self.w / (len(self.digits_buttons[0]) + 1))
        current_x = (self.w - dbtn_w * len(self.digits_buttons[0])) / (len(self.digits_buttons[0]) + 1)

        dbtn_h = int((self.h - 100) / (len(self.digits_buttons) + 1))
        current_y = (self.h - dbtn_h * len(self.digits_buttons)) / (len(self.digits_buttons) + 1) + 100

        space_x = current_x
        space_y = current_y - 125
        self.buttons = []

        for i in self.digits_buttons:
            for j in i:
                button = ui.Button(self.layer, current_x, current_y, dbtn_w, dbtn_h, str(j))
                self.buttons.append(button)
                current_x += dbtn_w + space_x
            current_y += dbtn_h + space_y
            current_x = space_x

        self.label = ui.Label(self.layer, 10, 30, self.w - 20, 70, "")

    def check_event(self, event):
        for button in self.buttons:
            button.check_event(event)
            if button.status == "active":
                button.status = "inactive"
                if not self.label.txt:
                    self.label.txt = str("")
                if button.text == "C":
                    self.label.txt = ""
                elif button.text == "<":
                    self.label.txt = self.label.txt[:-1]
                elif button.text == "()":
                    if self.br % 2 == 0:
                        self.label.txt += "("
                    else:
                        self.label.txt += ")"
                    self.br += 1
                elif button.text != "=":
                    self.label.txt = str(self.label.txt) + button.text
                else:
                    return 1

    def update(self, txt, pre):
        for button in self.buttons:
            button.update()
        if type(txt) == str and txt != pre:
            self.label.update()

    def draw(self):
        for button in self.buttons:
            button.draw(self.layer)
        self.label.draw(self.layer)


class Main:
    def __init__(self):
        self.txt = ""
        self.pre = ""

        self.text = ""
        self.ui = None
        self.tag = None

        self.x = cts.win_width / 2
        self.y = 10
        self.w = 700
        self.h = 700

        self.brackets = 0

        self.tag_img = "Counter_icon.png/"
        self.name = "Calculator"

    def create_tag(self, x, y, sf):
        self.tag = ui.Tag(x, y, "Counter_icon.png/", "Program", "", self.name, sf)
        return self.tag

    def wait_for_tag(self, sf, x, y, from_file):
        if not self.ui:
            self.ui = UI(sf, x, y + 20, self.w, self.h - 20, self.brackets)

    def compute(self):
        self.text = self.ui.label.txt
        numbers = []
        ops = []
        current_number = ""
        pr = 0
        if self.text:
            for i in range(len(self.text)):
                if i == 0 and self.text[i] == "-":
                    current_number += str(self.text[i])
                elif self.text[i] not in ["+", "-", "*", "/", "(", ")"]:
                    current_number += str(self.text[i])
                else:
                    numbers.append(current_number)
                    current_number = ""
                    ops.append(self.text[i])
            numbers.append(current_number)

            print(ops, numbers)
            for i in range(1, len(ops) + 1):
                if ops[i - 1] == "*" or ops[i - 1] == "/":
                    ind = 999
                    if "+" in ops:
                        ind = ops.index("+")
                    elif "-" in ops:
                        ind = ops.index("-")
                    if ind < i - 1:
                        ops[ind], ops[i - 1] = ops[i - 1], ops[ind]
                        print(numbers[ind], numbers[ind + 1], numbers[i], numbers[i - 1])
                        if numbers[i - 1] == numbers[ind + 1]:
                            numbers[ind], numbers[i] = numbers[i], numbers[ind]
                        else:
                            numbers[ind], numbers[ind + 1], numbers[i - 1], numbers[i] =\
                                numbers[i - 1], numbers[i], numbers[ind], numbers[ind + 1]

            print(ops, numbers)

            if "." in self.text:
                res = float(numbers[0])
            else:
                res = int(numbers[0])

            for j in range(1, len(ops) + 1):
                if "." in self.text:
                    if ops[j - 1] == "+":
                        res += float(numbers[j])
                    elif ops[j - 1] == "-":
                        res -= float(numbers[j])
                    elif ops[j - 1] == "*":
                        res *= float(numbers[j])
                    elif ops[j - 1] == "/":
                        res /= float(numbers[j])
                else:
                    if ops[j - 1] == "+":
                        res += int(numbers[j])
                    elif ops[j - 1] == "-":
                        res -= int(numbers[j])
                    elif ops[j - 1] == "*":
                        res *= int(numbers[j])
                    elif ops[j - 1] == "/":
                        res /= int(numbers[j])
            return str(res)

    def check_event(self, event=None):
        cmd = self.ui.check_event(event)
        if cmd:
            self.ui.label.txt = self.compute()

    def update(self):
        self.ui.update(self.txt, self.pre)

    def draw(self):
        self.ui.draw()

