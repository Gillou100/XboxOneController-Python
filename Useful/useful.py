#!/usr/bin/env python3
# -*-coding:utf-8 -*


def scaleChange(x0, xMin0, xMax0, xMin1, xMax1):
	return xMin1 + (((x0 - xMin0) * (xMax1 - xMin1)) / (xMax0 - xMin0))


def control(value, minimaLow, minimaHigh, middle):
	if value > min(minimaHigh, minimaLow) and value < max(minimaHigh, minimaLow):
		return middle
	return value


if __name__ == '__main__':
	pass
