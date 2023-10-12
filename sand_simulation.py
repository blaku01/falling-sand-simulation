import numpy as np

class Field:
    def __init__(self, x=None, y=None, field_type="air"):
        self.x = x
        self.y = y
        self.type = field_type

    def __str__(self):
        if self.type == "air":
            return "."
        elif self.type == "inlet":
            return "+"
        elif self.type == "sand":
            return "o"
        elif self.type == "wall":
            return "#"

class SandSimulation:
    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height
        self.board = None
        self.sand_inlet = None

    def draw_board(self):
        for row in np.flipud(self.board.T):
            print(''.join(str(field) for field in row))
        print()

    def simulate_sand_fall_step(self):
        x, y = self.check_fields_under(self.current_field)

        if y is None:
            return None

        self.board[x][y], self.board[self.current_field.x][self.current_field.y] = self.board[self.current_field.x][self.current_field.y], self.board[x][y]
        self.current_field.x, self.current_field.y = x, y
        return x, y

    def simulate_sand_fall(self):
        particle = self.create_new_sand_particle()
        if particle is not None:
            while self.simulate_sand_fall_step():
                pass
        return particle

    def check_fields_under(self, field):
        if (field.y - 1) < 0:
            return None, None

        new_y = field.y - 1

        if self.board[field.x][new_y].type == "air":
            new_x = field.x
        elif (
            field.x + 1 < self.width
            and self.board[field.x + 1][new_y].type == "air"
        ):
            new_x = field.x + 1
        elif (
            field.x - 1 >= 0
            and self.board[field.x - 1][new_y].type == "air"
        ):
            new_x = field.x - 1
        else:
            return None, None

        return new_x, new_y

    def create_new_sand_particle(self):
        x, y = self.check_fields_under(Field(self.sand_inlet.x, self.sand_inlet.y, field_type="sand"))
        if y is None:
            return
        self.current_field = Field(x, y, field_type="sand")
        self.board[x][y] = self.current_field
        return self.current_field

    def setup(self):
        board_shape = input("").split(" ")
        self.width, self.height = int(board_shape[0]), int(board_shape[1])
        self.create_blank_board()
        while True:
            user_input = input("")
            if user_input == "r":
                wall_params = [int(i) for i in input().split(" ")]
                self.create_wall(*wall_params)
            elif user_input == "s":
                start_x, start_y = input().split(" ")
                self.sand_inlet = Field(int(start_x), int(start_y), field_type="inlet")
                self.board[self.sand_inlet.x, self.sand_inlet.y] = self.sand_inlet
                break

    def simulate(self, num_steps=None):
        if not self.board:
            self.setup()
        iters = 0
        if num_steps is not None:
            for i in range(num_steps):
                if self.simulate_sand_fall() is None:
                    break
                else:
                    iters += 1
        else:
            while True:
                if self.simulate_sand_fall() is None:
                    break
                else:
                    iters += 1
        self.draw_board()
        print(f"Ziarenka: {iters}")

    def create_wall(self, start_x, start_y, end_x, end_y):
        wall = np.vectorize(lambda x: Field(field_type="wall"))
        width = end_x - start_x + 1
        height = end_y - start_y + 1
        wall_matrix = wall(np.arange(width * height).reshape(width, height))
        self.board[start_x:end_x + 1, start_y:end_y + 1] = wall_matrix

    def create_blank_board(self):
        matrix = np.empty((self.height, self.width), dtype=object)
        field = np.vectorize(lambda x: Field())
        matrix[:] = field(np.arange(self.width * self.height).reshape(self.height, self.width))
        self.board = matrix

if __name__ == "__main__":
    sand_sim = SandSimulation()
    sand_sim.simulate()
