extends Node2D

var file_path = "res://provinces-nodes.txt"
var province_scene = preload("res://Province.tscn")

# Dictionary to hold shapeid -> country name mapping
var country_attributes: Dictionary = {}

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var file = FileAccess.open(file_path, FileAccess.READ)
	var polygons = {}
	
	while not file.eof_reached():
		var line = file.get_line()
		var parts = line.split(",")
		var shapeid = 0
		var partid = 0
		if parts.size() < 4:
			continue
		shapeid = parts[0].to_int()
		partid = parts[1].to_int()
		var x = parts[2].to_float()
		var y = parts[3].to_float()
		
		if not polygons.has(shapeid):
			polygons[shapeid] = []
		while polygons[shapeid].size() <= partid:
			polygons[shapeid].append([])
		polygons[shapeid][partid].append(Vector2(x, -y))
	
	for shapeid in polygons.keys():
		create_shape(shapeid, polygons[shapeid])
	
	load_country_attributes()

func create_shape(shapeid, parts):
	var shape_area = province_scene.instantiate()
	shape_area.name = str(shapeid)
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
	
	
# Try to Get region country name by calling back to csv file
func load_country_attributes() -> void:
	# Open the file (make sure the path is correct)
	var file = FileAccess.open("res://provinces-attributes.txt", FileAccess.READ)
	if file:
		# Read header line and split by commas
		var header = file.get_line().split(",")
		# Find the column indexes. 
		# (Assuming the first column is shapeid and one column is "NAME")
		var shapeid_index = 0  # or: header.find("shapeid")
		var name_index = header.find("NAME")
		if name_index == -1:
			push_error("Could not find 'NAME' column in attributes file!")
			return

		# Read the file line by line
		while not file.eof_reached():
			var line = file.get_line().strip_edges()
			if line == "":
				continue  # Skip empty lines
			var parts = line.split(",")
			# Get the shapeid and the country name from the correct columns
			var shapeid = parts[shapeid_index]
			var country_name = parts[name_index]
			country_attributes[shapeid] = country_name
		file.close()
	else:
		push_error("Failed to open province-attribute.txt!")

# Call this function when a region is clicked
func get_country_name(shapeid: String) -> String:
	return country_attributes.get(shapeid, "Unknown")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
