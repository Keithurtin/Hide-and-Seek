#############################################################
#                       LƯU Ý                               #
# 1. Mặc dù trên lí thuyết seeker và hider hành động cùng   #
#    lúc nhưng trên thứ tự chạy chương trình phải cho       #
#    hider di chuyển trước, nếu không sẽ bị lỗi seeker bắt  #
#    được trước hider kịp di chuyển trong cùng turn         #
# 2. Một số hàm trong file main có thể cần phải chỉnh sửa   #
#    đôi chút trong trường hợp hider có thể di chuyển       #
# 3. Một số hàm của class Map có thể dùng được cho cả hider #
#                                                           #
#############################################################


from map import *
from seeker import *
import os
import copy
import pygame
import time

states = []

FPS = 60
CELL_SIZE = 40
WHITE = (255, 255, 255)
PINK = (238, 162, 173, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

hiderImg = pygame.image.load("../asset/human.png")
hiderPNG = pygame.transform.scale(hiderImg, (40, 40))
seekerImg = pygame.image.load("../asset/monster.png")
seekerPNG = pygame.transform.scale(seekerImg, (40, 40))
wallImg = pygame.image.load("../asset/wall.png")
wallPNG = pygame.transform.scale(wallImg, (40, 40))
pingImg = pygame.image.load("../asset/ping.png")
pingPNG = pygame.transform.scale(pingImg, (40, 40))

# Calculate distance between 2 points


def cal_dist(A, B):
    return max(abs(A[0] - B[0]), abs(A[1] - B[1]))


def output(map, counter):
    # os.system('cls')
    # print("Time: ", counter)
    # map.print_map()
    # pause = input("press Enter to continue")
    states.append(copy.deepcopy(map.grid))
    map.update_map()


def search_around_ping(map: Map, seeker: Seeker, counter, ping_freq, ping_list):
    found = seeker.catched
    search_list = seeker.search_around(map, seeker.priority_target)
    for cell in search_list:
        # Priority search unseen place because hider can hide behind walls
        if cell not in seeker.observed_list:
            seeker.priority_target = cell
            counter = target_focus(map, seeker, counter,
                                   ping_freq, ping_list, True)
            if (seeker.catched > found):
                return counter
    return counter


def target_focus(map: Map, seeker: Seeker, counter: int, ping_freq, ping_list, observe_only=False):
    route = seeker.backtrack(seeker.chase(map), seeker.priority_target)
    for cell in route:
        sight = seeker.get_sight(map)
        if not seeker.target_aim:
            for hider in map.hider_pos:
                if hider in sight:
                    seeker.priority_target = hider
                    seeker.target_aim = True
                    return target_focus(map, seeker, counter, ping_freq, ping_list)
            if not seeker.ping_aim:
                if ping_list:
                    for ping in ping_list:
                        if ping in sight:
                            seeker.priority_target = ping
                            seeker.ping_aim = True
                            counter = search_around_ping(
                                map, seeker, counter, ping_freq, ping_list)
                            seeker.ping_aim = False
                            return counter
        seeker.move(map, cell)
        counter += 1
        if (counter % ping_freq == 0):
            if ping_list:
                map.delete_ping(ping_list)
            ping_list = map.ping_hider()
        output(map, counter)
        if (observe_only):
            if seeker.priority_target in seeker.observed_list:
                return counter
    return counter


def play_level_1_and_2(map: Map, seeker: Seeker, ping_freq):
    counter = 0
    ping_list = None
    while True:
        for i in range(1, map.row - 1):
            for j in range(1, map.col - 1):
                if (map.grid[i, j] != 1) and ((i, j) not in seeker.observed_list):
                    seeker.priority_target = (i, j)
                    counter = target_focus(
                        map, seeker, counter, ping_freq, ping_list, True)
                    if (seeker.catched == map.numOfHider):
                        return seeker.catched * 20 - counter
        seeker.observed_list = []


def play(map: Map, level, ping_freq):
    seeker = Seeker(map.seeker_pos[0], map.seeker_pos[1], 3)
    if (level == 1):
        return play_level_1_and_2(map, seeker, ping_freq)
    if (level == 2):
        return play_level_1_and_2(map, seeker, ping_freq)


def redraw(rows, columns, grid, window, seeker):
    window.fill(WHITE)

    mp = Map()
    mp.row = rows
    mp.col = columns
    mp.grid = grid
    vision_cells = seeker.get_sight(mp)
    for cell in vision_cells:
        pygame.draw.rect(
            # Yellow with transparency
            window, PINK, (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for i in range(rows):
        for j in range(columns):
            rect = pygame.Rect(j * CELL_SIZE, i *
                               CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[i, j] == 9:
                window.blit(pingPNG, rect)
            elif grid[i, j] == -1:
                pygame.draw.rect(window, WHITE, rect)
            elif grid[i, j] == 1:
                window.blit(wallPNG, rect)
            elif grid[i, j] == 2:
                window.blit(hiderPNG, rect)
            elif grid[i, j] == 3:
                window.blit(seekerPNG, rect)

    x = 0
    y = 0

    for l in range(rows):
        y += CELL_SIZE
        pygame.draw.line(window, BLACK, (0, y), (CELL_SIZE * columns, y))

    for l in range(columns):
        x += CELL_SIZE
        pygame.draw.line(window, BLACK, (x, 0), (x, CELL_SIZE * rows))


def main():
    states.clear()
    map = Map()
    map.read_map()
    level = int(input("Input level: "))
    ping_freq = int(input("Input frequency of hider's announcement: "))
    score = play(map, level, ping_freq)
    pygame.init()
    rows = map.row
    columns = map.col
    screen_width = columns * CELL_SIZE
    screen_height = rows * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hide & Seek")
    run = True
    clock = pygame.time.Clock()

    count = 1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for state in states:
            count += 1
            for i in range(rows):
                for j in range(columns):
                    if state[i, j] == 3:
                        seekerPos = (i, j)
            seeker = Seeker(seekerPos[0], seekerPos[1], 3)
            redraw(rows, columns, state, screen, seeker)
            time.sleep(0.5)
            pygame.display.update()
            if count == len(states):
                run = False
    print('Score:', score)
    pygame.quit()


if __name__ == "__main__":
    main()
