import json
import os
import shutil

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Caminante:
	def toJSON(self):
		if(self.orientacion != None):
			shutil.copy(os.path.join(__location__, 'caminante.txt'), os.path.join(__location__, 'caminantePass.txt'))
		with open(os.path.join(__location__, 'caminante.txt'), 'w', encoding='utf-8') as f:
			f.write(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))
		return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
	def __init__(self, orientacion, pos_x, pos_y,fin_x,fin_y):
		self.orientacion = orientacion #N,S,E,W
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.fin_x = fin_x
		self.fin_y = fin_y

	def __repr__(self):
		return "<Caminante Orientacion: %s Pos_x: %s Pos_y :%s fin_x: %s fin_y:%s>" % (self.orientacion, self.pos_x, self.pos_y, self.fin_x, self.fin_y)

	def __str__(self):
		return "<Caminante Orientacion: %s Pos_x: %s Pos_y: %s fin_x: %s fin_y:%s>" % (self.orientacion, self.pos_x, self.pos_y, self.fin_x, self.fin_y)
