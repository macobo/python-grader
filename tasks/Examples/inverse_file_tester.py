from grader import *
import os

def size(matrix):
    if len(matrix) == 0:
        return 0, 0
    return len(matrix), len(matrix[0])

def transpose(matrix):
    rows, cols = size(matrix)
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]

def stringify(matrix):
    return "\n".join(" ".join(map(str, row)) for row in matrix)

def matrix_gen(matrix,
               infile_name="matrix.txt", 
               outfile_name="matrix_inverse.txt"):
    
    # Description management for the tests
    rows, cols = size(matrix)
    description = "Transposing a {rows}x{cols} matrix ({inf}, {out})"
    
    description = description.format(rows=rows, 
                                     cols=cols,
                                     matrix=matrix,
                                     inf=infile_name,
                                     out=outfile_name)
    
    # transform the list of lists into a multi-line string
    infile_contents = stringify(matrix)
    expected_outfile = stringify(transpose(matrix))
    
    # Internally create a function and register as a test
    # All the file checking logic goes in there.
    # Before the test is executed, the needed file is generated
    @test
    @before_test(create_file(infile_name, infile_contents))
    @set_description(description)
    def _inner_test(m):
        m.stdin.put(infile_name)
        m.stdin.put(outfile_name)
        
        assert os.path.exists(outfile_name), \
            "Solution did not create "+outfile_name
        
        with open(outfile_name) as f:
            output = f.read()
        
        # compare output to expected (ignore trailing whitespace)
        assert output.strip() == expected_outfile, (
            "Finding inverse of the following matrix:\n{matrix}\n\n"
            "Expected {outfile} to contain:\n{expected}\n\n"
            "{outfile} contained:\n{got}"
            .format(got=output, expected=expected_outfile, 
                    matrix=matrix, outfile=outfile_name)
        )
        
matrix_gen([])
matrix_gen([[1]])
matrix_gen([[1]], infile_name="another_input.txt")
matrix_gen([[1]], outfile_name="another_inverse_file.txt")
matrix_gen([[1,2], [3, 4]])
matrix_gen([[1,2,3], [4,5,6], [7,8,9], [10,11,12]])