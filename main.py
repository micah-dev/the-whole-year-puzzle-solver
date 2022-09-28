import utils
from constants import Board, SHAPES
from tqdm import tqdm
import time


for shape in SHAPES:
    shape.rots = shape.get_rots()


def get_board_possibility(board, srot, xy):
    new_board = Board(MONTH, DAY)
    new_board.mask = board.mask.copy()
    new_board.used_shapes = board.used_shapes.copy()
    placed, error = utils.place_shape(new_board, srot, xy)
    if placed: return True, new_board
    else: return False, new_board


DISPLAY_INTERMEDATE = False
MONTH = input("Enter target month:  ")
DAY   = input("Enter target day:    ")


board = Board(MONTH, DAY)
print("Start board:")
board.display()

start_time = time.time()

boards = [[board], [],[],[],[],[],[],[],[],[]]
n_placements = 0
for i in tqdm(range(len(boards)-1)):
    for board in tqdm(boards[i], leave=False):
        for shaperot in SHAPES[i].rots:
            for xy in utils.get_zero_indices(board.mask):
                success, new_board = get_board_possibility(board, shaperot, xy)
                if success:
                    boards[i+1].append(new_board)
                    n_placements += 1

boards[9][0].display()
print("--- %s seconds ---" % (time.time() - start_time))