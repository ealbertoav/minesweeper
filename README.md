# Minesweeper AI

A knowledge-based AI agent that plays Minesweeper using propositional logic and inference rules.

## Features

- **Knowledge-Based Inference**: The AI maintains a knowledge base of logical sentences about the game state, using propositional logic to deduce which cells are safe or contain mines.
- **Subset Rule Application**: Applies the subset inference rule to derive new knowledge from existing sentences (if A ⊂ B, then B - A contains B.count - A.count mines).
- **Safe Move Detection**: Prioritizes guaranteed safe moves before resorting to random moves.
- **Iterative Learning**: Continuously updates its knowledge base as new information is revealed.

## Implementation Details

### Sentence Class

Represents a logical statement about the game: "A set of cells contains exactly N mines."

| Method | Description |
|--------|-------------|
| `known_mines()` | Returns cells known to be mines (when count equals number of cells) |
| `known_safes()` | Returns cells known to be safe (when count is 0) |
| `mark_mine(cell)` | Updates sentence when a cell is confirmed as a mine |
| `mark_safe(cell)` | Updates sentence when a cell is confirmed as safe |

### MinesweeperAI Class

The AI agent that makes decisions based on accumulated knowledge.

| Method | Description |
|--------|-------------|
| `add_knowledge(cell, count)` | Updates knowledge base when a cell is revealed |
| `make_safe_move()` | Returns a guaranteed safe move if one exists |
| `make_random_move()` | Returns a random valid move when no safe move is available |

**Knowledge Update Algorithm (`add_knowledge`):**
1. Mark the revealed cell as a move made and as safe
2. Create a new sentence from undetermined neighbors
3. Iteratively mark known mines and safes from all sentences
4. Apply subset inference to derive new sentences
5. Repeat until no new inferences can be made

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python runner.py
```

## Requirements

- Python 3.7+
- pygame

## File Structure

```
minesweeper/
├── minesweeper.py    # Core game logic and AI implementation
│   ├── Minesweeper   # Game board representation
│   ├── Sentence      # Logical sentence for knowledge representation
│   └── MinesweeperAI # AI agent with inference capabilities
├── runner.py         # Pygame GUI for playing the game
├── requirements.txt  # Python dependencies
└── assets/           # Game assets (fonts, images)
```

## Usage Examples

### Playing the Game

1. Run `python runner.py` to start the game
2. Click "Play Game" to begin
3. **Left-click** a cell to reveal it
4. **Right-click** a cell to flag it as a mine
5. Click **"AI Move"** to let the AI make a move
6. Click **"Reset"** to start a new game

### Using the AI Programmatically

```python
from minesweeper import Minesweeper, MinesweeperAI

# Create game and AI
game = Minesweeper(height=8, width=8, mines=8)
ai = MinesweeperAI(height=8, width=8)

# Make a move and update AI knowledge
cell = (0, 0)
if not game.is_mine(cell):
    count = game.nearby_mines(cell)
    ai.add_knowledge(cell, count)

# Get AI's next move
safe_move = ai.make_safe_move()
if safe_move is None:
    random_move = ai.make_random_move()
```

## How the AI Works

The AI uses **propositional logic** to reason about the game:

1. Each revealed cell provides information: "These N neighbors contain exactly M mines"
2. This information is stored as `Sentence` objects in the knowledge base
3. When `count == 0`, all cells in the sentence are safe
4. When `count == len(cells)`, all cells in the sentence are mines
5. The **subset rule** allows inferring new sentences from existing ones

Example inference:
- Sentence A: `{(1,1), (1,2)} = 1` (one of these two cells is a mine)
- Sentence B: `{(1,1), (1,2), (1,3)} = 2` (two of these three cells are mines)
- Inference: `{(1,3)} = 1` (cell (1,3) must be a mine)

