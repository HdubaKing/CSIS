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
	
