init python:
    class Player(RPGCharacter):
        def __init__(self, **kwargs) -> None:
            super().__init__(**kwargs)

            self.deck = [
                Card(cost=1, type="attack", value=3),
                Card(cost=1, type="attack", value=3),
                Card(cost=2, type="heal", value=3),
                Card(cost=2, type="heal", value=3),
            ]

            self.draw_pile = []
            self.discard_pile = []
            self.hand = []

        def get_card(self, card_id: str) -> Card:
            """
            Get card by id.
            """
            return find_by_id(self.deck, card_id)

        def draw_cards(self, count=3) -> None:
            """
            Add cards to hand.
            """
            if not len(self.draw_pile):
                self.draw_pile = self.deck.copy()
                renpy.random.shuffle(self.draw_pile)

            for i in range(count):
                if not len(self.draw_pile):
                    self.draw_pile = self.discard_pile.copy()
                    self.discard_pile = []
                    renpy.random.shuffle(self.draw_pile)

                self.hand.append(self.draw_pile.pop(0))

        def discard_card(self, card: Card) -> None:
            """
            Discard card.
            """
            self.hand.remove(card)
            self.discard_pile.append(card)

        def end_turn(self) -> None:
            """
            End turn.
            """
            while len(self.hand):
                self.discard_pile.append(self.hand.pop(0))

            renpy.hide_screen("player_end_turn")
            renpy.jump("enemy_turn")

        def reset(self) -> None:
            """
            End battle.
            """
            self.draw_pile = []
            self.discard_pile = []
            self.hand = []

default player = Player(
    health=15,
    energy=2,
    attack_min=1,
    attack_max=3,
    heal_min=2,
    heal_max=5,
)
