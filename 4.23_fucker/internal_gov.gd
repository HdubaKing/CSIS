extends PopupPanel

var received_country_name: String = ""
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Hide by default so it doesn't appear on scene load.
	hide()

	# Connect the CloseButton's "pressed" signal to this script.
	$VBoxContainer/CloseButton.connect("pressed", Callable(self, "_on_CloseButton_pressed"))
	$VBoxContainer/Option_Button_List_1/Button/Label.text = "Switch Focus\nTo Economy"
	$VBoxContainer/Option_Button_List_1/Button2/Label.text = "Switch Focus\nTo Political Power"
	$VBoxContainer/Option_Button_List_2/Button/Label.text = "Internal Policy\nAdjustment"
	$VBoxContainer/Option_Button_List_2/Button2/Label.text = "Display Overall\nInformation"

# Call this function from anywhere to display the popup with info_text and an optional image.
func popup_info(info_text: String, image: Texture = null) -> void:
	$VBoxContainer/InfoLabel.text = received_country_name
	image = load("")
	
	if image != null:
		$VBoxContainer/HBoxContainer/TextureRect.texture = image
	else:
		$VBoxContainer/HBoxContainer/TextureRect.texture = null  # or keep existing

	# Show the popup in the center of the window
	popup_centered()


func _on_CloseButton_pressed() -> void:
	hide()
