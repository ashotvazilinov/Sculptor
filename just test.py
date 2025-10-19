while get_pos_x() != x:
    if abs(x - get_world_size() - get_pos_x()) + 1 > x - get_pos_x():
        move(East)
    else:
        move(West)
while get_pos_y() != y:
    if abs(y - get_world_size() - get_pos_y()) +1 > y - get_pos_y():
        move(North)
        quick_print(abs(y - get_world_size() - get_pos_y()))
    else:
        move(South)
