import re

# from team_assignment import team_assignment


show_team = True
infoFile = '../datasets/frej-bp.txt'

if show_team:
    with open(infoFile, 'r') as f:
        data = f.read()
        color_list = re.findall(r'team, (.*?) [J,j]erseys[)]', data)
        print(color_list)
