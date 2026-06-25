from model.modello import Model

mymdl = Model()

mymdl.creaG(1996, "circle")
print(mymdl.get())

nodi, archi = mymdl.get()
print(f"Grafo creato! Il grafo ha {nodi} nodi e {archi} archi")
