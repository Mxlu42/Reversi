# Reversi

A Python implementation of the classic strategy board game Reversi (Othello), featuring both a terminal interface and a live-updating Tkinter GUI that mirrors the game state as you play.

## Features

- Full Reversi rules: legal-move detection based on standard 8-directional flanking, automatic piece flipping, turn switching, and forced-pass handling when a player has no legal moves
- Dual interface: play via text commands in the terminal while a Tkinter window displays the board, current player, live scores, and all valid moves in parallel
- Automatic win detection with a results window summarizing the final score when neither player has a legal move remaining

## Getting Started

### Prerequisites

- Python 3.10+
- Tkinter (included with most standard Python installations; on some Linux distributions install it separately, e.g. `sudo apt install python3-tk`)

### Running the game

```bash
python reversi.py
```

## How to Play

- Moves are entered as a two-digit coordinate: `<row><column>`, e.g. `64` places a piece at row 6, column 4
- Type `moves` at any time to list all currently valid moves
- Type `quit` to end the game early
- Black (`B`) always moves first; if a player has no legal moves, their turn is automatically skipped

## Project Structure

| File | Responsibility |
| --- | --- |
| `reversi.py` | Core game engine — turn management, move validation, piece flipping, scoring, and the main game loop |
| `playboard.py` | Board state and the Tkinter GUI that renders it |
| `player.py` | Player data (identifier and score) |
| `move.py` | Parses and represents a single move's coordinates |

## Roadmap

- Automated test suite covering move validation and game-over conditions
- AI opponent with configurable difficulty
- Click-to-move support directly in the GUI

## License

This project does not currently specify a license.
