import pygame
import UI as ui
import Constants as cts


class Icon:
    def __init__(self, sf, x, y, img, aim="color"):
        self.sf = sf
        self.x = x
        self.y = y
        self.layer = pygame.surface.Surface.subsurface(self.sf, (self.x, self.y, 30, 30))
        self.img = pygame.image.load(img).convert_alpha()
        self.w = self.layer.get_width()
        self.h = self.layer.get_height()
        self.aim = aim

    def check_event(self, event):
        mouse = pygame.mouse.get_pos()
        pos = self.layer.get_abs_offset()
        check = pos[0] < mouse[0] < pos[0] + self.w and pos[1] < mouse[1] < pos[1] + self.h

        if event.type == pygame.MOUSEBUTTONDOWN:
            if check:
                return self.aim

    def update(self):
        self.layer.fill(cts.white)
        self.layer.blit(self.img, (0, 0))


class Panel:
    def __init__(self, sf, x, y, sense, color, img=""):
        self.sf = sf
        self.x = x
        self.y = y
        self.layer = pygame.surface.Surface.subsurface(self.sf, (x, y, 300, 300))
        self.sense = sense
        if self.sense != "size":
            self.img = pygame.image.load(img).convert_alpha()
        self.color = color
        if self.sense == "size":
            self.input = ui.TextInput(self.layer, self.x / 2, self.y / 2, 100, 50, self.color, cts.black, "Arial",
                                      cts.black, 18, "", False)
            self.input.hint = "size"

    def check_event(self, event):
        size = None
        if self.sense == "size":
            size = self.input.check_event(event)
        mouse = pygame.mouse.get_pos()
        pos = self.layer.get_abs_offset()
        check = pos[0] < mouse[0] < pos[0] + 300 and pos[1] < mouse[1] < pos[1] + 300
        if size:
            return size, self.input.hint
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if check and self.sense == "color" or self.sense == "fill":
                    x = mouse[0] - pos[0]
                    y = mouse[1] - pos[1]
                    color = self.img.get_at((x, y))
                    return color, self.sense

    def update(self):
        self.layer.fill(cts.white)
        if self.sense == "color" or self.sense == "fill":
            self.layer.blit(self.img, (0, 0))
        elif self.sense == "size":
            self.layer.fill(self.color)
            self.input.update()

    def draw(self):
        pass
        # self.sf.blit(self.layer, self.layer_rect)


