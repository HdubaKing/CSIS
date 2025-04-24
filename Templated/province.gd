extends Area2D

# Add a variable to store the country's name
var country_name: String = ""
var file_path = "res://Countries_Info.txt"
# Stores as Name, GDP, Usable Money, Power, Population
var country_info_list: Dictionary = {}

@onready var Country_Info = get_tree().get_root().get_node("Node2D/Country_Info")
@onready var Country_name = get_tree().get_root().get_node("Node2D/Country_Info/VBoxContainer/Label")
@onready var Country_GDP = get_tree().get_root().get_node("Node2D/Country_Info/VBoxContainer/Info_box1/GDP")
@onready var Country_Money = get_tree().get_root().get_node("Node2D/Country_Info/VBoxContainer/Info_box1/Money")
@onready var Country_Power = get_tree().get_root().get_node("Node2D/Country_Info/VBoxContainer/Info_box2/Power")
@onready var Country_Population = get_tree().get_root().get_node("Node2D/Country_Info/VBoxContainer/Info_box2/Population")

func _ready() -> void:
	pass

func _process(delta: float) -> void:
	pass

func load_province_attributes(file_path: String) -> void:
	if FileAccess.file_exists(file_path):
		var file: FileAccess = FileAccess.open(file_path, FileAccess.READ)
		while not file.eof_reached():
			var line = file.get_line()
			var parts = line.split(",")
		# Skip any line that doesn't have enough columns
			if parts.size() < 4:
				continue
			country_info_list[parts[0]] = [parts[1],parts[2],parts[3],parts[4]]
			print("Info stored: " + str(country_info_list[parts[0]][2] ))
		file.close()
	else:
		print("File not found: ", file_path)


func _on_input_event(viewport: Node, event: InputEvent, shape_idx: int) -> void:
	# Handle left-click: highlight the province in red
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		for node in get_parent().get_children():
			if node is Area2D:
				for subnode in node.get_children():
					if subnode is Polygon2D:
						subnode.modulate = Color(1,1,1,0)
		for subnode in self.get_children():
			if subnode is Polygon2D:
				subnode.modulate = Color(1,0,0,0.7)
	
	# Handle right-click: highlight and print the country's name
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
		for node in get_parent().get_children():
			if node is Area2D:
				for subnode in node.get_children():
					if subnode is Polygon2D:
						subnode.modulate = Color(1,1,1,0)
		for subnode in self.get_children():
			if subnode is Polygon2D:
				subnode.modulate = Color(0.392157, 0.584314, 0.929412, 1)
		
		load_province_attributes(file_path)
		# Print out the country's name (stored in this node)
		# print("Country: %s" % country_name)
		Country_name.text = country_name
		
		
		
		Country_GDP.text = "Country GDP: " + str(country_info_list[country_name][0])
		Country_Money.text = "Country Money: " + str(country_info_list[country_name][1])
		Country_Power.text = "Country Power: " + str(country_info_list[country_name][2])
		Country_Population.text = "Country Population: " + str(country_info_list[country_name][3])
		
		Country_Info.popup_centered()
		
		
