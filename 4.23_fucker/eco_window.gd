extends PopupPanel

var country_name = ""

func popup_info(info_text: String, image: Texture = null) -> void:
	$Label.text = info_text

	popup_centered()

func _http_request_completed(result, response_code, headers, body):
	var json = JSON.new()
	var error = json.parse(body.get_string_from_utf8())
	
	if error == OK:
		#print(json.data)
		pass
	else:
		print("JSON Parse Error: ", json.get_error_message(), " at line ", json.get_error_line())
		print(body.get_string_from_utf8())
	
	var response = json.get_data()
	print(response)
	
	var my_plot = $Eco_Graph.add_plot_item("My Plot", Color.GREEN, 1.0)
	for x in range(response.size()):
		my_plot.add_point(Vector2(x, response[x]))


func query_gdp_data(country: String):
	var http_request = HTTPRequest.new()
	
	var dict: Dictionary = {
		"country": country,
		"item": "GDP"
	}
	var json = JSON.stringify(dict)
	var headers = ["Content-Type: application/json"]
	
	add_child(http_request)
	http_request.request_completed.connect(self._http_request_completed)
	
	var error = http_request.request("http://127.0.0.1:5000/get_time_series", headers, HTTPClient.METHOD_GET, json)
	if error != OK:
		push_error("An error occurred in the HTTP request.")

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	hide()
	
	#var node_internal_gov = get_node("../Internal_gov")
	#var country_name = node_internal_gov.received_country_name
	# placeholder china for now
	if (country_name != ""):
		query_gdp_data(country_name)
	
func _process(delta: float) -> void:
	var node_internal_gov = get_node("../Internal_gov")
	
	if (country_name == "" && node_internal_gov.received_country_name != ""):
		country_name = node_internal_gov.received_country_name
		query_gdp_data(country_name)
