#!/usr/bin/python
import bpy
import os
import sys
import math

# user-configurable settings
config = {
	# location of this file
	"current_directory": "/home/jason/Dropbox/code/blender/sprite_wallpaper",
	# location of sprite file, relative to current_directory
	"sprite_file": "images/mario/mario_01.png",
	# color to exclude when rendering the sprite (r,g,b) or (r,g,b,a)
	"exclude_color": (1.0, 1.0, 1.0),
	# your monitor's resolution size
	"resolution_width": 1680,
	"resolution_height": 1050,
	# rendering clarity [1,100]
	"resolution_percentage": 100,
    # rendered background color (r,g,b)
    "background_color": (0.051, 0.051, 0.051),
    # extra padding around the sprite - percentage of the sprite height
    "padding_percentage": 20,
    # rotation angle of the camera around the sprite [-180,180] (- left, + right)
    "camera_offset_angle": -30,
}


# add current directory to the system path so we can import the helper library
sys.path.append(config["current_directory"])
import blenderlib

# start fresh
blenderlib.clear_scene()
scene = bpy.data.scenes["Scene"]

# add a hemisphere to light all objects evenly
bpy.ops.object.lamp_add(type='HEMI', location=(0,0,6))

# load image from local sprite file
image_path = os.path.join(config["current_directory"], config["sprite_file"])
image = bpy.data.images.load(image_path)
image_width, image_height = image.size

# convert pixel array to list
pixels = list(image.pixels)
pixels_length = len(pixels)
pixels = [pixels[i:i+4] for i in range(pixels_length)[::4]]

# add initial cube to center of screen
bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
cube = bpy.context.active_object

# subdivide cube and smooth the edges
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.subdivide(number_cuts=25, smoothness=0, quadtri=True, quadcorner='STRAIGHT_CUT')
bpy.ops.mesh.vertices_smooth(repeat=5)
bpy.ops.object.editmode_toggle()

# for each pixel in the image, duplicate the initial cube and apply material coloring
grid = blenderlib.Grid(image_width, image_height)
for y in range(image_height):
	for x in range(image_width):
		r, g, b, a = pixels[image_width*y + x]
		
		# don't render fully-transparent pixels or exclude color
		if a == 0 or (r,g,b,a)[0:len(config["exclude_color"])] == config["exclude_color"]:
			continue

		cube_x, cube_y = grid.get_cube_pos(y, x)

		# duplicate cube
		cube_duplicate = blenderlib.duplicate_object(scene, "Cube", cube)

		# set properties on new cube
		cube_duplicate.location = (cube_x, cube_y, 0)
		cube_duplicate.color = (r,g,b,a)
		
		# add material to color the cube
		material_duplicate = blenderlib.get_color_material_instance([r,g,b,a])
		material_duplicate.diffuse_color = cube_duplicate.color[0:3]
		material_duplicate.diffuse_intensity = 1.0
		material_duplicate.use_object_color = True
		cube_duplicate.active_material = material_duplicate

# calculate camera rotation and distance from the scene
fov = 45.0
half_vert_fov_radians = 2*math.atan(math.tan(math.radians(fov/2)/2)*(config["resolution_height"]/config["resolution_width"]))
## half the height of the image with padding
toa_opposite = (image_height + (image_height * (config["padding_percentage"]/100))) / 2
toa_adjacent = toa_opposite / math.tan(half_vert_fov_radians)
## best distance to get the padding we want
camera_distance = toa_adjacent * (grid.cell_size+grid.cell_spacing)
## make sure the clipping volume is big enough to include the sprite rotated at 90 degrees
camera_clip_distance = camera_distance + ((image_width/2) * (grid.cell_size+grid.cell_spacing))

# point camera and set its rendering volume
camera = blenderlib.camera_look_at((0,0,camera_distance), config["camera_offset_angle"])
camera = bpy.data.cameras["Camera"]
bpy.context.object.data.clip_end = camera_clip_distance

# deselect all objects in the scene, then remove original cube from the scene
bpy.ops.object.select_all(action='DESELECT')
cube.select = True
bpy.ops.object.delete()

# set render properties
bpy.context.scene.world.horizon_color = config["background_color"]
scene.render.resolution_x = config["resolution_width"]
scene.render.resolution_y = config["resolution_height"]
scene.render.resolution_percentage = config["resolution_percentage"]

# render with sprite's filename, appended with "_render"
root, ext = os.path.splitext(image_path)
blenderlib.render_to_file("{0}_render.png".format(root))
