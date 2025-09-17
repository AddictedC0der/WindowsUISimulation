import pygame
import Constants as cts
import time
import Calculator
import Paint
import Folder
import os
pygame.init()


class TextInput:
    def __init__(self, sf, x, y, w, h, back_color=cts.white, border_color=cts.black, font="Arial",
                 font_color=cts.black, font_size=18, hint="", replace_txt=True):
        self.sf = sf
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.surface.Surface.subsurface(self.sf, (x, y, w, h))
        self.back_color = back_color
        self.border_color = border_color
        self.font_size = font_size
        self.font = font
        self.font_ini = pygame.font.SysFont(font, self.font_size)
        self.font_color = font_color
        self.hint = hint
        self.status = "Inactive"
        self.text = ""
        self.txt = self.font_ini.render(self.text, True, self.font_color)
        self.replace = replace_txt
        self.curs = 0
        self.ref = None

    def ratio(self):
        if self.txt.get_width() > self.w:
            self.text += '\n'
        if self.txt.get_height() > self.h:
            self.h += self.txt.get_height()

    def check_event(self, event):
        mouse = pygame.mouse.get_pos()
        pos = self.img.get_abs_offset()
        check = pos[0] < mouse[0] < pos[0] + self.w and pos[1] < mouse[1] < pos[1] + self.h
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and check:
                if self.status == "Inactive":
                    self.status = "Active"
                    if self.text:
                        edit = list(self.text)
                        edit.append("|")
                        self.text = str("".join(edit))
                        self.curs = len(edit)
                    else:
                        self.text = "|"
            else:
                self.status = "Inactive"
                edit = list(self.text)
                for i in edit:
                    if i == "|":
                        edit.remove(i)
                        self.text = str("".join(edit))

        if event.type == pygame.KEYDOWN:
            edit = list(self.text)
            if self.status == "Active":
                if event.key == pygame.K_BACKSPACE:
                    if self.curs > 0:
                        if len(edit) > self.curs:
                            edit.remove("|")
                            del edit[self.curs - 1]
                            self.curs -= 1
                            edit.insert(self.curs, "|")
                        else:
                            self.curs = len(edit) - 1
                elif event.key == pygame.K_RETURN:
                    self.status = "Inactive"
                    for i in edit:
                        if i == "|":
                            edit.remove(i)
                    self.text = str("".join(edit))
                    if self.ref:
                        return self.text, self.ref
                    else:
                        return self.text

                elif event.key == pygame.K_LEFT:
                    for i in edit:
                        if i == "|":
                            edit.remove(i)
                    if self.curs > 0:
                        self.curs -= 1
                    edit.insert(self.curs, "|")

                elif event.key == pygame.K_RIGHT:
                    for i in edit:
                        if i == "|":
                            edit.remove(i)
                    if self.curs < len(edit):
                        self.curs += 1
                    edit.insert(self.curs, "|")

                else:
                    if "|" in edit:
                        edit.remove("|")
                    edit.insert(self.curs, event.unicode)
                    self.curs += 1
                    edit.insert(self.curs, "|")

                self.text = str("".join(edit))

    def update(self):
        if self.status == "Inactive" and self.replace:
            self.text = self.hint
        self.img.fill(self.back_color)
        pygame.draw.rect(self.img, self.border_color, (0, 0, self.w - 1, self.h - 1), 2)
        self.font_ini = pygame.font.SysFont(self.font, self.font_size)
        self.txt = self.font_ini.render(self.text, True, self.font_color)
        self.img.blit(self.txt, (10, 10))

    def draw(self, sf):
        pass


