import pygame
import random
from shapes import *

pygame.init()

WIDTH = 400
HEIGHT = 600
FONT_SIZE = 20
FONT_SIZE_LARGE = 40

screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
display_font = pygame.font.Font('VGA9.ttf', 20)
display_font_large = pygame.font.Font('VGA9.ttf', 40)
display_font_small = pygame.font.Font('VGA9.ttf', 10)

background_chr = "\u2219"

pygame.display.set_caption("TETRIS")

board = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]



class currentShape:
        def __init__(self, x, y, shape):
            self.x = x
            self.y = y
            self.shape = shape
            self.gravity_counter = 0

            self.bottom_units = []
            self.left_units = []
            self.right_units = []
            
            self.get_units()

            #print(self.side_units)

        def get_units(self):
            self.bottom_units = []
            self.left_units = []
            self.right_units = []


            for row in range(len(self.shape)):
                for column in range(len(self.shape[row])):

                    if self.shape[row][column] != 0 and column == len(self.shape[0]) - 1:
                        self.right_units.append((row, column))
                    elif self.shape[row][column] != 0 and column == len(self.shape[0]) - 2 and self.shape[row][column + 1] == 0:
                        self.right_units.append((row, column))

            for row in range(len(self.shape)):
                for column in range(len(self.shape[row])):

                    if self.shape[row][column] != 0 and column == 0:
                        self.left_units.append((row, column))
                    elif column == 1 and self.shape[row][column] != 0 and self.shape[row][column - 1] == 0:
                        self.left_units.append((row, column))

            for row in range(len(self.shape)):
                for column in range(len(self.shape[row])):

                    if self.shape[row][column] != 0 and row == len(self.shape) - 1:
                        self.bottom_units.append((row, column))
                    elif row < 2 and self.shape[row][column] != 0 and self.shape[row + 1][column] == 0:
                        self.bottom_units.append((row, column))

            #print(self.right_units)

        def collision_vertical(self):
                    # if self.shape[row][column] != 0 and (self.y + row >= len(board) - 1):
                    #     return True
                    
                    # elif self.y < len(board) - 3 and (row == 2 and (board[self.y + row + 1][column] != 0)): #or (self.shape[row + 1][column] == 0 and (self.y + row + 1) != 0):
                    #     #print('test')
                    #     return True
            for unit_coords in self.bottom_units:
                if unit_coords[0] + self.y >= len(board) - 1:
                    return True
                elif board[unit_coords[0] + self.y + 1][unit_coords[1] + self.x] != 0:
                    return True
                
            
            return False
        
        def collision_left(self):
            for unit_coords in self.left_units:
                if unit_coords[1] + self.x <= 0:
                    return True
                elif board[self.y][unit_coords[1] + self.x - 1] != 0:
                    return True
                
            return False
                
                
        def collision_right(self):
            for unit_coords in self.right_units:
                if unit_coords[1] + self.x >= len(board[0]) - 1:
                    print('collision 1')
                    return True
                elif board[self.y][unit_coords[1] + self.x + 1] != 0:
                    print('collsion2')
                    return True
                
            return False
                
        
        def clear(self):
            for row in range(len(self.shape)):
                for column in range(len(self.shape[row])):
                    if self.shape[row][column] != 0 and row + self.y < len(board):
                        board[row + self.y][column + self.x] = 0
        
        def move(self, x_amt, y_amt):
            self.clear()
            draw_shape(self.x + x_amt, self.y + y_amt, self.shape)
            self.x += x_amt
            self.y += y_amt
            
        def rotate(self):
            for shape_group in shapes:
                if self.shape in shape_group:
                    if shape_group.index(self.shape) == len(shape_group) - 1:
                        new_shape = shape_group[0]
                    else:
                        new_shape = shape_group[shape_group.index(self.shape) + 1]
                    for row in range(len(new_shape)):
                        for column in range(len(new_shape[0])):
                            if column + self.x > len(board[0]) - 1 or column + self.x < 0 or row + self.y > len(board) - 1 or row + self.y < 0:
                                return
                            elif board[row + self.y][column + self.x] != 0 and self.shape[row][column] == 0:
                                return
                            
                    self.clear()
                    self.shape = new_shape

            draw_shape(self.x, self.y, self.shape)
            self.get_units()

        def update(self):
            last_pressed = pygame.key.get_pressed()
            # for event in pygame.event.get():
            #     if event.type == pygame.KEYUP:
            #         if event.key == pygame.K_UP:
            #             self.rotate()

            #draw_shape(self.x, self.y, self.shape)
            self.gravity_counter += 0.4

            if not self.collision_vertical():
                if self.gravity_counter >= 1:
                    self.move(0, 1)
                    self.gravity_counter = 0

        def get_input(self, key):
            self.update()       
            
            if key == "left":
                if not self.collision_left():
                    self.move(-1, 0)
            elif key == 'right':
                if not self.collision_right():
                    self.move(1, 0)
            elif key == 'up':
                self.rotate()
                


