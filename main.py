import PySimpleGUI as sg
import matplotlib
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from mwclass import MosquitoWithWolbachia       #model
import weatherapi                               #temperature data api, calls two years historical temperature data from today's date

sg.SetOptions(background_color='white',text_element_background_color='white',font=('arial',15))
#blank graphs to show before selecting location:
dayslist=np.linspace(0,999,1000)         
blanklist=[None]*1000
plt.figure(figsize=(15,10))
plt.subplot(3, 2, 2)
plt.plot(dayslist,blanklist)
plt.title("Graph 2: Infected Human")
plt.subplot(3,2,4)
plt.plot(dayslist,blanklist)
plt.title("Infected Mosquito")
            
plt.subplot(3, 2, 1)
plt.plot(dayslist,blanklist)
plt.title("Graph 1: Infected Human")
plt.subplot(3,2,3)
plt.plot(dayslist,blanklist)
plt.title("Infected Mosquito")
plt.subplot(3,1,3)
plt.plot(dayslist,blanklist)
plt.title("Temperature")
plt.ylabel("Celsius")

plt.tight_layout(pad=2)
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
fig = plt.gcf()  
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
#the GUI layout, each list is a line on the program. 
layout = [     [sg.Text('Select the Location:'),
                sg.Combo(['Select Below:','Salt Lake City, UT','Bangkok, Thailand','Los Angeles, CA','Casablanca, Morocco','London, England'], key='location'),
                sg.Text('  ',size=(5,1)),
                sg.Text('Percentage for Graph 1:'),
                sg.Input(key='inputwolpercent1',size=(3,1)),
                sg.Text('Percentage for Graph 2:'),
                sg.Input(key='inputwolpercent2',size=(3,1)),
                sg.Text('   ',size=(6,1)),
                sg.Button('Run')
               ],
           [sg.Canvas(key='canvas')]]
# create the form and show it without the plot
window = sg.Window('Mosquito Disease Model', layout, finalize=True,size=(1024,768))
# add the plot to the window
fig_agg = draw_figure(window['canvas'].TKCanvas, fig)
v=[] #event actions dictionary
while True:  # Event Loop
    event, values = window.Read()
    print(event, values)
    v=values
    if event is None or event == 'Exit':
        break
    if (event=='Run'):
        if v['location']!='Select Below:' and len(v['inputwolpercent1'])!=0 and len(v['inputwolpercent2'])!=0:
            fig_agg.get_tk_widget().forget()

            wolbachiapercentage1=int(v['inputwolpercent1'])
            wolbachiapercentage2=int(v['inputwolpercent2'])
            if v['location']=='Salt Lake City, UT':
                tempdata=weatherapi.calltemp('72572')
            elif v['location']=='Bangkok, Thailand':
                tempdata=weatherapi.calltemp('48455')
            elif v['location']=='Los Angeles, CA':
                tempdata=weatherapi.calltemp('72295')
            elif v['location']=='Casablanca, Morocco':
                tempdata=weatherapi.calltemp('60155')
            elif v['location']=='London, England':
                tempdata=weatherapi.calltemp('03772')
            mosquitoModel=MosquitoWithWolbachia(tempdata,wolbachiapercentage1)
            days,dayslist=mosquitoModel.getDaysList()
            mosquitoModel.runModel()
            infectedhumans1,infectedmosquitoes1,aquaticwmosquitoes1,susceptiblewmosquitoes1,tempdata1=mosquitoModel.getQuickModel()

            mosquitoModel=MosquitoWithWolbachia(tempdata,wolbachiapercentage2)
            days,dayslist=mosquitoModel.getDaysList()
            mosquitoModel.runModel()
            infectedhumans2,infectedmosquitoes2,aquaticwmosquitoes2,susceptiblewmosquitoes2,tempdata2=mosquitoModel.getQuickModel()

            plt.figure(figsize=(15,10))
            plt.subplot(3, 2, 2)
            plt.plot(dayslist,infectedhumans2)
            plt.title("Graph 2: Infected Human")
            plt.subplot(3,2,4)
            plt.plot(dayslist,infectedmosquitoes2)
            plt.title("Infected Mosquito")
            
            plt.subplot(3, 2, 1)
            plt.plot(dayslist,infectedhumans1)
            plt.title("Graph 1: Infected Human")
            plt.subplot(3,2,3)
            plt.plot(dayslist,infectedmosquitoes1)
            plt.title("Infected Mosquito")
            plt.subplot(3,1,3)
            plt.plot(dayslist,tempdata2)
            plt.title("Temperature")
            plt.ylabel("Celsius")
            plt.tight_layout(pad=3)
            def draw_figure_nw(canvas, figure, loc=(0, 0)):
                figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
                figure_canvas_agg.draw()
                figure_canvas_agg.get_tk_widget().pack(side='top', fill='both')
                return figure_canvas_agg
            fig = plt.gcf()  
            figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
            fig_agg = draw_figure_nw(window['canvas'].TKCanvas, fig)
        else:
            fig_agg.get_tk_widget().forget()
window.Close()
