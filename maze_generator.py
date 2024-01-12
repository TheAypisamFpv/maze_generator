import random
import time
import pygame


"""SETTINGS"""
WIDTH = 20
HEIGHT = 10
VISUALIZE = 1
CPS = 5
CELL_SIZE = 20  # Adjust this value to change the size of the cells
MARGIN = 5  # Adjust this value to change the size of the margin

methodes = ["recursive_backtracking", "kruskal (not working)"]



class Cell_recursive_backtracking:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.backtracked = False  # New attribute
        self.walls = {"top": 1, "right": 1, "bottom": 1, "left": 1}

class Maze_recursive_backtracking:          
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.maze_grid = [[Cell_recursive_backtracking(x, y) for y in range(height)] for x in range(width)]
        self.stack = []

        maze.carve_path(visualize=VISUALIZE)
        maze.draw_maze()



    def to_list(self):
        maze_list = [[1 for _ in range(self.width * 2 + 1)] for _ in range(self.height * 2 + 1)]
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze_grid[x][y]
                maze_list[y * 2 + 1][x * 2 + 1] = 0
                if not cell.walls["right"] and x < self.width - 1:
                    maze_list[y * 2 + 1][x * 2 + 2] = 0
                if not cell.walls["bottom"] and y < self.height - 1:
                    maze_list[y * 2 + 2][x * 2 + 1] = 0

        #remove the left wall of the first cell, and the right wall of the bottom right cell
        maze_list[1][0] = 0
        maze_list[-2][-1] = 0
        
        return maze_list



    def show_maze(self, maze_list: list):
        for row in maze_list:
            for cell in row:
                if cell == 1:
                    print("⬛", end="")
                else:
                    print("⬜", end="")
            print()
        


    def get_neighbours(self, cell: Cell_recursive_backtracking):
        directions = [("top", (0, -1)), ("right", (1, 0)), ("bottom", (0, 1)), ("left", (-1, 0))]
        neighbours = []

        for direction, (dx, dy) in directions:
            nx, ny = cell.x + dx, cell.y + dy
            if (0 <= nx < self.width) and (0 <= ny < self.height):
                neighbour = self.maze_grid[nx][ny]
                if not neighbour.visited:
                    neighbours.append((direction, neighbour))

        return neighbours


    def draw_maze(self, current_cell=None, backtracked_cell=None):
        
        screen = pygame.display.set_mode((self.width * CELL_SIZE, self.height * CELL_SIZE))
        screen.fill((255, 255, 255))  # Fill the screen with white

        for x in range(self.width):
            for y in range(self.height):
                cell = self.maze_grid[x][y]
                if cell.walls["top"]:
                    pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, y * CELL_SIZE))
                if cell.walls["right"]:
                    pygame.draw.line(screen, (0, 0, 0), ((x + 1) * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
                if cell.walls["bottom"]:
                    pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE, (y + 1) * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
                if cell.walls["left"]:
                    pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, (y + 1) * CELL_SIZE))



        if current_cell:
            pygame.draw.rect(screen, (255, 0, 0), (current_cell.x * CELL_SIZE + MARGIN, current_cell.y * CELL_SIZE + MARGIN, CELL_SIZE - 2 * MARGIN, CELL_SIZE - 2 * MARGIN))

        if backtracked_cell:
            pygame.draw.rect(screen, (0, 0, 255), (backtracked_cell.x * CELL_SIZE + MARGIN, backtracked_cell.y * CELL_SIZE + MARGIN, CELL_SIZE - 2 * MARGIN, CELL_SIZE - 2 * MARGIN))

    
            

        #if the current cell is the one on the top left corner, drow it normally
        if current_cell and current_cell.x == 0 and current_cell.y == 0:
            pygame.draw.rect(screen, (255, 255, 255), (current_cell.x * CELL_SIZE + MARGIN, current_cell.y * CELL_SIZE + MARGIN, CELL_SIZE - 2 * MARGIN, CELL_SIZE - 2 * MARGIN))

            
        pygame.time.wait(int(100/CPS))
        pygame.display.flip()
    

    def carve_path(self, visualize=False):
        start_cell = self.maze_grid[0][0]
        start_cell.visited = True
        self.stack.append(start_cell)

        while len(self.stack) > 0:
            current_cell = self.stack[-1]
            neighbours = self.get_neighbours(current_cell)

            if not neighbours:
                backtracked_cell = self.stack.pop()
                backtracked_cell.backtracked = True  # Mark the cell as backtracked
                if visualize:
                    self.draw_maze(current_cell, backtracked_cell)
                    pygame.display.flip()
            else:
                direction, next_cell = random.choice(neighbours)
                # print(direction, next_cell.x, next_cell.y)
                # print(current_cell.walls)
                # #check if the next cell is not out of bounds
                # while next_cell.x >= self.width - 1 and next_cell.y >= self.height - 1 or next_cell.x <= 0 and next_cell.y <= 0:
                #     direction, next_cell = random.choice(neighbours)
                #     print(direction, next_cell.x, next_cell.y)
                #     print(current_cell.walls)
                    
                    
                current_cell.walls[direction] = 0
                if direction == "top":
                    next_cell.walls["bottom"] = 0
                elif direction == "right":
                    next_cell.walls["left"] = 0
                elif direction == "bottom":
                    next_cell.walls["top"] = 0
                elif direction == "left":
                    next_cell.walls["right"] = 0

                next_cell.visited = True
                self.stack.append(next_cell)
                if visualize:
                    self.draw_maze(current_cell)
                    pygame.display.flip()




