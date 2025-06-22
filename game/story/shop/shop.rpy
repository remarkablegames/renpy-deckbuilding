label shop:

    python:
        config.menu_include_disabled = True
        reward_cost = max(wins, 3)

    menu:
        "What do you want to buy?"

        "Get a reward (-$[reward_cost])
        {tooltip}Upgrade a stat" if money >= reward_cost:
            $ money -= reward_cost
            $ rewards += 1
            $ config.menu_include_disabled = False

            jump reward

        "Battle":
            $ config.menu_include_disabled = False

            jump combat
