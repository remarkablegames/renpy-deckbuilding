label player_turn:

    $ player.draw_cards()

    show screen player_end_turn

    jump player_hand

label player_hand:

    python:
        for enemy in enemies.enemies:
            if renpy.showing(enemy.image) and enemy.health <= 0:
                enemies.hide(enemy)

    if enemies.dead():
        jump win

    elif player.health <= 0:
        jump lose

    call screen player_hand

init python:
    def ondrag(drags, drop) -> None:
        drag = drags[0]
        card_id = drag.drag_name
        card = player.get_card(card_id)

        if not drop:
            drag.snap(card.get_xpos(), card.get_ypos(), 0.2)
            return

        enemy_id = drop.drag_name
        enemy = enemies.get(enemy_id)
        card.use(enemy)

        # snap unused card back
        if card in player.hand:
            drag.snap(card.get_xpos(), card.get_ypos(), 0.2)

        renpy.jump("player_hand")

    def onhovered(draggable) -> None:
        draggable.top()

screen player_hand:
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

        for card in player.hand:
            drag:
                as draggable
                drag_name card.id
                dragged ondrag
                droppable False
                drag_raise False
                pos card.get_pos()

                frame:
                    background Frame(card.IMAGE)
                    label card.label_cost()
                    label card.label_description():
                        xalign 0.5 yalign 0.5
                    xysize card.WIDTH, card.HEIGHT

                    mousearea:
                        area (0, 0, card.OFFSET, card.HEIGHT)
                        hovered Function(onhovered, draggable)
