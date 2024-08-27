from owlready2 import *

onto = get_ontology("file://onto.owl")

with onto:
    class Entity(Thing):
        pass

    class Robot(Entity):
        pass

    class Object(Entity):
        pass

    class Pile(Entity):
        pass

    class Place(Thing):
        pass

    class has_place(ObjectProperty, FunctionalProperty):
        domain = [Entity]
        range = [Place]

    class has_position(DataProperty, FunctionalProperty):
        domain = [Place]
        range = [str]