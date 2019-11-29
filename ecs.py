""" An implementation of an Entity-Component-System, hopefully it will work best
for pygame applications. I'm developing this as part of my goal to learn
more game development best practices and to develop my adventure game. """


class Entity:
    """ A basic implementation of an entity. It will have a unique ID for
    every entity created. """

    num_entities = 0

    def __init__(self):
        self.ent_id = Entity.num_entities
        Entity.num_entities += 1


for i in range(100):
    a = Entity()
    print(a.ent_id)
