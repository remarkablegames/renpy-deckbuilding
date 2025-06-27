label battle:

    scene bg plain with dissolve

    show screen player_stats

    $ enemies.show()
    $ player.energy = player.energy_max
    $ deck.shuffle()

    jump player_turn
