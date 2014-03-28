import ast
import grader
from grader.utils import read_code

def dump(T):
    " maps nested list of asts to strings "
    if isinstance(T, ast.AST):
        return ast.dump(T)
    else:
        type_ = type(T)
        return type_(map(dump, T))


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
    if j == len(compared_list) and not all(is_wildcard(x) for x in original_list[i:]):
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
        assert result == [], (
            "Program code does not match template.\n\nTemplate code:\n{}"
            .format(template_code)
        )

    return _inner
