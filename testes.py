import random
import copy
import time
from ordenation import OrderAlgos  

def test_algorithms(random_test=False, default_random =10, arr=[]):

    if random_test == True:
        lista = [random.randint(0, 10000) for i in range(default_random)]  
    else:
        print("ordenação de 1, 9, 1, 2, 1, 8")
        lista = arr if arr else [1, 9, 1, 2, 1, 8]

    algorithms = {
        "Bubble Sort": OrderAlgos.bubble_sort,
        "Selection Sort": OrderAlgos.selection_sort,
        "Insertion Sort": OrderAlgos.insertion_sort,
        "Merge Sort": OrderAlgos.merge_sort,
        "Quick Sort": OrderAlgos.quick_sort,
        "Heap Sort": OrderAlgos.heap_sort
    }

    print("Comparação de performance (milissegundos):\n")
    for name, func in algorithms.items():
        test_list = copy.deepcopy(lista)

        start = time.perf_counter()
        result = func(test_list) if name != "Quick Sort" else func(lista)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000

        is_sorted = result == sorted(lista)
        print(f"{name:<15} -> Tempo: {duration_ms:>8.2f} ms | Ordenado: {is_sorted} | Lista: {result}")

if __name__ == "__main__":
    test_algorithms()
