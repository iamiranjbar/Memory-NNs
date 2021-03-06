# -*- coding: utf-8 -*-
"""NNDL HW3 Q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WsMmVphKuMaYbH9HXHhAuf_ol-rAK4j-

# Problem 1 (Hebbian Rule)

## Import Libraries
"""

import math
import random
import numpy as np

"""## Hebbian Memory Nueral Network class"""

class HebMNN:

  def __init__(self, input_patterns, output_patterns):
    self.input_patterns = input_patterns
    self.memory = output_patterns
    self.input_nodes_count = len(self.input_patterns[0].flatten())
    self.output_nodes_count = len(self.memory[0].flatten())
    self.weights = np.zeros((self.input_nodes_count, self.output_nodes_count))
    self.weight_matrix_initialization()
    self.treshold = 0

  def weight_matrix_initialization(self): 
    for index in range(len(input_patterns)):
      input_pattern = self.input_patterns[index]
      output_pattern = self.memory[index]
      flatten_input_pattern = input_pattern.reshape((1, self.input_nodes_count))
      flatten_output_pattern = output_pattern.reshape((1, self.output_nodes_count))
      self.weights += np.dot(np.transpose(flatten_input_pattern), flatten_output_pattern)

  def predict(self, pattern, verbose=True):
    flatten_pattern = pattern.reshape((1, self.input_nodes_count))
    result = np.dot(flatten_pattern, self.weights)
    result[result > self.treshold] = 1
    result[result < self.treshold] = -1

    for memorise_pattern in self.memory:
      if (memorise_pattern.flatten() == result).all():
        if verbose:
          print('I remember =))')
        return memorise_pattern, True
    if verbose:
      print('I cant remember :((')
    return None, False

"""### Show matrix function"""

def show_result(matrix, pattern_found=None):
  if pattern_found is not None:
    if not pattern_found:
      print("Best achieved:")
    else:
      print("Result:")
  for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
      if matrix[i][j] == 1:
        print("#", end="")
      else:
        print("-", end="")
    print("")
  print("___________________________")

"""## Test Network"""

a_in_pattern = np.array([[-1,-1,-1,1,-1,-1,-1],
                        [-1,-1,-1,1,-1,-1,-1],
                        [-1,-1,-1,1,-1,-1,-1],
                        [-1,-1, 1,-1,1,-1,-1],
                        [-1,-1, 1,-1,1,-1,-1],
                        [-1, 1, 1, 1, 1,1,-1],
                        [-1,1,-1,-1,-1, 1,-1],
                        [-1,1,-1,-1,-1, 1,-1],
                        [1, 1, 1,-1, 1, 1, 1]])
b_in_pattern = np.array([[1, 1, 1, 1, 1, 1, 1],
                        [1,-1,-1,-1,-1,-1, 1],
                        [1,-1,-1,-1,-1, 1,-1],
                        [1,-1,-1,-1, 1,-1,-1],
                        [1, 1, 1, 1,-1,-1,-1],
                        [1,-1,-1,-1, 1,-1,-1],
                        [1,-1,-1,-1,-1, 1,-1],
                        [1,-1,-1,-1,-1,-1, 1],
                        [1, 1, 1, 1, 1, 1, 1]])
c_in_pattern = np.array([[-1,-1, 1, 1, 1, 1,-1],
                        [-1, 1,-1,-1,-1,-1, 1],
                        [1, -1,-1,-1,-1,-1,-1],
                        [1, -1,-1,-1,-1,-1,-1],
                        [1, -1,-1,-1,-1,-1,-1],
                        [1, -1,-1,-1,-1,-1,-1],
                        [1, -1,-1,-1,-1,-1,-1],
                        [-1, 1,-1,-1,-1,-1, 1],
                        [-1,-1, 1, 1, 1, 1,-1]])
a_out_pattern = np.array([[-1,1,-1],
                          [1,-1, 1],
                          [1, 1, 1],
                          [1,-1, 1],
                          [1,-1, 1]])
b_out_pattern = np.array([[1, 1,-1],
                          [1,-1, 1],
                          [1, 1,-1],
                          [1,-1, 1],
                          [1, 1,-1]])
c_out_pattern = np.array([[-1, 1, 1],
                          [ 1,-1,-1],
                          [ 1,-1,-1],
                          [ 1,-1,-1],
                          [-1, 1, 1]])
