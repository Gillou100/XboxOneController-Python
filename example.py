#!/usr/bin/env python3
# -*-coding:utf-8 -*


from Useful.XboxOneController import XboxOneController as Controller
from Useful.useful import control
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
			SL = list(controller["SL"])
			SR = list(controller["SR"])

			SL[0] = control(SL[0], middleValueLow, middleValueHigh, middleValue)
			SL[1] = control(SL[1], middleValueLow, middleValueHigh, middleValue)
			SR[0] = control(SR[0], middleValueLow, middleValueHigh, middleValue)
			SR[1] = control(SR[1], middleValueLow, middleValueHigh, middleValue)

			print(SL)
			print(SR)
			print()
			sleep(0.01)
	except KeyboardInterrupt:
		pass
	finally:
		controller.stop()
