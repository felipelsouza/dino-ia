import pygame
import os
# import random

pygame.font.init()
FONT = pygame.font.SysFont('Fira Code', 18)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 500

FRAME_RATE = 30

BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'background.png')))
GROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'ground.png')))
CACTUS_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'small_cactus_2.png')))
DINOSAUR_IDLE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'dino.png')))
DINOSAUR_RUNNING_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'dino_running_1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'dino_running_2.png')))
]
DINOSAUR_JUMPING_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'dino_jumping.png')))


class Dinosaur:
    IDLE_IMAGE = DINOSAUR_IDLE_IMAGE
    ANIMATION_TIME = 4
    RUNNING_IMAGES = DINOSAUR_RUNNING_IMAGES

    def __init__(self, x_axis, y_axis):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.min_y_axis = y_axis
        self.speed = 0
        self.time = 0
        self.height = self.y_axis
        self.actual_image_count = 0
        self.actual_image = self.IDLE_IMAGE

    def jump(self):
        self.speed = -14
        self.time = 0
        self.height += self.y_axis

    def move(self):
        # calculate displacement
        self.time += 1
        displacement = 1.5 * (self.time ** 2) + self.speed * self.time

        # restrict displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y_axis += displacement

    def run(self):
        self.actual_image_count += 1

        if self.actual_image_count < self.ANIMATION_TIME:
            self.actual_image = self.RUNNING_IMAGES[0]
        elif self.actual_image_count < self.ANIMATION_TIME * 2:
            self.actual_image = self.RUNNING_IMAGES[1]
        elif self.actual_image_count >= self.ANIMATION_TIME * 2 + 1:
            self.actual_image = self.RUNNING_IMAGES[0]
            self.actual_image_count = 0

    def spawn(self, screen):
        self.run()

        screen.blit(self.actual_image, (self.x_axis, self.y_axis))

    def get_image_mask(self):
        return pygame.mask.from_surface(self.actual_image)


class Cactus:
    SPEED = 10

    def __init__(self, x_axis):
        self.x_axis = x_axis
        self.y_axis = 424
        self.IMAGE = CACTUS_IMAGE
        self.has_passed = False

    def move(self):
        self.x_axis -= self.SPEED

    def spawn(self, screen):
        screen.blit(self.IMAGE, (self.x_axis, self.y_axis))

    def collide(self, dinosaur):
        dinosaur_mask = dinosaur.get_image_mask()
        cactus_mask = pygame.mask.from_surface(self.IMAGE)

        objects_distance = (self.x_axis - dinosaur.x_axis, self.y_axis - round(dinosaur.y_axis))

        has_collided = dinosaur_mask.overlap(cactus_mask, objects_distance)

        if has_collided:
            return True
        else:
            return False


class Ground:
    SPEED = 10
    WIDTH = GROUND_IMAGE.get_width()
    IMAGE = GROUND_IMAGE

    def __init__(self, y_axis):
        self.y_axis = y_axis
        self.x_axis_0 = 0
        self.x_axis_1 = self.WIDTH

    def move(self):
        self.x_axis_0 -= self.SPEED
        self.x_axis_1 -= self.SPEED

        if self.x_axis_0 + self.WIDTH < 0:
            self.x_axis_0 = self.x_axis_1 + self.WIDTH
        if self.x_axis_1 + self.WIDTH < 0:
            self.x_axis_1 = self.x_axis_0 + self.WIDTH

    def spawn(self, screen):
        screen.blit(self.IMAGE, (self.x_axis_0, self.y_axis))
        screen.blit(self.IMAGE, (self.x_axis_1, self.y_axis))


def render_screen(screen, ground, score, dinosaurs, cacti):
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    for dinosaur in dinosaurs:
        dinosaur.spawn(screen)

    for cactus in cacti:
        cactus.spawn(screen)

    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))

    ground.spawn(screen)

    pygame.display.update()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ground = Ground(475)
    score = 0
    dinosaurs = [Dinosaur(120, 405)]
    cacti = [Cactus(SCREEN_WIDTH)]
    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        clock.tick(FRAME_RATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    for dinosaur in dinosaurs:
                        dinosaur.jump()

        ground.move()

        for i, dinosaur in enumerate(dinosaurs):
            dinosaur.move()

            if (dinosaur.y_axis + dinosaur.actual_image.get_height()) > ground.y_axis:
                dinosaur.y_axis = 405

        has_to_add_cactus = False
        cacti_to_remove = []
        for cactus in cacti:
            for i, dinosaur in enumerate(dinosaurs):
                if cactus.collide(dinosaur):
                    dinosaurs.pop(i)
                if not cactus.has_passed and dinosaur.x_axis > cactus.x_axis:
                    cactus.has_passed = True
                    has_to_add_cactus = True

                cactus.move()
                if cactus.x_axis + cactus.IMAGE.get_width() < 0:
                    cacti_to_remove.append(cactus)

        if has_to_add_cactus:
            score += 1
            cacti.append(Cactus(SCREEN_WIDTH))

        for cactus in cacti_to_remove:
            cacti.remove(cactus)

        render_screen(screen, ground, score, dinosaurs, cacti)


if __name__ == '__main__':
    main()
