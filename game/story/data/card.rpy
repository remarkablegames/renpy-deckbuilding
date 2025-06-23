init python:
    from uuid import uuid4

    class Card:
        IMAGE = "card.png"
        WIDTH = 250
        HEIGHT = 350
        OFFSET = 50

        def __init__(self, **kwargs) -> None:
            self.id = str(uuid4())

            self.cost = kwargs.get("cost", 0)
            self.type = kwargs.get("type", "")
            self.value = kwargs.get("value", 0)

        def get_drag_name(self) -> str:
            """
            Get drag name.
            """
            return self.id

        def label_cost(self) -> str:
            """
            Get cost label.
            """
            return emojis.get(self.cost)

        def label_description(self) -> str:
            """
            Get description label.
            """
            return "{color=[colors.black]}" + f"{self.type} {self.value}".capitalize()

        def get_xpos(self) -> int:
            """
            Calculate x-position.
            """
            x = config.screen_width / 2
            x -= (self.WIDTH + self.OFFSET * (len(player.hand) - 1)) / 2
            x += player.hand.index(self) * self.OFFSET
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

            player.discard_card(self)

            player.energy -= self.cost
            is_enemy = target != player

            if self.type == "attack":
                target.hurt(self.value)
                if is_enemy:
                    renpy.show(target.image, at_list=[shake])
                else:
                    renpy.with_statement(vpunch)

            elif self.type == "heal":
                target.heal(self.value)