class Label:
    def __init__(self, sf, x, y, w, h, txt="", color=cts.black, font="Arial", font_size=18, back_color=cts.black,
                 border_color=cts.black):
        self.sf = sf
        self.img = pygame.Surface.subsurface(self.sf, (x, y, w, h))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.color = color
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, self.font_size)
        self.txt = txt
        self.text = self.font.render(self.txt, True, self.color)
        self.back_color = back_color
        self.border_color = border_color

    def ratio(self):
        if self.img_rect.w < self.text.get_rect().width:
            ratio = self.text.get_rect().width - self.img_rect.w
            self.img_rect.w = ratio

    def update(self):
        self.img.fill(self.back_color)

    def draw(self, sf):
        self.text = self.font.render(self.txt, True, self.color)
        self.img.blit(self.text, (5, 5))
        pygame.draw.rect(self.img, self.border_color, (0, 0, self.img_rect.w, self.img_rect.h), 1)


class Button:
    def __init__(self, sf, x, y, w, h, text="", cmd=""):
        self.sf = sf
        self.img = pygame.Surface.subsurface(self.sf, (x, y, w, h))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.text = text
        self.font = pygame.font.SysFont("Arial", 24)
        self.inactive_color = cts.white
        self.active_color = cts.gray
        self.hovered_color = cts.silver
        self.font_color = cts.black
        self.current_color = self.inactive_color
        self.txt = self.font.render(self.text, True, self.font_color)
        self.cmd = cmd
        self.status = "inactive"
        self.ref = None
        self.img.fill(self.current_color)

    def check_event(self, event):
        mouse = pygame.mouse.get_pos()
        pos = self.img.get_abs_offset()
        check = pos[0] <= mouse[0] <= pos[0] + self.img_rect.w and pos[1] <= mouse[1] <= pos[1] + self.img_rect.h
        if event.type == pygame.MOUSEMOTION:
            if check:
                self.status = "hovered"
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

            else:
                self.status = "inactive"
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEBUTTONUP:
            if check and event.button == 1:
                self.status = "active"
            else:
                self.status = "inactive"

        if self.status == "active":
            if self.ref:
                return self.cmd, self.ref
            else:
                return self.cmd

    def update(self):
        if self.status == "inactive":
            self.current_color = self.inactive_color
        elif self.status == "active":
            self.current_color = self.active_color
        elif self.status == "hovered":
            self.current_color = self.hovered_color

        self.img.fill(self.current_color)

    def draw(self, sf):
        self.img.fill(self.current_color)
        text_w = self.txt.get_rect().width
        text_h = self.txt.get_rect().height
        self.img.blit(self.txt, (self.img_rect.w / 2 - text_w / 2, self.img_rect.h / 2 - text_h / 2))
        pygame.draw.rect(sf, cts.black, self.img_rect, 1)


class Panel:
    def __init__(self, sf, x, y, w, h, color=cts.white):
        self.sf = sf
        self.img = pygame.Surface.subsurface(self.sf, (x, y, w, h))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.color = color
        self.buttons = []

    def check_event(self, event):
        mouse = pygame.mouse.get_pos()
        pos = self.img.get_abs_offset()
        check = pos[0] < mouse[0] < pos[0] + self.img_rect.w and pos[1] < mouse[1] < pos[1] + self.img_rect.h
        for button in self.buttons:
            cmd = button.check_event(event)
            if cmd:
                return cmd
        if check:
            return 1
        else:
            return 0

    def update(self):
        self.img.fill(self.color)
        for button in self.buttons:
            button.update()

    def draw(self, sf):
        for button in self.buttons:
            button.draw(self.img)


