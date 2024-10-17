from typing import List

SOUTH_NORTH = "south_north"
WEST_EAST = "west_east"
TIME = "Time"
HEIGHT_DIM_PREFIX = "height_"
FREQUENCY = "frequency"
DIRECTION = "direction"


def get_height_dim_from_parameter_key(key: str) -> str:
    return f"{HEIGHT_DIM_PREFIX}{key}"


def get_acceptable_dims_from_parameter_key(key: str) -> List[List[str]]:
    height_dim = get_height_dim_from_parameter_key(key)
    return [
        [],
        [SOUTH_NORTH, WEST_EAST],
        [TIME, SOUTH_NORTH, WEST_EAST],
        [height_dim, SOUTH_NORTH, WEST_EAST],
        [TIME, height_dim, SOUTH_NORTH, WEST_EAST],
        [TIME, SOUTH_NORTH, WEST_EAST, FREQUENCY, DIRECTION],
    ]
