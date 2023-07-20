const operators = {
    "+": (x, y) => x + y,
    "-": (x, y) => x - y,
    _: (x, y) => y - x,
    "*": (x, y) => x * y,
    "/": (x, y) => x / y,
    "//": (x, y) => y / x,
};

const trans = {
    _: "-",
    "//": "/",
    "*": "*",
    "/": "/",
    "+": "+",
    "-": "-",
};

const level = {
    "+": 0,
    "-": 0,
    _: 0,
    "*": 1,
    "/": 1,
    "//": 1,
};

class VNode {
    constructor(data) {
        this.value = data;
    }

    toString() {
        return this.value.toString();
    }
}

class ONode {
    constructor(op, left = null, right = null) {
        this.op = op;
        this.left = left;
        this.right = right;
        const val = [];
        [this.left, this.right].forEach((i) => {
            if (i instanceof ONode) {
                val.push(i.sum);
            } else {
                val.push(i.value);
            }
        });
        this.sum = operators[this.op](val[0], val[1]);
    }

    toString() {
        let le = this.left.toString();
        if (
            this.left instanceof ONode &&
            ((["//", "_"].includes(this.op) &&
                level[this.left.op] === level[this.op]) ||
                level[this.left.op] < level[this.op])
        ) {
            le = "(" + le + ")";
        }

        let re = this.right.toString();
        if (
            this.right instanceof ONode &&
            ((["/", "-"].includes(this.op) &&
                level[this.right.op] === level[this.op]) ||
                level[this.right.op] < level[this.op])
        ) {
            re = "(" + re + ")";
        }

        if (["_", "//"].includes(this.op)) {
            return re + trans[this.op] + le;
        }

        return le + this.op + re;
    }

    equals(haystack) {
        return this.toString() === haystack.toString();
    }
}

function construct(nodes, ops) {
    return [
        new ONode(
            ops[2],
            new VNode(nodes[0]),
            new ONode(
                ops[1],
                new ONode(ops[0], new VNode(nodes[1]), new VNode(nodes[2])),
                new VNode(nodes[3])
            )
        ),
        new ONode(
            ops[2],
            new ONode(
                ops[1],
                new ONode(ops[0], new VNode(nodes[0]), new VNode(nodes[1])),
                new VNode(nodes[2])
            ),
            new VNode(nodes[3])
        ),
        new ONode(
            ops[2],
            new ONode(ops[0], new VNode(nodes[0]), new VNode(nodes[1])),
            new ONode(ops[1], new VNode(nodes[2]), new VNode(nodes[3]))
        ),
    ];
}

function permutations(inputArr) {
    let result = [];

    const permute = (arr, m = []) => {
        if (arr.length === 0) {
            result.push(m);
        } else {
            for (let i = 0; i < arr.length; i++) {
                let curr = arr.slice();
                let next = curr.splice(i, 1);
                permute(curr.slice(), m.concat(next));
            }
        }
    };

    permute(inputArr);

    return result;
}

function get24Point(values) {
    const order = new Set(permutations(values));

    const ops = new Set();
    for (const op1 of Object.keys(operators)) {
        for (const op2 of Object.keys(operators)) {
            for (const op3 of Object.keys(operators)) {
                ops.add([op1, op2, op3]);
            }
        }
    }

    const trees = [];
    for (const i of order) {
        for (const j of ops) {
            try {
                for (const tree of construct(i, j)) {
                    if (
                        Math.abs(tree.sum - 24) < 1e-5 &&
                        !trees.some((t) => t.equals(tree))
                    ) {
                        trees.push(tree);
                    }
                }
            } catch (err) {
                continue;
            }
        }
    }

    return trees.map((item) => item.toString());
}

export { get24Point };
