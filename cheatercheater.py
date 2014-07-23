import random

old_shuffle = random.shuffle

def cheat_shuffle(x, *args, **kwargs):
	"Cheat wrapper for random.shuffle to let me peek at the 5 upcoming cards."
	old_shuffle(x, *args, **kwargs)
	print("Upcoming cards: {}".format(",".join(x[-10:])))
	
random.shuffle = cheat_shuffle

import blackjackfoura
blackjackfoura.playgame()