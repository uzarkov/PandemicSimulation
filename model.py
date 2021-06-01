from __future__ import annotations

import math
from typing import List
from random import random
import constants
from math import sin, cos, pi


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)


class InfectedArea:
    center: List[Point]

    def __init__(self):
        self.center = []


class Cell:
    location: Point
    direction: Point
    sickness_time: int = 0
    state: str = "green"

    def __init__(self, location: Point, direction: Point):
        self.location = location
        self.direction = direction

    def tick(self) -> None:
        self.location = self.location.add(self.direction)

    def color(self) -> str:
        return self.state

    def heal(self) -> None:
        self.state = "blue"
        self.sickness_time = 0

    @staticmethod
    def is_dead(death_chance) -> bool:
        return random() < death_chance

    def infect(self):
        self.state = "red"

    def is_infected(self) -> bool:
        return self.state == "red"


class Model:
    population: dict[str, List[Cell]]
    infected_area: InfectedArea
    day: float
    full_day: int
    dead_count: int

    def __init__(self, param_pack):
        self.population = {'red': [], 'green': [], 'blue': []}
        self.infected_area = InfectedArea()
        self.day = 1
        self.full_day = 1
        self.dead_count = 0
        self.param_pack = param_pack

        for i in range(0, self.param_pack.population_size - 1):
            starting_location = self.random_location()
            starting_direction = self.random_direction(constants.CELL_SPEED)
            self.population['green'].append(Cell(starting_location, starting_direction))

        infected_cell = Cell(self.random_location(), self.random_direction(constants.CELL_SPEED))
        infected_cell.infect()
        self.population['red'].append(infected_cell)

    def tick(self) -> None:
        self.day += 0.1
        if (self.full_day + 1) <= self.day:
            self.full_day += 1

        self.infected_area.center.clear()

        infected_list = []
        for cell in self.population['red']:
            if cell.sickness_time > self.param_pack.sickness_time:
                if cell.is_dead(self.param_pack.death_chance):
                    self.dead_count += 1
                else:
                    cell.heal()
                    self.population['blue'].append(cell)
            else:
                cell.tick()
                self.enforce_bounds(cell)
                self.infected_area.center.append(cell.location)
                cell.sickness_time += 0.1
                infected_list.append(cell)

        self.population['red'] = infected_list

        healthy_list = []
        for cell in self.population['green']:
            cell.tick()
            self.enforce_bounds(cell)
            if self.check_for_infection(cell, self.param_pack.infection_chance):
                cell.infect()
                self.population['red'].append(cell)
            else:
                healthy_list.append(cell)
        self.population['green'] = healthy_list

        cured_list = []
        for cell in self.population['blue']:
            cell.tick()
            self.enforce_bounds(cell)
            if self.check_for_infection(cell, self.param_pack.reinfection_chance):
                cell.infect()
                self.population['red'].append(cell)
            else:
                cured_list.append(cell)
        self.population['blue'] = cured_list

    def check_for_infection(self, cell: Cell, infection_chance: float) -> bool:
        for area in self.infected_area.center:
            x = math.sqrt(math.pow(cell.location.x - area.x, 2) + math.pow(cell.location.y - area.y, 2))
            if x < 2 * constants.CELL_RADIUS / 2:
                if random() < infection_chance:
                    return True
        return False

    def random_location(self) -> Point:
        starting_x = abs(random() * constants.BOUNDS_WIDTH - constants.MAX_X)
        starting_y = abs(random() * constants.BOUNDS_HEIGHT - constants.MAX_Y)
        return Point(starting_x, starting_y)

    def random_direction(self, speed: float) -> Point:
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1

        elif cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1

        elif cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1

        elif cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def is_complete(self) -> bool:
        red_len = len(self.population['red'])

        return red_len == 0

    def data_package(self):
        red_len = len(self.population['red'])
        green_len = len(self.population['green'])
        blue_len = len(self.population['blue'])
        population_size = red_len + green_len + blue_len
        day = self.full_day
        healthy_size = green_len
        sick_size = red_len
        cured_size = blue_len
        dead_size = self.dead_count

        return population_size, day, healthy_size, sick_size, cured_size, dead_size
