class Square:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.right = x + size
        self.bottom = y + size
 
class BacktrackState:
    def __init__(self, squares, occupied_area, current_count, start_x, start_y, grid_size, best_count, best_solution):
        self.squares = squares.copy()
        self.occupied_area = occupied_area
        self.current_count = current_count
        self.start_x = start_x
        self.start_y = start_y
        self.grid_size = grid_size
        self.best_count = best_count
        self.best_solution = best_solution
 
    def is_overlapping(self, x, y):
        for square in self.squares:
            if (x >= square.x and x < square.right) and (y >= square.y and y < square.bottom):
                return True
        return False
 
    def backtrack(self):
        if self.occupied_area == self.grid_size * self.grid_size:
            if self.current_count < self.best_count[0]:
                self.best_count[0] = self.current_count
                self.best_solution[:] = self.squares.copy()
            return
 
        for x in range(self.start_x, self.grid_size):
            for y in range(self.start_y, self.grid_size):
                if self.is_overlapping(x, y):
                    continue
 
                max_size = self.calculate_max_size(x, y)
                if max_size <= 0:
                    continue
 
                self.try_place_squares(x, y, max_size)
                return
            self.start_y = 0
 
    def calculate_max_size(self, x, y):
        max_size = min(self.grid_size - x, self.grid_size - y)
        for square in self.squares:
            if square.right > x and square.y > y:
                max_size = min(max_size, square.y - y)
            elif square.bottom > y and square.x > x:
                max_size = min(max_size, square.x - x)
        return max_size
 
    def try_place_squares(self, x, y, max_size):
        for size in range(max_size, 0, -1):
            new_square = Square(x, y, size)
            new_occupied_area = self.occupied_area + size * size
 
            if self.should_skip(new_occupied_area, x, y, size):
                continue
 
            self.squares.append(new_square)
            if new_occupied_area == self.grid_size * self.grid_size:
                self.update_best_solution()
                self.squares.pop()
                continue
 
            if self.current_count + 1 < self.best_count[0]:
                new_state = BacktrackState(
                    self.squares,
                    new_occupied_area,
                    self.current_count + 1,
                    x,
                    y,
                    self.grid_size,
                    self.best_count,
                    self.best_solution
                )
                new_state.backtrack()
            self.squares.pop()
 
    def should_skip(self, new_occupied_area, x, y, size):
        remaining_area = self.grid_size * self.grid_size - new_occupied_area
        if remaining_area > 0:
            max_possible_size = min(self.grid_size - x, self.grid_size - y)
            if max_possible_size == 0:
                return True
            min_squares_needed = (remaining_area + (max_possible_size ** 2 - 1)) // (max_possible_size ** 2)
            if (self.current_count + 1 + min_squares_needed) >= self.best_count[0]:
                return True
        return False
 
    def update_best_solution(self):
        if self.current_count + 1 < self.best_count[0]:
            self.best_count[0] = self.current_count + 1
            self.best_solution[:] = self.squares.copy()
 
def initialize_initial_squares(grid_size):
    half_size = (grid_size + 1) // 2
    small_size = grid_size // 2
    return [
        Square(0, 0, half_size),
        Square(0, half_size, small_size),
        Square(half_size, 0, small_size)
    ]
 
def find_max_square_size(grid_size):
    max_divisor = 1
    for i in range(grid_size // 2, 0, -1):
        if grid_size % i == 0:
            max_divisor = i
            break
    return max_divisor, grid_size // max_divisor
 
def main():
    grid_size = int(input().strip())
 
    square_size, new_grid_size = find_max_square_size(grid_size)
    best_count = [2 * new_grid_size + 1]
    initial_squares = initialize_initial_squares(new_grid_size)
    best_solution = []
 
    initial_occupied_area = initial_squares[0].size ** 2 + 2 * initial_squares[1].size ** 2
    start_x = initial_squares[2].bottom
    start_y = initial_squares[2].x
 
    state = BacktrackState(
        initial_squares,
        initial_occupied_area,
        3,
        start_x,
        start_y,
        new_grid_size,
        best_count,
        best_solution
    )
    state.backtrack()
 
    print(best_count[0])
    for square in best_solution:
        print(f"{1 + square.x * square_size} {1 + square.y * square_size} {square.size * square_size}")
 
if __name__ == "__main__":
    main()