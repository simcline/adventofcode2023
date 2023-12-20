with open('aoc18.txt') as f:
    lines = [line[:-1] if line.endswith('\n') else line for line in f]

# I tried many, many hand-made formulas for part 2 that would not give me the exact result. Then I realized that
# this is a direct consequence of the shoelace formula along with Pick's theorem ...
#
# https://en.wikipedia.org/wiki/Shoelace_formula
# https://en.wikipedia.org/wiki/Pick%27s_theorem
#
# The "area" (U) we are looking for is not a proper geometrical area, instead it is the sum of exteriors (B) (on the
# perimeter) and interior (I) points having integer coordinates. Now the shoelace formula gives a way of calculating
# the proper area A. It is also easy to calculate B. Pick's thm says that if all vertices have integer coordinates
# then A = I + B/2 - 1. Then U = I + B = A + B/2 + 1.

def shoelace(vertices):
    n=len(vertices)
    return abs(0.5*sum(vertices[i][0]*vertices[(i+1)%n][1]-vertices[(i+1)%n][0]*vertices[i][1] for i in range(n)))

def perimeter(vertices):
    n = len(vertices)
    return sum( abs(vertices[(i+1)%n][1] - vertices[i][1])+abs(vertices[(i+1)%n][0] - vertices[i][0]) for i in range(n))

def area_from_pick(vertices):
    return int(shoelace(vertices)+perimeter(vertices)/2+1)

def compute_vertices(directions, lengths):
    vertices = [(0, 0)]

    for d, l in zip(directions, lengths):
        i, j = vertices[-1]
        match d:
            case 'U':
                vertices.append((i - l, j))
            case 'D':
                vertices.append((i + l, j))
            case 'L':
                vertices.append((i, j - l))
            case 'R':
                vertices.append((i, j + l))

    minX = min(v[0] for v in vertices)
    minY = min(v[1] for v in vertices)

    return [(v[0] - minX, v[1] - minY) for v in vertices]

directions = [l.split(' ')[0] for l in lines]
lengths = [int(l.split(' ')[1]) for l in lines]

vertices = compute_vertices(directions, lengths)
area_from_pick(vertices)

# part 2
hexa = [l.split(' ')[2][2:-1] for l in lines]
lengths2 = [int(x[:-1],16) for x in hexa]
dico = {'0':'R', '1':'D', '2':'L', '3':'U'}
directions2 = [dico[y[-1]] for y in hexa]

vertices2 = compute_vertices(directions2, lengths2)
area_from_pick(vertices2)
