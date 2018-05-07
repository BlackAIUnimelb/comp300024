class Player():
	def __init__(self, colour):
		self.cnt = 0;
		self.movingPhase = True;
		return;


	def action(self, turns):
		self.cnt = self.cnt + 1;
		if (self.cnt > 12):
			self.movingPhase = False;

		paction = None;
		if self.movingPhase:
			pos = input("Placing Phase Black Player:");
			# tmplist = ();
			pos = pos.split();
			a = int(float(pos[0]));
			b = int(float(pos[1]));
			paction = (a ,b);
		else:
			pos = input("Moving Phase Black Player:");
			# tmplist = ();
			pos = pos.split();
			a = int(float(pos[0]));
			b = int(float(pos[1]));
			c = int(float(pos[2]));
			d = int(float(pos[3]));
			paction = ((a ,b), (c, d));
		return paction;


	def update(self, actions):

		return;