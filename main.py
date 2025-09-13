import pygame
import sys
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    ui_font = pygame.font.SysFont("jetbrainsmononerdfontmono", 20)
    game_over_font = pygame.font.SysFont("jetbrainsmononerdfontmono", 40)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if game_over:
            # Clear screen
            screen.fill("black")

            # Draw the frozen game state (all sprites as they were at death)
            for obj in drawable:
                obj.draw(screen)

            # Draw a semi-transparent overlay to darken the background
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)  # 50% transparency
            overlay.fill("black")
            screen.blit(overlay, (0, 0))

            # Display game over text on top
            game_over_surf = game_over_font.render("Game Over!", True, "white")
            game_over_rect = game_over_surf.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            screen.blit(game_over_surf, game_over_rect)

            final_score_surf = ui_font.render(f"Final Score: {score}", True, "white")
            final_score_rect = final_score_surf.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            )
            screen.blit(final_score_surf, final_score_rect)

            restart_surf = ui_font.render("Press ESC to quit", True, "white")
            restart_rect = restart_surf.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
            )
            screen.blit(restart_surf, restart_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return

            pygame.display.flip()
            dt = clock.tick(60) / 1000  # Still need to tick the clock
            continue

        screen.fill("black")
        updatable.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if shot.collided(asteroid):
                    match asteroid.size:
                        case 3:
                            score += 1
                        case 2:
                            score += 2
                        case 1:
                            score += 3
                        case _:
                            score += 0
                    asteroid.split()
                    shot.kill()

        for asteroid in asteroids:
            if asteroid.collided(player):
                print(f"Player hit! Lives before: {player.lives}")
                for ast in asteroids:
                    ast.kill()
                if player.hit():
                    game_over = True
                else:
                    print(f"Player respawned! Lives remaining: {player.lives}")
                break

        for obj in drawable:
            obj.draw(screen)

        score_surf = ui_font.render(f"Score: {score}", True, "white")
        lives_surf = ui_font.render(f"Lives: {player.lives}", True, "white")
        screen.blit(score_surf, (50, 645))
        screen.blit(lives_surf, (50, 670))

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
