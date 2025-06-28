init python:
    from uuid import uuid4

    class Card:
        IMAGE = "card.png"
        WIDTH = 250
        HEIGHT = 350
        OFFSET = 80

        def __init__(self, **kwargs) -> None:
            self.id = str(uuid4())
            self.cost = kwargs.get("cost", 0)
            self.action = kwargs.get("action", {})
            self.value = kwargs.get("value", 0)

        def label_cost(self) -> str:
            """
            Cost label.
            """
            return emojis.get(self.cost)

        def label_description(self) -> str:
            """
            Description label.
            """
            label = "{color=[colors.black]}"
            for action, data in self.action.items():
                label += action.capitalize()
                label += f" {data['value']}"
                if data.get("stun"):
                    label += " Stun"
                if data.get("all"):
                    label += " All"
                if data.get("times"):
                    label += f" ×{data.get('times')}"
                label += "\n"
            return label.rstrip()

        @staticmethod
        def label_upgrade(action: str, value=1) -> str:
            """
            Upgrade label.
            """
            if action == "cost":
                return f"Select a card to decrease {{b}}cost{{/b}} by {emojis.get(1)}:"
            else:
                return f"Select a card to increase {{b}}{action}{{/b}} by {{b}}{value}{{/b}}:"

        def upgrade(self, action: str, value=1) -> None:
            """
            Upgrade card.
            """
            if action == "cost" and self.cost > 0:
                self.cost -= 1
            else:
                if self.action.get(action):
                    self.action[action]["value"] += value
                else:
                    self.action[action] = {"value": value}

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

            energy = self.action.get("energy")
            if energy:
                renpy.sound.queue("sound/powerup.ogg")
                player.energy += energy["value"]

            draw = self.action.get("draw")
            if draw:
                deck.draw_cards(draw["value"])

            heal = self.action.get("heal")
            if heal:
                for _ in range(heal.get("times", 1)):
                    target.heal(heal["value"])

            attack = self.action.get("attack")
            if attack:
                if is_enemy and attack.get("all"):
                    targets = enemies.get_alive()
                else:
                    targets = [target]
                for target in targets:
                    target.hurt(attack["value"])
                    if is_enemy:
                        if attack.get("stun"):
                            target.stunned = True
                        renpy.show(target.image, at_list=[shake])
                    else:
                        renpy.invoke_in_thread(renpy.with_statement, vpunch)

        @staticmethod
        def generate(count=1) -> list:
            """
            Generate card(s).
            """
            cards = []

            for _ in range(count):
                card = Card(
                    cost=renpy.random.randint(1, 3),
                    action={
                        renpy.random.choice(["attack", "draw", "energy", "heal"]): {
                            "value": renpy.random.randint(1, 6)
                        },
                    },
                )
                cards.append(card)

            return cards
