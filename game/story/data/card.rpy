init python:
    from uuid import uuid4

    class Card:
        IMAGE = "card.png"
        WIDTH = 250
        HEIGHT = 350
        OFFSET = 80

        # action
        ATTACK = "attack"
        HEAL = "heal"
        DRAW = "draw"
        ENERGY = "energy"

        def __init__(self, **kwargs) -> None:
            self.id = str(uuid4())

            self.cost = kwargs.get("cost", 0)
            self.action = kwargs.get("action", {})
            self.value = kwargs.get("value", 0)

        def label_cost(self) -> str:
            """
            Get cost label.
            """
            return emojis.get(self.cost)

        def label_description(self) -> str:
            """
            Get description label.
            """
            label = "{color=[colors.black]}"
            for key, value in self.action.items():
                label += f"{key} {value.get('value')}\n".capitalize()
            return label.rstrip()

        def get_xpos(self) -> int:
            """
            Calculate x-position.
            """
            x = config.screen_width / 2
            x -= (self.WIDTH + self.OFFSET * (len(deck.hand) - 1)) / 2
            x += deck.hand.index(self) * self.OFFSET
            return int(x)

        def get_ypos(self) -> int:
            """
            Calculate y-position.
            """
            return config.screen_height - self.HEIGHT

        def get_pos(self) -> int:
            """
            Calculate xy-position.
            """
            return self.get_xpos(), self.get_ypos()

        def use(self, target) -> None:
            """
            Use card.
            """
            if player.energy < self.cost:
                return

            deck.discard_card(self)

            player.energy -= self.cost
            is_enemy = target != player

            energy = self.action.get(self.ENERGY)
            if energy:
                player.energy += energy["value"]

            draw = self.action.get(self.DRAW)
            if draw:
                deck.draw_cards(draw["value"])

            heal = self.action.get(self.HEAL)
            if heal:
                target.heal(heal["value"])

            attack = self.action.get(self.ATTACK)
            if attack:
                target.hurt(attack["value"])
                if is_enemy:
                    renpy.show(target.image, at_list=[shake])
                else:
                    renpy.invoke_in_thread(renpy.with_statement, vpunch)
