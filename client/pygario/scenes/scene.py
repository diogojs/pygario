import pygame


class Scene:
    def run(self):
        raise NotImplementedError("Scene.run not implemented")
    
    def draw(self, deltatime: float):
        raise NotImplementedError("Scene.draw not implemented")

    def update(self, deltatime: float):
        raise NotImplementedError("Scene.update not implemented")
    
    def handle_events(self):
        from pygario.game import Game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Game.is_running = False
                elif event.key == pygame.K_PAGEUP:  # TODO: remove this / only for debugging
                    self.player.radius = self.player.radius*2
                
            elif event.type == pygame.MOUSEMOTION:
                Game.Mouse.x = event.pos[0]
                Game.Mouse.y = event.pos[1]
