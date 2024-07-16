* client

must have:
[X] check collision only for nearby cells/blobs (on player.py)
[X] when eating a cell/blob, send message to server
[X] Send message when moving
[] lerp radius increasing when eating (should not be instanteaneous)
[] Implement Menu
    [] Start
    [] Name, Server IP/Port
    [] Quit
[] use weakreference to optimize
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
[X] receive connection of new player, generate data and send it back
[X] receive eat msg
[X] receive moving/updating msg
[X] store color of cells as well because otherwise it's being randomized each frame on the client
    [] or change so server don't send the whole map, but only what changed (could be 2 lists one for added/changed cells and other for removed cells)
[] validate move and eating
[X] regularly generate new cells
[] broadcast state each clock tick (or when there is any changes)
[] receive disconnect msg and remove player from the map