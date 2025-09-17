import tkinter as tk
import pygame
pygame.init()

root = tk.Tk()

win_width = root.winfo_screenwidth()
win_height = root.winfo_screenheight()
FPS = 30

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
silver = (192, 192, 192)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
light_red = (182, 84, 84)

main_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 14)