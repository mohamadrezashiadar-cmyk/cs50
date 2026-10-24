
import math
import random
import time


class Nim:

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Return all available actions (i, j).
        """
        actions = set()

        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))

        return actions

    @classmethod
    def other_player(cls, player):
        """
        Return the other player.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make a move.
        """
        pile, count = action

        if self.winner is not None:
            raise Exception("Game already won")

        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")

        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count

        # Switch player
        self.switch_player()

        # Check for winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI:

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize the AI.
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-value for the previous action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)

        self.update_q_value(
            old_state,
            action,
            old,
            reward,
            best_future
        )

    def get_q_value(self, state, action):
        """
        Return Q-value for a state-action pair.
        Default value is 0.
        """
        return self.q.get((tuple(state), action), 0)

    def update_q_value(
        self,
        state,
        action,
        old_q,
        reward,
        future_rewards
    ):
        """
        Update Q-value using the Q-learning formula.
        """
        new_q = old_q + self.alpha * (
            reward + future_rewards - old_q
        )

        self.q[(tuple(state), action)] = new_q

    def best_future_reward(self, state):
        """
        Return the highest Q-value among available actions.
        """
        actions = Nim.available_actions(state)

        if not actions:
            return 0

        return max(
            self.get_q_value(state, action)
            for action in actions
        )

    def choose_action(self, state, epsilon=True):
        """
        Choose an action using the epsilon-greedy strategy.
        """
        actions = list(Nim.available_actions(state))

        if not actions:
            return None

        # Explore: choose a random action
        if epsilon and random.random() < self.epsilon:
            return random.choice(actions)

        # Exploit: choose an action with the highest Q-value
        best_value = self.best_future_reward(state)

        best_actions = [
            action
            for action in actions
            if self.get_q_value(state, action) == best_value
        ]

        return random.choice(best_actions)


def train(n):
    """
    Train an AI by playing n games against itself.
    """
    player = NimAI()

    for i in range(n):
        print(f"Playing training game {i + 1}")

        game = Nim()

        # Store the last state and action of each player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        while True:

            # Current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Store the move
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Execute the move
            game.move(action)

            new_state = game.piles.copy()

            # Game is over
            if game.winner is not None:

                # Current player lost
                player.update(
                    state,
                    action,
                    new_state,
                    -1
                )

                # Previous player won
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )

                break

            # Update the previous player's move
            elif last[game.player]["state"] is not None:

                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    return player


def play(ai, human_player=None):
    """
    Play against the trained AI.
    """

    # Randomly select who goes first
    if human_player is None:
        human_player = random.randint(0, 1)

    game = Nim()

    while True:

        # Display piles
        print("\nPiles:")

        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")

        print()

        available_actions = Nim.available_actions(game.piles)

        # Human's turn
        if game.player == human_player:

            print("Your Turn")

            while True:
                try:
                    pile = int(input("Choose Pile: "))
                    count = int(input("Choose Count: "))

                    if (pile, count) in available_actions:
                        break

                    print("Invalid move, try again.")

                except ValueError:
                    print("Please enter valid integers.")

        # AI's turn
        else:
            print("AI's Turn")

            pile, count = ai.choose_action(
                game.piles,
                epsilon=False
            )

            print(
                f"AI chose to take {count} "
                f"from pile {pile}."
            )

        # Execute move
        game.move((pile, count))

        # Check winner
        if game.winner is not None:

            print("\nGAME OVER")

            winner = (
                "Human"
                if game.winner == human_player
                else "AI"
            )

            print(f"Winner is {winner}")

            return


if __name__ == "__main__":

    # Train the AI
    ai = train(10000)

    # Start the game
    play(ai)
