init python:
    class Player(RPGCharacter):
        def __init__(self, **kwargs) -> None:
            super().__init__(**kwargs)

            self.cards = [
                Card(cost=1, type="attack", value=3),
                Card(cost=1, type="attack", value=3),
                Card(cost=2, type="heal", value=3),
                Card(cost=2, type="heal", value=3),
            ]

        def get_card(self, card_id: str) -> Card:
            """
            Get card by id.
            """
            return next((card for card in self.cards if card.id == card_id), None)

        def get_cards(self) -> list:
            """
            Get all cards.
            """
            return self.cards

        def discard_card(self, card: Card) -> None:
            """
            Discard card.
            """
            self.cards.remove(card)

        def action_attack(self) -> None:
            """
            Player attack enemy.
            """
            attack_skill = self.skills["attack"]
            energy_cost = attack_skill.energy

            if self.energy < energy_cost:
                narrator("You don’t have enough energy.")
                renpy.jump("player_turn")
            else:
                renpy.jump("player_attack")

        def action_heal(self) -> None:
            """
            Heal player.
            """
            heal_skill = self.skills["heal"]
            energy_cost = heal_skill.energy

            if self.energy < energy_cost:
                narrator("You don’t have enough energy.")
            else:
                self.energy -= energy_cost
                self.perform_heal(overheal="overheal" in heal_skill.tags)
                narrator("You healed [player.heal] health.")

            renpy.jump("player_turn")

        def action_life_force(self) -> None:
            """
            Player convert health to energy.
            """
            health_cost = self.health_max // 4

            if self.health <= health_cost:
                narrator("You don’t have enough health.")
            else:
                self.health -= health_cost
                self.energy += 1

            renpy.jump("player_turn")

        def action_rage(self) -> None:
            """
            Player increase attack multiplier.
            """
            energy_cost = self.skills["attack"].energy

            if self.energy < energy_cost:
                narrator("You don’t have enough energy.")
            else:
                self.energy -= energy_cost
                self.attack_multiplier *= 2

            renpy.jump("player_turn")

        def end_turn(self) -> None:
            """
            Player end turn.
            """
            self.attack_multiplier = 1

            renpy.jump("enemy_turn")

default player = Player(
    health=15,
    energy=2,
    attack_min=1,
    attack_max=3,
    heal_min=2,
    heal_max=5,
)
