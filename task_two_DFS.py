

def valid_pos_target(dim_y, dim_x, diagram):
    for i in range(dim_y):
        for j in range(dim_x):
            if diagram[i][j] == 'f':
                sample_y = i
                sample_x = j
    return (sample_y, sample_x)


def valid_pos_agent(dim_y, dim_x, diagram):
    for i in range(dim_y):
        for j in range(dim_x):
            if diagram[i][j] == 'a':
                sample_y = i
                sample_x = j
    return (sample_y, sample_x)


def create_presentation_agent(agent_pos, dim, diagram):
    presentation_agent = [[1 for i in range(dim[1])] for j in range(dim[0])]
    for i in range(len(diagram)):
        for j in range(len(diagram[i])):
            if (diagram[i][j] == '*'):
                presentation_agent[i][j] = '*'
            else:
                presentation_agent[i][j] = 1
    presentation_agent[agent_pos[0]][agent_pos[1]] = 0
    return presentation_agent


def calc_directions(presentation_agent):
    global stack_direction, agent_pos_x, agent_pos_y
    movements = []
    dim_y, dim_x = len(presentation_agent), len(presentation_agent[0])
    flag = False

    while (not flag):
        if (agent_pos_y + 1 <= dim_y - 1 and presentation_agent[agent_pos_y + 1][agent_pos_x] not in ('*', '0')):
            movements.append('DOWN')
            flag = True
        if (agent_pos_y - 1 >= 0 and presentation_agent[agent_pos_y - 1][agent_pos_x] not in ('*', '0')):
            movements.append('UP')
            flag = True
        if (agent_pos_x - 1 >= 0 and presentation_agent[agent_pos_y][agent_pos_x - 1] not in ('*', '0')):
            movements.append('LEFT')
            flag = True
        if (agent_pos_x + 1 <= dim_x - 1 and presentation_agent[agent_pos_y][agent_pos_x + 1] not in ('*', '0')):
            movements.append('RIGHT')
            flag = True

        if (not flag):
            presentation_agent[agent_pos_y][agent_pos_x] = '0'
            backward = stack_direction.pop()

            if (backward.lower() == 'right'):
                agent_pos_x -= 1
            elif (backward.lower() == 'left'):
                agent_pos_x += 1
            elif (backward.lower() == 'up'):
                agent_pos_y += 1
            else:
                agent_pos_y -= 1
            print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
            continue
        return movements


def env(action):
    global presentation_agent, agent_pos_x, agent_pos_y, target_pos_x, target_pos_y
    presentation_agent[agent_pos_y][agent_pos_x] = '0'
    # Expantion time
    # if action == 'RIGHT':
    #     agent_pos_x += 1
    # elif action == 'LEFT':
    #     agent_pos_x -= 1
    # elif action == 'UP':
    #     agent_pos_y -= 1
    # elif action == 'DOWN':
    #     agent_pos_y += 1
    # print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
    # if target_pos_x == agent_pos_x and target_pos_y == agent_pos_y:
    #     return 1
    # return 0
    # Produce time
    if action == 'RIGHT':
        if target_pos_x == agent_pos_x+1 and target_pos_y == agent_pos_y:
            agent_pos_x += 1
            print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
            return 1
        agent_pos_x += 1
        print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
        return 0
    elif action == 'LEFT':
        if target_pos_x == agent_pos_x-1 and target_pos_y == agent_pos_y:
            agent_pos_x -= 1
            print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
            return 1
        agent_pos_x -= 1
        print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
        return 0
    elif action == 'UP':
        if target_pos_x == agent_pos_x and target_pos_y == agent_pos_y-1:
            agent_pos_y -= 1
            print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
            return 1
        agent_pos_y -= 1
        print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
        return 0
    elif action == 'DOWN':
        if target_pos_x == agent_pos_x and target_pos_y == agent_pos_y+1:
            agent_pos_y += 1
            print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
            return 1
        agent_pos_y += 1
        print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
        return 0
    return 0

def agent(percept):
    global presentation_agent
    sum = 0
    agent_x, agent_y, goal = percept
    for i in presentation_agent:
        for j in i:
            sum += int(j) if j != '*' else 0
    if (goal):
        return True
    # elif (not goal and sum <= 1):
    #     print("Not found")
    #     return True
    return False


if __name__ == '__main__':
    # read data from file
    with open('env1.txt', 'r+') as reader:
        diagram = reader.readlines()
        for i in range(len(diagram)):
            diagram[i] = diagram[i].strip()

    dim_y, dim_x = (len(diagram), len(diagram[0]))

    target_pos_y, target_pos_x = valid_pos_target(dim_y=dim_y, dim_x=dim_x, diagram=diagram)
    agent_pos_y, agent_pos_x = valid_pos_agent(dim_y=dim_y, dim_x=dim_x, diagram=diagram)

    stack_direction = []
    presentation_agent = create_presentation_agent(agent_pos=(agent_pos_y, agent_pos_x),
                                                   dim=(dim_y, dim_x),
                                                   diagram=diagram)
    while (True):
        movements = calc_directions(presentation_agent)
        stack_direction.append(movements.pop())
        find_goal = env(stack_direction[-1])
        flag = agent((agent_pos_x, agent_pos_y, find_goal))
        if flag:
            print("GOAL IS FOUND")
            break
