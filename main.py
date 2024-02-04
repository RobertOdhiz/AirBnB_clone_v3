#!/usr/bin/python3
"""
 Test cities access from a state
"""
from models import storage
from models.state import State
from models.city import City

"""
 Objects creations
"""
state_1 = State(name="California")
print("New state: {}".format(state_1))
state_1.save()
state_2 = State(name="Arizona")
print("New state: {}".format(state_2))
state_2.save()

state_2 = State(name="Allabama")
print("New state: {}".format(state_2))
state_2.save()
state_2 = State(name="Texas")
print("New state: {}".format(state_2))
state_2.save()
state_2 = State(name="Nairobi")
print("New state: {}".format(state_2))
state_2.save()