class UI:
    def __init__(self, sf, x, y, w, h):
        self.sf = sf
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.color = (0, 0, 0)
        self.size = 5

        self.layer = pygame.surface.Surface.subsurface(self.sf, (0, 20, self.w, self.h - 20))
        self.file = pygame.surface.Surface.subsurface(self.layer, (0, 50, self.layer.get_width(), self.layer.get_height() - 50))
        self.save = None
        self.top_panel = ui.Panel(self.layer, 0, 0, self.w, 50, cts.light_red)
        self.icons = []
        self.panels = []

        self.images = ["color_map.png"]

        self.change = False
        self.btn_cmd = None

        self.from_file = False
        self.storage = None

        self.top_panel_btns_img = ["palette.png", "size.png"]
        self.top_panel_btns_aims = ["color", "size"]

        self.save_btn = ui.Button(self.top_panel.img, 30, 10, 60, 30, "Save", "save")
        current_x = 120
        for i in range(len(self.top_panel_btns_img)):
            icon = Icon(self.top_panel.img, current_x, 10, self.top_panel_btns_img[i], self.top_panel_btns_aims[i])
            self.icons.append(icon)
            current_x += 60

    def check_event(self, event):
        self.top_panel.check_event(event)
        if self.save:
            self.btn_cmd = self.save_btn.check_event(event)
        for i in self.icons:
            cmd = i.check_event(event)

            if cmd == "color" and not self.panels:
                panel = Panel(self.layer, 10, self.top_panel.img.get_height() + 5, "color", cts.light_red,
                              self.images[0])
                self.panels.append(panel)
                self.change = True

            elif cmd == "size" and not self.panels:
                panel = Panel(self.layer, 10, self.top_panel.img.get_height() + 5, "size", cts.light_red)
                self.panels.append(panel)
                self.change = True

            elif cmd == "fill" and not self.panels:
                panel = Panel(self.layer, 10, self.top_panel.img.get_height() + 5, "fill", cts.light_red,
                              self.images[0])
                self.panels.append(panel)
                self.change = True

        if self.panels:
            cmd = self.panels[0].check_event(event)
            digital = None
            if type(cmd) == tuple:
                if cmd[1] == "size":
                    digital = int(cmd[0])
                    self.size = digital
                elif cmd[1] == "color":
                    self.color = cmd[0]
                elif cmd[1] == "fill":
                    self.file.fill(cmd[0])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.file.fill(self.color)
                self.save = pygame.surface.Surface.copy(self.file)

        if event.type == pygame.MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
            pos = self.file.get_abs_offset()
            check = pos[0] < mouse[0] < pos[0] + self.file.get_width() and \
                    pos[1] < mouse[1] < pos[1] + self.file.get_height()

            if check:
                curs = pygame.mouse.get_cursor()
                if curs != pygame.SYSTEM_CURSOR_CROSSHAIR:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

            pressed = pygame.mouse.get_pressed(3)[0]
            if pressed and not self.panels:
                x = mouse[0] - pos[0]
                y = mouse[1] - pos[1]
                pygame.draw.rect(self.file, self.color, (x, y, self.size, self.size))
                if not self.change:
                    self.save = pygame.Surface.copy(self.file)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            pos = self.file.get_abs_offset()
            check = pos[0] < mouse[0] < pos[0] + self.file.get_width() and\
                pos[1] < mouse[1] < pos[1] + self.file.get_height()
            check2 = False
            if self.panels:
                panel = self.panels[0].layer.get_abs_offset()
                check2 = panel[0] < mouse[0] < panel[0] + self.panels[0].layer.get_width() and\
                    panel[1] < mouse[1] < panel[1] + self.panels[0].layer.get_height()

            if event.button == 1 and check and not check2:
                if self.panels:
                    self.panels.clear()
                    self.file.fill(cts.white)
                x = mouse[0] - pos[0]
                y = mouse[1] - pos[1]
                pygame.draw.rect(self.file, self.color, (x, y, self.size, self.size))
                if not self.panels and not self.change:
                    self.save = pygame.Surface.copy(self.file)

    def update(self):
        self.save_btn.update()
        self.file.fill(cts.white)
        self.top_panel.update()
        if self.save and not self.panels:
            self.file.blit(self.save, (0, 0))
            self.change = False
        for i in self.icons:
            i.update()

        for i in self.panels:
            i.update()

    def draw(self):
        self.save_btn.draw(self.top_panel.img)
        if self.panels:
            self.panels[0].draw()


class Main:
    def __init__(self, store):
        self.ui = None
        self.w = 1300
        self.h = 900
        self.x = cts.win_width - self.w
        self.y = 0

        self.store = store
        self.tag = None
        self.name = "Paint"
        self.file_img = "png.png/"
        self.tag_img = "Paint_icon.png/"

    def create_tag(self, x, y, sf):
        self.tag = ui.Tag(x, y, "Paint_icon.png/", "Program", "", self.name, sf)
        return self.tag

    def wait_for_tag(self, sf, x, y, from_file):
        self.ui = UI(sf, x, y + 20, self.w, self.h - 20)
        self.ui.from_file = from_file[0]
        self.ui.storage = from_file[1]

    def create_file(self):
        if self.ui.btn_cmd:
            if self.ui.btn_cmd == "save":
                if not self.ui.from_file:
                    if self.ui.save:
                        self.store[2].append([True, self.file_img, "Paint", "Picture.png", "Paint", self.ui.save])
                else:
                    self.ui.save = None
                self.ui.btn_cmd = None

    def check_event(self, event):
        self.create_file()
        self.ui.check_event(event)

    def update(self):
        self.ui.update()

    def draw(self):
        self.ui.draw()