class Window:
    def __init__(self, sf, x, y, w, h, color=cts.white, tag="Desktop", ref=None):
        self.sf = sf
        self.img = pygame.surface.Surface.subsurface(self.sf, (x, y, w, h))
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.color = color
        self.tag = tag
        self.status = "Opened"
        self.active = True
        self.buttons = []
        self.panels = []
        self.bind = None
        self.img.unlock()
        self.ref = ref
        if self.ref:
            self.tag_img = self.ref.tag_img

        self.motion1 = None
        self.motion2 = None

    def draw_modules(self):
        if self.tag == "Start_menu":
            if not self.panels:
                self.sm_side_panel = Panel(self.img, self.img_rect.right / 2, 0, self.img_rect.right / 2,
                                           self.img_rect.height, cts.dark_gray)

                self.panels.append(self.sm_side_panel)

            if not self.sm_side_panel.buttons:
                self.stop_btn = Button(self.sm_side_panel.img, 20, self.sm_side_panel.img_rect.height - 50,
                                       self.sm_side_panel.img_rect.w / 1.2, 30, "Work conclusion", "Exit")
                self.sm_side_panel.buttons.append(self.stop_btn)

        elif self.tag == "Folder" or self.tag == "Program":
            if not self.panels:
                self.top_panel = Panel(self.img, 0, 0, self.img_rect.w, 20, cts.dark_gray)
                self.panels.append(self.top_panel)

            if not self.top_panel.buttons:
                if self.tag != "Program":
                    top_panel_w = 60
                    top_panel_x = self.img.get_width() - top_panel_w
                    text = ["-", "<>", "x"]
                    cmd = ["Flex", "Full", "Close"]
                else:
                    top_panel_w = 40
                    top_panel_x = self.img.get_width() - top_panel_w
                    text = ["-", "x"]
                    cmd = ["Flex", "Close"]

                for i in range(len(text)):
                    self.btn = Button(self.top_panel.img, top_panel_x, 0, 20, 20, text[i], cmd[i])
                    top_panel_x += 20
                    self.top_panel.buttons.append(self.btn)

        pygame.draw.rect(self.img, cts.black, (0, 0, self.img.get_width(), self.img.get_height()), 1)

    def check_event(self, event=None):
        if self.tag == "Folder" or self.tag == "Program":
            mouse = pygame.mouse.get_pos()
            pos = self.img.get_abs_offset()
            check = pos[0] < mouse[0] < pos[0] + self.img_rect.w and pos[1] < mouse[1] < pos[1] + self.img_rect.h
            pressed = pygame.mouse.get_pressed(3)[0]

            if self.status == "Opened":
                if event.type == pygame.MOUSEMOTION:
                    if pressed and check:
                        if not self.motion1:
                            self.motion1 = pygame.mouse.get_rel()
                        else:
                            self.motion2 = pygame.mouse.get_rel()
                            self.img_rect.x += self.motion2[0]
                            self.img_rect.y += self.motion2[1]

            for panel in self.panels:
                cmd = panel.check_event(event)
                if cmd == "Full" and self.status == "Full_sc":
                    if self.bind:
                        return "Window"
                    else:
                        return cmd
                elif cmd:
                    return cmd

        elif self.tag == "Start_menu":
            mouse = pygame.mouse.get_pos()
            pos = self.img.get_abs_offset()
            check = pos[0] < mouse[0] < pos[0] + self.img_rect.w and pos[1] < mouse[1] < pos[1] + self.img_rect.h

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not check:
                    return "Close"

            cmd = self.sm_side_panel.check_event(event)
            return cmd

    def update(self):
        self.img.fill(self.color)
        self.draw_modules()

        for panel in self.panels:
            panel.update()

        for button in self.buttons:
            button.update()

    def draw(self, sf):
        # sf.blit(self.img, self.img_rect)
        for button in self.buttons:
            button.draw(self.img)
        for panel in self.panels:
            panel.draw(self.img)


