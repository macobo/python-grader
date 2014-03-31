import ast
import grader
from grader.utils import read_code

__all__ = ["template_test", "compare_trees", "is_underscore", "is_wildcard", "pprint_ast", "dump"]

def dump(T):
    " maps nested list of asts to strings "
    if isinstance(T, ast.AST):
        return pprint_ast(T)
    elif type(T) in [list, tuple]:
        type_ = type(T)
        return type_(map(dump, T))
    else:
        return T


def is_underscore(node):
    " Function matching a ____ expression. Used to allow to be filled with any expression. "
    return isinstance(node, ast.Name) and len(node.id) > 2 and all(x == "_" for x in node.id)


def is_wildcard(node):
    " Function matching a ... expression (used as a wildcard expression) "
    return isinstance(node, ast.Expr) and type(node.value) == ast.Ellipsis


def matching_ast_lists(original_list, compared_list, i=0, j=0):
    " Returns if the ast lists are identical or not (allowing for wildcards) "
    # terrible performance, but enough for a POC
    if i == len(original_list) and j == len(compared_list):
        return []
    if j == len(compared_list):
        if all(is_wildcard(x) for x in original_list[i:]):
            return []
        return [(original_list, compared_list)]
    if i == len(original_list):
        return [(original_list, compared_list)]

    original, compared = original_list[i], compared_list[j]
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
        Returns a list of differences, pairs of (expected, got).

        In addition to doing straight-forward comparison, it allows
        for two kinds of wildcard expressions:
            1) ____ expressions which can be filled with a single expression/statement.
            2) ... expressions which can be filled with any number of
                valid expressions/statements. Used in bodies.
    """

    type_differs = lambda a, b: type(a) != type(b)
    value_type_in = lambda a, b, _set: any(isinstance(a, x) for x in _set)

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


def load_ast_from_file(file_path):
    source = read_code(file_path)
    return ast.parse(source)


def template_test(template_file=None, template_code=None,
                  description="Program should match the template."):

    if template_file is not None:
        template_code = read_code(template_file)

    assert template_code is not None
    template_tree = ast.parse(template_code)

    @grader.test
    @grader.set_description(description)
    @grader.expose_ast
    def _inner(m, AST):
        result = compare_trees(template_tree, AST)
        if result:
            m.log(pprint_ast(AST))
            m.log(pprint_ast(template_tree))
            m.log(dump(result))
        assert result == [], (
            "Program code does not match template.\n\nTemplate code:\n{}"
            .format(template_code)
        )

    return _inner

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
            yield "\n" + block * level
            continue
        if ch in '([':
            yield ch
            if N and N[0] == i+1 and N[1] in "])":
                yield N[1]
                skipNext = True
            else:
                level += 1
                yield "\n" + block * level

        if ch in '])':
            level -= 1
            yield "\n" + block * level + ch
            if not (N and N[0] == i + 1 and N[1] in "])"):
                yield "\n" + block * level


def pprint_ast(tree):
    return "".join(traverse(ast.dump(tree)))