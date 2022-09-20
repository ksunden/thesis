import yaqc

c = yaqc.Client(38401)
c.set_position(23)

while c.busy():
    ...

print(c.get_position())

c.set_position(2)

while c.busy():
    ...

print(c.get_position())
