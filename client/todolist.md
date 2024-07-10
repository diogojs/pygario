* client

must have:
[X] check collision only for nearby cells/blobs (on player.py)
[] lerp radius increasing when eating (should not be instanteaneous)
[] when eating a cell/blob, send message to server
[] implement blob border waving/flickering
[] implement flattening of blob when pressing to the edges of the map
[] player splitting (when press SPACE)
[] player spit mass (when press W)

good to have:
[] virus

if possible:
[] lerp velocity change (direction)

* server

must have:
[] receive connection of new player, generate data and send it back
[] regularly generate new cells
[] broadcast state each clock tick (or when there is any changes)
[] receive moving/updating msg
[] receive eat msg
[] receive disconnect msg and remove player from the map