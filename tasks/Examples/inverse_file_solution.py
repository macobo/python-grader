infile = input()
outfile = input()

matrix = []
with open(infile) as f:
    for line in f:
        matrix.append(line.strip().split())
        
rows, cols = len(matrix), len(matrix[0])

with open(outfile, "w") as out:
    for c in range(cols):
        row = []
        for r in range(rows):
            row.append(matrix[r][c])
        out.write(" ".join(row))
        out.write("\n")