import pygame
import UI as ui
import Constants as cts
pygame.init()


class UI:
    def __init__(self, sf, x, y, w, h):
        self.sf = sf
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.layer = pygame.surface.Surface.subsurface(self.sf, (0, 0, w, h))
        self.files = []

    def prepare_inside(self, contents):
        current_y = 50
        for i in contents:
            if type(i) == list:
                if i[0]:
                    # tag = ui.Tag(50, current_y, i[3], i[2], "", i[4], self.layer)
                    i[1].img_rect.x = 50
                    i[1].img_rect.y = current_y
                    i[1].font_color = cts.black
                    i[1].font_padding = -45
                    i[1].is_in_folder = True
                    i[1].layer = pygame.surface.Surface.subsurface(self.layer, (i[1].img_rect.x, i[1].img_rect.y, 50,
                                                                                50))
                    i[1].img = pygame.transform.scale(i[1].img, (50, 50))
                    self.files.append(i[1])
                    current_y += 90
        return self.files

    def check_event(self, event):
        for i in self.files:
            cmd = i.check_event(event)

    def update(self):
        self.layer.fill(cts.white)
        for i in self.files:
            i.update()

    def draw(self):
        for i in self.files:
            i.draw(self.layer)


class Main:
    def __init__(self):
        self.x = 600
        self.y = 200
        self.w = 1000
        self.h = 600

        self.tag = None
        self.tag_img = "Folder_tag.png/"
        self.ui = None

        self.contents = []

    def add_contents(self, file):
        self.contents.append([True, file[0], file[1], file[2], file[3]])

    def create_tag(self, x, y, sf):
        self.tag = ui.Tag(x, y, "Folder_tag.png/", "Folder", "", "New Folder", sf)
        return self.tag

    def wait_for_tag(self, sf, x, y):
        if not self.ui:
            self.ui = UI(sf, x, y + 20, self.w, self.h - 20)
        return self.ui.prepare_inside(self.contents)

    def check_event(self, event):
        self.ui.check_event(event)

    def update(self):
        self.ui.update()

    def draw(self):
        self.ui.draw()
