extends Node2D

var file_path = "res://provinces-nodes.txt"
var province_scene = preload("res://Province.tscn")

# Global array to hold each province's attribute row.
# Each row is an Array, where the 5th element (index 4) is the country's name.
var province_attributes: Array = []

func load_province_attributes(file_path: String) -> void:
	if FileAccess.file_exists(file_path):
		var file: FileAccess = FileAccess.open(file_path, FileAccess.READ)
		var i = 0
		while not file.eof_reached():
			var line = file.get_line()
			var parts = line.split(",")
		# Skip any line that doesn't have enough columns
			if parts.size() < 4:
				continue
			province_attributes.append([parts[0],parts[4]])
		file.close()
		province_attributes.pop_front()
	else:
		print("File not found: ", file_path)

func _ready() -> void:
	var file = FileAccess.open(file_path, FileAccess.READ)
	var polygons = {}
	load_province_attributes("res://provinces-attributes.txt")
	
	while not file.eof_reached():
		var line = file.get_line()
		var parts = line.split(",")
		# Skip any line that doesn't have enough columns
		if parts.size() < 4:
			continue
		var shapeid = parts[0].to_int()
		var partid = parts[1].to_int()
		var x = parts[2].to_float()
		var y = parts[3].to_float()
		
		if not polygons.has(shapeid):
			polygons[shapeid] = []
		while polygons[shapeid].size() <= partid:
			polygons[shapeid].append([])
		polygons[shapeid][partid].append(Vector2(x, -y))
	file.close()
	
	# Create the province nodes
	for shapeid in polygons.keys():
		create_shape(shapeid, polygons[shapeid])
	
	# Load the province attributes AFTER processing the nodes so they can be assigned

func create_shape(shapeid: int, parts) -> void:
	var shape_area = province_scene.instantiate()
	shape_area.name = str(shapeid)
	for attr in province_attributes:
		if attr[0].to_int() == shapeid:
			shape_area.country_name = attr[1]  # the 5th element is the country's name
			break
	
	add_child(shape_area)
	for partid in range(parts.size()):
		var polygon_points = parts[partid]
		create_part(shape_area, partid, polygon_points)

func create_part(parent_node, partid, points):
	var unique_points = points.duplicate()
	
	var polygon = Polygon2D.new()
	polygon.polygon = unique_points
	polygon.name = str(partid)
	polygon.modulate = Color(0,0,0,0)
	
	var collision_polygon = CollisionPolygon2D.new()
	collision_polygon.polygon = unique_points
	collision_polygon.name = str(partid)
	
	var line = Line2D.new()
	line.points = unique_points
	line.name = str(partid)
	line.modulate = Color(0,0,0,0.5)
	line.width = 0.5
	line.closed = true
	
	parent_node.add_child(polygon)
	parent_node.add_child(collision_polygon)
	parent_node.add_child(line)
