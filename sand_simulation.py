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
    def __init__(self):
        """Initialize the SandSimulation object.

        After initializing the SandSimulation object, users should call the 'setup' method to
        configure the board with the desired parameters.
        """
        self.board = None
        self.sand_inlet = None

    def draw_board(self):
        for row in np.flipud(self.board.T):
            print("".join(str(field) for field in row))
        print()

    def simulate_sand_fall_step(self):
        x, y = self.check_fields_under(self.current_field)

        if y is None:
            return None

        self.board[x][y], self.board[self.current_field.x][self.current_field.y] = (
            self.board[self.current_field.x][self.current_field.y],
            self.board[x][y],
        )
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
        elif field.x + 1 < self.width and self.board[field.x + 1][new_y].type == "air":
            new_x = field.x + 1
        elif field.x - 1 >= 0 and self.board[field.x - 1][new_y].type == "air":
            new_x = field.x - 1
        else:
            return None, None

        return new_x, new_y

    def create_new_sand_particle(self):
        x, y = self.check_fields_under(
            Field(self.sand_inlet.x, self.sand_inlet.y, field_type="sand")
        )
        if y is None:
            return
        self.current_field = Field(x, y, field_type="sand")
        self.board[x][y] = self.current_field
        return self.current_field

    def setup(self):
        """Set up the board configuration.

        This method allows users to set up the board by specifying its dimensions, creating walls, defining an inlet, and starting the simulation.

        Usage:
            1. Enter the board dimensions as space-separated integers, e.g., "10 10". (Width and height must be between 5 and 100)
            2. To create a wall, type "r" followed by the wall parameters (start_x, start_y, end_x, end_y) as space-separated integers, e.g., "r" -> "1 1 4 4".
            3. To define the inlet for sand particles, type "s" followed by the inlet position (start_x, start_y) as space-separated integers, e.g., "s" -> "5 0".
            4. After setting up the board configuration, the simulation will start automatically.

        Example:
            >>> sand_sim = SandSimulation()
            >>> sand_sim.setup()
        """
        board_shape = input("").split(" ")
        width, height = int(board_shape[0]), int(board_shape[1])

        if not (5 <= width <= 100 and 5 <= height <= 100):
            raise ValueError("Width and height must be between 5 and 100 (inclusive).")

        self.width, self.height = width, height
        self.create_blank_board()
        while True:
            user_input = input("")
            if user_input == "r":
                wall_params = [int(i) for i in input().split(" ")]
                if len(wall_params) != 4:
                    raise ValueError("Wall parameters must consist of four integers.")
                start_x, start_y, end_x, end_y = wall_params
                if not (
                    0 <= start_x < self.width
                    and 0 <= start_y < self.height
                    and 0 <= end_x < self.width
                    and 0 <= end_y < self.height
                ):
                    raise ValueError("Wall parameters must be within valid bounds.")
                self.create_wall(start_x, start_y, end_x, end_y)
            elif user_input == "s":
                inlet_params = [int(i) for i in input().split(" ")]
                if len(inlet_params) != 2:
                    raise ValueError("Inlet parameters must consist of two integers.")
                start_x, start_y = inlet_params
                if not (0 <= start_x < self.width and 0 <= start_y < self.height):
                    raise ValueError("Inlet parameters must be within valid bounds.")
                self.sand_inlet = Field(start_x, start_y, field_type="inlet")
                self.board[self.sand_inlet.x, self.sand_inlet.y] = self.sand_inlet
                break

    def simulate(self, num_steps=None):
        """Simulate the behavior of sand particles on the board.

        This method simulates the movement of sand particles on the board. If the `setup` method hasn't been called before, it will be called automatically to configure the board with default values.

        Args:
            num_steps (int, optional): The number of simulation steps to perform. If not specified, the simulation will run until no further sand particles can move.

        Example:
            >>> sand_sim = SandSimulation()
            >>> sand_sim.simulate()  # Calls the setup method automatically if not already called before.
        """
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
        self.board[start_x : end_x + 1, start_y : end_y + 1] = wall_matrix

    def create_blank_board(self):
        matrix = np.empty((self.height, self.width), dtype=object)
        field = np.vectorize(lambda x: Field())
        matrix[:] = field(np.arange(self.width * self.height).reshape(self.height, self.width))
        self.board = matrix


if __name__ == "__main__":
    sand_sim = SandSimulation()
    sand_sim.simulate()
