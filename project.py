
from sympy import *
import sys
import time
import itertools as it


def read_input(filename):
    
    with open(filename) as f:
        lines = f.readlines()
    graph = {}
    ind = {}
    count = 0
    for line in lines:
        line = line.split('=')
        line[0] = list(exp(line[0]).free_symbols)[0]
        if str(line[0]).startswith('d'):
            line[0] = str(line[0]).split('d')[1]
            line[0] = Symbol(line[0])
        graph[line[0]] = list(exp(line[1]).free_symbols)
        ind[line[0]] = count
        count += 1

    return ind, graph


def list_of_states(graph): #X = list of states, Y = list of outputs
    X = []  
    for value in graph.values():
        for i in value:
            if i not in X:
                X.append(i)

    Y = []  
    for key in graph.keys():
        if key not in Y and str(key).startswith('y'):
            Y.append(key)
    return X, Y


def dfs(graph, start, path=[]):
    path = path + [start]
    for node in graph[start]:
        if node not in path:
            path = dfs(graph, node, path)
    return path

# traverse the graph
def find_models(graph, Y): 
    models = {}
    for y in Y:
        models[y] = dfs(graph, y)
    return models


def find_submodels(graph, models, Y):
    for y in Y:
        for i in Y:
            if i != y:
                if set(graph[i]).issubset(set(models[y])):
                    models[y].append(i)

    res = []
    for y in Y:
        res.append(models[y])
    return res


def sort_list(list1):
  list2 = []
  for element in list1:
    list2.append(str(element))  

  zipped_pairs = zip(list2, list1)
 
  z = [x for _, x in sorted(zipped_pairs)] 
  return z



def search_add_unions(result):
  #Extract the total number of elements in the model
  full_lenght = len({i for lst in result for i in lst})

  #Iter over the dimension of the unions
  n = len(result)
  for r in range(n):
    models_to_add = []

    #Iter over all the possible pair combinations
    for combination in list(it.combinations(result, 2)):
      union_model = {i for lst in combination for i in lst}
      len_model_1 = len(combination[0])
      len_model_2 = len(combination[1])

      #We add a new submodel just if its dimension is smaller than the one of the
      #full model and bigger than each one of the two model that compose the union
      if (len(union_model) <= full_lenght) and (len(union_model) > len_model_1) and (len(union_model) > len_model_2):
        new_model = sort_list(list(union_model))

        #We add the submodel just if it's not already found before, we want to
        #avoid repetitions of models in the output
        if new_model not in (models_to_add):
          if new_model not in (result):
            models_to_add.append(new_model)
            #print(new_model)

    #Add all the models found in this iteration
    for model in models_to_add:
      result.append(model)

  #Final sorting before returning, TO BE FIXED
  for element in result:
    element = sort_list(element)
  return result


def new_search_add_unions(input_array):
  #We define the lenght of the total model (maybe we can use the variables X, Y)
  full_lenght = len({i for lst in input_array for i in lst})

  #We start by sorting the input, very important
  for element in input_array:
    element.sort(key=str)
  input_array.sort(key=len)

  #We initialize a new list that we will iteratively fill with the
  #union submodels and the submodels itself
  res = [[]]

  for model in input_array:
    for index in range(len(res)):

      candidate_model = list(set(res[index]) | set(model)) 
      candidate_model.sort(key=str)

      if len(candidate_model) < full_lenght:
        res.append(candidate_model)

      else:  # This would mean that candidate_model = total model
        res.append(candidate_model)
        res.sort(key=len)
        return res

    #It's important to keep the list sorted
    res.sort(key=len)




def output(res, ind, filename):
    ln = []
    for i in res:
        il = []
        for j in i:
            il.append(ind[j])
        ln.append(il)
    with open(f"{filename}.txt", "r") as f:
        lines = f.readlines()
    with open(f'{filename}' + '-res.txt', 'w') as f:
        for i in ln:
            f.write('Submodel ' + str(ln.index(i) + 1) + ':'+'\n')
            for j in i:
                f.write(lines[j])
 


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 project.py <input_file>')
        return
    input = sys.argv[1]
    ind, graph = read_input(input)
    X, Y = list_of_states(graph)
    models = find_models(graph, Y)
    res_partial = find_submodels(graph, models, Y)
    res = new_search_add_unions(res_partial)
    output(res, ind, input[:-4])


if __name__ == '__main__':
    # measure process time
    start_time = time.process_time()
    main()
    print("Process Time: %s seconds" % (time.process_time() - start_time))
