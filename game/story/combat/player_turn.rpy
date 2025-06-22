label player_turn:

    $ player.turn_rng()

    jump player_turn_menu

label player_turn_menu:

    if enemies.dead():
        jump win

    elif player.health <= 0:
        jump lose

    call screen player_hand

init python:
    def ondrag(drags, drop):
        drag = drags[0]
        cards = player.get_cards()
        card_id = drag.drag_name
        card = player.get_card(card_id)

        if not drop:
            drag.snap(card.get_xpos(cards), card.get_ypos(), 0.2)
            return

        enemy_id = drop.drag_name
        enemy = enemies.get(enemy_id)
        card.use(enemy)

        # snap unused card back
        if player.get_card(card_id):
            drag.snap(card.get_xpos(cards), card.get_ypos(), 0.2)

screen player_hand:
    $ cards = player.get_cards()

    draggroup:
        for enemy_index, enemy in enumerate(enemies.enemies):
            if enemy.health > 0:
                drag:
                    drag_name enemy.id
                    draggable False
                    droppable True
                    idle_child f"enemies/{enemy.image}.png"
                    selected_idle_child f"enemies/{enemy.image} hover.png"
                    xalign enemies.xalign_position(enemy) yalign 1.0

        for card in cards:
            drag:
                drag_name card.id
                dragged ondrag
                droppable False
                drag_raise False
                pos card.get_pos(cards)

                frame:
                    background Frame(card.IMAGE)
                    xysize card.WIDTH, card.HEIGHT
                    label emojis.get(card.cost)
                    label card.get_label():
                        xalign 0.5 yalign 0.5
