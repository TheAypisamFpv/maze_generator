import random
import time
import pygame


"""SETTINGS"""
WIDTH = 40
HEIGHT = 20
VISUALIZE = False
CPS = 2000


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
                    draw_maze(self, current_cell, backtracked_cell)
                    pygame.display.flip()
                    pygame.time.wait(int(100/CPS))
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
                    draw_maze(self, current_cell)
                    pygame.display.flip()
                    pygame.time.wait(int(100/CPS))



class Cell_kruskal:
    def __init__(self):
        self.x = None
        self.y = None
        self.walls = {"top": 1, "right": 1, "bottom": 1, "left": 1}
        self.parent = self
        self.rank = 0

    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent

    def union(self, cell):
        root1 = self.find()
        root2 = cell.find()
        if root1 == root2:
            return
        if root1.rank > root2.rank:
            root2.parent = root1
        elif root2.rank > root1.rank:
            root1.parent = root2
        else:
            root2.parent = root1
            root1.rank += 1
            
class Maze_kruskal:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.maze_grid = [[Cell_kruskal() for y in range(height)] for x in range(width)]
        self.walls = []
        self.create_walls()
        self.create_maze()

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

    def create_walls(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.maze_grid[x][y]
                if x < self.width - 1:
                    self.walls.append((cell, self.maze_grid[x + 1][y]))
                if y < self.height - 1:
                    self.walls.append((cell, self.maze_grid[x][y + 1]))


    def create_maze(self):
        random.shuffle(self.walls)
        for cell1, cell2 in self.walls:
            if cell1.find() != cell2.find():
                cell1.union(cell2)
                if cell1.x == cell2.x:
                    cell1.walls["bottom"] = 0
                    cell2.walls["top"] = 0
                else:
                    cell1.walls["right"] = 0
                    cell2.walls["left"] = 0

                    

                    



def draw_maze(maze, current_cell=None, backtracked_cell=None):
    cell_size = 20  # Adjust this value to change the size of the cells
    margin = 5  # Adjust this value to change the size of the margin
    screen = pygame.display.set_mode((maze.width * cell_size, maze.height * cell_size))
    screen.fill((255, 255, 255))  # Fill the screen with white

    for x in range(maze.width):
        for y in range(maze.height):
            cell = maze.maze_grid[x][y]
            if cell.walls["top"]:
                pygame.draw.line(screen, (0, 0, 0), (x * cell_size, y * cell_size), ((x + 1) * cell_size, y * cell_size))
            if cell.walls["right"]:
                pygame.draw.line(screen, (0, 0, 0), ((x + 1) * cell_size, y * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size))
            if cell.walls["bottom"]:
                pygame.draw.line(screen, (0, 0, 0), (x * cell_size, (y + 1) * cell_size), ((x + 1) * cell_size, (y + 1) * cell_size))
            if cell.walls["left"]:
                pygame.draw.line(screen, (0, 0, 0), (x * cell_size, y * cell_size), (x * cell_size, (y + 1) * cell_size))


    if current_cell:
        pygame.draw.rect(screen, (255, 0, 0), (current_cell.x * cell_size + margin, current_cell.y * cell_size + margin, cell_size - 2 * margin, cell_size - 2 * margin))

    if backtracked_cell:
        pygame.draw.rect(screen, (0, 0, 255), (backtracked_cell.x * cell_size + margin, backtracked_cell.y * cell_size + margin, cell_size - 2 * margin, cell_size - 2 * margin))


    #if the current cell is the one on the top left corner, drow it normally
    if current_cell and current_cell.x == 0 and current_cell.y == 0:
        pygame.draw.rect(screen, (255, 255, 255), (current_cell.x * cell_size + margin, current_cell.y * cell_size + margin, cell_size - 2 * margin, cell_size - 2 * margin))





def create_maze(methode:str,width, height):
    if methode == "recursive_backtracking":
        maze = Maze_recursive_backtracking(width, height)
        maze.carve_path(visualize=VISUALIZE)
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
    maze.show_maze(maze.to_list())
    # time.sleep(1)
    if VISUALIZE:
        pygame.init()
        draw_maze(maze)
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.quit()
