from collections import defaultdict
from random import uniform
from math import sqrt

# 利用均值等方法更新该类的中心值
def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    NB. points can have more dimensions than 2
    
    Returns a new point which is the center of all the points.
    """
    dimensions = len(points[0])
    print(dimensions)
    # 生成新的中心点
    new_center = []
    # 将所有归属该类的点求均值，计算出新的中心点
    for dimension in range(dimensions):
        dim_sum = 0  # dimension sum
        for p in points:
            dim_sum += p[dimension]

        # average of each dimension
        new_center.append(dim_sum / float(len(points)))

    return new_center
# 将样本归属到距离最短的中心所在的类
def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.

    Compute the center for each of the assigned groups.

    Return `k` centers where `k` is the number of unique assignments.
    """
    # 建立字典
    new_means = defaultdict(list)
    centers = []
    # 将样本归属到距离最短的中心所在的类
    for assignment, point in zip(assignments, data_set):
        new_means[assignment].append(point)
     
    # new_means.itervalues() 2 values()
    print(new_means)
    # 取出new_means字典中所有数值
    for points in new_means.values():
        # print('points')
        # print(points)
        centers.append(point_avg(points))

    return centers


def assign_points(data_points, centers):
    """
    Given a data set and a list of points betweeen other points,
    assign each point to an index that corresponds to the index
    of the center point on it's proximity to that point. 
    Return a an array of indexes of centers that correspond to
    an index in the data set; that is, if there are N points
    in `data_set` the list we return will have N elements. Also
    If there are Y points in `centers` there will be Y unique
    possible values within the returned list.
    """
    assignments = []
    for point in data_points:
        shortest = float("inf")  # positive infinity创建无穷大数
        shortest_index = 0      # 建立索引，值为0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            # print(val)
            # 取最短距离
            if val < shortest:
                shortest = val
                shortest_index = i
        # 求其到k个中心的距离，将该样本归到距离最短的中心所在的类；
        assignments.append(shortest_index)
    # 返回距离最短的k中心点的分类
    return assignments

# 求图片矢量数据与生成的随机数据的距离sqrt((a1-a2)²+(b1-b2)²)
def distance(a, b):
    """
    """
    dimensions = len(a)
    
    _sum = 0
    for dimension in range(dimensions):
        difference_sq = (a[dimension] - b[dimension]) ** 2
        _sum += difference_sq
    return sqrt(_sum)


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    find the minimum and maximum for each coordinate, a range.
    Generate `k` random points between the ranges.
    Return an array of the random points within the ranges.
    """
    centers = []
    dimensions = len(data_set[0])
    min_max = defaultdict(int)
    # 每个point都有12个元素作为向量
    for point in data_set:
        # 筛选出每个向量位上的最大值和最小值
        for i in range(dimensions):
            val = point[i]
            min_key = 'min_%d' % i
            max_key = 'max_%d' % i
            if min_key not in min_max or val < min_max[min_key]:
                min_max[min_key] = val
            if max_key not in min_max or val > min_max[max_key]:
                min_max[max_key] = val
    # 生成k个中心点，分出k类
    for _k in range(k):
        rand_point = []
        for i in range(dimensions):
            min_val = min_max['min_%d' % i]
            max_val = min_max['max_%d' % i]
            # 在每个向量最大最小值之间生成随机数
            rand_point.append(uniform(min_val, max_val))
        # 返回范围内的随机点数组，作为每类的中心点
        centers.append(rand_point)

    return centers


def k_means(dataset, k):
    # （1）适当选择c个类的初始中心
    k_points = generate_k(dataset, k)
    # （2）在第k次迭代中，对任意一个样本，求其到c个中心的距离，将该样本归到距离最短的中心所在的类；
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        # （3）利用均值等方法更新该类的中心值；
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        #（4）对于所有的c个聚类中心，如果利用（2）（3）的迭代法更新后，值保持不变，则迭代结束，否则继续迭代。
        assignments = assign_points(dataset, new_centers)
    return assignments
