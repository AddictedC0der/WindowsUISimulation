import pygame
import Constants as cts
import UI
import time
import Calculator
import Paint
import Word
pygame.init()


class Core:
    def __init__(self):
        self.sc = pygame.display.set_mode((cts.win_width, cts.win_height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.programs = []
        self.folders = []
        self.files = []
        self.C = [self.programs, self.folders, self.files]

        calc = Calculator.Main()
        paint = Paint.Main(self.C)
        word = Word.Main(self.C)
        self.programs.append(calc)
        self.programs.append(paint)
        self.programs.append(word)

        self.ui = UI.UI(self.sc, self.C)

    def start(self):
        center_x = self.sc.get_width() / 2
        center_y = self.sc.get_height() / 2

        loading = 0
        while loading < 100:
            self.sc.fill(cts.black)
            pygame.draw.rect(self.sc, cts.white, (center_x / 2, center_y, center_x, 0))
            loading += 1
            time.sleep(0.01)
            pygame.display.update()
            self.clock.tick(cts.FPS)

    def run(self):
        # self.start()
        while self.running:
            for i in pygame.event.get():
                if i.type == pygame.QUIT or i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    self.running = False
                cmd = self.ui.check_event(i)
                if cmd == "Exit":
                    self.running = False

            self.sc.fill(cts.gray)
            self.ui.update()
            self.ui.draw(self.sc)

            pygame.display.update()
            self.clock.tick(cts.FPS)


core = Core()
core.run()
quit()
