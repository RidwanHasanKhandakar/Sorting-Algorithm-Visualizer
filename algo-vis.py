import pygame
import random
pygame.init()
class DrawInformation:
    #this are just global color that we will use in our program
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = BLACK
    SIDE_PAD = 100
    TOP_PAD = 150
    GRADIENTS = [
        GREY,
        (160,160,160),
        (192,192,192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)

    def __init__(self,width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm VIS made by RRHIN")
        self.set_lst(lst)
    def set_lst(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = (self.height -self.TOP_PAD) / (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, color_positions={}, algorithm_name="Bubble Sort", ascending=True, min_val=0, max_val=100):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    controls = draw_info.FONT.render("R - Reset | Space - Start Sorting | A - Ascending | D - Descending", 1, draw_info.RED)
    draw_info.window.blit(controls,(draw_info.width/2-controls.get_width()/2,5))
    sorting = draw_info.FONT.render("I - Insertion | B - Bubble | M - Merge | Q - Quick | H - Heap | U - Bucket | R - Radix", 1, draw_info.RED)
    draw_info.window.blit(sorting,(draw_info.width/2-sorting.get_width()/2,30))
    hybrid = draw_info.FONT.render("T - Tim Sort | N - Intro Sort", 1, draw_info.RED)
    draw_info.window.blit(hybrid,(draw_info.width/2-hybrid.get_width()/2,55))
    status = draw_info.FONT.render(f"Current: {algorithm_name} ({'Ascending' if ascending else 'Descending'})", 1, draw_info.RED)
    draw_info.window.blit(status,(draw_info.width/2-status.get_width()/2,80))
    draw_list(draw_info, color_positions)
    pygame.display.update()

def draw_list(draw_info, color_positions={}):
    lst = draw_info.lst
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        bar_height = (val - draw_info.min_val) * draw_info.block_height
        y = draw_info.height - bar_height
        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, bar_height))

def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending=True, algorithm_name="Bubble Sort", min_val=0, max_val=100):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1>num2 and ascending) or (num1<num2 and not ascending):
                lst[j],lst[j+1] = lst[j+1], lst[j]
                draw(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, algorithm_name, ascending, min_val, max_val)
                yield True
                #^- let's stop the function kinda like halfway & then resume it where-ever i put this line
    return lst

