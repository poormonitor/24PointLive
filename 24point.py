import itertools
import math

operators = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "_": lambda x, y: y - x,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "//": lambda x, y: y / x,
}

trans = {
    "_": "-",
    "//": "/",
    "*": "*",
    "/": "/",
    "+": "+",
    "-": "-",
}

level = {
    "+": 0,
    "-": 0,
    "_": 0,
    "*": 1,
    "/": 1,
    "//": 1,
}


class VNode:
    def __init__(self, data):
        self.value = data

    def __repr__(self):
        return str(self.value)


class ONode:
    def __init__(self, op, left=None, right=None, sum=None):
        self.op = op
        self.left = left
        self.right = right
        val = []
        for i in (self.left, self.right):
            if isinstance(i, ONode):
                val.append(i.sum)
            else:
                val.append(i.value)
        self.sum = operators[self.op](val[0], val[1])

    def __repr__(self):
        le = repr(self.left)
        if isinstance(self.left, ONode) and (
            (self.op in ("//", "_") and level[self.left.op] == level[self.op])
            or level[self.left.op] < level[self.op]
        ):
            le = "(" + le + ")"
        re = repr(self.right)
        if isinstance(self.right, ONode) and (
            (self.op in ("/", "-") and level[self.right.op] == level[self.op])
            or level[self.right.op] < level[self.op]
        ):
            re = "(" + re + ")"
        if self.op in ("_", "//"):
            return re + trans[self.op] + le
        return le + self.op + re

    def __eq__(self, haystack):
        if isinstance(haystack, ONode):
            return (
                (
                    (self.left == haystack.left and self.right == haystack.right)
                    or (self.right == haystack.left and self.left == haystack.right)
                )
                and (self.op == haystack.op or trans[self.op] == trans[haystack.op])
            ) or repr(self) == repr(haystack)
        return self.sum == haystack


def construct(nodes, ops):
    return ONode(
        ops[2],
        ONode(ops[1], ONode(ops[0], VNode(nodes[0]), VNode(nodes[1])), VNode(nodes[2])),
        VNode(nodes[3]),
    ), ONode(
        ops[2],
        ONode(ops[0], VNode(nodes[0]), VNode(nodes[1])),
        ONode(ops[1], VNode(nodes[2]), VNode(nodes[3])),
    )


while True:
    a, b, c, d = map(int, input().split())

    order = {i for i in itertools.permutations([a, b, c, d])}

    ops = itertools.combinations_with_replacement(operators.keys(), 3)
    ops = {j for i in ops for j in {q for q in itertools.permutations(i)}}

    trees = []
    for i in order:
        for j in ops:
            try:
                for tree in construct(i, j):
                    if math.isclose(tree.sum, 24, rel_tol=1e-5) and tree not in trees:
                        trees.append(tree)
            except ZeroDivisionError:
                continue

    print(trees)
