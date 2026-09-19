time — переменная, хранит текущее время раунда в миллисекундах (начинается с 0).
creat_box(name, x, y, width, height, color, type) — создать прямоугольник (type="static" или "dynamic").
deleted_box(name) — удалить объект по имени.
exists_box(name) — проверить, жив ли объект (возвращает True/False).
move(name, x, y) — сдвинуть объект на дельту (включает физику увлечения/столкновения).
change_size(name, x, y) - изменить размер на дельту (без физики!).
move_to(name, width, height) — телепортировать объект в точные координаты (без физики!).
сhange_size_to(name, width, height) - Изменить размер (без физики!).
check_collision(name1, name2) — проверка столкновения двух объектов (True/False).
creat_text(name, message, x, y, size, color) — вывести текст на экран.
exists_text(name) — проверить существование текста.
wait(ms) — приостановить выполнение кода в файле на ms миллисекунд (не фризит экран!).
key_pressed(char) — зажата ли клавиша ('w', 'a', 's', 'd', 'space', 'up', 'down').
play_sound(path) — воспроизвести аудиофайл (кэшируется автоматически).
restart() — полностью сбросить игру, стереть объекты и начать раунд с 0 мс.
get_x(name), get_y(name), get_width(name), get_height(name) — получить параметры бокса.