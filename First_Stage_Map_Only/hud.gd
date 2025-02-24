extends CanvasLayer

func _ready():
	# Optional: set initial text
	$Top_Infos/InfoBox1/DataLabel1.text = "Loading..."
	$Top_Infos/InfoBox2/DataLabel2.text = "Loading..."
	$Top_Infos/InfoBox3/DataLabel3.text = "Loading..."

func _process(delta: float) -> void:
	# Example: updating each box with different info
	var data_a = Time.get_ticks_msec() / 1000.0
	var data_b = 12345  # Some other value
	var data_c = 11342

	$Top_Infos/InfoBox1/DataLabel1.text = "Time: " + str(data_a)
	$Top_Infos/InfoBox2/DataLabel2.text = "Political Power: " + str(data_b)
	$Top_Infos/InfoBox3/DataLabel3.text = "Usable: " + str(data_c)