class Maze_kruskal:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze_grid = [[Cell_recursive_backtracking(x, y) for y in range(height)] for x in range(width)]
        rank = 0
        for x in range(width):
            for y in range(height):
                self.maze_grid[x][y] = rank
                rank += 1

        self.generate_maze()


    def render_maze(self):
        #render maze in pygame
        screen = pygame.display.set_mode((self.width * CELL_SIZE, self.height * CELL_SIZE))
        
        for x in range(self.width):
            for y in range(self.height):
                cell = self.maze_grid[x][y]

                #render the cell a color depending on the rank
                color = (cell**2 % 255, cell**3 % 255, cell**4 % 255)
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                directions = {
                        "top": (0, 1),
                        "bottom": (0, -1),
                        "left": (-1, 0),
                        "right": (1, 0)
                    }
                    
                if cell != self.maze_grid[x][y + 1]:
                    pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, y * CELL_SIZE))
                if cell != self.maze_grid[x + 1][y]:
                    pygame.draw.line(screen, (0, 0, 0), ((x + 1) * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
                if cell != self.maze_grid[x][y - 1]:
                    pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE, (y + 1) * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE))
                if cell != self.maze_grid[x - 1][y]:
                    pygame.draw.line(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, (y + 1) * CELL_SIZE))

                


    def generate_maze(self):
        #while there is more than 1 rank, generate maze

        while len(set([cell for row in self.maze_grid for cell in row])) > 1:

            #chose 2 random cells (2nd cell is next to the first one)
            x_1, y_1 = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            
            #random direction
            directions = []
            if x_1 > 0:
                directions.append("left")
            if x_1 < self.width - 1:
                directions.append("right")
            if y_1 > 0:
                directions.append("top")
            if y_1 < self.height - 1:
                directions.append("bottom")
            
            direction = random.choice(directions)
            
            x_2, y_2 = x_1, y_1
            if direction == "top":
                y_2 -= 1
            elif direction == "right":
                x_2 += 1
            elif direction == "bottom":
                y_2 += 1
            elif direction == "left":
                x_2 -= 1

            self.merge_cells((x_1, y_1), (x_2, y_2))
            self.render_maze()


    def merge_cells(self, cell1, cell2):
        #merge cell1 into cell2
        self.maze_grid[cell1[0]][cell1[1]] = self.maze_grid[cell2[0]][cell2[1]]
        







def create_maze(methode:str,width, height):
    if methode == "recursive_backtracking":
        maze = Maze_recursive_backtracking(width, height)
    elif methode == "kruskal":
        maze = Maze_kruskal(width, height)
    else:
        print(f"methode {methode} not found\n methode available : {methodes}")
        return None

    
    return maze





while __name__ == "__main__":
    maze = create_maze(input("methode :\n> "), WIDTH, HEIGHT)
    if maze == None:
        continue
    # time.sleep(1)
    if VISUALIZE:
        pygame.time.wait(1000)
        pygame.quit()

