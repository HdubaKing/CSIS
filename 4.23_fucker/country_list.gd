extends PopupPanel

# Called when the node enters the scene tree for the first time.
func _http_request_completed(result, response_code, headers, body):
	var json = JSON.new()
	var error = json.parse( body.get_string_from_utf8())
	
	if error == OK:
		#print(json.data)
		pass
	else:
		print(body.get_string_from_utf8())
		print("JSON Parse Error: ", json.get_error_message(), " at line ", json.get_error_line())
		
	var countries = json.get_data()
	#print(countries)
	var vbox = $ScrollContainer/VBoxContainer
	
	for i in range(countries.size()):
		var button = Button.new()
		button.text = countries[i]
		button.custom_minimum_size = Vector2(100,75)
		button.pressed.connect(Callable(self, "_on_country_button_pressed").bind(countries[i]))
		vbox.add_child(button)
	

func update_country_names():
	var http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(self._http_request_completed)
	
	var error = http_request.request("http://127.0.0.1:5000/get_country_list")
	if error != OK:
		push_error("An error occured in the HTTP request")

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	# Hide by default so it doesn't appear on scene load.
	hide()
	update_country_names()

	
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
	