class Tag:
    def __init__(self, x, y, img="Word_icon.png", tag="Folder", ref="", name="New Folder", sf=None):
        self.sf = sf
        self.txt_img = img
        self.img = pygame.image.load(img[:-1]).convert_alpha()
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x
        self.img_rect.y = y
        self.first_click = False
        self.layer = None
        self.layer = pygame.surface.Surface.subsurface(self.sf, (self.img_rect.x, self.img_rect.y, 50, 50))
        self.tag = tag
        self.ref = ref
        self.name = name
        self.name_txt = None
        self.font = pygame.font.SysFont("Arial", 18)
        self.font_color = cts.white
        self.font_padding = 5
        self.cont = None
        self.is_in_folder = False
        self.folder = None
        self.start = None

    def check_event(self, i):
        mouse = pygame.mouse.get_pos()
        if not self.is_in_folder:
            check = self.img_rect.left < mouse[0] < self.img_rect.right and self.img_rect.top < mouse[1] <\
                self.img_rect.bottom
        else:
            pos = self.layer.get_abs_offset()
            check = pos[0] < mouse[0] < pos[0] + self.img_rect.w and pos[1] < mouse[1] < pos[1] + self.img.get_rect().h

        if i.type == pygame.MOUSEMOTION:
            if check:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1 and check:
                if not self.first_click:
                    self.first_click = True
                    self.start = pygame.time.get_ticks()
                else:
                    current = pygame.time.get_ticks()
                    if (current - self.start) < 400:
                        self.first_click = False
                        return "Open folder", self.tag, self.ref, self.cont

                    else:
                        self.first_click = False

            elif i.button == 3 and check:
                if self.layer:
                    c = self.layer.get_abs_offset()
                    return "Open panel", self, c, self.img_rect
                else:
                    return "Open panel", self, self.img_rect

        return None, ""

    def update(self):
        pass

    def draw(self, sf):
        sf.blit(self.img, self.img_rect)
        self.name_txt = self.font.render(self.name, True, self.font_color)
        sf.blit(self.name_txt, (self.img_rect.x + 5, self.img_rect.y + self.img_rect.h + self.font_padding))


