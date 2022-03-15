import xmltodict
import json
import pygame

# Get tilesets.
def load_tileset(filepath):
    with open(filepath, 'r', encoding='utf-8') as tileset_file:
        tileset_xml = tileset_file.read()
        tileset_json = xmltodict.parse(tileset_xml)
        tileset_dict = json.loads(json.dumps(tileset_json))["tileset"]

        tileset_offset = (int(tileset_dict["tileoffset"]["@x"]), int(tileset_dict["tileoffset"]["@y"]))
        if tileset_offset[1] == 0:
            tileset_offset = (tileset_offset[0], 14)
        
        tiles_size = (int(tileset_dict["@tilewidth"]), int(tileset_dict["@tileheight"]))
        tileset_image_path = tileset_dict["image"]["@source"]
        
        print(f'Loaded tileset: {tileset_dict["@name"]}.')

        tileset_image = pygame.image.load(tileset_image_path).convert()
        print(f'Loaded tileset image: {tileset_image_path} ({tileset_image.get_size()[0]}x{tileset_image.get_size()[1]}).')
        
        return tileset_image, tiles_size, tileset_offset

def split_tileset_image(chunk_size, tileset_image, targets):
    tileset_image_size = tileset_image.get_size()
    
    tiles = []
    for tile_index in range(0, int((tileset_image_size[0]/chunk_size[0]) * (tileset_image_size[1]/chunk_size[1]))):
        if tile_index in targets:
            tile_index = int(tile_index)
            tile_pos = (tile_index % int(tileset_image_size[0]/chunk_size[0]) - 1, tile_index // int(tileset_image_size[0]/chunk_size[0]))
            if (tile_pos[0] < 0):
                tiles.append(None)
                continue
            if tile_pos[1] * chunk_size[1] > tileset_image_size[1]:
                raise IndexError(f'Tile index {tile_index} is not in the tileset image.')
            else:
                tile_rect = pygame.Rect(tile_pos[0] * chunk_size[0], tile_pos[1] * chunk_size[1], chunk_size[0], chunk_size[1])
                tile_image = tileset_image.subsurface(tile_rect).convert()
                tile_image.set_colorkey((0, 0, 0))
                tiles.append(tile_image)
        else:
            tiles.append(None)

    return tiles
        