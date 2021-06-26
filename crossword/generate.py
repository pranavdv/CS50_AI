import sys

from crossword import *
import itertools
import copy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for var in self.domains.keys():
            rem = set()
            for word in self.domains[var] :
                if len(word) != var.length : rem.add(word)
            for word in rem :
                self.domains[var].remove(word)

        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        ov = self.crossword.overlaps[x,y]
        if not ov : return False

        ix = ov[0]
        jy = ov[1]

        rem = set()
        for wx in self.domains[x] :
            found = False
            for wy in self.domains[y]:
                if wx[ix] == wy[jy] :
                    found = True
                    break
            
            if not found : rem.add(wx)

        for word in rem :
            self.domains[x].remove(word)

        return len(rem)>0

        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            q = list(itertools.product(self.crossword.variables,self.crossword.variables))
            q = [arc for arc in q if arc[0]!=arc[1] and self.crossword.overlaps[arc[0],arc[1]] is not None]
        else : q=arcs

        while len(q):
            cur = q.pop(0)
            x, y=cur[0],cur[1]
            if self.revise(x,y):
                if not self.domains[x] :
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    q.append((z,x))

        return True
        
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if set(assignment.keys()) == self.crossword.variables and all(assignment.values()) : return True
        return False
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        if len(set(assignment.keys())) != len(set(assignment.values())): return False

        if any(var.length != len(word) for var,word in assignment.items()): return False

        for var,word in assignment.items():
            for nei in self.crossword.neighbors(var).intersection(assignment.keys()) :
                ov = self.crossword.overlaps[var,nei]
                if word[ov[0]] != assignment[nei][ov[1]] : return False

        return True

        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        res = []
        check = (self.crossword.neighbors(var) - set(assignment.keys()))
        for choice in self.domains[var] :
            cnt = 0
            for nei in check:
                ov = self.crossword.overlaps[var,nei]
                for word in self.domains[nei] :
                    cnt += (choice[ov[0]]!=word[ov[1]])
            cur = [choice,cnt]
            res.append(cur)

        return [cur[0] for cur in sorted(res,key=lambda it : it[1])]

        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        res = []
        for var in self.crossword.variables - assignment.keys() : 
            remval = len(self.domains[var])
            nei = len(self.crossword.neighbors(var)) 
            cur = [var,remval,nei]
            res.append(cur)

        res = sorted(res, key = lambda cur: cur[2],reverse=True)
        res = sorted(res, key = lambda cur : cur[1])

        return res[0][0]
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment) : return assignment

        cur = self.select_unassigned_variable(assignment)

        for val in self.order_domain_values(cur,assignment) :
            try_ass = copy.deepcopy(assignment)
            try_ass[cur] = val
            if self.consistent(try_ass) :
                assignment[cur] =val
                res = self.backtrack(assignment)
                if res is not None :
                    return res
            assignment.pop(cur,None)

        return None

        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