input_patterns = np.array([a_in_pattern, b_in_pattern, c_in_pattern])
output_patterns = np.array([a_out_pattern, b_out_pattern, c_out_pattern])
heb_mnn = HebMNN(input_patterns, output_patterns)

a_result, pattern_found = heb_mnn.predict(a_in_pattern)
show_result(a_result, pattern_found)

b_result, pattern_found = heb_mnn.predict(b_in_pattern)
show_result(b_result, pattern_found)

c_result, pattern_found = heb_mnn.predict(c_in_pattern)
show_result(c_result, pattern_found)

"""## Add noise and Test network robustness

### Add noise function
"""

def add_noise(pattern, noise_percentage=0.3):
  noisy_pattern = np.copy(pattern)
  pattern_cells = len(pattern.flatten())
  mistaken_cells_count = math.floor(noise_percentage * pattern_cells)
  to_change_indices = random.sample(range(pattern_cells), mistaken_cells_count)
  for index in to_change_indices:
    to_change_row = index // noisy_pattern.shape[1]
    to_change_col = index % noisy_pattern.shape[1]
    noisy_pattern[to_change_row][to_change_col] *= -1
  return noisy_pattern

"""### Miss data function"""

def miss_data(pattern, miss_percentage=0.3):
  missed_pattern = np.copy(pattern)
  black_cells = list(zip(*np.where(missed_pattern == 1)))
  black_cells_count = len(black_cells)
  mistaken_cells_count = math.floor(miss_percentage * black_cells_count)
  to_change_indices = random.sample(range(black_cells_count), mistaken_cells_count)
  for index in to_change_indices:
    to_change_row, to_change_col = black_cells[index]
    missed_pattern[to_change_row][to_change_col] = -1
  return missed_pattern

"""### Test against 10, 25 percent noises"""

ten_noisy_a = add_noise(a_in_pattern, 0.1)
show_result(ten_noisy_a)
ten_noisy_a_result, pattern_found = heb_mnn.predict(ten_noisy_a)
show_result(ten_noisy_a_result, pattern_found)

twfive_noisy_a = add_noise(a_in_pattern, 0.25)
show_result(twfive_noisy_a)
twfive_noisy_a_result, pattern_found = heb_mnn.predict(twfive_noisy_a)
show_result(twfive_noisy_a_result, pattern_found)

ten_noisy_b = add_noise(b_in_pattern, 0.1)
show_result(ten_noisy_b)
ten_noisy_b_result, pattern_found = heb_mnn.predict(ten_noisy_b)
show_result(ten_noisy_b_result, pattern_found)

twfive_noisy_b = add_noise(b_in_pattern, 0.25)
show_result(twfive_noisy_b)
twfive_noisy_b_result, pattern_found = heb_mnn.predict(twfive_noisy_b)
show_result(twfive_noisy_b_result, pattern_found)

ten_noisy_c = add_noise(c_in_pattern, 0.1)
show_result(ten_noisy_c)
ten_noisy_c_result, pattern_found = heb_mnn.predict(ten_noisy_c)
show_result(ten_noisy_c_result, pattern_found)

twfive_noisy_c = add_noise(c_in_pattern, 0.25)
show_result(twfive_noisy_c)
twfive_noisy_c_result, pattern_found = heb_mnn.predict(twfive_noisy_c)
show_result(twfive_noisy_c_result, pattern_found)

"""### Test against 10, 25 percent missing data"""

ten_missed_a = miss_data(a_in_pattern, 0.1)
show_result(ten_missed_a)
ten_missed_a_result, pattern_found = heb_mnn.predict(ten_missed_a)
show_result(ten_missed_a_result, pattern_found)

twfive_missed_a = miss_data(a_in_pattern, 0.25)
show_result(twfive_missed_a)
twfive_missed_a_result, pattern_found = heb_mnn.predict(twfive_missed_a)
show_result(twfive_missed_a_result, pattern_found)

ten_missed_b = miss_data(b_in_pattern, 0.1)
show_result(ten_missed_b)
ten_missed_b_result, pattern_found = heb_mnn.predict(ten_missed_b)
show_result(ten_missed_b_result, pattern_found)

twfive_missed_b = miss_data(b_in_pattern, 0.25)
show_result(twfive_missed_b)
twfive_missed_b_result, pattern_found = heb_mnn.predict(twfive_missed_b)
show_result(twfive_missed_b_result, pattern_found)