class UI:
    def __init__(self, sf, store):
        self.sf = sf
        self.desktop = Window(self.sf, 0, 0, cts.win_width, cts.win_height, cts.gray)
        self.windows = [self.desktop]
        self.windows_rect = []
        self.tags = []
        self.inputs = []
        self.store = store
        self.full_window = None

        self.btm_panel_icons = {}
        self.btm_panel_x = 60

        # Tag data
        self.w = None
        self.h = None
        self.current_x = None
        self.current_y = None
        self.dt_cmd = None
        self.input_txt = None
        self.dragging = (False, None)

        self.btm = None

        # Sounds
        self.folder_open_sound = pygame.mixer.Sound("sound_04676.mp3")

    def upgrade_desktop(self):
        self.btm = Panel(self.desktop.img, 0, cts.win_height - 50, cts.win_width, 50, (90, 90, 90))
        self.btm.update()
        self.btm.draw(self.sf)

        epoch = time.time()
        current_time = time.ctime(epoch)
        local_time = Label(self.btm.img, self.btm.img_rect.w - 150, self.btm.img_rect.h - 50, 145, 45, current_time,
                           cts.white, "Arial", 14, (90, 90, 90), (90, 90, 90))

        local_time.ratio()
        local_time.update()
        local_time.draw(self.btm.img)

        if not self.tags:
            start = Tag(self.btm.img_rect.x + 5, self.btm.img_rect.y, "Start_icon.png\n", "Start", "", "",
                        self.desktop.img)
            self.tags.append(start)

            self.w = 101
            self.h = 101
            self.current_x = 50
            self.current_y = 50

            for i in self.store[0]:
                if self.current_y + self.h + 50 < cts.win_height - 50:
                    tag = i.create_tag(self.current_x, self.current_y, self.desktop.img)
                    self.tags.append(tag)
                    self.current_y += (self.h + 50)
                else:
                    self.current_x += (self.w + 50)
                    self.current_y = 50

        for i in self.store[1]:
            if not i.tag:
                if self.current_y + self.h + 50 < cts.win_height - 50:
                    tag = i.create_tag(self.current_x, self.current_y, self.desktop.img)
                    self.tags.append(tag)
                    self.current_y += (self.h + 50)
                else:
                    self.current_x += (self.w + 50)
                    self.current_y = 50

        for i in self.store[2]:
            if i[0]:
                if self.current_y + self.h + 50 < cts.win_height - 50:
                    tag = Tag(self.current_x, self.current_y, i[1], "Program", i[4], i[3], self.desktop.img)
                    tag.cont = i[5]
                    self.tags.append(tag)
                    i[0] = False
                    self.current_y += (self.h + 50)
                else:
                    self.current_x += (self.w + 50)
                    self.current_y = 50

    def check_event(self, event=None):
        if self.full_window:
            cmd = self.full_window.check_event(event)
            if cmd == "Window":
                self.full_window.bind.status = "Opened"
                self.windows.remove(self.full_window)
                self.windows_rect.remove(self.full_window.img_rect)
                del self.full_window
                self.full_window = None

        for window in self.windows:
            if window.tag == "Desktop":
                if window.panels:
                    self.dt_cmd = window.panels[0].check_event(event)
                    if self.dt_cmd == "Create Folder":
                        folder = Folder.Main()
                        self.store[1].append(folder)
                        del self.desktop.panels[-1]
                    elif type(self.dt_cmd) == tuple:
                        if self.dt_cmd[0] == "Rename":
                            print(self.dt_cmd)
                            if not self.dt_cmd[1].is_in_folder:
                                input1 = TextInput(self.desktop.img, self.dt_cmd[1].img_rect.x,
                                                   self.dt_cmd[1].img_rect.y + self.dt_cmd[1].img_rect.h,
                                                   self.dt_cmd[1].img_rect.w, 30, cts.white, cts.black, "Arial",
                                                   cts.black, 18, self.dt_cmd[1].name, False)
                            else:
                                input1 = TextInput(self.dt_cmd[1].folder.ui.layer, self.dt_cmd[1].img_rect.x,
                                                   self.dt_cmd[1].img_rect.y + self.dt_cmd[1].img_rect.h,
                                                   self.dt_cmd[1].img_rect.w, 30, cts.white, cts.black, "Arial",
                                                   cts.black, 18, self.dt_cmd[1].name, False)
                            input1.ref = self.dt_cmd[1]
                            self.dt_cmd[1].name = ""
                            self.inputs.append(input1)
                            del self.desktop.panels[-1]
                        elif self.dt_cmd[0] == "Delete":
                            self.dt_cmd = list(self.dt_cmd)
                            if len(self.dt_cmd) == 2:
                                if self.dt_cmd[1].cont:
                                    os.remove(self.dt_cmd[1].cont)
                                if self.dt_cmd[1].is_in_folder:
                                    for i in self.dt_cmd[1].folder.contents:
                                        if self.dt_cmd[1] in i:
                                            self.dt_cmd[1].folder.ui.files.remove(self.dt_cmd[1])
                                            self.dt_cmd[1].folder.contents.remove(i)
                                            break
                                    # self.dt_cmd[1].folder.contents.remove(self.dt_cmd[1])
                                self.tags.remove(self.dt_cmd[1])
                                del self.dt_cmd[1]
                            del self.desktop.panels[-1]
                            # self.current_y -= (self.h + 50)

                        elif self.dt_cmd[0] == "Withdraw":
                            for i in self.dt_cmd[1].folder.contents:
                                if i[1] == self.dt_cmd[1]:
                                    self.dt_cmd[1].folder.contents.remove(i)
                                    break
                            self.dt_cmd[1].folder.ui.files.remove(self.dt_cmd[1])
                            self.tags.append(self.dt_cmd[1])
                            self.dt_cmd[1].layer = self.desktop.img
                            self.dt_cmd[1].is_in_folder = False
                            self.dt_cmd[1].folder = None
                            self.dt_cmd[1].font_padding = 5
                            self.dt_cmd[1].font_color = cts.white
                            self.dt_cmd[1].img_rect.x = 50
                            self.dt_cmd[1].img_rect.y = self.current_y
                            self.dt_cmd[1].img = pygame.transform.smoothscale(self.dt_cmd[1].img, (101, 101))
                            del self.desktop.panels[-1]

                if self.input_txt:
                    self.input_txt[1].name = self.input_txt[0]
                    if not self.input_txt[1].name:
                        self.input_txt[1].name = "File"
                    del self.inputs[0]
                    self.input_txt = None

            if window.tag == "Program":
                if window.ref:
                    window.ref.check_event(event)
            win_cmd = window.check_event(event)

            if win_cmd == "Close":
                if window.tag == "Folder":
                    for i in window.ref.contents:
                        self.tags.remove(i[1])
                self.windows.remove(window)
                self.windows_rect.remove(window.img_rect)

                for i in self.btm_panel_icons.keys():
                    if self.btm_panel_icons[i] == window:
                        del self.btm_panel_icons[i]
                        # del self.btm_panel_icons[i]
                        self.btm_panel_x -= 50
                        break

                if window.status == "Full_sc":
                    self.full_window = None
                    self.windows.remove(window.bind)
                    del window.bind
                    del window
                    break

            elif win_cmd == "Full":
                window.status = "Full_sc"
                new = Window(self.desktop.img, 0, 0, cts.win_width, cts.win_height - self.btm.img.get_height(),
                             cts.white, window.tag)
                new.status = "Full_sc"
                self.full_window = new
                window.bind = new
                new.bind = window
                self.windows.append(new)
                self.windows_rect.append(new.img_rect)
            elif win_cmd == "Flex":
                self.windows.remove(window)
                self.windows_rect.remove(window.img_rect)

            elif win_cmd == "Exit":
                return "Exit"

        if event.type == pygame.MOUSEMOTION:
            pressed = pygame.mouse.get_pressed(3)[0]
            if pressed and not self.dragging[0]:
                mouse = pygame.mouse.get_pos()
                for i in self.tags:
                    pos = (i.img_rect.x, i.img_rect.y)
                    if pos[0] < mouse[0] < pos[0] + i.img_rect.w and pos[1] < mouse[1] < pos[1] + i.img_rect.h:
                        self.dragging = (True, i)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.dragging[0]:
                mouse = pygame.mouse.get_pos()
                for i in self.tags:
                    if i.tag == "Folder" and i != self.dragging[1]:
                        pos = (i.img_rect.x, i.img_rect.y)
                        if pos[0] < mouse[0] < pos[0] + i.img_rect.w and pos[1] < mouse[1] <\
                                pos[1] + i.img_rect.h:

                            for j in self.store[1]:
                                if i == j.tag:
                                    j.add_contents([self.dragging[1], self.dragging[1].tag,
                                                    self.dragging[1].txt_img, self.dragging[1].name])
                                    self.tags.remove(self.dragging[1])

                self.dragging = (False, None)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.desktop.panels:
                    if self.desktop.panels[-1].check_event(event) == 0:
                        del self.desktop.panels[-1]

            elif event.button == 3 and len(self.windows) == 1:
                if self.desktop.panels:
                    del self.desktop.panels[-1]
                mouse = pygame.mouse.get_pos()
                if mouse[0] + 200 < cts.win_width:
                    if mouse[1] + 280 < cts.win_height:
                        roll = Panel(self.desktop.img, mouse[0], mouse[1], 200, 280, cts.white)
                    else:
                        roll = Panel(self.desktop.img, mouse[0], mouse[1] - 280, 200, 280, cts.white)
                else:
                    roll = Panel(self.desktop.img, mouse[0] - 200, mouse[1], 200, 280, cts.white)
                if not roll.buttons:
                    btn = Button(roll.img, 0, 0, roll.img_rect.width, 20, "Create Folder", "Create Folder")
                    roll.buttons.append(btn)
                self.desktop.panels.append(roll)

        for i in self.btm_panel_icons.keys():
            cmd = i.check_event(event)
            if cmd[0] == "Open folder" and not self.btm_panel_icons[i] in self.windows:
                self.windows.append(self.btm_panel_icons[i])
                self.windows_rect.append(self.btm_panel_icons[i].img_rect)
        for tag in self.tags:
            tag_cmd = tag.check_event(event)
            if self.dt_cmd == "Open":
                tag_cmd[0] = "Open folder"

            if tag_cmd[0] == "Open panel":
                if self.desktop.panels:
                    del self.desktop.panels[-1]
                if tag_cmd[2][0] + tag_cmd[3].w + 5 + 200 < cts.win_width:
                    if tag_cmd[2][1] + 280 < cts.win_height:
                        roll = Panel(self.desktop.img, tag_cmd[2][0] + tag_cmd[3].w + 5, tag_cmd[2][1], 200, 280,
                                     cts.white)
                    else:
                        roll = Panel(self.desktop.img, tag_cmd[2][0] + tag_cmd[3].w + 5, tag_cmd[2][1] - 200, 200,
                                     280, cts.white)
                else:
                    roll = Panel(self.desktop.img, tag_cmd[2][0] - tag_cmd[3].w - 5 - 200, tag_cmd[2][1], 200, 280,
                                 cts.white)
                if not roll.buttons:
                    if tag_cmd[1].is_in_folder:
                        btn1 = Button(roll.img, 0, 20, roll.img_rect.width, 20, "Rename", "Rename")
                        btn2 = Button(roll.img, 0, 40, roll.img_rect.width, 20, "Delete", "Delete")
                        btn3 = Button(roll.img, 0, 60, roll.img_rect.width, 20, "Withdraw", "Withdraw")
                        btn1.ref = tag_cmd[1]
                        btn2.ref = tag_cmd[1]
                        btn3.ref = tag_cmd[1]
                        roll.buttons.append(btn1)
                        roll.buttons.append(btn2)
                        roll.buttons.append(btn3)
                    else:
                        btn1 = Button(roll.img, 0, 20, roll.img_rect.width, 20, "Rename", "Rename")
                        btn2 = Button(roll.img, 0, 40, roll.img_rect.width, 20, "Delete", "Delete")
                        btn1.ref = tag_cmd[1]
                        btn2.ref = tag_cmd[1]
                        roll.buttons.append(btn1)
                        roll.buttons.append(btn2)
                self.desktop.panels.append(roll)

            if tag_cmd[0] == "Open folder":
                self.folder_open_sound.play()
                if tag_cmd[1] == "Program":
                    if tag_cmd[2]:
                        if tag_cmd[2] == "Word":
                            for i in self.store[0]:
                                if i.name == "Word":
                                    new_win = Window(self.desktop.img, i.x, i.y, i.w, i.h, cts.white, "Program", i)
                                    self.windows.append(new_win)
                                    self.windows_rect.append(new_win.img_rect)
                                    f = open(tag_cmd[3], "r")
                                    contents = f.readlines()
                                    i.wait_for_tag(new_win.img, new_win.img_rect.x, new_win.img_rect.y, (True,
                                                                                                         tag_cmd[3]))
                                    i.ui.input1.text = contents[0][:-1]
                                    i.ui.color = contents[1][:-1]
                                    i.ui.size = contents[2][:-1]
                                    i.ui.indents = contents[3][:-1]
                                    i.ui.font = contents[4][:-1]
                                    f.close()

                                    tag = Tag(self.btm_panel_x, cts.win_height - 50, new_win.tag_img, new_win.tag,
                                              new_win.ref, "", self.desktop.img)
                                    tag.img = pygame.transform.scale(tag.img, (50, 50))
                                    self.btm_panel_icons[tag] = new_win
                                    self.btm_panel_x += 50

                        elif tag_cmd[2] == "Paint":
                            for i in self.store[0]:
                                if i.name == "Paint":
                                    new_win = Window(self.desktop.img, i.x, i.y, i.w, i.h, cts.white, "Program", i)
                                    self.windows.append(new_win)
                                    self.windows_rect.append(new_win.img_rect)
                                    i.wait_for_tag(new_win.img, new_win.img_rect.x, new_win.img_rect.y, (True,
                                                                                                         tag_cmd[3]))

                                    i.ui.save = tag_cmd[3]

                                    tag = Tag(self.btm_panel_x, cts.win_height - 50, new_win.tag_img, new_win.tag,
                                              new_win.ref, "", self.desktop.img)
                                    tag.img = pygame.transform.scale(tag.img, (50, 50))
                                    self.btm_panel_icons[tag] = new_win
                                    self.btm_panel_x += 50

                    else:
                        for i in self.store[0]:
                            if i.tag == tag:
                                new_win = Window(self.desktop.img, i.x, i.y, i.w, i.h, cts.white, "Program", i)
                                self.windows.append(new_win)
                                self.windows_rect.append(new_win.img_rect)

                                i.wait_for_tag(new_win.img, new_win.img_rect.x, new_win.img_rect.y, (False, None))

                                tag = Tag(self.btm_panel_x, cts.win_height - 50, new_win.tag_img, new_win.tag,
                                          new_win.ref, "", self.desktop.img)
                                tag.img = pygame.transform.scale(tag.img, (50, 50))
                                self.btm_panel_icons[tag] = new_win
                                self.btm_panel_x += 50

                elif tag_cmd[1] == "Folder":
                    for i in self.store[1]:
                        if i.tag == tag:
                            new_win = Window(self.desktop.img, i.x, i.y, i.w, i.h, cts.white, "Folder", i)
                            self.windows.append(new_win)
                            self.windows_rect.append(new_win.img_rect)

                            files = i.wait_for_tag(new_win.img, new_win.img_rect.x, new_win.img_rect.y)
                            for j in files:
                                self.tags.append(j)
                                j.folder = i
                                if j.tag == "Program":
                                    for k in self.store[0]:
                                        if k.tag == j:
                                            k.tag = j
                            tag = Tag(self.btm_panel_x, cts.win_height - 50, new_win.tag_img, new_win.tag,
                                      new_win.ref, "", self.desktop.img)
                            tag.img = pygame.transform.scale(tag.img, (50, 50))
                            self.btm_panel_icons[tag] = new_win
                            self.btm_panel_x += 50

                elif tag_cmd[1] == "Start" or self.dt_cmd[1] == "Start":

                    new_win = Window(self.desktop.img, 0, cts.win_height - 600, 500, 600 - self.btm.img_rect.h,
                                     cts.white, "Start_menu")

                    self.windows.append(new_win)
                    self.windows_rect.append(new_win.img_rect)
        for i in self.inputs:
            self.input_txt = i.check_event(event)

    def update(self):
        self.desktop.img.fill(self.desktop.color)
        for i in self.btm_panel_icons.keys():
            i.update()

        for tag in self.tags:
            tag.update()

        if self.full_window:
            self.full_window.update()
        for window in self.windows:
            if window.tag == "Desktop":
                self.desktop.update()
                self.upgrade_desktop()
            elif window.tag == "Folder" or window.tag == "Start_menu":
                window.update()
            elif window.tag == "Program":
                window.update()
                if window.ref:
                    window.ref.update()

        for i in self.inputs:
            i.update()

    def draw(self, sf):
        # self.sf.blit(self.desktop.img, self.desktop.img_rect)
        for i in self.btm_panel_icons.keys():
            i.draw(self.desktop.img)

        for tag in self.tags:
            if not tag.is_in_folder:
                if not self.full_window:
                    if pygame.Rect.collidelist(tag.img_rect, self.windows_rect) == -1:
                        tag.draw(self.desktop.img)
                else:
                    self.tags[0].draw(self.desktop.img)
            else:
                for i in self.windows:
                    if pygame.Rect.colliderect(tag.img_rect, i.img_rect) and i.ref != tag.folder and i.tag != "Desktop":

                        check = True
                        break
                else:
                    check = False

                if not check:
                    tag.draw(tag.folder.ui.layer)

        if self.full_window:
            self.full_window.draw(self.desktop)
        for i in self.inputs:
            i.draw(sf)

        for window in self.windows:
            if window.tag == "Desktop":
                if window.panels:
                    window.panels[0].draw(self.desktop.img)

            if window.tag == "Program" or window.tag == "Folder" or window.tag == "Start_menu":
                for i in self.windows_rect:
                    if pygame.Rect.colliderect(window.img_rect, i) and window.img_rect != i:
                        check = True
                        break
                else:
                    check = False
                if not check:
                    window.draw(self.desktop.img)
                if window.ref:
                    window.ref.draw()

            elif window.sf != self.sf:
                window.draw(window.img)
