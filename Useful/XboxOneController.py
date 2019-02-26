#!/usr/bin/env python3
# -*-coding:utf-8 -*


from time import sleep
from copy import deepcopy
import sys
from threading import Thread, RLock
from Useful.OrderedDictionary import OrderedDictionary
from Useful.useful import scaleChange
try:
	from inputs import get_gamepad
except ImportError as e:
	print("""You must install the "inputs" library, using "python3 -m pip install inputs" before using this programm""")
	print("""If pip is not installed for python3, use "sudo apt-get install python3-pip", then "python3 -m pip install --upgrade pip", and, finally, use the abose command""")
	sys.exit(0)


class XboxOneController(Thread):
	"""This class represent a Xbox One controller"""
	# A dictionnary which contains values of extreme position for each analog buttons
	_lastMaximas = {
		"SL": {
			"U": -32768,
			"D": 32767,
			"L": -32768,
			"R": 32767
		},
		"SR": {
			"U": -32768,
			"D": 32767,
			"L": -32768,
			"R": 32767
		},
		"L2": {
			"R": 0,
			"P": 1023
		},
		"R2": {
			"R": 0,
			"P": 1023
		}
	}
	_simpleButtons = {
		"BTN_SOUTH": "A",
		"BTN_EAST": "B",
		"BTN_NORTH": "X",
		"BTN_WEST": "Y",

		"BTN_TL": "L1",
		"BTN_TR": "R1",

		"BTN_THUMBL": "L3",
		"BTN_THUMBR": "R3",

		"BTN_START": "Start",
		"BTN_SELECT": "Select",
		"BTN_MODE": "Central"
	}
	_directionalButtons = {
		"ABS_HAT0X": ("L", "R"),
		"ABS_HAT0Y": ("U", "D")
	}
	_analogValues = {
		"ABS_X": ("SL", 0),
		"ABS_Y": ("SL", 1),
		"ABS_RX": ("SR", 0),
		"ABS_RY": ("SR", 1),
		"ABS_Z": ("L2", 2),
		"ABS_RZ": ("R2", 2)
	}

	def __init__(self, SLU = 100, SLD = -100, SLL = -100, SLR = 100, SRU = 100, SRD = -100, SRL = -100, SRR = 100, LR = 0, LP = 100, RR = 0, RP = 100):
		"""This is the constructor. Each analog values can be personnalised but they are % by default:
			SLU -> value given by the left joystick when he is on the top
			SLD -> value given by the left joystick when he is on the bottom
			SLL -> value given by the left joystick when he is on the left
			SLR -> value given by the left joystick when he is on the right

			SRU -> value given by the right joystick when he is on the top
			SRD -> value given by the right joystick when he is on the bottom
			SRL -> value given by the right joystick when he is on the left
			SRR -> value given by the right joystick when he is on the right

			LR -> value given by 

			LR -> valeur donnée lorsque la gachette gauche (L2) est relâchée
			LP -> valeur donnée lorsque la gachette gauche (L2) est enfoncée

			RR -> valeur donnée lorsque la gachette droite (R2) est relâchée
			RP -> valeur donnée lorsque la gachette droite (R2) est enfoncée
		"""
		Thread.__init__(self)
		# a lock to modifie the state of the controller's buttons
		self._lock = RLock()
		self._running = False
		self._newMaximas = {
			"SL": {
				"U": SLU,
				"D": SLD,
				"L": SLL,
				"R": SLR
			},
			"SR": {
				"U": SRU,
				"D": SRD,
				"L": SRL,
				"R": SRR
			},
			"L2": {
				"R": LR,
				"P": LP
			},
			"R2": {
				"R": RR,
				"P": RP
			}
		}
		self._virtualController = OrderedDictionary()
		self._virtualController["A"] = False
		self._virtualController["B"] = False
		self._virtualController["X"] = False
		self._virtualController["Y"] = False

		self._virtualController["U"] = False
		self._virtualController["D"] = False
		self._virtualController["L"] = False
		self._virtualController["R"] = False

		self._virtualController["L1"] = False
		self._virtualController["L2"] = self._newMaximas["L2"]["R"]
		self._virtualController["L3"] = False
		self._virtualController["R1"] = False
		self._virtualController["R2"] = self._newMaximas["R2"]["R"]
		self._virtualController["R3"] = False

		self._virtualController["SL"] = [(self._newMaximas["SL"]["L"] + self._newMaximas["SL"]["R"])/2, (self._newMaximas["SL"]["U"] + self._newMaximas["SL"]["D"])/2]
		self._virtualController["SR"] = [(self._newMaximas["SR"]["L"] + self._newMaximas["SR"]["R"])/2, (self._newMaximas["SR"]["U"] + self._newMaximas["SR"]["D"])/2]

		self._virtualController["Start"] = False
		self._virtualController["Select"] = False
		self._virtualController["Central"] = False

	def __repr__(self):
		"""Méthode qui modifie la façon dont l'objet est affiché quand on tape directement son nom"""
		string = ""
		for key, value in self._virtualController.items():
			string += str(key) + " : " + str(value) + "\n"
		return string

	def __str__(self):
		"""Méthode appelée pour la conversion en str de l'objet"""
		return repr(self)

	def __getattr__(self, nom_attr):
		"""Méthode appelée lorsque le programme tente d'accéder à un attribut qui n'existe pas."""
		print("Attention ! L'attribut", nom_attr, "n'existe pas pour les objets de la classe XboxOneRemote")
	def __delattr__(self, nom_attr):
		"""Méthode permettant d'empêcher la suppression des attributs de la classe."""
		raise TypeError("'XboxOneRemote' object does not support item deletion")

	def __getitem__(self, index):
		"""Méthode permettant de récupérer les états de la mannette en utilisant l'objet comme étant la variable _virutalController."""
		return deepcopy(self._virtualController[index])
	def __setitem__(self, index, valeur):
		"""Méthode permettant d'empêcher un programme externe de modifier les états de la mannette."""
		raise TypeError("'XboxOneRemote' object does not support state assignment")
	def __delitem__(self, index):
		"""Méthode permettant d'empêcher un programme externe de supprimer les états de la mannette."""
		raise TypeError("'XboxOneRemote' object does not support state deletion")

	def __contains__(self, val):
		"""Méthode permettant d'utiliser le mot-clé in sur un objet de la classe, renvoie vers la même méthode sur le dictionnaire _virtualController."""
		return self._virtualController.__contains__(val)
	def __len__(self):
		"""Méthode permettant d'utiliser le mot-clé len sur un objet de la classe, renvoie vers la même méthode sur le dictionnaire _virtualController."""
		return self._virtualController.__len__()

	def _setattr(self, nom_attr, val_attr):
		"""Méthode permettant d'empêcher la modification des attributs de la classe."""
		raise TypeError("'XboxOneRemote' object does not support item assignment")
	def _getNewMaximas(self):
		return deepcopy(self._newMaximas)
	newMaximas = property(_getNewMaximas, _setattr, __delattr__)
	def _getVirtualController(self):
		return deepcopy(self._virtualController)
	virtualController = property(_getVirtualController, _setattr, __delattr__)
	def _getLastMaximas(self):
		return deepcopy(self._lastMaximas)
	lastMaximas = property(_getLastMaximas, _setattr, __delattr__)
	def _getSimpleButtons(self):
		return deepcopy(self._simpleButtons)
	simpleButtons = property(_getSimpleButtons, _setattr, __delattr__)
	def _getDirectionalButtons(self):
		return deepcopy(self._directionalButtons)
	directionalButtons = property(_getDirectionalButtons, _setattr, __delattr__)
	def _getAnalogValues(self):
		return deepcopy(self._analogValues)
	analogValues = property(_getAnalogValues, _setattr, __delattr__)

	def _listenController(self):
		events = get_gamepad()
		with self._lock:
			for event in events:
				for key, value in self._simpleButtons.items():
					if(event.code == key):
						self._virtualController[value] = bool(event.state)
						break
				for key, value in self._directionalButtons.items():
					if(event.code == key):
						for i in range(len(value)):
							self._virtualController[value[i]] = (False, False, True)[i + event.state]
						break
				for key, value in self._analogValues.items():
					if(event.code == key):
						if(value[1] != 2):
							self._virtualController[value[0]][value[1]] = scaleChange(event.state, self._lastMaximas[value[0]][("L", "D")[value[1]]], self._lastMaximas[value[0]][("R", "U")[value[1]]], self._newMaximas[value[0]][("L", "D")[value[1]]], self._newMaximas[value[0]][("R", "U")[value[1]]])
						else:
							self._virtualController[value[0]] = scaleChange(event.state, self._lastMaximas[value[0]]["R"], self._lastMaximas[value[0]]["P"], self._newMaximas[value[0]]["R"], self._newMaximas[value[0]]["P"])
						break
	def run(self):
		self._running = True
		while self._running:
			self._listenController()
	def stop(self):
		self._running = False
		self.join()



if __name__ == '__main__':
	pass
	#while(1):
		#events = get_gamepad()
		#for event in events:
			#print(event.code, event.state, event.ev_type)
