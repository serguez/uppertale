import pygame

def convert_map_image(image_path):
    img = pygame.image.load(image_path)
    width, height = img.get_size()
    map_data = [["" for _ in range(width)] for _ in range(height)]
    
    for y in range(height):
        for x in range(width):
            color = img.get_at((x, y))
            if (color.r, color.g, color.b) == (0, 0, 255):
                map_data[y][x] = "BB"
            elif color.r == 0 and color.g == 255:
                if color.b == 99:
                    map_data[y][x] = "BACK"
                else:
                    map_data[y][x] = f"NEXT_{color.b}"
            elif (color.r, color.g, color.b) == (255, 0, 0):
                map_data[y][x] = "XX"
            elif color.r == 255 and color.b == 255:
                ennemy_number = color.g
                map_data[y][x] = f"EN{ennemy_number}"
            elif color.r == 255 and color.g == 255:
                pnj_number = color.b + 1
                map_data[y][x] = f"Q{pnj_number}"
            elif color.r == 255 and color.g == 165:
                lever_id = color.b
                map_data[y][x] = f"LEVER_{lever_id}"
            elif color.r == 139 and color.g == 69:
                door_id = color.b
                map_data[y][x] = f"DOOR_{door_id}"
    return map_data