def insertion_sort(draw_info, ascending=True, algorithm_name="Insertion Sort", min_val=0, max_val=100):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and ((lst[j] > key and ascending) or (lst[j] < key and not ascending)):
            lst[j + 1] = lst[j]
            draw(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, algorithm_name, ascending, min_val, max_val)
            yield True
            j -= 1
        lst[j + 1] = key
        draw(draw_info, {j + 1: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
        yield True
    return lst

def merge_sort(draw_info, ascending=True, algorithm_name="Merge Sort", min_val=0, max_val=100):
    lst = draw_info.lst

    def merge(start, mid, end):
        left = lst[start:mid+1]
        right = lst[mid+1:end+1]
        i = j = 0
        k = start
        while i < len(left) and j < len(right):
            if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            draw(draw_info, {k: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            k += 1
        while i < len(left):
            lst[k] = left[i]
            draw(draw_info, {k: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            i += 1
            k += 1
        while j < len(right):
            lst[k] = right[j]
            draw(draw_info, {k: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            j += 1
            k += 1

    def merge_sort_helper(start, end):
        if start < end:
            mid = (start + end) // 2
            yield from merge_sort_helper(start, mid)
            yield from merge_sort_helper(mid+1, end)
            yield from merge(start, mid, end)

    yield from merge_sort_helper(0, len(lst)-1)
    return lst

def quick_sort(draw_info, ascending=True, algorithm_name="Quick Sort", min_val=0, max_val=100):
    lst = draw_info.lst

    def partition(low, high):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
                yield True
        lst[i+1], lst[high] = lst[high], lst[i+1]
        draw(draw_info, {i+1: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
        yield True
        return i+1

    def quick_sort_helper(low, high):
        if low < high:
            pi = yield from partition(low, high)
            yield from quick_sort_helper(low, pi-1)
            yield from quick_sort_helper(pi+1, high)

    yield from quick_sort_helper(0, len(lst)-1)
    return lst

def heap_sort(draw_info, ascending=True, algorithm_name="Heap Sort", min_val=0, max_val=100):
    lst = draw_info.lst

    def heapify(n, i):
        if ascending:
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and lst[l] > lst[largest]:
                largest = l
            if r < n and lst[r] > lst[largest]:
                largest = r
        else:
            smallest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and lst[l] < lst[smallest]:
                smallest = l
            if r < n and lst[r] < lst[smallest]:
                smallest = r
            largest = smallest  # for not ascending, it's min-heap

        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]
            draw(draw_info, {i: draw_info.RED, largest: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            yield from heapify(n, largest)

    n = len(lst)
    for i in range(n//2 - 1, -1, -1):
        yield from heapify(n, i)
    for i in range(n-1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw(draw_info, {i: draw_info.RED, 0: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
        yield True
        yield from heapify(i, 0)
    return lst

def bucket_sort(draw_info, ascending=True, algorithm_name="Bucket Sort", min_val=0, max_val=100):
    lst = draw_info.lst
    bucket_count = 10
    buckets = [[] for _ in range(bucket_count)]
    for val in lst:
        index = int((val - min_val) / (max_val - min_val + 1) * bucket_count)
        if index == bucket_count:
            index -= 1
        buckets[index].append(val)
    for bucket in buckets:
        # simple insertion sort for each bucket
        for i in range(1, len(bucket)):
            key = bucket[i]
            j = i - 1
            while j >= 0 and ((bucket[j] > key and ascending) or (bucket[j] < key and not ascending)):
                bucket[j+1] = bucket[j]
                j -= 1
            bucket[j+1] = key
    index = 0
    for bucket in buckets:
        for val in bucket:
            lst[index] = val
            draw(draw_info, {index: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            index += 1
    return lst

def radix_sort(draw_info, ascending=True, algorithm_name="Radix Sort", min_val=0, max_val=100):
    lst = draw_info.lst
    max_val_in_lst = max(lst)
    exp = 1
    while max_val_in_lst // exp > 0:
        count = [0] * 10
        output = [0] * len(lst)
        for val in lst:
            index = (val // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i-1]
        for i in range(len(lst)-1, -1, -1):
            index = (lst[i] // exp) % 10
            output[count[index]-1] = lst[i]
            count[index] -= 1
        for i in range(len(lst)):
            lst[i] = output[i]
            draw(draw_info, {i: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
        exp *= 10
    return lst

def tim_sort(draw_info, ascending=True, algorithm_name="Tim Sort", min_val=0, max_val=100):
    # Simplified Tim Sort (similar to merge sort)
    lst = draw_info.lst

    def merge(start, mid, end):
        left = lst[start:mid+1]
        right = lst[mid+1:end+1]
        i = j = 0
        k = start
        while i < len(left) and j < len(right):
            if (left[i] <= right[j] and ascending) or (left[i] >= right[j] and not ascending):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
            draw(draw_info, {k: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            k += 1
        while i < len(left):
            lst[k] = left[i]
            draw(draw_info, {k: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            i += 1
            k += 1
        while j < len(right):
            lst[k] = right[j]
            draw(draw_info, {k: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
            yield True
            j += 1
            k += 1

    def tim_sort_helper(start, end):
        if start < end:
            mid = (start + end) // 2
            yield from tim_sort_helper(start, mid)
            yield from tim_sort_helper(mid+1, end)
            yield from merge(start, mid, end)

    yield from tim_sort_helper(0, len(lst)-1)
    return lst

def intro_sort(draw_info, ascending=True, algorithm_name="Intro Sort", min_val=0, max_val=100):
    # Simplified Intro Sort (similar to quick sort)
    lst = draw_info.lst

    def partition(low, high):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
                yield True
        lst[i+1], lst[high] = lst[high], lst[i+1]
        draw(draw_info, {i+1: draw_info.GREEN}, algorithm_name, ascending, min_val, max_val)
        yield True
        return i+1

    def intro_sort_helper(low, high):
        if low < high:
            pi = yield from partition(low, high)
            yield from intro_sort_helper(low, pi-1)
            yield from intro_sort_helper(pi+1, high)

    yield from intro_sort_helper(0, len(lst)-1)
    return lst

def main():
    run = True
    clock = pygame.time.Clock()
    n=int(input("Enter number of elements: "))
    min_val = 0
    max_val =100
    lst = generate_starting_list(n,min_val,max_val)
    width = max(800, n + 200)
    draw_info = DrawInformation(width,600,lst)
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_gena = None
    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algo_gena)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, {}, sorting_algo_name, ascending, min_val, max_val)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_lst(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algo_gena = sorting_algorithm(draw_info, ascending, sorting_algo_name, min_val, max_val)
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"
            elif event.key == pygame.K_u and not sorting:
                sorting_algorithm = bucket_sort
                sorting_algo_name = "Bucket Sort"
            elif event.key == pygame.K_x and not sorting:
                sorting_algorithm = radix_sort
                sorting_algo_name = "Radix Sort"
            elif event.key == pygame.K_t and not sorting:
                sorting_algorithm = tim_sort
                sorting_algo_name = "Tim Sort"
            elif event.key == pygame.K_n and not sorting:
                sorting_algorithm = intro_sort
                sorting_algo_name = "Intro Sort"
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

    pygame.quit()

if __name__ == "__main__":
    main()