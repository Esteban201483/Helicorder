class Evento:

    tiempo_inicial = 0
    tiempo_final = 0
    tipo = ""


    def __init__(self,mi,mf,t):
        self.tiempo_inicial = mi
        self.tiempo_final = mf
        self.tipo = t

    def get_tiempo_inicial(self):
        return self.tiempo_inicial

    def get_tiempo_final(self):
        return self.tiempo_final

    def get_tipo(self):
        return self.tipo

    def imprimir(self):
        print("ti: " + str(self.tiempo_inicial) + ", tf: " + str(self.tiempo_final) + ", tipo: " + str(self.tipo))