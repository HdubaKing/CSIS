extends PopupPanel

func popup_info(info_text: String, image: Texture = null) -> void:
	$Label.text = info_text

	popup_centered()


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	hide()
	var my_plot = $Environ_Graph.add_plot_item("My Plot", Color.GREEN, 1.0)
	for x in range(0, 11, 1):
		var y = randf_range(0, 1)
		my_plot.add_point(Vector2(x, y))


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
