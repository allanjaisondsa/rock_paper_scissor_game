
from dataclasses import dataclass, field
from typing import Dict, Tuple
import random

# -----------------------------
# GAME STATE MODEL
# -----------------------------

@dataclass
class GameState:
    round: int = 0
    max_rounds: int = 3
    user_score: int = 0
    bot_score: int = 0
    user_used_bomb: bool = False
    bot_used_bomb: bool = False
    finished: bool = False


# -----------------------------
# TOOLS (EXPLICIT)
# -----------------------------

def validate_move(move: str, used_bomb: bool) -> Tuple[bool, str]:
    valid_moves = ["rock", "paper", "scissors", "bomb"]

    if move not in valid_moves:
        return False, "Invalid move"
    if move == "bomb" and used_bomb:
        return False, "Bomb already used"
    return True, "OK"


def resolve_round(user_move: str, bot_move: str) -> str:
    if user_move == bot_move:
        return "draw"

    if user_move == "bomb" and bot_move == "bomb":
        return "draw"
    if user_move == "bomb":
        return "user"
    if bot_move == "bomb":
        return "bot"

    wins_against = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    return "user" if wins_against[user_move] == bot_move else "bot"


def update_game_state(state: GameState, result: str):
    state.round += 1
    if result == "user":
        state.user_score += 1
    elif result == "bot":
        state.bot_score += 1

    if state.round >= state.max_rounds:
        state.finished = True


# -----------------------------
# AGENT (REFEREE)
# -----------------------------

class RPSRefereeAgent:

    def __init__(self):
        self.state = GameState()

    def explain_rules(self):
        print(
            "Rules:\n"
            "• Best of 3 rounds\n"
            "• Moves: rock, paper, scissors, bomb (once)\n"
            "• Bomb beats everything\n"
            "• Invalid input wastes the round\n"
        )

    def get_bot_move(self) -> str:
        moves = ["rock", "paper", "scissors"]
        if not self.state.bot_used_bomb:
            moves.append("bomb")
        return random.choice(moves)

    def handle_turn(self, user_input: str):
        if self.state.finished:
            print("Game already finished.")
            return

        user_move = user_input.lower().strip()

        valid, reason = validate_move(user_move, self.state.user_used_bomb)

        bot_move = self.get_bot_move()

        if not valid:
            print(f"\nRound {self.state.round + 1}")
            print(f"❌ Invalid move ({reason}). Round wasted.")
            update_game_state(self.state, "draw")
            return

        if user_move == "bomb":
            self.state.user_used_bomb = True
        if bot_move == "bomb":
            self.state.bot_used_bomb = True

        result = resolve_round(user_move, bot_move)
        update_game_state(self.state, result)

        print(f"\nRound {self.state.round}")
        print(f"User played: {user_move}")
        print(f"Bot played:  {bot_move}")

        if result == "draw":
            print("➡️  Result: Draw")
        elif result == "user":
            print("✅ Result: User wins the round")
        else:
            print("🤖 Result: Bot wins the round")

    def finish_game(self):
        print("\n=== GAME OVER ===")
        print(f"Final Score → User: {self.state.user_score} | Bot: {self.state.bot_score}")

        if self.state.user_score > self.state.bot_score:
            print("🏆 Final Result: USER WINS")
        elif self.state.bot_score > self.state.user_score:
            print("🤖 Final Result: BOT WINS")
        else:
            print("⚖️ Final Result: DRAW")


# -----------------------------
# CLI LOOP
# -----------------------------

if __name__ == "__main__":
    agent = RPSRefereeAgent()
    agent.explain_rules()

    while not agent.state.finished:
        user_input = input("Enter your move: ")
        agent.handle_turn(user_input)

    agent.finish_game()
