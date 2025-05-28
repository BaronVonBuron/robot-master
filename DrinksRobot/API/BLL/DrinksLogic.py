
from DrinksRobot.API.DAL.DrinkContext import DrinkContext

drink_context = DrinkContext()

class DrinkLogic:

    def get_drinks(self):
        drinks = drink_context.get_all_drinks()
        return drinks

    def create_drink_with_content(self, drink_name, img, bottles):
        use_count = 0
        drink_context.create_drink_with_content(drink_name, img, bottles, use_count, )

    def add_drink_count(self, drink_id):
        drink_context.update_drink_use_count(drink_id)

    def get_drink_by_id(self, drink_id):
        drink = drink_context.get_drink_by_id(drink_id)
        return drink


