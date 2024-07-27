"""Extension for csv2d module
"""


def get_indices(data: tuple[tuple[int, ...], ...], item: int):
    for index, listitem in enumerate([element for data_x in data for element in data_x]):
        if item == listitem:
            yield index


if __name__ == "__main__":
    csv_data = ((0, 1, 0), \
                (0, 1, 0), \
                (0, 1, 0))
    indices = list(get_indices(csv_data, 1))
    print(indices)