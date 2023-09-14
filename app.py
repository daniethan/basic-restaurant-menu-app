from flask import Flask, request, flash, redirect, render_template, url_for
from src.dbconfig import get_db_con
from src import crud
from decouple import config


app = Flask(__name__)


@app.route("/")
@app.route("/restaurants")
def index():
    restaurants = crud.get_restaurants(session=get_db_con())

    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/restaurants/new", methods=["GET", "POST"])
def create_restaurant():
    if request.method == "POST":
        if len(request.form.get("name")) != 0:
            crud.register_new_restaurant(name=request.form.get("name"))
            flash(f"A new restaurant is created")
            return redirect(url_for("index"))
        else:
            return "Failed because no name was provided"
    return render_template("create-restaurant.html")


@app.route("/restaurants/<int:restaurant_id>/edit", methods=["GET", "POST"])
def edit_restaurant(restaurant_id: int):
    if request.method == "POST":
        crud.update_restaurant(
            restaurant_id,
            new_name=request.form.get("new_name"),
        )

        flash(f"Restaurant updated successfully!")

        return redirect(url_for("index"))

    return render_template(
        "edit-restaurant.html",
        restaurant=crud.get_restaurant_by_id(restaurant_id, session=get_db_con()),
    )


@app.route("/restaurants/<int:restaurant_id>/delete", methods=["GET", "POST"])
def delete_restaurant(restaurant_id: int):
    if request.method == "POST":
        crud.delete_restaurant(restaurant_id)

        flash(f"Restaurant was deleted")
        return redirect(url_for("index"))

    restaurant = crud.get_restaurant_by_id(restaurant_id, session=get_db_con())

    if not restaurant:
        return redirect(url_for("index"))
    return render_template(
        "delete-restaurant.html",
        restaurant=restaurant,
    )


@app.route("/restaurants/<int:restaurant_id>/menu")
def restaurant_menu(restaurant_id: int):
    return render_template(
        "menu.html",
        restaurant=crud.get_restaurant_by_id(restaurant_id, get_db_con()),
        items=crud.get_menu_items(restaurant_id, get_db_con()),
    )


@app.route("/restaurants/<int:restaurant_id>/menu/new", methods=["GET", "POST"])
def new_menu_item(restaurant_id):
    if request.method == "POST":
        crud.create_menu_item(restaurant_id, data=request.form.copy())

        flash("New menu item was created successfully")
        return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id))

    return render_template("new-menu-item.html", restaurant_id=restaurant_id)


@app.route(
    "/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit", methods=["GET", "POST"]
)
def edit_menu_item(restaurant_id, menu_id):
    if request.method == "POST":
        crud.update_menu_item(menu_id, data=request.form.copy())

        flash(f"Menu item was updated")
        return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id))

    return render_template(
        "edit-menu-item.html",
        restaurant_id=restaurant_id,
        menu_id=menu_id,
        item=crud.get_menu_item_by_id(menu_id, get_db_con()),
    )


@app.route(
    "/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete",
    methods=["GET", "POST"],
)
def delete_menu_item(restaurant_id: int, menu_id: int):
    if request.method == "POST":
        crud.delete_menu_item(menu_id)

        flash(f"Menu item has been deleted")
        return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id))

    menu_item = crud.get_menu_item_by_id(menu_id, get_db_con())
    if not menu_item:
        return redirect(url_for("restaurant_menu", restaurant_id=restaurant_id))
    return render_template(
        "delete-menu-item.html",
        menu_item=menu_item,
    )


if __name__ == "__main__":
    app.secret_key = config("SECRET_KEY")
    app.run(debug=True)
