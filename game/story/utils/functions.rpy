init python:
    def find_by_id(items: list, item_id: str):
        return next((item for item in items if item.id == item_id), None)
