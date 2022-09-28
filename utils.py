import numpy as np
from constants import BAD_PATTERNS

def get_zero_indices(board_mask):
    x,y = np.where(board_mask == 0)
    data = []
    for i in range(len(x)): data.append((x[i], y[i]))
    return data

def get_neighbors(board_mask, xy=(0,0)):
    x,y = xy
    xmin = x-1 if x-1 >= 0 else False
    xmax = x+1 if x+1 <= 6 else False
    ymin = y-1 if y-1 >= 0 else False
    ymax = y+1 if y+1 <= 6 else False
    neighbors = []
    if xmin is not False: neighbors.append(board_mask[xmin][y])
    if xmax is not False: neighbors.append(board_mask[xmax][y]) 
    if ymin is not False: neighbors.append(board_mask[x][ymin])
    if ymax is not False: neighbors.append(board_mask[x][ymax])
    return neighbors

def is_hole(board_mask, xy=(0,0)):
    x,y = xy
    neighbors = get_neighbors(board_mask, (x,y))
    if sum(neighbors) == len(neighbors) and board_mask[x][y] == 0: return True
    else: return False
    
def im2col(A, BLKSZ):
    M,N = A.shape
    col_extent = N - BLKSZ[1] + 1
    row_extent = M - BLKSZ[0] + 1
    start_idx = np.arange(BLKSZ[0])[:,None]*N + np.arange(BLKSZ[1])
    offset_idx = np.arange(row_extent)[:,None]*N + np.arange(col_extent)
    return np.take (A,start_idx.ravel()[:,None] + offset_idx.ravel())

def find_pattern(field, pattern):
    col_match = im2col(field.copy(), pattern.shape) == pattern.ravel()[:,None]
    out_shape = np.asarray(field.shape) - np.asarray(pattern.shape) + 1
    RC = np.where(col_match.all(0).reshape(out_shape))
    R, C = np.where(col_match.all(0).reshape(out_shape))
    
    has_pattern = False
    for i in RC:
        if len(i) > 0:
            has_pattern = True
            
    coords = []
    for i in range(len(R)):
        coords.append((R[i], C[i]))
        
    return has_pattern, coords

def place_shape(board, shape, xy=(0,0)):
    
    y, x = xy
    h1, w1 = board.mask.shape
    h2, w2 = shape.mat.shape
    
    # get slice ranges for matrix1
    x1min = max(0, x)
    y1min = max(0, y)
    x1max = max(min(x + w2, w1), 0)
    y1max = max(min(y + h2, h1), 0)
    
    # get slice ranges for matrix2
    x2min = max(0, -x)
    y2min = max(0, -y)
    x2max = min(-x + w1, w2)
    y2max = min(-y + h1, h2)
    
    # create and return a new matrix
    board_mask_copy = board.mask.copy()
    board_mask_copy[y1min:y1max, x1min:x1max] += shape.mat[y2min:y2max, x2min:x2max]
    x2, y2 = np.where(board_mask_copy == 2)
    
    # place on an empty board too
    bmc = np.zeros((9,9), dtype=int)
    bmc[y1min:y1max, x1min:x1max] += shape.mat[y2min:y2max, x2min:x2max]
    
    if len(x2) > 0:
        return False, "Shape overlaps."
    
    if np.sum(board_mask_copy) > (np.sum(board_mask_copy) + np.sum(shape.mat)):
        return False, "Shape falls outside of board."
    
    for ij in get_zero_indices(board_mask_copy):
        if is_hole(board_mask_copy, (ij)):
            return False, "Shape created 1x1 hole."
        
    for bp in BAD_PATTERNS:
        has_pattern, coords = find_pattern(board_mask_copy, bp)
        if has_pattern:
            return False, "Shape created bad pattern."
    
    board.mask = board_mask_copy
    board.append_used_shape(np.array(bmc), shape.sym)
    return True, ""