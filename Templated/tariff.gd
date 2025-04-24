extends PopupPanel

func _ready() -> void:
	hide()


func popup_info(info_text: String, image: Texture = null) -> void:
	$ListCountries_Bars/HBoxContainer/InfoLabel.text = info_text

	popup_centered()


func _process(delta: float) -> void:
	var value1 = 0
	var value2 = 0
	$ListCountries_Bars/China_box/China.text = "China"
	$ListCountries_Bars/India_box/India.text = "India"
