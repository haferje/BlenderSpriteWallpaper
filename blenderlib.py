
import bpy
import math

# clear all objects in the scene
def clear_scene():
	#unselect everything
	bpy.ops.object.select_all(action='DESELECT')

	# gather list of items of interest
	candidates = [item.name for item in bpy.data.objects]# if item.type == "MESH"]

	# select only them
	for name in candidates:
		bpy.data.objects[name].select = True

	# remove all selected
	bpy.ops.object.delete()

	# remove the meshes, they have no users anymore
	for item in bpy.data.meshes:
		bpy.data.meshes.remove(item)

	bpy.context.screen.scene = bpy.data.scenes[0]
	bpy.data.scenes[0].name = "Scene"

def camera_look_at(eye=(-60,0,60), rotation_angle=-30):
	fov = 45.0

	# create a camera
	bpy.ops.object.add(type='CAMERA', location=eye, rotation=(0,0,0))
	camera = bpy.context.active_object

	# set the scene's default camera
	bpy.data.scenes["Scene"].camera = camera

	# set camera FOV in radians
	camera.data.angle = fov*(math.pi/180.0) # horizontal
	
	# add an empty object to track with the camera
	bpy.ops.object.add(location=(0,0,0))
	empty = bpy.context.active_object

	# add camera constraint to track empty object
	bpy.ops.object.select_pattern(pattern=camera.name, extend=False)
	bpy.ops.object.select_pattern(pattern=empty.name, extend=True)
	bpy.context.scene.objects.active = camera
	bpy.ops.object.constraint_add_with_targets(type='TRACK_TO')
	constraint = camera.constraints[-1]
	constraint.track_axis = 'TRACK_NEGATIVE_Z'
	constraint.up_axis = 'UP_X'
	
	revolve_camera_by_fraction_of_circle(camera, rotation_angle/360, 'Y')
	
	return camera

# http://blenderartists.org/forum/archive/index.php/t-232542.html
def revolve_camera_by_fraction_of_circle(camera, fraction, axis='Z'):
	import mathutils
	rotation = mathutils.Matrix.Rotation(fraction * 2.0*math.pi, 4, axis)
	camera.location.rotate(rotation)

# https://github.com/Blender-Brussels/bpy-bge-library/blob/master/scripts/bpy/duplicate_object.py
def duplicate_object(scene, name, original):
    # create new mesh
    mesh = bpy.data.meshes.new(name)
 
    # create new object associated with the mesh
    copy = bpy.data.objects.new(name, mesh)
 
    # copy data block from the old object into the new object
    copy.data = original.data.copy()
    copy.scale = original.scale
    copy.location = original.location
    copy.rotation_euler = original.rotation_euler
 
    # link new object to the given scene and select it
    scene.objects.link(copy)
    copy.select = True
 
    return copy

# retrieve material with existing color, else create a new one
def get_color_material_instance(color=[0.5, 0.5, 0.5, 1]):
	material = None

	for i, item in enumerate(color):
		color[i] = round(item*255)

	name = "Material_r{0}g{1}b{2}".format(*color)

	if name in bpy.data.materials:
		material = bpy.data.materials[name]
	else:
		material = bpy.data.materials.new(name)

	return material

def render_to_file(file_path):
	bpy.data.scenes['Scene'].render.filepath = file_path
	bpy.ops.render.render(write_still=True)

class Grid:
	rows = 0
	cols = 0
	cell_size = 0
	cell_spacing = 0
	top_left_x = 0
	top_left_y = 0

	def __init__(self, cols, rows, cell_size=2, cell_spacing=0):
		self.rows = rows;
		self.cols = cols;
		self.cell_size = cell_size;
		self.cell_spacing = cell_spacing;

		self.set_top_left()

	def set_top_left(self):
		width = self.cell_size + self.cell_spacing
		self.top_left_x = -((self.cols*width - self.cell_spacing - self.cell_size) / 2)
		self.top_left_y = -((self.rows*width - self.cell_spacing - self.cell_size) / 2)

	def get_cube_pos(self, x, y):
		s = self.cell_size + self.cell_spacing
		pos_x = self.top_left_x + y*s
		pos_y = self.top_left_y + x*s
		return (pos_x, pos_y)
