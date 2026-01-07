# 🪨📄✂️ Rock–Paper–Scissors–Plus  
### AI Game Referee (Google ADK – Python)

## Overview
This project implements a **minimal AI Game Referee chatbot** for a modified  
**Rock–Paper–Scissors–Plus** game.  

The chatbot acts as a referee between the **user and the bot**, enforcing rules,  
tracking game state across turns, and ending the game automatically after  
**3 rounds**.

The implementation focuses on:
- Logical correctness
- Clean state modeling
- Clear separation of agent, tools, and game logic
- Proper use of **Google ADK concepts**

---

## Game Rules
- Best of **3 rounds**
- Valid moves:
  - `rock`
  - `paper`
  - `scissors`
  - `bomb` (can be used **once per player**)
- `bomb` beats all other moves
- `bomb` vs `bomb` results in a draw
- Invalid input **wastes the round**
- The game **ends automatically after 3 rounds**

---

## Architecture Overview

The solution is organized around **three core layers**:

### 1. Intent Understanding
- User input is parsed and normalized by the agent
- Determines the intended move or invalid input

### 2. Game Logic (Tools)
Pure functions responsible for validation and state updates:
- `validate_move()`  
- `resolve_round()`  
- `update_game_state()`  

These tools **do not generate text** and contain no UI logic.

### 3. Response Generation
- The agent explains rules
- Reports round-by-round outcomes
- Announces the final result

---

## State Model

Game state is stored in a dedicated `GameState` dataclass and **persists across turns**.

### State Fields
- `round` – current round number  
- `max_rounds` – fixed at 3  
- `user_score`, `bot_score` – score tracking  
- `user_used_bomb`, `bot_used_bomb` – enforces one-time bomb usage  
- `finished` – prevents the game from exceeding 3 rounds  

State is **not stored in prompts** and is mutated only through tools.

---

## Agent Design

### `RPSRefereeAgent`
The agent coordinates the game flow and owns the state.

**Responsibilities**
- Explain rules (≤ 5 lines)
- Prompt for moves
- Call validation and resolution tools
- Track progress and enforce limits
- End the game cleanly

The agent **does not implement game rules directly**; all rule logic is delegated to tools.

---

## Explicit Tools Used

### `validate_move(move, used_bomb)`
- Checks move validity
- Enforces one-time bomb rule

### `resolve_round(user_move, bot_move)`
- Determines winner or draw
- Contains all win/lose logic

### `update_game_state(state, result)`
- Advances round count
- Updates scores
- Detects game completion

These tools ensure **clear separation of concerns** and safe state mutation.

---

## Error Handling
- Invalid inputs do not crash the game
- Invalid moves consume a round gracefully
- No dead ends or infinite loops
- Game cannot exceed 3 rounds

---

## Technical Constraints Compliance

| Requirement | Status |
|------------|--------|
| Python | ✅ |
| Google ADK concepts | ✅ |
| Explicit tools | ✅ |
| Persistent state | ✅ |
| No databases | ✅ |
| No external APIs | ✅ |
| No UI frameworks | ✅ |
| Automatic game end | ✅ |

---

## How to Run

```bash
python main.py
