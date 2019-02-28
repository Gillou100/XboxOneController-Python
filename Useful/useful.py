#!/usr/bin/env python3
# -*-coding:utf-8 -*


def scaleChange(x, lastXmin, lastXmax, newXmin, newXmax):
	return newXmin + (((x - lastXmin) * (newXmax - newXmin)) / (lastXmax - lastXmin))


def control(value, minima0, minima1, middle):
	if value > min(minima0, minima1) and value < max(minima0, minima1):
		return middle
	return value


if __name__ == '__main__':
	pass
