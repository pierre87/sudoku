import json
import sys
import copy


class Sudoku(object):
    board = []
    depth = 0

    def solve(self, max_iterations=100, max_depth=3):
        self.depth += 1
        # limit the recursion depth a bit
        if self.depth > max_depth:
            return
        # sys.stdout.write("depth: {}\r".format(self.depth))
        # sys.stdout.flush()
        # fill up the possible solutions board
        # each spot in the board gets a list of all possible values assigned
        posi = []
        for i in range(9):
            row = []
            for p in range(9):
                row.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            posi.append(row)

        # in case it is not possible to solve keep track of the numbers of iterations
        # in order to be able to stop at some point
        iterations = 0
        bruteforce = 0

        while not self.solved():
            if not self.is_valid():
                return
            # keep track if something has changed
            changed = 0

            # update posi
            for r in range(9):
                for c in range(9):
                    if len(posi[r][c]) == 0:
                        # print("wrong posi")
                        return
                    if self.board[r][c] != 0:
                        # this position is already done if there is already a number in that spot in the box
                        # set the only possible solution in the possible solution box
                        posi[r][c] = [self.board[r][c]]
                    else:
                        # check same row
                        for n in self.get_row(r):
                            if n in posi[r][c]:
                                posi[r][c].remove(n)
                                changed = 1
                        # check same col
                        for n in self.get_col(c):
                            if n in posi[r][c]:
                                posi[r][c].remove(n)
                                changed = 1
                        # check same box
                        for n in self.get_box(int(r/3), int(c/3)):
                            if n in posi[r][c]:
                                posi[r][c].remove(n)
                                changed = 1

            # check every position in every row/col
            for r in range(9):
                for i in range(9):
                    oc_sum = 0
                    for l in self.get_posi_row(posi, r):
                        oc_sum += l.count(i)
                    if oc_sum == 1:
                        for n in range(9):
                            if i in posi[r][n]:
                                posi[r][n] = [i]

            for c in range(9):
                for i in range(9):
                    oc_sum = 0
                    for l in self.get_posi_col(posi, c):
                        oc_sum += l.count(i)
                    if oc_sum == 1:
                        for n in range(9):
                            if i in posi[n][c]:
                                posi[n][c] = [i]

            # go through all rows/cols/boxes "versteckter einer"
            # rows
            for row_n in range(9):
                row = self.get_row(row_n)

                # check every possible number for that row
                for i in range(1, 10):
                    # if that number is not already in that row
                    if i not in row:
                        candidate_l = []
                        # check for every column if it is possible to put the number there and put it in a list
                        for c in range(9):
                            if (self.board[row_n][c] == 0) and (i not in self.get_col(c)) and (i not in self.get_box(int(row_n/3), int(c/3))):
                                candidate_l.append((row_n, c))
                        # if the list has only one element then put it
                        if len(candidate_l) == 1:
                            self.board[candidate_l[0][0] ][candidate_l[0][1]] = i
                            changed = 1

            # cols
            for col_n in range(9):
                col = self.get_col(col_n)

                # check every possible number for that col
                for i in range(1, 10):
                    # if that number is not already in that row
                    if i not in col:
                        candidate_l = []
                        # check for every row if it is possible to put the number there and if so put it in a list
                        for r in range(9):
                            if (self.board[r][col_n] == 0) and (i not in self.get_row(r)) and (i not in self.get_box(int(r/3), int(col_n/3))):
                                candidate_l.append((r, col_n))
                        # if the list has only one element then put it
                        if len(candidate_l) == 1:
                            self.board[candidate_l[0][0] ][candidate_l[0][1]] = i
                            changed = 1

            # boxes
            for box_n_x in range(9):
                for box_n_y in range(9):
                    box = self.get_box(int(box_n_x/3), int(box_n_y/3))

                    # check every possible number for that box
                    for i in range(1, 10):
                        # if that number is not already in that box
                        if i not in box:
                            candidate_l = []
                            # check for every row and col if it is possible to put the number there. if so put it in a list
                            for bb_x in range(int(box_n_x/3)*3, int(box_n_x/3)*3+3):
                                for bb_y in range(int(box_n_y/3)*3, int(box_n_y/3)*3+3):
                                    if self.board[bb_x][bb_y] == 0 and i not in self.get_row(bb_x) and i not in self.get_col(bb_y):
                                        candidate_l.append((bb_x, bb_y))
                            # if the list has only one element then put it
                            if len(candidate_l) == 1:
                                self.board[candidate_l[0][0]][candidate_l[0][1]] = i
                                changed = 1

            # methode: "nackter einer"
            for r in range(9):
                for c in range(9):
                    if self.board[r][c] == 0:
                        candidate_l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                        for i in self.get_row(r):
                            if i in candidate_l:
                                candidate_l.remove(i)
                        for i in self.get_col(c):
                            if i in candidate_l:
                                candidate_l.remove(i)
                        for i in self.get_box(int(r/3), int(c/3)):
                            if i in candidate_l:
                                candidate_l.remove(i)
                        if len(candidate_l) == 1:
                            self.board[r][c] = candidate_l[0]
                            changed = 1

            # if a posi has only one element put it in the board
            for r in range(9):
                for c in range(9):
                    if len(posi[r][c]) == 1 and self.board[r][c] == 0:
                        self.board[r][c] = posi[r][c][0]
                        changed = 1
            iterations += 1
            if max_iterations != 0:
                if iterations >= max_iterations:
                    # sys.stdout.write("no solution found after {} iterations.\r".format(iterations))
                    # sys.stdout.flush()
                    return

            if changed == 0:
                # sys.stdout.write("no more changes after {} iterations.\r".format(iterations))
                # sys.stdout.flush()
                # print("strating bruteforce")
                self.bruteforceme(posi)
                bruteforce = 1
                return

        if bruteforce == 1:
            return
        else:
            # sys.stdout.write("done after {} iterations\r".format(iterations))
            # sys.stdout.flush()
            return

    def bruteforceme(self, poses):
        # create a list in which order numbers should be guessed
        guess_order = []

        for n in range(2,10):
            candidate = []
            minimum = 10
            for r in range(9):
                for c in range(9):
                    if len(poses[r][c]) == n:
                        guess_order.append([r,c])

        for pos in guess_order:
            for i in range(len(poses[pos[0]][pos[1]])):
                cp = copy.deepcopy(self)
                sys.stdout.write("guessing {} at {}\r".format(poses[pos[0]][pos[1]][i], pos))
                sys.stdout.flush()
                cp.board[pos[0]][pos[1]] = poses[pos[0]][pos[1]][i]
                cp.solve()
                if cp.is_valid() and cp.solved():
                    self.board = cp.board
                    return

    def get_posi_row(self, p, r):
        return p[r]

    def solved(self):
        for r in self.board:
            for c in r:
                if c == 0 or c > 9:
                    return False
        return True

    def get_box(self, r, c):
        box = []
        for i in range(3):
            for j in range(3):
                box.append(self.board[i+r*3][j+c*3])
        return box

    def get_row(self, r):
        return self.board[r]

    def get_col(self, c):
        col = []
        for r in self.board:
            col.append(r[c])
        return col

    def get_posi_col(self, p, c):
        col = []
        for r in p:
            col.append(r[c])
        return col

    def is_valid(self):
        # check boad size
        if len(self.board) != 9:
            return False
        for r in self.board:
            if len(r) != 9:
                return False

        # check for doubles in rows
        for r in self.board:
            for n in range(1, 10):
                if r.count(n) > 1:
                    # print("multible {} in row {}".format(n, r))
                    return False

        # check for doubles in cols
        col = []
        for n in range(9):
            for r in self.board:
                col.append(r[n])
            for p in range(1, 10):
                if col.count(p) > 1:
                    # print("multible {} in col {}".format(p, col))
                    return False
            col = []

        # check boxes
        box = []
        for n in range(3):
            for o in range(3):
                for i in range(3):
                    for j in range(3):
                        box.append(self.board[i+n*3][j+o*3])
                for p in range(1, 10):
                    if box.count(p) > 1:
                        # print("multible {} in box {}".format(p, box))
                        return False
                box = []

        return True

    def read_json(self, filename):
        try:
            data = json.load(open(filename))
            self.board = data["puzzle"]
        except:
            print("error reading file")
            exit(0)

    def __str__(self):
        out = ""
        outer_count = 0
        for r in self.board:
            outer_count += 1
            count = 0
            for c in r:
                count += 1
                if c == 0:
                    out += "  "
                else:
                    out += "{} ".format(c)
                if count == 3 or count == 6:
                    out += "| "
            out += "\n"
            if outer_count == 3 or outer_count == 6:
                out += "----------------------\n"
        return out+"\n"


if __name__ == '__main__':
    usage = "usage:\npython solver.py <json file>\n"
    a = Sudoku()
    print("This is your input\n")
    if len(sys.argv) != 2:
        print(usage)
        exit(0)

    # read the puzzle file
    a.read_json(sys.argv[1])

    # print the input board
    print(a)

    # check if the file is valid
    if a.is_valid():
        print("your input is valid")
    else:
        print("your input is invalid")

    # solve it
    p = a.solve()
    print("")

    if a.is_valid():
        if a.solved():
            print(a)
        else:
            print("invalid")
            print(a)
    else:
        print("invalid")
        print(a)
