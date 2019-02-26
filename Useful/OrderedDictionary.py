#!/usr/bin/env python3
# -*-coding:utf-8 -*


class OrderedDictionary:
	"""Notre dictionnaire ordonné. L'ordre des données est maintenu et il peut donc, contrairement aux dictionnaires usuels, être trié ou voir l'ordre de ses données inversées"""
	def __init__(self, base={}, **donnees):
		"""Constructeur de notre objet. Il peut ne prendre aucun paramètre (dans ce cas, le dictionnaire sera vide) ou construire un dictionnaire remplis grâce :
			-   au dictionnaire 'base' passé en premier paramètre ;
			-   aux valeurs que l'on retrouve dans 'donnees'."""
		self._cles = [] # Liste contenant nos clés
		self._valeurs = [] # Liste contenant les valeurs correspondant à nos clés

		# On vérifie que 'base' est un dictionnaire exploitable
		if type(base) not in (dict, OrderedDictionary):
			raise TypeError("le type attendu est un dictionnaire (usuel ou ordonne)")
		# On récupère les données de 'base'
		for cle in base.keys():
			self[cle] = base[cle]
		# On récupère les données de 'donnees'
		for cle in donnees.keys():
			self[cle] = donnees[cle]

	def __repr__(self):
		"""Représentation de notre objet. C'est cette chaîne qui sera affichée quand on saisit directement le dictionnaire dans l'interpréteur, ou en utilisant la fonction 'repr'"""
		string = "{"
		for key, value in self._virtualController.items():
			string += str(key) + " : " + str(value) + ", "
		string = string[:-2]
		string += "}"
		return string
	def __str__(self):
		"""Fonction appelée quand on souhaite afficher le dictionnaire grâce à la fonction 'print' ou le convertir en chaîne grâce au constructeur 'str'. On redirige sur __repr__"""
		return repr(self)

	def __len__(self):
		"""Renvoie la taille du dictionnaire"""
		return len(self._cles)
	def __contains__(self, cle):
		"""Renvoie True si la clé est dans la liste des clés, False sinon"""
		return cle in self._cles

	def __getitem__(self, cle):
		"""Renvoie la valeur correspondant à la clé si elle existe, lève une exception KeyError sinon"""
		if cle not in self._cles:
			raise KeyError("La clé {0} ne se trouve pas dans le dictionnaire".format(cle))
		else:
			indice = self._cles.index(cle)
		return self._valeurs[indice]
	def __setitem__(self, cle, valeur):
		"""Méthode spéciale appelée quand on cherche à modifier une cle présente dans le dictionnaire. Si la clé n'est pas présente, on l'ajoute à la fin du dictionnaire"""
		if cle in self._cles:
			indice = self._cles.index(cle)
			self._valeurs[indice] = valeur
		else:
			self._cles.append(cle)
			self._valeurs.append(valeur)
	def __delitem__(self, cle):
		"""Méthode appelée quand on souhaite supprimer une clé"""
		if cle not in self._cles:
			raise KeyError("La clé {0} ne se trouve pas dans le dictionnaire".format(cle))
		else:
			indice = self._cles.index(cle)
			del self._cles[indice]
			del self._valeurs[indice]

	def __iter__(self):
		"""Méthode de parcours de l'objet. On renvoie l'itérateur des clés"""
		return iter(self._cles)
	def items(self):
		"""Renvoie un générateur contenant les couples (cle, valeur)"""
		for i, cle in enumerate(self._cles):
			valeur = self._valeurs[i]
			yield (cle, valeur)
	def keys(self):
		"""Cette méthode renvoie la liste des clés"""
		return list(self._cles)
	def values(self):
		"""Cette méthode renvoie la liste des valeurs"""
		return list(self._valeurs)


if __name__ == '__main__':
	pass
