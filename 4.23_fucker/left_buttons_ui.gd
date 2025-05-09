extends CanvasLayer

func _ready():
	# Make sure we seed the random number generator.
	randomize()
	
	# Connect each button's pressed signal to a unique callback.
	# Adjust the node paths as needed if your names differ.
	$ButtonsContainer/Button1.connect("pressed", Callable(self, "_on_Button1_pressed"))
	$ButtonsContainer/Button2.connect("pressed", Callable(self, "_on_Button2_pressed"))
	$ButtonsContainer/Button3.connect("pressed", Callable(self, "_on_Button3_pressed"))
	$ButtonsContainer/Eco_Button.connect("pressed", Callable(self, "_on_Eco_Button_pressed"))
	$ButtonsContainer/Environ_Button.connect("pressed", Callable(self, "_on_Environ_Button_pressed"))
	
	
	
func _process(delta: float) -> void:
	$ButtonsContainer/Button1/Label.text = "Internal \nGovernment"
	$ButtonsContainer/Button2/Label.text = "International \nDiplomacy"
	$ButtonsContainer/Button3/Label.text = "Tariff"
	$ButtonsContainer/Eco_Button/Label.text = "Economy"
	$ButtonsContainer/Environ_Button/Label.text = "Environment"


func _on_Button1_pressed():
	var text = "Internal Government Setting"
	# Climb up one level to the parent, then down to Internal_gov
	get_parent().get_node("Internal_gov").popup_info(text)

func _on_Button2_pressed():
	var text = "Country List"
	get_parent().get_node("Country_List").popup_info(text)

func _on_Button3_pressed():
	var text = "Tariff"
	get_parent().get_node("Tariff").popup_info(text)
	
func _on_Eco_Button_pressed():
	var text = "Eco"
	get_parent().get_node("Eco_Window").popup_info(text)
	
func _on_Environ_Button_pressed():
	var text = "Environment"
	get_parent().get_node("Environ_Window").popup_info(text)
