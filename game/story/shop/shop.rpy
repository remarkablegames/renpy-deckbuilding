label shop:

    python:
        config.menu_include_disabled = True
        reward_cost = max(wins, 3)

    menu:
        "What do you want to do?"

        "Buy card (-$[reward_cost])
        {tooltip}Add 1 card to your deck" if money >= reward_cost:
            $ money -= reward_cost
            $ config.menu_include_disabled = False

            call screen add_card

        "Remove card (-$[reward_cost])
        {tooltip}Remove 1 card from your deck" if money >= reward_cost:
            $ money -= reward_cost
            $ config.menu_include_disabled = False

            call screen remove_card

        "Get reward (-$[reward_cost])
        {tooltip}Upgrade a stat" if money >= reward_cost:
            $ money -= reward_cost
            $ rewards += 1
            $ config.menu_include_disabled = False

            jump reward

        "Battle":
            $ config.menu_include_disabled = False

            jump battle

screen add_card:

    frame:
        xalign 0.5 yalign 0.5
        padding (50, 50)
        has vbox

        hbox:
            spacing 25

            for card in Card.generate(3):
                button:
                    action [Function(deck.cards.append, card), Jump("shop")]

                    frame:
                        background Frame(Card.IMAGE)
                        label card.label_cost()
                        label card.label_description():
                            xalign 0.5 yalign 0.5
                        xysize Card.WIDTH, Card.HEIGHT

        null height 25

        frame:
            xalign 0.5
            textbutton "Pass":
                action Jump("shop")

screen remove_card:

    frame:
        xalign 0.5 yalign 0.5
        padding (50, 50)
        has vbox

        viewport:
            scrollbars "horizontal"
            ysize 450

            hbox:
                spacing 25

                for card in deck.cards:
                    button:
                        action [Function(deck.cards.remove, card), Jump("shop")]

                        frame:
                            background Frame(Card.IMAGE)
                            label card.label_cost()
                            label card.label_description():
                                xalign 0.5 yalign 0.5
                            xysize Card.WIDTH, Card.HEIGHT

        null height 50

        frame:
            xalign 0.5
            textbutton "Pass":
                action Jump("shop")
