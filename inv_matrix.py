ALPHABET_TABLE = {
  'A': (1, -26),
  'B': (2, -25),
  'C': (3, -24),
  'D': (4, -23),
  'E': (5, -22),
  'F': (6, -21),
  'G': (7, -20),
  'H': (8, -19),
  'I': (9, -18),
  'J': (10, -17),
  'K': (11, -16),
  'L': (12, -15),
  'M': (13, -14),
  'N': (14, -13),
  'O': (15, -12),
  'P': (16, -11),
  'Q': (17, -10),
  'R': (18, -9),
  'S': (19, -8),
  'T': (20, -7),
  'U': (21, -6),
  'V': (22, -5),
  'W': (23, -4),
  'X': (24, -3),
  'Y': (25, -2),
  'Z': (26, -1),
  '-': (27, 0),
}

# key is a 4 by 4 matrix, which its determinant has an inverse 1 mod 27
KEY = [ [ 1, 1, 1, 1 ],
        [ 1, 2, 1, 5 ],
        [ 2, 1, 2, 3 ],
        [ 7, 1, 3, 1 ] ]    


def determinant(matrix):
  if len(matrix) == 1:
    return matrix[0][0]
  elif len(matrix) == 2:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
  else:
    det = 0
    for i in range(len(matrix)):
      det += matrix[0][i] * determinant(minor(matrix, 0, i)) * (-1)**i
    return det

def minor(matrix, row, col):
  return [row[:col] + row[col+1:] for row in (matrix[:row]+matrix[row+1:])]


def inverse(matrix):
  det = determinant(matrix)
  if det == 0:
    raise ValueError('Determinant is zero')
  else:
    matrix = transpose(cofactor(matrix))
    for i in range(len(matrix)):
      for j in range(len(matrix)):
        matrix[i][j] = matrix[i][j] * 1 / det
    return matrix

def transpose(matrix):
  return [list(row) for row in zip(*matrix)]

def cofactor(matrix):
  return [[(-1)**(i+j) * determinant(minor(matrix, i, j)) for j in range(len(matrix))] for i in range(len(matrix))]

print(inverse([[1,2], [3,4]]))