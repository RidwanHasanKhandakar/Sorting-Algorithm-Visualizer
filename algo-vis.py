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
    TOP_PAD = 150
    GRADIENTS = [
        GREY,
        (160,160,160),
        (192,192,192)
    ]
    def __init__(self,width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm VIS made by RRHIN")
        self.set_lst(lst)
    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = (self.height -self.TOP_PAD) / (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info):
    lst = draw_info.lst
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        bar_height = (val - draw_info.min_val) * draw_info.block_height
        y = draw_info.height - bar_height
        color = draw_info.GRADIENTS[i % 3] 
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, bar_height))

def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def main():
    run = True
    clock = pygame.time.Clock()
    n=50
    min_val = 0
    max_val =100
    lst = generate_starting_list(n,min_val,max_val)
    draw_info = DrawInformation(800,600,lst)
    while run:
        clock.tick(60)
        #pygame.display.update()
        draw(draw_info)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_lst(lst)
            
    pygame.quit()

if __name__ == "__main__":
    main()