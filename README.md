# Dots and Boxes (Python)

A playable Dots and Boxes implementation with a simple referee that can run
human or external players. The UI is built with `pygame`, and the game logic
is in pure Python for easy modification and experimentation.

## Requirements

- Python 3.9+
- `numpy`
- `pygame`

Install dependencies:

```powershell
python -m pip install numpy pygame
```

## Run the Game (UI)

Launch the interactive UI game:

```powershell
python game.py <Player1Name> <Player2Name>
```

This starts a game using the built-in player hooks. The UI opens in a
`pygame` window.

## Run the Referee (External Players)

The referee drives a game between two external players that communicate via
files. It creates and watches a `move_file` and uses `.go` / `.pass` files to
signal turns.

```powershell
python referee.py <Player1Name> <Player2Name> --time_limit 10
```

- `--time_limit` is optional and defaults to 10 seconds.
- The referee creates/cleans its files in the same directory as `referee.py`.

### External Player Protocol (Summary)

When it is a player's turn, the referee creates `<PlayerName>.go` (or
`<PlayerName>.pass` for a forced pass). The player writes a move to
`move_file` in the following format:

```
<PlayerName> r1,c1 r2,c2
```

Coordinates are integers describing the selected edge. A pass is represented
by `0,0 0,0` when a pass is required.

## Project Structure

- `game.py`: UI game loop and main entry point for interactive play.
- `referee.py`: Headless referee that runs external players.
- `core_gameplay.py`, `dotsandboxes.py`: Game rules and board logic.
- `display.py`: Rendering and UI helpers.
- `external_players.py`: File-based turn protocol for external bots.

## Notes

If you are creating your own external player, keep it in a separate process
and have it watch for its `.go` file, then write moves to `move_file`.

Implemented for CS 4341 A23 in collaboration with 2 other students.