ALPHABET_TABLE = {
  'A': 1,
  'B': 2,
  'C': 3,
  'D': 4,
  'E': 5,
  'F': 6,
  'G': 7,
  'H': 8,
  'I': 9,
  'J': 10,
  'K': 11,
  'L': 12,
  'M': 13,
  'N': 14,
  'O': 15,
  'P': 16,
  'Q': 17,
  'R': 18,
  'S': 19,
  'T': 20,
  'U': 21,
  'V': 22,
  'W': 23,
  'X': 24,
  'Y': 25,
  'Z': 26,
  '-': 0,
}

# key is a 4 by 4 matrix, which its determinant has an inverse 1 mod 27
KEY = [ [ 1, 1, 1, 1 ],
        [ 1, 2, 1, 5 ],
        [ 2, 1, 2, 3 ],
        [ 7, 1, 3, 1 ] ]

MOD = 27    

# inverse calculates the inverse of a matrix
def inverse(matrix):
  det = determinant(matrix)
  if det == 0:
    raise ValueError('Determinant is zero')
  else:
    matrix = transpose(cofactor(matrix))
    return matrix

# determinant calculates the determinant of a matrix
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

# minor calculates the minor of a matrix
def minor(matrix, row, col):
  return [row[:col] + row[col+1:] for row in (matrix[:row]+matrix[row+1:])]

# transpose calculates the transpose of a matrix
def transpose(matrix):
  return [list(row) for row in zip(*matrix)]

# cofactor calculates the cofactor of a matrix
def cofactor(matrix):
  return [[(-1)**(i+j) * determinant(minor(matrix, i, j)) for j in range(len(matrix))] for i in range(len(matrix))]


# break_message breaks the message into a list of list of 4 elements. 
# if the last list has less than 4 elements, it will be padded with '-'
def split_message(message):
  message = message.upper()
  message = message.replace(' ', '-')
  
  if len(message) % 4 != 0:
    message += '-' * (4 - len(message) % 4)

  return [list(message[i:i+4]) for i in range(0, len(message), 4)]

# to_number converts a message into a list of list of numbers
def to_number(message):
  l = split_message(message)
  for i in range(len(l)):
    for j in range(len(l[i])):
      l[i][j] = ALPHABET_TABLE[l[i][j]]
  return l

# to_letter converts a list of list of numbers into a message
def to_letter(matrix):
  result = ''
  for i in range(len(matrix)):
    for j in range(len(matrix[i])):
      for k, v in ALPHABET_TABLE.items():
        if v == matrix[i][j]:
          result += k
  return result

# matrix_multiply_key multiplies a matrix with a key
def matrix_multiply_key(matrix, key):
  result = [[0 for i in range(len(key))] for j in range(len(matrix))]
  for i in range(len(key)):
    for j in range(len(matrix)):
      for k in range(len(matrix[0])):
        result[j][i] += matrix[j][k] * key[i][k]
        result[j][i] = result[j][i] % MOD
  return result

# inverse_key performs modulo 27 operation on every element in the matrix
def inverse_key_matrix(key):
  inv_det = find_inverse_det(key)
  inverse_matrix = inverse(key)
  for i in range(len(inverse_matrix)):
    for j in range(len(inverse_matrix[i])):
      inverse_matrix[i][j] = (inverse_matrix[i][j] * inv_det) % MOD
  return inverse_matrix

# find_inverse_det finds the nearest inverse value of the determinant of a key mod 27
def find_inverse_det(key):
  for i in range(MOD):
    if (i * determinant(key)) % MOD == 1:
      return i

# encrypt encrypts a message
def encrypt(text, key):
  digraph = to_number(text)
  cipher = matrix_multiply_key(digraph, key)
  for i in range(len(cipher)):
    for j in range(len(cipher[i])):
      cipher[i][j] %= MOD
  return to_letter(cipher)

# decrypt decrypts a cipher text
def decrypt(cipher, key):
  digraph = to_number(cipher)
  inverse_key = inverse_key_matrix(key)
  plain = matrix_multiply_key(digraph, inverse_key)
  for i in range(len(plain)):
    for j in range(len(plain[i])):
      plain[i][j] %= MOD
  return to_letter(plain).replace('-', ' ')



message = 'PLEASE USE THE OTHER DOOR AND DO NOT ENTER THIS ROOM'
cipher = encrypt(message, KEY)

print(cipher)
print(decrypt(cipher, KEY))
