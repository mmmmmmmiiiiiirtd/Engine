import pygame
import sys
import time
import random

class Engine:
    def __init__(self, width, height):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Micro Text Engine (MTE) | Идет игра...")
        icon_image = pygame.image.load("icon.png")
        pygame.display.set_icon(icon_image)
        self.clock = pygame.time.Clock()
        self.game_objects = {}
        self.text = {}
        self.wait_ticks = 0
        self.loop_process = None
        self.current_line = 0
        self.sleep_until = 0
        self.if_was_true = False
        self.if_stack = []
        self.sounds = {}
        self.just_restarted = False
        self.sleep_until = 0
        self.start_time = pygame.time.get_ticks()

        self.context = {
            "creat_box": self.creat_box,
            "move": self.move,
            "wait": self.wait,
            "deleted_box": self.deleted_box,
            "exists_box": self.exists_box,
            "key_pressed": self.key_pressed,
            "change_color": self.change_color,
            "move_to": self.move_to,
            "random_range": self.random_range,
            "get_x": self.get_x,
            "get_y": self.get_y,
            "get_width": self.get_width,
            "get_height": self.get_height,
            "change_size": self.change_size,
            "change_size_to": self.change_size_to,
            "exists_text": self.exists_text,
            "creat_text": self.creat_text,
            "check_collision": self.check_collision,
            "restart": self.restart,
            "play_sound": self.play_sound,
            "time": 0
        }

    def play_sound(self, path):
        if path not in self.sounds:
            self.sounds[path] = pygame.mixer.Sound(path)

        self.sounds[path].play()

    def restart(self):
        self.game_objects.clear()
        self.text.clear()
        self.if_stack.clear()
        self.current_line = 0
        self.sleep_until = 0
        self.just_restarted = True

        self.start_time = pygame.time.get_ticks()

        self.run_init(init_code)

    def check_collision(self, name1, name2):
        if name1 in self.game_objects and name2 in self.game_objects:
            return self.game_objects[name1]["rect"].colliderect(self.game_objects[name2]["rect"])
        else:
            return False

    def random_range(self, min, max):
        return random.randint(min, max)

    def creat_box(self, name, x, y, width, height, color="white", type="static"):
        actual_color = pygame.Color(color) if isinstance(color, str) else color
        box = {
            "rect": pygame.Rect(x, y, width, height),
            "color": actual_color,
            "body_type": type
        }
        self.game_objects[name] = box

    def deleted_box(self, name):
        self.game_objects.pop(name)

    def exists_box(self, name):
        if name in self.game_objects:
            return True
        else:
            return False

    def get_x(self, name):
        return self.game_objects[name]["rect"].x

    def get_y(self, name):
        return self.game_objects[name]["rect"].y

    def get_width(self, name):
        return self.game_objects[name]["rect"].width

    def get_height(self, name):
        return self.game_objects[name]["rect"].height

    def creat_text(self, name, message, x, y, size=30, color="white"):
        actual_color = pygame.Color(color) if isinstance(color, str) else color

        self.text[name] = {
            "message": str(message),
            "x": x,
            "y": y,
            "size": size,
            "color": actual_color
        }

    def exists_text(self, name):
        if name in self.text:
            return True
        else:
            return False

    def move(self, name, x, y):
        if self.game_objects[name]["body_type"] == "static":
            self.game_objects[name]["rect"].x += x
            for other_name, other_box in self.game_objects.items():
                if other_name != name and other_box["body_type"] == "dynamic":
                    if self.game_objects[name]["rect"].colliderect(other_box["rect"]):
                        other_box["rect"].x += x

            self.game_objects[name]["rect"].y += y
            for other_name, other_box in self.game_objects.items():
                if other_name != name and other_box["body_type"] == "dynamic":
                    if self.game_objects[name]["rect"].colliderect(other_box["rect"]):
                        other_box["rect"].y += y
        else:
            self.game_objects[name]["rect"].x += x
            for other_name, other_box in self.game_objects.items():
                if other_name != name and other_box["body_type"] == "static":
                    if self.game_objects[name]["rect"].colliderect(other_box["rect"]):
                        self.game_objects[name]["rect"].x -= x

            self.game_objects[name]["rect"].y += y
            for other_name, other_box in self.game_objects.items():
                if other_name != name and other_box["body_type"] == "static":
                    if self.game_objects[name]["rect"].colliderect(other_box["rect"]):
                        self.game_objects[name]["rect"].y -= y

    def move_to(self, name, x, y):
        self.game_objects[name]["rect"].x = x
        self.game_objects[name]["rect"].y = y

    def change_color(self, name, color):
        actual_color = pygame.Color(color) if isinstance(color, str) else color

        self.game_objects[name]["color"] = actual_color

    def change_size(self, name, width, height):
        self.game_objects[name]["rect"].width += width
        self.game_objects[name]["rect"].height += height

    def change_size_to(self, name, width, height):
        self.game_objects[name]["rect"].width = width
        self.game_objects[name]["rect"].height = height

    def wait(self, seconds):
        current_time = pygame.time.get_ticks()
        self.sleep_until = current_time + int(seconds)

    def key_pressed(self, key_name):
        keys = pygame.key.get_pressed()

        key_map = {
            'w': pygame.K_w, 'a': pygame.K_a, 's': pygame.K_s, 'd': pygame.K_d,
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
            'space': pygame.K_SPACE
        }

        pygame_key = key_map.get(key_name.lower())
        if pygame_key is not None:
            return keys[pygame_key]
        return False

    def run_init(self, raw_lines):
        full_code = "\n".join(raw_lines)

        exec(full_code, self.context, self.context)

    def run_loop(self, raw_lines):
        if not raw_lines:
            return

        current_time = pygame.time.get_ticks()
        self.context["time"] = current_time - self.start_time

        if current_time < self.sleep_until:
            return

        def get_indent(s):
            return len(s) - len(s.lstrip(' '))

        if hasattr(self, 'just_restarted') and self.just_restarted:
            self.just_restarted = False
            return

        if current_time < self.sleep_until:
            return

        while self.current_line < len(raw_lines):
            line = raw_lines[self.current_line]

            if not line.strip() or line.strip().startswith("#"):
                self.current_line += 1
                continue

            current_indent = get_indent(line)
            stripped_line = line.strip()

            if stripped_line.endswith(":"):
                token = stripped_line[:-1].strip()

                if token.startswith("if "):
                    condition = token.replace("if ", "")

                    if eval(condition, self.context, self.context):
                        self.if_stack = [x for x in self.if_stack if x[0] < current_indent]
                        self.if_stack.append((current_indent, True))
                        self.current_line += 1
                    else:
                        self.if_stack = [x for x in self.if_stack if x[0] < current_indent]
                        self.if_stack.append((current_indent, False))
                        self.current_line += 1

                        while self.current_line < len(raw_lines):
                            next_line = raw_lines[self.current_line]
                            if not next_line.strip() or next_line.strip().startswith("#"):
                                self.current_line += 1
                                continue
                            if get_indent(next_line) > current_indent:
                                self.current_line += 1
                            else:
                                break
                    continue

                elif token == "else":
                    prior_if = [x for x in self.if_stack if x[0] == current_indent]
                    if_was_true = prior_if[-1][1] if prior_if else False

                    if if_was_true:
                        self.current_line += 1
                        while self.current_line < len(raw_lines):
                            next_line = raw_lines[self.current_line]
                            if not next_line.strip() or next_line.strip().startswith("#"):
                                self.current_line += 1
                                continue
                            if get_indent(next_line) > current_indent:
                                self.current_line += 1
                            else:
                                break
                    else:
                        self.current_line += 1
                    continue

            self.current_line += 1
            exec(stripped_line, self.context, self.context)

            if self.just_restarted:
                self.just_restarted = False
                break

            if current_time < self.sleep_until:
                break

        if self.current_line >= len(raw_lines):
            self.current_line = 0


def start():
    engine = Engine(int(init_code[0]), int(init_code[1]))

    running = True

    engine.run_init(init_code[2::])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.screen.fill((30, 30, 30))

        engine.run_loop(loop_code)

        for text in engine.text.values():
            font = pygame.font.SysFont(None, text["size"])
            text_surface = font.render(text["message"], True, text["color"])
            engine.screen.blit(text_surface, (text["x"], text["y"]))

        for box in engine.game_objects.values():
            pygame.draw.rect(engine.screen, box["color"], box["rect"])

        pygame.display.flip()

        engine.clock.tick(60)

    pygame.display.quit()

if __name__ == '__main__':
    with open("code\\init.txt", "r", encoding="utf-8") as file:
        init_code = file.read().splitlines()
    with open("code\\loop.txt", "r", encoding="utf-8") as file:
        loop_code = file.read().splitlines()
    start()