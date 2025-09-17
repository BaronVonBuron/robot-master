from flask import Blueprint, request, jsonify
from DrinksRobot.API.DAL.MenuContext import MenuContext
from DrinksRobot.API.Helpers.logger import get_logger

log = get_logger("MenuController")
menu_ctx = MenuContext()

MenuController = Blueprint('MenuController', __name__)


@MenuController.route('/catalog', methods=['GET'])
def list_catalog():
    return jsonify(menu_ctx.list_catalog())


@MenuController.route('/menus', methods=['GET'])
def list_menus():
    return jsonify(menu_ctx.list_menus())


@MenuController.route('/menus', methods=['POST'])
def create_menu():
    data = request.get_json(silent=True) or {}
    name = data.get('menu_name') or data.get('name')
    if not name:
        return jsonify({"error": "Missing menu_name"}), 400
    menu_id = menu_ctx.create_menu(name)
    log.info("Created menu %s id=%s", name, menu_id)
    return jsonify({"menu_id": menu_id, "menu_name": name}), 201


@MenuController.route('/menus/<int:menu_id>/activate', methods=['POST'])
def activate_menu(menu_id: int):
    ok = menu_ctx.set_active_menu(menu_id)
    return (jsonify({"status": "activated"}), 200) if ok else (jsonify({"error": "not found"}), 404)


@MenuController.route('/menus/<int:menu_id>/bottles', methods=['GET'])
def get_menu_bottles(menu_id: int):
    return jsonify(menu_ctx.get_menu_bottles(menu_id))


@MenuController.route('/menus/<int:menu_id>/bottles', methods=['POST'])
def add_bottle(menu_id: int):
    data = request.get_json(silent=True) or {}
    catalog_bottle_id = data.get('catalog_bottle_id')
    position = data.get('position')
    if not catalog_bottle_id:
        return jsonify({"error": "Missing catalog_bottle_id"}), 400
    menu_ctx.add_bottle_to_menu(menu_id, int(catalog_bottle_id), position)
    return jsonify({"status": "added"}), 200


@MenuController.route('/menus/<int:menu_id>/bottles/<int:catalog_bottle_id>', methods=['DELETE'])
def remove_bottle(menu_id: int, catalog_bottle_id: int):
    ok = menu_ctx.remove_bottle_from_menu(menu_id, catalog_bottle_id)
    return (jsonify({"status": "removed"}), 200) if ok else (jsonify({"error": "not found"}), 404)
