import pygame
import random
pygame.init()
class DrawInformation:
    #this are just global color that we will use in our program
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE
    SIDE_PAD = 100
    def __init__(self,width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm VIS made by RRHIN")
        self.set_list(lst)
    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.pixel_width = self.width - self.SIDE_PAD / len(lst)
        
    