import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set the initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If count equals the number of cells, all cells must be mines
        if len(self.cells) == self.count and self.count > 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the count is 0, all cells must be safe
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1: Add a cell to moves_made
        self.moves_made.add(cell)

        # Step 2: Mark cell as safe
        self.mark_safe(cell)

        # Step 3: Create a new sentence based on cell and count
        # Get all neighbors of the cell
        i, j = cell
        neighbors = set()
        for di in range(-1, 2):
            for dj in range(-1, 2):
                ni, nj = i + di, j + dj
                # Skip the cell itself
                if (ni, nj) == cell:
                    continue
                # Check board boundaries
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    # Only include undetermined cells
                    if (ni, nj) not in self.safes and (ni, nj) not in self.mines:
                        neighbors.add((ni, nj))

        # Adjust count for known mines in neighbors
        adjusted_count = count
        for di in range(-1, 2):
            for dj in range(-1, 2):
                ni, nj = i + di, j + dj
                # Decrements count when a neighbor is known mine
                if (ni, nj) != cell and 0 <= ni < self.height and 0 <= nj < self.width:
                    if (ni, nj) in self.mines:
                        adjusted_count -= 1

        # Add a new sentence if it contains cells
        if neighbors:
            self.knowledge.append(Sentence(neighbors, adjusted_count))

        # Steps 4-6: Iteratively update knowledge until no changes
        changed = True
        # Iteratively updates knowledge by marking safes/mines and inferring subsets
        while changed:
            changed = False

            # Step 5: Check for known mines and safes
            safes_to_mark = set()
            mines_to_mark = set()

            for sentence in self.knowledge:
                safes_to_mark.update(sentence.known_safes())
                mines_to_mark.update(sentence.known_mines())

            # Mark safes
            for safe_cell in safes_to_mark:
                if safe_cell not in self.safes:
                    self.mark_safe(safe_cell)
                    changed = True

            # Mark mines
            for mine_cell in mines_to_mark:
                if mine_cell not in self.mines:
                    self.mark_mine(mine_cell)
                    changed = True

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

            # Step 6: Apply subset inference rule
            new_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2:
                        continue
                    # Check if s1 is a proper subset of s2
                    if s1.cells and s1.cells < s2.cells:
                        new_cells = s2.cells - s1.cells
                        new_count = s2.count - s1.count
                        new_sentence = Sentence(new_cells, new_count)
                        # Only add if not already in knowledge
                        if new_sentence not in self.knowledge and new_sentence not in new_sentences:
                            new_sentences.append(new_sentence)
                            changed = True

            self.knowledge.extend(new_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes,
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Collect all valid moves
        valid_moves = []
        # Collects valid moves not known to be mines
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    valid_moves.append(cell)

        if valid_moves:
            return random.choice(valid_moves)
        return None
