import ast

def next_in(str, char_set):
    for i, ch in enumerate(str):
        if ch in char_set:
            yield i, ch

def pair_with_next(iterator):
    prev = None
    for current in iterator:
        if prev is not None:
            yield prev, current
        prev = current
    yield current, None

def traverse(tree_string, indent=4):
    cut_offs = list(next_in(tree_string, '([])'))
    level = 0

    block = " " * indent
    at = 0
    skipNext = False
    for (i, ch), N in pair_with_next(cut_offs):
        yield tree_string[at:i]
        at = i+1
        if skipNext:
            skipNext = False
            yield "\n"
            yield block * level
            continue
        if ch in '([':
            yield ch
            if N and N[0] == i+1 and N[1] in "])":
                yield N[1]
                #print("skipping at", tree_string[i:])
                skipNext = True
            else:
                level += 1
                yield "\n"
                yield block * level

        if ch in '])':

            level -= 1
            yield "\n"
            yield block * level
            yield ch
            if not (N and N[0] == i + 1 and N[1] in "])"):
                yield "\n"
                yield block * level


class Tree:
    def __init__(self, source):
        self.source = source
        self.tree = ast.parse(source)

    def __repr__(self):
        D = ast.dump(self.tree)
        return "".join(traverse(D))


def is_underscore(node):
    return isinstance(node, ast.Name) and len(node.id) > 2 and all(x == "_" for x in node.id)


def is_wildcard(node):
    return isinstance(node, ast.Expr) and type(node.value) == ast.Ellipsis


def matching_ast_lists(original_list, compared_list, i=0, j=0):
    " Returns if the ast lists are identical or not (allowing for wildcards) "
    # terrible performance, but enough for a POC
    if i == len(original_list) and j == len(compared_list):
        return []
    if j == len(compared_list) and not all(is_wildcard(x) for x in original_list[i:]):
        return [(original_list, compared_list)]
    if i == len(original_list):
        return [(original_list, compared_list)]

    original = original_list[i]
    compared = compared_list[j]
    if is_wildcard(original):
        end_wildcard_result = matching_ast_lists(original_list, compared_list, i + 1, j)
        if end_wildcard_result == []:
            return []
        # wildcard matches
        return matching_ast_lists(original_list, compared_list, i, j + 1)
    else:
        return compare_trees(original, compared) + \
            matching_ast_lists(original_list, compared_list, i + 1, j + 1)


def compare_trees(original_tree, compared_tree):
    """ Compares two AST trees with each other.
        Returns a list of differences, pairs of (expected, got) """

    type_differs = lambda a, b: type(a) != type(b)
    value_type_in = lambda a, b, _set: \
        not type_differs(a, b) and any(isinstance(a, x) for x in _set)

    if isinstance(original_tree, ast.AST) and isinstance(compared_tree, ast.AST):
        # Blanks shown by ____
        if is_underscore(original_tree):
            return []
        # different types of expressions? fail
        if type(original_tree) != type(compared_tree):
            return [(original_tree, compared_tree)]
        result = []
        # look over fields
        for field_name, _ in ast.iter_fields(original_tree):
            expected_new = getattr(original_tree, field_name, None)
            got_new = getattr(compared_tree, field_name, None)

            # if we should check recursively, do so
            if value_type_in(expected_new, got_new, [list, ast.AST]):
                result.extend(compare_trees(expected_new, got_new))
            elif type_differs(expected_new, got_new) or expected_new != got_new:
                result.append((original_tree, compared_tree))
        return result

    elif (isinstance(original_tree, list) and
            isinstance(compared_tree, list)):
        return matching_ast_lists(original_tree, compared_tree)
    return [(original_tree, compared_tree)]

def dump(T):
    if isinstance(T, ast.AST):
        return ast.dump(T)
    else:
        return list(map(dump, T))

T1_a = Tree("""
if ___: 
    a = a+1; b = a
""")

T1_b = Tree("""
if something: 
    a = a+1
    b = c
""")

T2_a = Tree("""
if ___: pass

a = b
...
c = d
e = g
...
d = f
""")

T2_b = Tree("""
if ___: pass

a = b
c = d
c = d
e = g
something.something()
d = f
""")

T2_c = Tree("""
if ___: pass

a = b
e = g
c = d
e = g
d = f
something.something()
""")