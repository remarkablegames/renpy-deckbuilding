init python:
    class Deck:
        def __init__(self) -> None:
            self.cards = [
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
            Find card by id.
            """
            return find_by_id(self.cards, card_id)

        def draw_cards(self, count=3) -> None:
            """
            Add card(s) to hand.
            """
            if not len(self.draw_pile):
                self.draw_pile = self.cards.copy()
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

        def discard_hand(self) -> None:
            """
            Discard hand at end of turn.
            """
            while len(self.hand):
                self.discard_pile.append(self.hand.pop(0))

        def reset_hand_pile(self) -> None:
            """
            Reset hand and pile after battle.
            """
            self.draw_pile = []
            self.discard_pile = []
            self.hand = []

default deck = Deck()
