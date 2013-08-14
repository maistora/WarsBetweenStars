#!/usr/bin/env python

import pygame
import player
import enemy
import stats


class Game:

    player_pos = (400, 500)
    bg_img_pos = (0, 0)
    stat_img_pos = (0, 640)
    stat_bar_size = 60
    bound_size = 2
    border = 1
    clock_tick = 300
    enemy_y_range = range(40, 300, 90)
    enemy_x_range = range(-900, -20, 120)
    e_dmg_level = tuple()

    def __init__(self, screen):
        """Initializes game components

        Sets background.
        Call the player creation.
        Call the enemies creation.
        Call the game bounds creation.

        """
        self.screen = screen
        self.screen_size = screen.get_size()
        self.game_level = 1
        self.e_dmg_level = 0
        self.e_health = 0

        self.background = pygame.image.load('images/background.png')
        self.status_img = pygame.image.load('images/stats.png')

        stats_img_pos = (0, self.screen_size[1] - self.stat_bar_size)

        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()

        self.enemies = self.__load_enemies()
        self.sprites.add(self.enemies)

        self.players = pygame.sprite.Group()
        self.gamer = player.Player(self.player_pos, self.players)
        self.sprites.add(self.players)

        self.walls = self.__make_bounds()
        self.sprites.add(self.walls)

    def __make_bounds(self):
        """Create game walls"""

        walls = pygame.sprite.Group()
        wall_image = pygame.image.load('images/wall.png')
        height = self.screen_size[1] - self.stat_bar_size
        for x in range(self.bound_size, self.screen_size[0], self.border):
            for y in range(self.bound_size, height, self.border):
                if x in (
                        self.bound_size, \
                        self.screen_size[0] - self.bound_size) \
                or y in (self.bound_size, height - self.bound_size):
                    wall = pygame.sprite.Sprite(walls)
                    wall.image = wall_image
                    wall.rect = pygame.rect.Rect((x, y), wall_image.get_size())
        return walls

    def __load_enemies(self):
        """Create enemies for current game level"""

        enemies = pygame.sprite.Group()
        for y in self.enemy_y_range:
            for x in self.enemy_x_range:
                enemy_bot = enemy.Enemy((x, y), self.game_level, enemies)
        self.__set_enemy_stats(enemies)
        return enemies

    def __set_enemy_stats(self, enemies):
        """Gets enemies stats for current level"""

        for enemy in enemies:
            self.e_dmg_level = enemy.dmg_level
            self.e_health = enemy.health_level.get(enemy.level)
            break

    def __load_game_stats(self):
        """Gets and displays all game statuses"""

        self.stats = self.stat_class.load_stats()
        health = self.stats.get('health')
        shield = self.stats.get('shield')
        score = self.stats.get('score')
        level = self.stats.get('level')
        overflow = self.stats.get('overflow')
        kills = self.stats.get('kills')
        gun_lvl = self.stats.get('gun')
        dmg_lvl = self.stats.get('dmg')
        e_dmg_lvl = self.stats.get('e_dmg')
        e_health = self.stats.get('e_health')

        screen.blit(self.status_img, self.stat_img_pos)
        screen.blit(health[0], health[1])
        screen.blit(shield[0], shield[1])
        screen.blit(score[0], score[1])
        screen.blit(level[0], level[1])
        screen.blit(overflow[0], overflow[1])
        screen.blit(kills[0], kills[1])
        screen.blit(gun_lvl[0], gun_lvl[1])
        screen.blit(dmg_lvl[0], dmg_lvl[1])
        screen.blit(e_dmg_lvl[0], e_dmg_lvl[1])
        screen.blit(e_health[0], e_health[1])

    def __load_congratz(self):
        self.stat_class.congratz()
        congr = self.stats.get('congratz')
        screen.blit(congr[0], congr[1])

    def __load_lose(self):
        self.stat_class.lose()
        lose = self.stats.get('lose')
        screen.blit(lose[0], lose[1])

    def __check_status(self):
        if self.players.sprites().__len__() < 1:
            self.__load_lose()
            return
        elif self.enemies.sprites().__len__() < 1\
            and self.game_level > 5:
            self.__load_congratz()

    def __load_boss(self):
        """Creates the boss for the final level"""

        self.boss = enemy.Enemy((-400, 60), self.game_level, self.enemies)
        self.sprites.add(self.boss)
        self.__set_enemy_stats(self.enemies)

    def main(self, player_name):
        self.player_name = player_name
        game_running = True
        while game_running:
            tick = self.clock.tick(self.clock_tick)
            self.events = pygame.event.get()
            self.stat_class = stats.Stats(self)
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.stat_class.print_scores()
                    return
                if event.type == pygame.KEYDOWN \
                and event.key == pygame.K_ESCAPE:
                    self.stat_class.print_scores()
                    return

            enemy_count = self.enemies.sprites().__len__()

            if enemy_count < 1 and self.game_level <= 5:
                self.game_level += 1

            if enemy_count < 1 and self.game_level <= 4:
                self.enemies = self.__load_enemies()
                self.sprites.add(self.enemies)
            if enemy_count < 1 and self.game_level == 5:
                self.__load_boss()

            self.sprites.update(tick / 1000., self)
            screen.blit(self.background, self.bg_img_pos)
            self.sprites.draw(screen)
            self.__load_game_stats()
            self.__check_status()
            pygame.display.flip()

if __name__ == '__main__':
    player_name = raw_input("Enter your name: ")
    pygame.init()
    screen = pygame.display.set_mode(
            (1000, 700),
            pygame.HWSURFACE | pygame.DOUBLEBUF
            )
    Game(screen).main(player_name)
