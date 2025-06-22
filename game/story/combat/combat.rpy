label combat:

    scene bg plain with dissolve

    show screen player_stats
    show screen end_turn

    $ enemies.show()
    $ player.energy = player.energy_max

    jump player_turn
