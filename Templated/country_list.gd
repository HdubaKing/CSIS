extends PopupPanel


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Hide by default so it doesn't appear on scene load.
	hide()
	var file_path = "res://Country_File.txt"
	var file = FileAccess.open(file_path, FileAccess.READ)
	var content = file.get_as_text()
	var countries = content.split(",")
	
	var vbox = $ScrollContainer/VBoxContainer
	
	for i in range(countries.size()):
		var button = Button.new()
		button.text = countries[i]
		button.custom_minimum_size = Vector2(100,75)
		button.pressed.connect(Callable(self, "_on_country_button_pressed").bind(countries[i]))
		vbox.add_child(button)
	
# Call this function from anywhere to display the popup with info_text and an optional image.
func popup_info(info_text: String, image: Texture = null) -> void:
	$ScrollContainer/VBoxContainer/InfoLabel.text = info_text

	popup_centered()


#func _on_CloseButton_pressed() -> void:
#	hide()
	
func _on_country_button_pressed(country: String) -> void:
	print("Button pressed for country: %s" % country)
	$PopupPanel/VBoxContainer/Country_Name.text = country
	$PopupPanel.popup_centered()

# func _process(delta: float) -> void:
	
