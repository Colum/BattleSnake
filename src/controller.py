import json
import random
import numpy
from enum import Enum
from .a_star import a_star


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    NONE = None


'''
helper functions
'''

def get_position_vector(position):
    return numpy.array([position['x'], position['y']])


def normalize_vector(vector):
    return vector / numpy.linalg.norm(vector)


def distance_scalar(vector1, vector2):
    return numpy.linalg.norm(vector1 - vector2)


def get_move_direction(head_position, move_position):
    direction_vector = numpy.subtract(move_position, head_position)
    if numpy.array_equal(direction_vector, [0, 1]):
        return Direction.DOWN.value
    elif numpy.array_equal(direction_vector, [0, -1]):
        return Direction.UP.value
    elif numpy.array_equal(direction_vector, [1, 0]):
        return Direction.RIGHT.value
    elif numpy.array_equal(direction_vector, [-1, 0]):
        return Direction.LEFT.value
    else:
        return Direction.NONE.value

def is_unoccupied(position, occupied_positions):
    for occupied_position in occupied_positions:
        if numpy.array_equal(occupied_position, position):
            return False
    return True

def get_occupied_positions(snakes):
    # tail does not count as an occupied space if health is 100 (ie. just ate)
    occupied_positions = [get_position_vector(snake_position) for snake in snakes for snake_position in (snake['body'][:-1] if snake['health'] < 100 else snake['body'])]
    return occupied_positions

def get_possible_moves(width, height, position, snakes):
    occupied_positions = get_occupied_positions(snakes)

    up = numpy.add(position, [0, -1])
    down = numpy.add(position, [0, 1])
    left = numpy.add(position, [-1, 0])
    right = numpy.add(position, [1, 0])

    possible_moves = []

    if is_unoccupied(up, occupied_positions) and up[1] > -1:
        possible_moves.append(Direction.UP.value)
    if is_unoccupied(down, occupied_positions) and down[1] < height:
        possible_moves.append(Direction.DOWN.value)
    if is_unoccupied(left, occupied_positions) and left[0] > -1:
        possible_moves.append(Direction.LEFT.value)
    if is_unoccupied(right, occupied_positions) and right[0] < width:
        possible_moves.append(Direction.RIGHT.value)

    return possible_moves


def get_food_positions(food_list):
    food_positions = [get_position_vector(food) for food in food_list]
    return food_positions


def get_closest_food_positions(position, food_positions):
    return sorted(food_positions, key=lambda x: distance_scalar(x, position))

'''
path finding functions
'''

def chase_tail(graph, body):
    head = get_position_vector(body[0])
    tail = get_position_vector(body[-1])

    path_to_tail = a_star(graph, head, tail)

    if not path_to_tail:
        return None
    return get_move_direction(head, path_to_tail[0])


def go_to_closest_food(graph, body, food):
    head = get_position_vector(body[0])
    food_positions = get_food_positions(food)
    closest_food_positions = get_closest_food_positions(head, food_positions)

    for close_food_position in closest_food_positions:
        moves_to_food = a_star(graph, head, close_food_position)
        if moves_to_food:
            return get_move_direction(head, moves_to_food[0])
    
    # no paths to food
    return None


def determine_move(data):
    turn = data['turn']
    board = data['board']
    my_snake = data['you']
    my_body = my_snake['body']
    my_head = get_position_vector(my_body[0])

    height = board['height']
    width = board['width']
    food = board['food']
    snakes = board['snakes']

    my_health = my_snake['health']

    occupied_positions = get_occupied_positions(snakes)
    graph = {
        'occupied_positions': occupied_positions,
        'width': width,
        'height': height
    }

    # chase tail
    if len(my_body) > 7 and 50 < my_health < 100:
        move = chase_tail(graph, my_body)
        if move:
            return move
    else:
        # go to closest food
        move = go_to_closest_food(graph, my_body, food)
        if move:
            return move
        else:
            move = chase_tail(graph, my_body)
            if move:
                return move

    # last resort
    possible_moves = get_possible_moves(width, height, my_head, snakes)
    if possible_moves:
        random_move = random.choice(possible_moves)
        return random_move

    # no moves left
    return Direction.UP.value


'''
main function
'''

def controller(req):
    # gather data from Battlensake request
    data = {**req}
    # snake logic
    move = determine_move(data)
    return move
