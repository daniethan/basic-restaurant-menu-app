from src.dbconfig import MenuItem, Restaurant, get_db_con, Session
from typing import Callable

# fetch all restaurants
get_restaurants: Callable[[Session], list[Restaurant]] = lambda session: session.query(
    Restaurant
).all()

# fetch restaurant by id
get_restaurant_by_id: Callable[
    [int, Session], Restaurant
] = lambda restaurant_id, session: session.get(Restaurant, restaurant_id)


def register_new_restaurant(name: str, session: Session = get_db_con()) -> None:
    """Register new restaurant with a name"""
    # new_restaurant = Restaurant(name=name)
    session.add(Restaurant(name=name))
    session.commit()
    return


def update_restaurant(
    restaurant_id: int, new_name: str, session: Session = get_db_con()
) -> None:
    """Edit restaurant name thru its ID"""
    restaurant_to_edit = get_restaurant_by_id(restaurant_id, session)
    restaurant_to_edit.name = new_name
    session.commit()
    return


def delete_restaurant(restaurant_id: int, session: Session = get_db_con()) -> None:
    """Delete a restaurant by ID"""
    restaurant_to_delete = get_restaurant_by_id(restaurant_id, session)
    session.delete(restaurant_to_delete)
    session.commit()
    return


# fetch all menu items for a specific restaurant
get_menu_items: Callable[[int, Session], list[MenuItem]] = (
    lambda restaurant_id, session: session.query(MenuItem)
    .filter_by(restaurant_id=restaurant_id)
    .all()
)

# fetch a particular menu item for a specific restaurant
get_menu_item_by_id: Callable[
    [int, Session], MenuItem
] = lambda item_id, session: session.get(MenuItem, item_id)


def create_menu_item(
    restaurant_id: int, data: dict, session: Session = get_db_con()
) -> None:
    """Create a new menu item for a specific restaurant ID"""
    new_item = MenuItem(
        name=data.get("name"),
        price=data.get("price"),
        restaurant_id=restaurant_id,
        description=data.get("description"),
        course=data.get("course"),
    )
    session.add(new_item)
    session.commit()
    return


def update_menu_item(menu_id: int, data: dict, session: Session = get_db_con()) -> None:
    """Update menu item data thru its ID"""
    item_to_edit = session.get(MenuItem, menu_id)

    if data.get("new_name"):
        item_to_edit.name = data.get("new_name")
    if data.get("new_description"):
        item_to_edit.description = data.get("new_description")
    if data.get("new_price"):
        item_to_edit.price = data.get("new_price")
    if data.get("new_course"):
        item_to_edit.course = data.get("new_course")

    session.commit()
    return


def delete_menu_item(menu_id: int, session: Session = get_db_con()):
    """Delete menu item data thru its ID"""
    item_to_delete = session.get(MenuItem, menu_id)
    session.delete(item_to_delete)
    session.commit()
    return