ten_missed_c = miss_data(c_in_pattern, 0.1)
show_result(ten_missed_c)
ten_missed_c_result, pattern_found = heb_mnn.predict(ten_missed_c)
show_result(ten_missed_c_result, pattern_found)

twfive_missed_c = miss_data(c_in_pattern, 0.25)
show_result(twfive_missed_c)
twfive_missed_c_result, pattern_found = heb_mnn.predict(twfive_missed_c)
show_result(twfive_missed_c_result, pattern_found)

"""## Run 100 times for calculating accuracy"""

correct = 0
all = 0
for _ in range(100):
  ten_noisy_a = add_noise(a_in_pattern, 0.1)
  ten_noisy_a_result, pattern_found = heb_mnn.predict(ten_noisy_a, False)
  if (a_out_pattern == ten_noisy_a_result).all():
    correct += 1
  all += 1

  ten_noisy_b = add_noise(b_in_pattern, 0.1)
  ten_noisy_b_result, pattern_found = heb_mnn.predict(ten_noisy_b, False)
  if (b_out_pattern == ten_noisy_b_result).all():
    correct += 1
  all += 1

  ten_noisy_c = add_noise(c_in_pattern, 0.1)
  ten_noisy_c_result, pattern_found = heb_mnn.predict(ten_noisy_c, False)
  if (c_out_pattern == ten_noisy_c_result).all():
    correct += 1
  all += 1

print("Ten Percent Noise accuracy: {} %".format(correct*100/all))

correct = 0
all = 0
for _ in range(100):
  twfive_noisy_a = add_noise(a_in_pattern, 0.25)
  twfive_noisy_a_result, pattern_found = heb_mnn.predict(twfive_noisy_a, False)
  if (a_out_pattern == twfive_noisy_a_result).all():
    correct += 1
  all += 1

  twfive_noisy_b = add_noise(b_in_pattern, 0.25)
  twfive_noisy_b_result, pattern_found = heb_mnn.predict(twfive_noisy_b, False)
  if (b_out_pattern == twfive_noisy_b_result).all():
    correct += 1
  all += 1

  twfive_noisy_c = add_noise(c_in_pattern, 0.25)
  twfive_noisy_c_result, pattern_found = heb_mnn.predict(twfive_noisy_c, False)
  if (c_out_pattern == twfive_noisy_c_result).all():
    correct += 1
  all += 1

print("Twenty Five Percent Noise accuracy: {} %".format(correct*100/all))

correct = 0
all = 0
for _ in range(100):
  ten_missed_a = miss_data(a_in_pattern, 0.1)
  ten_missed_a_result, pattern_found = heb_mnn.predict(ten_missed_a, False)
  if (a_out_pattern == ten_missed_a_result).all():
    correct += 1
  all += 1

  ten_missed_b = miss_data(b_in_pattern, 0.1)
  ten_missed_b_result, pattern_found = heb_mnn.predict(ten_missed_b, False)
  if (b_out_pattern == ten_missed_b_result).all():
    correct += 1
  all += 1

  ten_missed_c = miss_data(c_in_pattern, 0.1)
  ten_missed_c_result, pattern_found = heb_mnn.predict(ten_missed_c, False)
  if (c_out_pattern == ten_missed_c_result).all():
    correct += 1
  all += 1

print("Ten Percent Missing accuracy: {} %".format(correct*100/all))

correct = 0
all = 0
for _ in range(100):
  twfive_missed_a = miss_data(a_in_pattern, 0.25)
  twfive_missed_a_result, pattern_found = heb_mnn.predict(twfive_missed_a, False)
  if (a_out_pattern == twfive_missed_a_result).all():
    correct += 1
  all += 1

  twfive_missed_b = miss_data(b_in_pattern, 0.25)
  twfive_missed_b_result, pattern_found = heb_mnn.predict(twfive_missed_b, False)
  if (b_out_pattern == twfive_missed_b_result).all():
    correct += 1
  all += 1

  twfive_missed_c = miss_data(c_in_pattern, 0.25)
  twfive_missed_c_result, pattern_found = heb_mnn.predict(twfive_missed_c, False)
  if (c_out_pattern == twfive_missed_c_result).all():
    correct += 1
  all += 1

print("Twenty Five Percent Missing accuracy: {} %".format(correct*100/all))