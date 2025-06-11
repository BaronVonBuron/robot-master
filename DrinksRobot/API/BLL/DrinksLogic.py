
from DrinksRobot.API.DAL.DrinkContext import DrinkContext

drink_context = DrinkContext()

class DrinkLogic:

    def get_drinks(self):
        drinks = drink_context.get_all_drinks_with_bottles()
        drink_list = []

        for drink in drinks:
            drink_list.append({
                "drink_id": drink["DrinkId"],
                "drink_name": drink["DrinkName"],
                "drink_image": drink["Img"],
                "use_count": drink["UseCount"],
                "bottles": [
                    {
                        "bottle_id": bottle["BottleId"],
                        "title": bottle["Title"]
                    }
                    for bottle in drink["Bottles"]
                ]
            })

        return drink_list

    def create_drink_with_content(self, drink_name, img, bottles):
        use_count = 0
        drink_context.create_drink_with_content(drink_name, img, bottles, use_count, )

    def add_drink_count(self, drink_id):
        drink_context.update_drink_use_count(drink_id)

    def get_drink_by_id(self, drink_id):
        drink = drink_context.get_drink_by_id(drink_id)
        return drink


