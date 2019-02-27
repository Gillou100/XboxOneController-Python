#!/usr/bin/env python3
# -*-coding:utf-8 -*


from Useful.XboxOneController import XboxOneController as Controller
from Useful.useful import control
from copy import deepcopy
from time import sleep


if __name__ == '__main__':
	minValue = -10
	maxValue = 10
	middleValue = 0
	middleValueHigh = 2
	middleValueLow = -2

	try:
		controller = Controller(
			SLU = maxValue,
			SLD = minValue,
			SLL = minValue,
			SLR = maxValue,
			SRU = maxValue,
			SRD = minValue,
			SRL = minValue,
			SRR = maxValue
		)

		controller.start()

		while True:
			SL = deepcopy(controller["SL"])
			SR = deepcopy(controller["SR"])

			SL["H"] = control(SL["H"], middleValueLow, middleValueHigh, middleValue)
			SL["V"] = control(SL["V"], middleValueLow, middleValueHigh, middleValue)
			SR["H"] = control(SR["H"], middleValueLow, middleValueHigh, middleValue)
			SR["V"] = control(SR["V"], middleValueLow, middleValueHigh, middleValue)

			print("SL: ", SL)
			print("SR: ", SR)
			print()
			sleep(0.01)
	except KeyboardInterrupt:
		pass
	finally:
		controller.stop()
