

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
    global agent_pos_x, agent_pos_y, target_pos_x, target_pos_y
    movements = {}
    dim_y, dim_x = len(presentation_agent), len(presentation_agent[0])
    presentation_agent[agent_pos_y][agent_pos_x] = '0'

    if (agent_pos_y + 1 <= dim_y - 1 and presentation_agent[agent_pos_y + 1][agent_pos_x] not in ('*', '0')):
        if target_pos_y == agent_pos_y+1 and agent_pos_x == target_pos_x:
            print(f"MY agent position is {agent_pos_y} {agent_pos_x} and in move Down I get target")
            return True
        movements[f"{agent_pos_y + 1} {agent_pos_x}"] = "Down"
    if (agent_pos_y - 1 >= 0 and presentation_agent[agent_pos_y - 1][agent_pos_x] not in ('*', '0')):
        if target_pos_y == agent_pos_y-1 and agent_pos_x == target_pos_x:
            print(f"MY agent position is {agent_pos_y} {agent_pos_x} and in move Up I get target")
            return True
        movements[f"{agent_pos_y - 1} {agent_pos_x}"] = "Up"
    if (agent_pos_x - 1 >= 0 and presentation_agent[agent_pos_y][agent_pos_x - 1] not in ('*', '0')):
        if target_pos_y == agent_pos_y and agent_pos_x-1 == target_pos_x:
            print(f"MY agent position is {agent_pos_y} {agent_pos_x} and in move Left I get target")
            return True
        movements[f"{agent_pos_y} {agent_pos_x - 1}"] = "Left"
    if (agent_pos_x + 1 <= dim_x - 1 and presentation_agent[agent_pos_y][agent_pos_x + 1] not in ('*', '0')):
        if target_pos_y+1 == agent_pos_y and agent_pos_x+1 == target_pos_x:
            print(f"MY agent position is {agent_pos_y} {agent_pos_x} and in move Right I get target")
            return True
        movements[f"{agent_pos_y} {agent_pos_x + 1}"] = "Right"
    return movements


def agent():
    global presentation_agent, agent_pos_x, agent_pos_y, target_pos_x, target_pos_y, next_movements
    if target_pos_x == agent_pos_x and target_pos_y == agent_pos_y:
        print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
        return 1

    output = calc_directions(presentation_agent)
    if type(output) == bool:
        return 1
    next_movements = {**next_movements, **output}
    print(f'agent current position is {agent_pos_y}, {agent_pos_x} .')
    return 0


if __name__ == '__main__':
    # read data from file
    with open('env1.txt', 'r+') as reader:
        diagram = reader.readlines()
        for i in range(len(diagram)):
            diagram[i] = diagram[i].strip()

    dim_y, dim_x = (len(diagram), len(diagram[0]))

    target_pos_y, target_pos_x = valid_pos_target(dim_y=dim_y, dim_x=dim_x, diagram=diagram)
    agent_pos_y, agent_pos_x = valid_pos_agent(dim_y=dim_y, dim_x=dim_x, diagram=diagram)

    presentation_agent = create_presentation_agent(agent_pos=(agent_pos_y, agent_pos_x),
                                                   dim=(dim_y, dim_x),
                                                   diagram=diagram)

    next_movements = {}
    movements = calc_directions(presentation_agent)

    while (True):
        for mov in movements.keys():
            agent_pos_y, agent_pos_x = list(map(int, mov.split()))
            flag = agent()
            if flag:
                break
        if flag:
            print("GOAL IS FOUND")
            break
        movements = next_movements.copy()
        print(f"NEXT MOVE IS {movements}")
        next_movements.clear()
        if len(movements) == 0:
            print("GOAL Not FOUND")
            break
