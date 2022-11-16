import random

# environment function
def environment(action):
    x, y = move(action)
    x0, y0 = before_moving(action)
    if matrix[x][y] == 'f':
        a = [x, y, True]
        matrix[x][y], matrix[x0][y0] = matrix[x0][y0], '-'
    else:
        a = [x, y, False]
        matrix[x][y], matrix[x0][y0] = matrix[x0][y0], matrix[x][y]

    return a  # as agent's position (percept).


# getting the last position
def before_moving(action):
    l_move = movements[len(movements) - 1]
    x = l_move[0]
    y = l_move[1]
    return x, y


# determining the agent's position after moving
def move(action):
    last_move = movements[len(movements) - 1]
    if action == "left":
        x = last_move[0]
        y = last_move[1] - 1
    elif action == "right":
        x = last_move[0]
        y = last_move[1] + 1
    elif action == "up":
        x = last_move[0] - 1
        y = last_move[1]
    elif action == "down":
        x = last_move[0] + 1
        y = last_move[1]
    return x, y


# if we have no choice to move we can use last positions in agent function
def we_have_no_choice(x, y):
    x_up, y_up = move('up')
    x_down, y_down = move('down')
    x_left, y_left = move('left')
    x_right, y_right = move('right')
    if ([x_up, y_up, False] in movements) or (matrix[x_up][y_up] == "*" and
        [x_down, y_down, False] in movements) or (matrix[x_down][y_down] == "*" and
        [x_left, y_left, False] in movements) or (matrix[x_left][y_left] == "*" and
        [x_right, y_right, False] in movements) or (matrix[x_right][y_right] == "*"):
        return True
    return False


# deciding the next move
def agent(percept):
    directions = ['left', 'right', 'up', 'down']
    action = random.choice(directions)
    x, y = move(action)
    if ([x, y, False] in movements):
        if we_have_no_choice(x, y):
            return action
        return agent(percept)
    elif (matrix[x][y] == "*"):
        return agent(percept)
    return action


# make the matrix
file = open("./test.txt", "r")
x, y = file.readline().split(",")
x, y = int(x), int(y)
lines = file.readlines()
global matrix
matrix = [[lines[i][j] for j in range(y)] for i in range(x)]

global a  #agent position
for i in range(x):
    if "a" in matrix[i]:
        a = [i, matrix[i].index("a"), False]
# add fist node to list
movements = []
movements.append(a)


# function for printing the matrix
def print_matrix():
    print()
    for i in range(x):
        for j in range(y):
            print(matrix[i][j], end="")
        print()
    print()


if __name__ == '__main__':
    while a[2] == False:
        action = agent(percept=a)
        a = environment(action=action)
        movements.append(a)
        print_matrix()
        #time.sleep(0.5)

    print(f"\n{movements}\n{len(movements)}")
    print_matrix()

