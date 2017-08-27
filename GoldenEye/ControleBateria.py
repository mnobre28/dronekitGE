#!/usr/bin/python2
# coding: utf-8
"""Classe que controla a Bateria"""

class ControleBateria:
    def __init__(self):
        self._bateriaMim

    def get_bateriaMin(self):
        return self._bateria

    def set_bateriaMin(self, bateria):
        self._bateria = bateria

    def reabastecer(self):
        pass#implementar

    def modoEconomico(self):
        pass#implementar