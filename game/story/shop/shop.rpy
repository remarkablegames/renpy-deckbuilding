label shop:

    $ config.menu_include_disabled = True
    $ reward_cost = max(wins, 3)

    menu:
        "What do you want to do?"

        "Buy a card (-$[reward_cost])
        {tooltip}Add 1 card to your deck" if money >= reward_cost:
            $ money -= reward_cost
            $ config.menu_include_disabled = False
            call screen add_card

        "Upgrade a card (-$[reward_cost])
        {tooltip}Upgrade 1 card in your deck" if money >= reward_cost:
            $ money -= reward_cost
            $ config.menu_include_disabled = False
            $ upgrade_card_action = renpy.random.choice(["draw"] * 2 + ["energy"] * 2 + ["heal"] * 3 + ["cost"] * 1 + ["attack"] * 6)
            $ upgrade_card_value = renpy.random.randint(1, 3)
            call screen upgrade_card

        "Remove a card (-$[reward_cost])
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

        text "Add 1 card to your deck:"

        null height 25

        hbox:
            spacing 25

            for card in Card.generate(3):
                button:
                    action [Function(deck.cards.append, card), Jump("shop")]

                    frame:
                        background Frame(Card.IMAGE)
                        label card.label_cost()
                        label card.label_description() xalign 0.5 yalign 0.5
                        xysize Card.WIDTH, Card.HEIGHT

        null height 25

        frame:
            xalign 0.5
            textbutton "Pass":
                action Jump("shop")

screen upgrade_card:

    frame:
        xalign 0.5 yalign 0.5
        padding (50, 50)
        has vbox

        text Card.label_upgrade(upgrade_card_action)

        null height 25

        hbox:
            spacing 25

            for card in deck.get_cards(3, lambda card: card.cost > 0 if upgrade_card_action == "cost" else True):
                button:
                    action [Function(card.upgrade, upgrade_card_action, upgrade_card_value), Jump("shop")]

                    frame:
                        background Frame(Card.IMAGE)
                        label card.label_cost()
                        label card.label_description() xalign 0.5 yalign 0.5
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
                            label card.label_description() xalign 0.5 yalign 0.5
                            xysize Card.WIDTH, Card.HEIGHT

        null height 50

        frame:
            xalign 0.5
            textbutton "Pass":
                action Jump("shop")
