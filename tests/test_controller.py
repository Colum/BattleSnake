from src.controller import Direction, get_move_direction, get_possible_moves, get_position_vector, get_food_positions, could_kill_enemy
import numpy as np


def test_get_position_vector():
    position_dict = {
        'x': 2,
        'y': 7
    }
    position = get_position_vector(position_dict)
    expected_position = np.array([2, 7])
    assert np.array_equal(position, expected_position)


def test_direction_UP():
    head = [2,3]
    move_position = [2,2]
    move_direction = get_move_direction(head, move_position)
    assert move_direction == Direction.UP.value

def test_direction_DOWN():
    head = [2,3]
    move_position = [2,4]
    move_direction = get_move_direction(head, move_position)
    assert move_direction == Direction.DOWN.value

def test_direction_LEFT():
    head = [1,3]
    move_position = [0,3]
    move_direction = get_move_direction(head, move_position)
    assert move_direction == Direction.LEFT.value

def test_direction_RIGHT():
    head = [3,3]
    move_position = [4,3]
    move_direction = get_move_direction(head, move_position)
    assert move_direction == Direction.RIGHT.value

def test_get_possible_moves_alone():
    snakes = [
        {
            "id": "db9afed1-d45d-4bb0-85d8-f48de5dd3d79",
            "name": "",
            "health": 98,
            "body": [
                {
                    "x": 11,
                    "y": 10
                },
                {
                    "x": 11,
                    "y": 11
                },
                {
                    "x": 10,
                    "y": 11
                },
                {
                    "x": 9,
                    "y": 11
                }
            ]
        }
    ]

    my_head = [11, 10]

    possible_moves = get_possible_moves(15, 15, my_head, snakes)
    expected_possible_moves = [Direction.UP.value, Direction.LEFT.value, Direction.RIGHT.value]

    assert np.array_equal(expected_possible_moves, possible_moves)


def test_get_food_positions():

    food = [
        {
            "x": 3,
            "y": 1
        },
        {
            "x": 6,
            "y": 3
        },
        {
            "x": 9,
            "y": 5
        }
    ]

    food_positions = get_food_positions(food)
    print(food_positions)
    expected_food_positions = np.array([[3, 1], [6, 3], [9, 5]])
    print(expected_food_positions)
    assert np.array_equal(expected_food_positions, food_positions)

def test_could_attack():
    data = {
        "board": {
            "height": 11,
            "width": 11,
            "snakes": [
                {
                    "id": "gs_6kRDgWTKdVKBKY4mGStVtPq9",
                    "name": "colum / enemy",
                    "health": 70,
                    "body": [
                        {
                            "x": 3,
                            "y": 4

                        },
                        {
                            "x": 4,
                            "y": 4

                        },
                    ],
                    "shout": ""

                },
                {
                    "id": "gs_qr6Y7B3Dyd6b6cKQpKKqW7mH",
                    "name": "colum / snake1",
                    "health": 100,
                    "body": [
                        {
                            "x": 9,
                            "y": 6

                        },
                        {
                            "x": 9,
                            "y": 7

                        },
                        {
                            "x": 9,
                            "y": 8
                        }
                    ],
                    "shout": ""

                }

            ]

        },
        "you": {
            "id": "gs_qr6Y7B3Dyd6b6cKQpKKqW7mH",
            "name": "colum / snake1",
            "health": 100,
            "body": [
                {
                    "x": 9,
                    "y": 6

                },
                {
                    "x": 9,
                    "y": 7

                },
                {
                    "x": 9,
                    "y": 8
                }
            ],
            "shout": ""

        }
    }
    my_snake = data['you']
    my_body = my_snake['body']
    height = data['board']['height']
    width = data['board']['width']
    snakes = data['board']['snakes']

    could_kill_enemy(snakes, my_body, height, width, len(my_body))