def draw_shape(x, y, shape):
        drawn_shape = shape

        for row in range(len(drawn_shape)):
            for column in range(len(drawn_shape[row])):
                if ((y + row < len(board)) and (x + column < len(board[y]))) and drawn_shape[row][column] != 0:
                    board[y + row][x + column] = drawn_shape[row][column]

def check_row():
    for n in range(len(board)):
        if 0 not in board[n]:
            return n
    return -1

def move_board(n):
    for row in range(n, 0, -1):
        #print(row)
        board[row] = board[row - 1].copy()

def display_text(text, font, location, color, screen):
        txt = font.render(text, True, color)
        txt_rect = txt.get_rect(midtop = location)
        screen.blit(txt, txt_rect)

def get_high_score():
    try:
        f = open('high_score.txt', 'r')
        return int(f.readline())
    except:
        f = open('high_score.txt', 'w')
        f.write("0")
        f.close()
        return 0

def save_high_score(score):
    f = open('high_score.txt', 'w')
    f.write(str(score))
    f.close()

def main():

    score = 0

    game_running = False
    game_state = 0

    #def display

    

    for n in range(len(board)):
        for i in range(10):
            board[n].append(0)

    # board[0][2] = 1
    # board[2][3] = "\u0040"
    # board[2][4] = "\u2261"





    # Draws shape at the top left coordinates x, y
    


    current_shape = currentShape(5, 0, random.choice(random.choice(shapes)))
    #current_shape = currentShape(5, 0, random.choice(shapes[5]))
    #draw_shape(3, 7, shapes.get('t')[0])


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
            if game_running:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        current_shape.get_input('up')
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_shape.get_input('left')
                    elif event.key == pygame.K_RIGHT:
                        current_shape.get_input('right')
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_state == 0:
                        game_running = True
                        game_state = 1

        
        
        screen.fill((0, 0, 0))

        if game_running:

            for y in range(len(board)):
                for x in range(len(board[y])):
                    color = (255, 255, 255)
                    display_chr = "?"

                    if board[y][x] == 0:
                        display_chr = "\u2219"
                    elif board[y][x] == 1:
                        display_chr = "#"
                        color = (255, 0, 0)
                    elif board[y][x] == 2:
                        display_chr = "#"
                        color = (0, 255, 0)
                    elif board[y][x] == 3:
                        display_chr = "#"
                        color = (0, 0, 255)
                    elif board[y][x] == 4:
                        display_chr = "#"
                        color = (255, 255, 0)
                    elif board[y][x] == 5:
                        display_chr = "#"
                        color = (255, 170, 0)
                    elif board[y][x] == 6:
                        display_chr = "#"
                        color = (255,140,220)
                    elif board[y][x] == 7:
                        display_chr = "#"
                        color = (255, 255, 255)
                    display_txt = display_font.render(display_chr, True, color)
                    display_rect = display_txt.get_rect(topleft = ((FONT_SIZE * 5) + (x * FONT_SIZE), (FONT_SIZE * 5) + (y * FONT_SIZE)))
                    screen.blit(display_txt, display_rect)

            for row in range(len(board)):
                border_txt = display_font.render("\u2551", True, (255, 255, 255))
                border_rect = display_txt.get_rect(topleft = (FONT_SIZE * 4, (row * FONT_SIZE) + (FONT_SIZE * 5)))
                screen.blit(border_txt, border_rect)
                border_txt = display_font.render("\u2551", True, (255, 255, 255))
                border_rect = display_txt.get_rect(topleft = (FONT_SIZE * 15, (row * FONT_SIZE) + (FONT_SIZE * 5)))
                screen.blit(border_txt, border_rect)

            for column in range(len(board[0])):
                border_txt = display_font.render("\u2550", True, (255, 255, 255))
                border_rect = display_txt.get_rect(topleft = ((FONT_SIZE * 5) + (FONT_SIZE * column), (FONT_SIZE * 4)))
                screen.blit(border_txt, border_rect)
                border_txt = display_font.render("\u2550", True, (255, 255, 255))
                border_rect = display_txt.get_rect(topleft = ((FONT_SIZE * 5) + (FONT_SIZE * column), (FONT_SIZE * 25)))
                screen.blit(border_txt, border_rect)

            corner_txt = display_font.render("\u2554", True, (255, 255, 255))
            corner_rect = corner_txt.get_rect(topleft = (FONT_SIZE * 4, FONT_SIZE * 4))
            screen.blit(corner_txt, corner_rect)

            corner_txt = display_font.render("\u2557", True, (255, 255, 255))
            corner_rect = corner_txt.get_rect(topleft = (FONT_SIZE * 15, FONT_SIZE * 4))
            screen.blit(corner_txt, corner_rect)

            corner_txt = display_font.render("\u255A", True, (255, 255, 255))
            corner_rect = corner_txt.get_rect(topleft = (FONT_SIZE * 4, FONT_SIZE * 25))
            screen.blit(corner_txt, corner_rect)

            corner_txt = display_font.render("\u255D", True, (255, 255, 255))
            corner_rect = corner_txt.get_rect(topleft = (FONT_SIZE * 15, FONT_SIZE * 25))
            screen.blit(corner_txt, corner_rect)

            
            if current_shape.collision_vertical():
                if board[3][3] or board[3][4] or board[3][5] or board[3][6] != 0:
                        game_running = False
                        game_state = 2
                while check_row() != -1:
                    move_board(check_row())
                    score += 1
                    if score > get_high_score():
                        save_high_score(score)
                current_shape = currentShape(3, 0, random.choice(random.choice(shapes)))

            current_shape.update()

            display_text("Score: " + str(score), display_font, ((WIDTH / 2), FONT_SIZE * 2), (255, 255, 255), screen)
            display_text("High Score: " + str(get_high_score()), display_font, ((WIDTH / 2), FONT_SIZE * 27), (255, 255, 255), screen)


        elif game_state == 0:
            instructions_txt = display_font.render("Press Space", True, (255, 255, 255))
            instructions_rect = instructions_txt.get_rect(midtop = (WIDTH / 2, FONT_SIZE * 20))
            screen.blit(instructions_txt, instructions_rect)
            instructions_txt = display_font.render("To Play", True, (255, 255, 255))
            instructions_rect = instructions_txt.get_rect(midtop = (WIDTH / 2, FONT_SIZE * 22))
            screen.blit(instructions_txt, instructions_rect)
            # instructions_txt = display_font_large.render("\u263A", True, (0, 255, 0))
            # instructions_rect = instructions_txt.get_rect(midtop = (WIDTH / 2, FONT_SIZE * 14))
            # screen.blit(instructions_txt, instructions_rect)

            display_text("###", display_font_large, (WIDTH / 2, FONT_SIZE_LARGE * 6), (255, 0, 0), screen)
            display_text(" # ", display_font_large, (WIDTH / 2, FONT_SIZE_LARGE * 7), (255, 0, 0), screen)

            display_text("TETRIS", display_font_large, (WIDTH / 2, FONT_SIZE_LARGE * 3), (0, 255, 0), screen)
            display_text("Created By Talon Couture", display_font_small, (WIDTH / 2, FONT_SIZE * 29), (255, 255, 255), screen)

        elif game_state == 2:
            display_text("GAME", display_font_large, (WIDTH / 2, FONT_SIZE_LARGE * 5), (0, 255, 0), screen)
            display_text("OVER", display_font_large, (WIDTH / 2, FONT_SIZE_LARGE * 7), (0, 255, 0), screen)
            display_text("Score: " + str(score), display_font, (WIDTH / 2, FONT_SIZE * 18), (255, 255, 255), screen)
            display_text("High Score: " + str(get_high_score()), display_font, (WIDTH / 2, FONT_SIZE * 20), (255, 255, 255), screen)

            display_text("Created By Talon Couture", display_font_small, (WIDTH / 2, FONT_SIZE * 29), (255, 255, 255), screen)

        
        pygame.display.update()
        clock.tick(12)

if __name__ == "__main__":
    main()