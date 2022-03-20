from tools import HiddenPrints
with HiddenPrints():
	import pygame
	from pygame.locals import *
import isometric
from pytmx.util_pygame import load_pygame
import pytmx
import entity
import math
del HiddenPrints

# Setup pygame stuff
print('Successfully initialized %s pygame modules, %s failed.' % (pygame.init()))
fps = 60
clock = pygame.time.Clock()
width, height = 900, 900
pygame.display.set_caption('game')
screen = pygame.display.set_mode((width, height),  pygame.RESIZABLE)
display = pygame.Surface((height / 3, height / 3))
debug_font = pygame.font.SysFont('Arial', 30)

offset = (150, 150)
falling = False

# Load map
filename = 'example.tmx'
tmxdata = load_pygame(filename)
print(f'Loaded map: {tmxdata.filename}\n - Tile size: {tmxdata.tilewidth}x{tmxdata.tileheight}\n - Map size: {tmxdata.width}x{tmxdata.height} \n - Map version: {tmxdata.version}\n - Tiled version: {tmxdata.tiledversion}')

# Load entities
entity_count = 0
entity_manager = entity.EntityManager()
for z, layer in enumerate(tmxdata.layers):
	if isinstance(layer, pytmx.TiledObjectGroup):
		for obj in layer:
			entity_manager.add_entity(entity.Entity((obj.x + 5) / 10, obj.y/10, (layer.offsety * -1 / 14) + 1, obj))
			entity_count += 1
print(f'Loaded {entity_count} entit{"y" if entity_count == 1 else "ies"}.')
del entity_count

# Game loop.
print('Starting game loop.')
while True:
	display.fill((0, 0, 0))

	max = (0, 0)
	colliders = []
	layer_tot = 0

	for task in entity_manager.get_outside_tiles(0, 0, max[0], max[1], 0, layer_tot):
		display.blit(task.image, isometric.isometric(task.x, task.y, task.z, offset[0], offset[1]))

	for z, layer in enumerate(tmxdata.layers):
		if isinstance(layer, pytmx.TiledTileLayer):
			layer_tot += 1
			colliders.append([])
			for y, row in enumerate(layer.data):
				for x, tile in enumerate(row):
					max = (x, y)
				
					tile = tmxdata.get_tile_image(x, y, z)

					# Draws all entities that rendering order matters to.
					tasks = entity_manager.get_tasks(x, y, z)
					if len(tasks) > 0:
						for task in tasks:
							display.blit(task.image, isometric.isometric(task.x, task.y, task.z, offset[0], offset[1]))

					if tile != None:
						display.blit(tile, isometric.isometric(x, y, z, offset[0], offset[1]), (0, 0, 20, 24))

						collider = tmxdata.get_tile_properties(x, y, z)["colliders"][0]
						if collider.type is not None:
							colliders[z].append((x, y))
							colliders[z].append(collider.type)

	for event in pygame.event.get():
		if event.type == QUIT: # Quit routine.
			pygame.quit()
			quit()
		elif event.type == pygame.WINDOWRESIZED: # If window is resized, resize the display surface.
			width, height = pygame.display.get_surface().get_size()
			display = pygame.Surface((height / 3, height / 3))
		
	# Temporary movement system
	keys = pygame.key.get_pressed()

	player_index = 0
	speed = 10

	player = entity_manager.entities[player_index]
	progress = (player.x - int(player.x), player.y - int(player.y))
	try:
		player_collision_layer = colliders[math.floor(player.z)]
	except IndexError:
		player_collision_layer = []
	if True in list(keys) and not falling:
		if keys[pygame.K_LEFT]:
			target = (math.floor(player.x - speed * delta_time), math.floor(player.y))
			if target not in player_collision_layer:
				player.x -= speed * delta_time
			else:
				target_type = player_collision_layer[player_collision_layer.index(target) + 1]
				if target_type == 'solid':
					pass
				elif target_type == 'stairs_east':
					# player.x -= speed * delta_time
					# player.z = math.floor(player.z) + (1 - progress[0]) + 0.1
					pass
		if keys[pygame.K_RIGHT]:
			target = (math.floor(player.x + speed * delta_time), math.floor(player.y))
			if target not in player_collision_layer:
				player.x += speed * delta_time
			else:
				target_type = player_collision_layer[player_collision_layer.index(target) + 1]
				if target_type == 'solid':
					pass
				elif target_type == 'stairs_west':
					# player.x += speed * delta_time
					# player.z = math.floor(player.z) + (1 - progress[0]) + 0.1
					pass
		if keys[pygame.K_UP]:
			target = (math.floor(player.x), math.floor(player.y - speed * delta_time))
			if target not in player_collision_layer:
				player.y -= speed * delta_time
			else:
				target_type = player_collision_layer[player_collision_layer.index(target) + 1]
				if target_type == 'solid':
					pass
				elif target_type == 'stairs_north':
				# 	player.y -= speed * delta_time
				# 	player.z = math.floor(player.z) + (1 - progress[1]) + 0.1
					pass
		if keys[pygame.K_DOWN]:
			target = (math.floor(player.x), math.floor(player.y + speed * delta_time))
			if target not in player_collision_layer:
				player.y += speed * delta_time
			else:
				target_type = player_collision_layer[player_collision_layer.index(target) + 1]
				if target_type == 'solid':
					pass
				elif target_type == 'stairs_south':
				# 	player.y += speed * delta_time
				# 	player.z = math.floor(player.z) + (1 - progress[1]) + 0.1
					pass

		entity_manager.entities[player_index] = player

	target = (math.floor(player.x), math.floor(player.y))
	try:
		player_collision_layer = colliders[math.floor(player.z - 1)]
	except IndexError:
		player_collision_layer = []
	if target not in player_collision_layer:
		falling = True
		player.z -= 3 * delta_time
	else:
		falling = False

	# Transform the screen so game content is always the same size, then update.
	screen.blit(pygame.transform.scale(display, (height, height)), (0, 0))

	fps_surface = debug_font.render(f'Fps: {int(clock.get_fps())}', False, (255, 255, 255))
	screen.blit(fps_surface, (0, 0))

	pygame.display.update()
	delta_time = clock.tick(fps) / 1000
