import datetime
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import obspy
from evento import Evento

def get_color(tipo):
    '''
    Devuelve el color del marcado según el tipo de evento
    :param tipo:
    :return: el color en formato string interpretable para la matplotlib
    '''

    color = "k" #negro
    if tipo ==  "Der":
        color = "orange" #naranja
    elif tipo ==  "EXP":
        color = "m" # magenta
    elif tipo ==  "SIL":
        color = "b" #azul
    elif tipo == "VT":
        color = "r" #rojo
    elif tipo == "LP":
        color = "y" #amarillo
    elif tipo == "Pul": #todo preguntar por la minusuculas de este
        color = "C" #cyan
    elif tipo == "TH":
        color =  "g" #verde
    return color

def ploteo(archivo_configuracion):

    #Genera el helicorder normal
    traza = 0
    lista_archivos = glob.glob("data/*.sac")

    for archivo in lista_archivos:
        if traza == 0:
            traza = obspy.read(archivo)
        else:
            traza += obspy.read(archivo)


    #Devuelve una figura del helicorder de la hora actual, para manipularlo con la matplotlib
    helicorder = traza.plot(type="dayplot", color=['b'], handle=True, interval=60,
                            one_tick_per_line=True,number_of_ticks=7)
    plt.Figure = helicorder
    lineas = plt.gca().get_lines()

    #calculos para el mapeo entre puntos y segundos
    segundos_por_hora = 3600
    puntos_por_linea = len(lineas[0].get_xdata())
    puntos_por_segundo  =  puntos_por_linea  / segundos_por_hora #
    puntos_por_minuto = puntos_por_segundo * 60

    eventos = open(archivo_configuracion)
    eventos.readline() #Bota el encabezado
    eventos.readline()  # Bota el encabezado
    #Recorre el archivo de configuración mlf y obtiene los eventos
    for linea in eventos:

        if linea[0] == ".":
            break

        l = linea.split()
        evento = Evento(int(l[0])//10000, int(l[1])//10000,l[2])

        punto_inicial = datetime.datetime(day=9,month=9,year=2017)
        punto_inicial += datetime.timedelta(seconds=evento.get_tiempo_inicial())


        punto_final = datetime.datetime(day=9,month=9,year=2017)
        punto_final += datetime.timedelta(seconds=evento.get_tiempo_final())

        #calcula la duracion en segundos
        duracion = evento.get_tiempo_final()-evento.get_tiempo_inicial()

        #fixme ¿Que pasa si evento empieza a las xx:59:59?

        linea_actual = lineas[punto_inicial.hour]
        color = get_color(evento.get_tipo())
        #Muestra el evento en el helicorder


        indice_inicio = round(punto_inicial.minute * puntos_por_minuto  + punto_inicial.second * puntos_por_segundo)
        indice_final = round(punto_final.minute * puntos_por_minuto + punto_final.second * puntos_por_segundo)

        plt.plot(linea_actual.get_xdata()[indice_inicio:indice_final],
                 linea_actual.get_ydata()[indice_inicio:indice_final], color=color)
    
    #Guarda los cambios realizados
    plt.legend(handles=[mpatches.Patch(color='red', label='SIL'),
                        mpatches.Patch(color='gold', label='LPG'),
                        mpatches.Patch(color='olivedrab', label='LPF'),
                        mpatches.Patch(color='blue', label='HFL'),
                        mpatches.Patch(color='m', label='VLP'),
                        mpatches.Patch(color='coral', label='TOR'),
                        mpatches.Patch(color='orange', label='VTP'),
                        mpatches.Patch(color='lawngreen', label='VTD'),
                        mpatches.Patch(color='c', label='TEH'),
                        mpatches.Patch(color='dodgerblue', label='TES'),
                        mpatches.Patch(color='green', label='NAR'),
                        mpatches.Patch(color='violet', label='LFS'),
                        mpatches.Patch(color='teal', label='REG'),
                        mpatches.Patch(color='indigo', label='DRB')],
               bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
                              
    plt.show()
    plt.close()


ploteo("data/popo_20170509.recog.mlf")

