#coding=utf8
class Node:
    '''''Represents a decision tree node.

    '''

    def __init__(self, parent=None, dataset=None):
        self.dataset = dataset  # 落在该结点的训练实例集
        self.result = None  # 结果类标签
        self.attr = None  # 该结点的分裂属性ID
        self.childs = {}  # 该结点的子树列表，key-value pair: (属性attr的值, 对应的子树) 因为字典可以自动添加没有的 键-值 对
        self.parent = parent  # 该结点的父亲结点


def entropy(props):
    if (not isinstance(props, (tuple, list))):
        return None

    from math import log
    log2 = lambda x: log(x) / log(2)  # an anonymous function
    e = 0.0
    for p in props:
        if p == 0:
            continue
        e -= p * log2(p)
    return e


def info_gain(D, A, T=-1, return_ratio=False):
    '''''特征A对训练数据集D的信息增益 g(D,A)

    g(D,A)=entropy(D) - entropy(D|A)
            假设数据集D的每个元组的最后一个特征为类标签
    T为目标属性的ID，-1表示元组的最后一个元素为目标'''
    if (not isinstance(D, (set, list))):
        return None
    if (not type(A) is int):
        return None
    # 决策树是统计特征的计数，然后求概率和增益，所以用字典来对应 特征-次数 这样方便。
    C = {}  # 类别计数字典
    DA = {}  # 特征A的取值计数字典
    CDA = {}  # 类别和特征A的不同组合的取值计数字典
    for t in D:
        C[t[T]] = C.get(t[T], 0) + 1  # t[T] 即t[-1]：类标属性的名称。
        DA[t[A]] = DA.get(t[A], 0) + 1
        CDA[(t[T], t[A])] = CDA.get((t[T], t[A]), 0) + 1

    PC = map(lambda x: x / len(D), C.values())  # 类别的概率列表 即PC= C.values()/ len(D)，map()太强大了
    entropy_D = entropy(tuple(PC))  # map返回的对象类型为map，需要强制类型转换为元组

    PCDA = {}  # 特征A的每个取值给定的条件下各个类别的概率（条件概率）
    for key, value in CDA.items():
        a = key[1]  # 特征A
        pca = value / DA[a]
        PCDA.setdefault(a, []).append(pca)

    condition_entropy = 0.0
    for a, v in DA.items():
        p = v / len(D)
        e = entropy(PCDA[a])
        condition_entropy += e * p

    if (return_ratio):
        return (entropy_D - condition_entropy) / entropy_D
    else:
        return entropy_D - condition_entropy


def get_result(D, T=-1):
    '''''获取数据集D中实例数最大的目标特征T的值'''
    if (not isinstance(D, (set, list))):
        return None
    if (not type(T) is int):
        return None
    count = {}
    for t in D:
        count[t[T]] = count.get(t[T], 0) + 1  # 字典的get(key,b)方法，返回key对应的值，如果没有key,则返回b.这条语句很精简，就是key-key的次数 相对应为字典
    max_count = 0
    for key, value in count.items():
        if (value > max_count):
            max_count = value
            result = key
    return result  # 返回关键字统计的次数最大的值


def devide_set(D, A):
    '''''根据特征A的值把数据集D分裂为多个子集'''
    if (not isinstance(D, (set, list))):
        return None
    if (not type(A) is int):
        return None
    subset = {}
    for t in D:
        subset.setdefault(t[A], []).append(t)  # 字典一键多值的创建
    return subset


def build_tree(D, A, threshold=0.0001, T=-1, Tree=None, algo="ID3"):  # T=-1是最后一个属性，即类标
    '''''根据数据集D和特征集A构建决策树.

    T为目标属性在元组中的索引 . 目前支持ID3和C4.5两种算法'''
    if (Tree != None and not isinstance(Tree, Node)):
        return None
    if (not isinstance(D, (set, list))):
        return None
    if (not type(A) is set):
        return None

    if (None == Tree):
        Tree = Node(None, D)
    subset = devide_set(D, T)  # 分裂最后一个属性（类标）
    if (len(subset) <= 1):  # 如果该属性只有一个类标（很纯），则该类标就是当前节点的类标，并且结束
        for key in subset.keys():
            Tree.result = key
        del (subset)
        return Tree
    if (len(A) <= 0):  # 如果属性用完，则结束，A中不包括最后一个的类标属性
        Tree.result = get_result(D)  # 标记的类标是 各类标数目中，数目最多的类标
        return Tree
    use_gain_ratio = False if algo == "ID3" else True
    max_gain = 0.0
    for a in A:  # 对属性循环，求最大的增益
        gain = info_gain(D, a, return_ratio=use_gain_ratio)
        if (gain > max_gain):
            max_gain = gain
            attr_id = a  # 获取信息增益最大的特征
    if (max_gain < threshold):  # 信息熵增益小于某个阈值，则停止，返回树
        Tree.result = get_result(D)
        return Tree
    Tree.attr = attr_id  # 分裂的属性ID（这个ID号，和集合A中的顺序无关，只和集合A中的各个值有关，A中的各个值对应 data的属性ID）
    # 下面是循环迭代过程
    subD = devide_set(D, attr_id)
    del (D[:])  # 删除中间数据,释放内存
    Tree.dataset = None
    A.discard(attr_id)  # 从特征集中排查已经使用过的特征  ，这儿体现出了用集合的好处，只是删除了对应集合中的索引值，data中并没有删除
    for key in subD.keys():
        tree = Node(Tree, subD.get(key))  # 求取孩子节点
        Tree.childs[key] = tree  # 添加孩子（用的是字典，自动添加）
        build_tree(subD.get(key), A, threshold, T, tree)  # 循环迭代
    return Tree


def print_brance(brance, target):
    odd = 0
    for e in brance:
        print(e, ('=' if odd == 0 else '∧'))
        odd = 1 - odd
    print("target =", target)


def print_tree(Tree, stack=[]):
    if (None == Tree):
        return
    if (None != Tree.result):
        print_brance(stack, Tree.result)
        return
    stack.append(Tree.attr)
    for key, value in Tree.childs.items():
        stack.append(key)
        print_tree(value, stack)
        stack.pop()
    stack.pop()


def classify(Tree, instance):
    if (None == Tree):
        return None
    if (None != Tree.result):
        return Tree.result
    return classify(Tree.childs[instance[Tree.attr]], instance)


dataset = [
    ("青年", "否", "否", "一般", "否")
    , ("青年", "否", "否", "好", "否")
    , ("青年", "是", "否", "好", "是")
    , ("青年", "是", "是", "一般", "是")
    , ("青年", "否", "否", "一般", "否")
    , ("中年", "否", "否", "一般", "否")
    , ("中年", "否", "否", "好", "否")
    , ("中年", "是", "是", "好", "是")
    , ("中年", "否", "是", "非常好", "是")
    , ("中年", "否", "是", "非常好", "是")
    , ("老年", "否", "是", "非常好", "是")
    , ("老年", "否", "是", "好", "是")
    , ("老年", "是", "否", "好", "是")
    , ("老年", "是", "否", "非常好", "是")
    , ("老年", "否", "否", "一般", "否")
]

T = build_tree(dataset, set(range(0, len(dataset[0]) - 1)))

print_tree(T)
print(classify(T, ("老年", "否", "否", "一般")))