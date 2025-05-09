extends CanvasLayer

func _ready():
	# Optional: set initial text
	$Top_Infos/Climate/Climate/BotInfo.text = "Loading..."
	$Top_Infos/Climate/Climate/TopInfo.text = "Loading..."
	
	$Top_Infos/GDP/GDP/TopInfo.text = "Loading..."
	$Top_Infos/GDP/GDP/BotInfo.text = "Loading..."
	
	$Top_Infos/Money/Money/BotInfo.text = "Loading..."
	$Top_Infos/Money/Money/TopInfo.text = "Loading..."
	
	$Top_Infos/PolPower/PolPower/BotInfo.text = "Loading..."
	$Top_Infos/PolPower/PolPower/TopInfo.text = "Loading..."
	
	$Top_Infos/Next_Round/Label.text = "Loading..."
	$VBoxContainer/Panel2/Label.text = "Pick your country"
	
	
	$Top_Infos/Next_Round.connect("pressed", Callable(self, "_on_Next_round_Button_pressed"))
	
	var file_path = "res://Country_File.txt"
	var file = FileAccess.open(file_path, FileAccess.READ)
	var content = file.get_as_text()
	var countries = content.split(",")
	
	var vbox = $VBoxContainer/Panel/ScrollContainer/Country_List
	
	for i in range(countries.size()):
		var button = Button.new()
		button.text = countries[i]
		button.custom_minimum_size = Vector2(100,75)
		button.pressed.connect(Callable(self, "_on_country_button_pressed").bind(countries[i]))
		vbox.add_child(button)
		print("Add country " + str(countries[i]))
	

func _process(delta: float) -> void:
	var data_a = Time.get_ticks_msec() / 1000.0
	var data_b = 12345  # Some other value
	var data_c = 113429
	var GDP = 100
	
	$Top_Infos/Climate/Climate/BotInfo.text = "  Bot Climate: " + str(1001)
	$Top_Infos/Climate/Climate/TopInfo.text = "  Top Climate: " + str(1000) 
	
	$Top_Infos/GDP/GDP/TopInfo.text = "  Top GDP: " + str(1000)
	$Top_Infos/GDP/GDP/BotInfo.text = "  Bot GDP: " + str(1001)
	
	$Top_Infos/Money/Money/BotInfo.text = "  Bot Money: " + str(1001)
	$Top_Infos/Money/Money/TopInfo.text = "  Top Money: " + str(1000)
	
	$Top_Infos/PolPower/PolPower/BotInfo.text = " Bot Political Power: " + str(1001)
	$Top_Infos/PolPower/PolPower/TopInfo.text = " Top Political Power: " + str(1000)
	
	$Top_Infos/Next_Round/Label.text = "Click for \nnext Round"
	
	
func _on_country_button_pressed(country: String) -> void:
	var node_Internal_gov = get_node("../Internal_gov")
	node_Internal_gov.received_country_name = country
	print("Button pressed for country: %s" % country)
	$VBoxContainer.hide()
	#$PopupPanel/VBoxContainer/Country_Name.text = country
	#$PopupPanel.popup_centered()
