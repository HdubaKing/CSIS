extends PopupPanel


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Hide by default so it doesn't appear on scene load.
	hide()

	# Connect the CloseButton's "pressed" signal to this script.
	$VBoxContainer/CloseButton.connect("pressed", Callable(self, "_on_CloseButton_pressed"))

# Call this function from anywhere to display the popup with info_text and an optional image.
func popup_info(info_text: String, image: Texture = null) -> void:
	$VBoxContainer/InfoLabel.text = info_text


	# Show the popup in the center of the window
	popup_centered()


func _on_CloseButton_pressed() -> void:
	hide()
	

func _process(delta: float) -> void:
	$VBoxContainer/China/Label.text = "China"
	$VBoxContainer/US/Label.text = "US"
	$VBoxContainer/India/Label.text = "India"
