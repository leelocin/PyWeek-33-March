import math

class EntityManager:
    def __init__(self):
        self.entities = []

    def get_tasks(self, x, y, z):
        found = False
        tasks = []
        for entity in self.entities:
            if math.floor(entity.x) == x and math.floor(entity.y) == y and math.floor(entity.z) == z:
                found = True
                tasks.append(entity)
            elif found == True:
                break
        return tasks

    def get_outside_back_entities(self):
        outside_tiles = []
        for entity in self.entities:
            if entity.x < 0 or entity.y < 0 or entity.z < 0:
                outside_tiles.append(entity)
        return outside_tiles

    def get_outside_front_entities(self, x, y, z):
        outside_tiles = []
        for entity in self.entities:
            if entity.x > x or entity.y > y or entity.z > z:
                outside_tiles.append(entity)
        return outside_tiles

    def add_entity(self, entity):
        for existing_entity in self.entities:
            if existing_entity.z < entity.z:
                self.entities.insert(self.entities.index(existing_entity), entity)
                copy = self.entities
                copy.reverse()
                return self.entities
            elif existing_entity.z == entity.z:
                if existing_entity.y < entity.y:
                    self.entities.insert(self.entities.index(existing_entity), entity)
                    return self.entities
                elif existing_entity.y == entity.y:
                    if existing_entity.x <= entity.x:
                        self.entities.insert(self.entities.index(existing_entity), entity)
                        return self.entities
        # If it reaches this point, append to end.
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)


class Entity:
    def __init__(self, x, y, z, obj):
        self.x = x
        self.y = y
        self.z = z
        self.obj = obj
        self.image = obj.image

    def __str__(self) -> str:
        return f'Entity: {self.x}, {self.y}, {self.z}'
