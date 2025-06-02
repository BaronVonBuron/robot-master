from DrinksRobot.API.DAL.BottleContext import BottleContext

bottle_context = BottleContext()

class BottleLogic:

    def get_bottles(self):
        bottles = bottle_context.get_all_bottles()
        # Assuming the column names are 'id' and 'name' in the BottleTabel
        bottle_list = []
        for bottle in bottles:
            bottle_list.append({"bottle_id": bottle[0], "bottle_position": bottle[1], "urscript_get": bottle[2], "urscript_pour": bottle[3],
                                "urscript_back": bottle[4],"bottle_image": bottle[5], "bottle_name": bottle[6], "bottle_type": bottle[7],
                                "use_count": bottle[8]})
        return bottle_list

    def get_nonalch_bottles(self):
        bottles = bottle_context.get_all_bottles()
        nonalch_bottles = []
        for bottle in bottles:
            if bottle.type == "nonalch":
                nonalch_bottles.append(bottle)
        return nonalch_bottles

    def get_alch_bottles(self):
        bottles = bottle_context.get_all_bottles()
        alch_bottles = []
        for bottle in bottles:
            if bottle.type == "alch":
                alch_bottles.append(bottle)

    def delete_bottle(self, bottle_id):
        toDelete = bottle_id
        bottle_context.delete_bottle(toDelete)

    def add_bottle(self, position, urscript_get, urscript_pour, urscript_back, img, title, bottle_type):
        use_count = 0
        bottle_context.create_bottle(position, urscript_get, urscript_pour, urscript_back, img, title, bottle_type, use_count)

    def add_count(self, bottle_ids):
        for bottle_id in bottle_ids:
            bottle_context.update_bottle_use_count(bottle_id)

    def get_bottle_by_id(self, bottle_id):
        bottles = bottle_context.get_Bottles_with_id([bottle_id])
        if bottles:
            bottle = bottles[0]
            return {
                "bottle_id": bottle.bottle_id,
                "bottle_name": bottle.title,
                "urscript_get": bottle.urscript_get,
                "urscript_pour": bottle.urscript_pour,
                "urscript_back": bottle.urscript_back
            }
        return {"error": f"Bottle with ID {bottle_id} not found"}
