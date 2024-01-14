import random
import pygame


"""default parameters for the maze generator and visualizer"""
WIDTH = 10
HEIGHT = 5
VISUALIZE = 0
CPS = 10        # Adjust this value to change the speed of the visualization
CELL_SIZE = 20  # Adjust this value to change the size of the cells
MARGIN = 5      # Adjust this value to change the size of the margin


class Cell_recursive_backtracking:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.backtracked = False  # New attribute
        self.walls = {"top": 1, "right": 1, "bottom": 1, "left": 1}

class Maze_recursive_backtracking:          
    def __init__(self, width:int, height:int, visualize:bool):
        self.width = width
        self.height = height
        self.maze_grid = [[Cell_recursive_backtracking(x, y) for y in range(height)] for x in range(width)]
        self.stack = []

        self.carve_path(visualize)
        self.draw_maze()



    def to_list(self, save_to_file=False):
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

        if save_to_file:
            with open("maze.txt", "w") as f:
                for row in maze_list:
                    for cell in row:
                        f.write(str(cell))
                    f.write("\n")
        
        return maze_list

        

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

    

    def make_complex(self):
        #remove some walls to make the maze more complex
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze_grid[x][y]
                if random.randint(0,5) == 0:
                    #choose a random direction where there is a wall
                    directions = []
                    for direction in cell.walls:
                        if cell.walls[direction]:
                            directions.append(direction)

                    if len(directions) > 0:
                        direction = random.choice(directions)
                        if direction == "top" and y > 0:
                            cell.walls["top"] = 0
                            self.maze_grid[x][y-1].walls["bottom"] = 0

                        elif direction == "right" and x < self.width - 1:
                            cell.walls["right"] = 0
                            self.maze_grid[x+1][y].walls["left"] = 0

                        elif direction == "bottom" and y < self.height - 1:
                            cell.walls["bottom"] = 0
                            self.maze_grid[x][y+1].walls["top"] = 0
                            
                        elif direction == "left" and x > 0:
                            cell.walls["left"] = 0
                            self.maze_grid[x-1][y].walls["right"] = 0
                



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

        self.make_complex()




def show_maze(maze_list: list[list[int]]):
    """
    Display the maze in the terminal as a grid of black and white squares
    """
    for row in maze_list:
        for cell in row:
            print("⬛", end="") if cell else print("⬜", end="")
        print()




def create_maze(width=WIDTH, height=HEIGHT, visualize=VISUALIZE):
    """
    Create a maze using the recursive backtracking algorithm
    ---------------------------------
    Return a list of lists representing the maze
    
    -width : width of the maze (default: 10)

    -height : height of the maze (default: 5)

    -visualize : whether to visualize the maze generation process (default: False)
    
    """
    maze = Maze_recursive_backtracking(width, height, visualize)
    maze_list = maze.to_list()
    if visualize:
        show_maze(maze_list)
        # freeze for 5s
        try:
            pygame.time.wait(5000)
        except:
            pass

    return maze_list