extends Panel

# This function is called every frame
func _process(delta: float) -> void:
	# Replace this with your internal calculation.
	var some_data = Time.get_ticks_msec() / 1000.0  # Example: seconds elapsed
	# Update the label text.
	$DataLabel.text = "Time in seconds: " + str(some_data)
