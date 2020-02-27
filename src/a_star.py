import numpy
import heapq
'''
https://en.wikipedia.org/wiki/A*_search_algorithm
http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html

A* finds the shortest path from start to goal. It is an extension of Dijkstra's algorithm
minimizes f(n) = g(n) + h(n)
n: next node on the path
f(n) A* cost
g(n): cost of path from the start node to n
h(n): heuristic function that estimates cost from n to goal

A* terminates when the path it extends is from start to goal (ie. solution found)
or there are no more paths to extend (ie. no solution)
'''


class Node:
    __slots__ = ('parent_node', 'position', 'f', 'g', 'h')

    def __init__(self, parent_node=None, position=None):
        self.parent_node = parent_node
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return numpy.array_equal(self.position, other.position)

    def __hash__(self):
        return hash((self.position[0], self.position[1]))

    def __lt__(self, other):
        return self.f < other.f

# steps through linked nodes and returns path in the correct order
def reconstruct_path(solution):
    path = []
    while solution is not None:
        path.append(solution.position)
        solution = solution.parent_node
    return path[len(path)-2::-1]

# Manhattan distance
def heuristic_cost(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

def a_star(graph, start_position, goal_position):
    occupied_positions = graph['occupied_positions']
    width = graph['width']
    height = graph['height']

    start_node = Node(None, start_position)
    end_node = Node(None, goal_position)

    # nodes that have not been fully evaluated
    open_set = set()
    # node priority queue implemented as a heap
    open_heap = []
    # nodes that have been fully evaluated
    closed_set = set()
    # all four adjacent moves (up, down, left, right)
    adjacent_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    open_set.add(start_node)
    heapq.heappush(open_heap, start_node)

    try:
        while open_set:
            current_node = heapq.heappop(open_heap)

            # return path if solution found
            if current_node == end_node:
                return reconstruct_path(current_node)

            # open_set.remove(current_node)
            closed_set.add(current_node)
            children = set()
            # generate child nodes
            for move in adjacent_moves:
                new_position = numpy.add(current_node.position, move)

                # check border boundaries
                if new_position[0] not in range(0, width) or new_position[1] not in range(0, height):
                    continue

                # check if position is occupied
                is_occupied = False
                for occupied_position in occupied_positions:
                    if numpy.array_equal(new_position, occupied_position):
                        is_occupied = True
                        break
                if is_occupied:
                    continue

                new_node = Node(current_node, new_position)
                children.add(new_node)
                
            # check if child_node is in closed_list 
            for child_node in children:
                
                is_closed = False
                for closed_node in closed_set:
                    if child_node == closed_node:
                        is_closed = True
                        break
                if is_closed:
                    continue

                child_node.g = current_node.g + 1
                child_node.h = heuristic_cost(child_node.position, end_node.position)
                child_node.f = child_node.g + child_node.h

                in_open_set = False
                for open_node in open_set:
                    # >= makes straighter lines, > makes squggly lines
                    if child_node == open_node and child_node.g >= open_node.g:
                        in_open_set = True
                        break
                
                if in_open_set:
                    continue
                
                open_set.add(child_node)
                heapq.heappush(open_heap, child_node)
    except:
        pass

    return None