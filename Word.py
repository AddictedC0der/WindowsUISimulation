import pygame
import UI as ui
import Constants as cts
import random
pygame.init()


class UI:
    def __init__(self, sf, x, y, w, h):
        self.sf = sf
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.indents = 50
        self.size = 18
        self.color = cts.black
        self.font = "Arial"
        self.layer = pygame.surface.Surface.subsurface(self.sf, (0, 20, self.w, self.h - 20))
        self.file = pygame.surface.Surface.subsurface(self.layer, (0, 50, self.layer.get_width(),
                                                                   self.layer.get_height() - 50))
        self.top_panel = ui.Panel(self.layer, 0, 0, self.w, 100, cts.blue)
        self.input1 = ui.TextInput(self.file, self.indents, self.file.get_rect().y + 70, self.file.get_width() -
                                   self.indents - 10, self.file.get_height() - 80, cts.white, cts.black, self.font,
                                   self.color, self.size, "", False)
        self.buttons_blueprint = ["save", "font", "size", "color", "indents"]
        self.buttons = []
        self.labels_blueprint = ["Save", "Font", "Font size", "Font color", "Indents"]
        self.labels = []
        current_x = 50
        self.underlabel_moduels = []
        self.text = None
        self.desc = ""
        self.cmd = None

        self.from_file = False
        self.storage = None

        for i in self.labels_blueprint:
            if i != "Save":
                input2 = ui.TextInput(self.top_panel.img, current_x, 50, 100, 40, cts.white, cts.blue, "Arial",
                                      cts.black, 15, i, False)
                self.underlabel_moduels.append(input2)
            else:
                btn = ui.Button(self.top_panel.img, current_x, 50, 100, 40, "Save", "save")
                self.underlabel_moduels.append(btn)

            current_x += 170

        current_x = 50
        for i in self.labels_blueprint:
            label = ui.Label(self.layer, current_x, 20, 80, 30, i, cts.white, "Arial", 19, cts.blue, cts.blue)
            self.labels.append(label)
            current_x += 170

    def check_event(self, event):
        self.top_panel.check_event(event)
        self.input1.check_event(event)
        for i in self.underlabel_moduels:
            if isinstance(i, ui.TextInput):
                if not self.text:
                    self.text = i.check_event(event)
                    self.desc = i.hint

                else:
                    break
            else:
                if self.input1.text:
                    self.cmd = i.check_event(event)

        if self.text:
            if self.desc == "Font size":
                self.size = int(self.text)
                self.input1.font_size = self.size
            elif self.desc == "Font color":
                self.color = tuple(map(int, self.text.split(", ")))
                self.input1.font_color = self.color
            elif self.desc == "Indents":
                self.indents = int(self.text)
                self.input1.x = self.indents + 100
                self.input1.w = self.file.get_width() - self.indents
            elif self.desc == "Font":
                self.font = str(self.text)
                self.input1.font = self.font
            self.text = None

    def update(self):
        self.top_panel.update()
        self.input1.ratio()
        self.input1.update()
        for i in self.underlabel_moduels:
            i.update()

        for i in self.labels:
            i.ratio()
            i.update()

    def draw(self):
        self.top_panel.draw(self.layer)
        for i in self.underlabel_moduels:
            i.draw(self.top_panel.img)
        for i in self.labels:
            i.draw(self.top_panel)


class Main:
    def __init__(self, store):
        self.ui = None

        self.store = store

        self.w = 1300
        self.h = 900
        self.x = cts.win_width - self.w
        self.y = 0

        self.file_img = "docx.png/"
        self.name = "Word"
        self.tag_img = "Word_icon.png/"

        self.tag = None
        self.f = None

    def create_tag(self, x, y, sf):
        self.tag = ui.Tag(x, y, "Word_icon.png/", "Program", "", self.name, sf)
        return self.tag

    def wait_for_tag(self, sf, x, y, from_file):
        self.ui = UI(sf, x, y, self.w, self.h)
        self.ui.from_file = from_file[0]
        self.ui.storage = from_file[1]

    def create_file(self):
        if self.ui.cmd:
            if self.ui.cmd == "save":
                if not self.ui.from_file:
                    if self.ui.input1.text:
                        text_to_write = [self.ui.input1.text, str(self.ui.color), str(self.ui.size),
                                         str(self.ui.indents), str(self.ui.font)]
                        rand_name = str(random.randrange(-999999999, 999999999))
                        self.f = open(rand_name, "w+")
                        for i in text_to_write:
                            self.f.write(i)
                            self.f.write("\n")
                        self.f.close()
                    self.store[2].append([True, self.file_img, "Word", "Document.docx", "Word", self.f.name])
                else:
                    self.f = open(self.ui.storage, "w+")
                    self.f.truncate(0)
                    text_to_write = [self.ui.input1.text, str(self.ui.color), str(self.ui.size),
                                     str(self.ui.indents)]
                    for i in text_to_write:
                        self.f.write(i)
                        self.f.write("\n")
                    self.f.close()
                self.ui.cmd = None

    def check_event(self, event):
        self.create_file()
        self.ui.check_event(event)

    def update(self):
        self.ui.update()

    def draw(self):
        self.ui.draw()
