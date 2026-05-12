import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
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


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
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
        if len(self.cells) == self.count and self.count > 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0 and self.cells:
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


class MinesweeperAI():
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
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        print(f"Marked {cell} as a mine")
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        print(f"Marked {cell} as safe")
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
        print()
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Build the set of unknown neighboring cells.
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
                    neighbor = (i, j)
                    # For each neighbor already known to be a mine, decrement count
                    if neighbor in self.mines:
                        count -= 1
                        continue
                    # Safe and already-visited cells are simply skipped.
                    if neighbor in self.safes or neighbor in self.moves_made:
                        continue
                    neighbors.add(neighbor)

        # Add the new sentence with the adjusted count to the knowledge base
        ordered_neighbors = sorted(neighbors)
        self.knowledge.append(Sentence(ordered_neighbors, count))
        print(f"Added sentence: {ordered_neighbors} = {count}")

        # Infer new sentences by subset inference:
        # if s1 ⊂ s2, then (s2.cells - s1.cells) = (s2.count - s1.count)
        new_sentences = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 == s2 or not s1.cells or not s2.cells:
                    continue
                if s1.cells < s2.cells and s1.cells & s2.cells:
                    diff_cells = s2.cells - s1.cells
                    diff_count = s2.count - s1.count
                    if diff_cells and diff_count >= 0:
                        new_sentence = Sentence(diff_cells, diff_count)
                        if new_sentence not in self.knowledge and new_sentence not in new_sentences:
                            new_sentences.append(new_sentence)
        print(f"Inferred new sentences: {[str(sentence) for sentence in new_sentences]}")
        self.knowledge.extend(new_sentences)

        # Repeatedly extract and apply safe/mine conclusions until no new ones are found
        while True:
            new_safes = set()
            new_mines = set()
            for sentence in self.knowledge:
                new_safes |= sentence.known_safes()
                new_mines |= sentence.known_mines()
            if not new_safes and not new_mines:
                break
            for cell in new_safes:
                self.mark_safe(cell)
            for cell in new_mines:
                self.mark_mine(cell)

        # Remove empty sentences
        self.knowledge = [s for s in self.knowledge if s.cells]

        # Remove duplicate sentences
        unique_knowledge = []
        for sentence in self.knowledge:
            if sentence not in unique_knowledge:
                unique_knowledge.append(sentence)
        self.knowledge = unique_knowledge

        print(f"Current knowledge: {[str(sentence) for sentence in self.knowledge]}")

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("make_safe_move called")
        for cell in self.safes:
            if cell not in self.moves_made:
                print(f"Making safe move: {cell}")
                self.moves_made.add(cell)
                return cell
        print("No safe moves available")
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print("make_random_move called")
        choices = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        if choices:
            move = random.choice(choices)
            self.moves_made.add(move)
            print(f"Making random move: {move}")
            return move
        print("No random moves available")
        return None
