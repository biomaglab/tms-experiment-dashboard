#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nicegui import ui
from nicegui.elements.label import Label
import numpy as np
from matplotlib import pyplot as plt
from dataclasses import dataclass
import csv
import os
import math
import time
from datetime import datetime
import socketio
import threading
from threading import Lock
import queue

# for local testing in Windows (using VS Code, conda venv with Pythin 3.12.2 in tms_dashboard env):
# 1. run relay_server in VSCode terminal using:  
# "python.exe relay_server.py 127.0.0.1 5000"
# 2. in a separate environment, activate the invesalius virtual env (conda activate invesalius) and run InVesalius3 using:  
# "C:/Users/bioma/anaconda3/envs/invesalius/python.exe c:/Users/bioma/Documents/GitHub/invesalius3/app.py --remote-host http://localhost:5000
# 3. run main_nicegui in VSCode terminal using: 
# "C:/Users/bioma/anaconda3/envs/tms_dashboard/python.exe c:/Users/bioma/Documents/GitHub/tms-experiment-dashboard/main_nicegui.py"
# 
# for remote connection in a ubuntu OS:
# using sudo sh ../rede_biomag.sh
# start in terminal with:
# python main_nicegui.py 192.168.200.201 5000
# 

# Define variaveis
global robot_messages
CSV_FILE = 'nice_details.csv'

robot_messages = {'Neuronavigation to Robot: Set target', 'Start navigation', 'Open navigation menu', 'Close Project', 'Project loaded successfully', 'Set image fiducial', 'Reset image fiducials', 'Set robot transformation matrix', 'Set target', 'Tracker fiducials set', 'Set objective', 'Unset target', 'Remove sensors ID', 'Reset tracker fiducials', 'Robot connection status','Reset image fiducials', 'Disconnect tracker', 'Tracker changed', 'From Neuronavigation: Update tracker poses','Coil at target', 'Neuronavigation to Robot: Update displacement to target', 'Trials started', 'Trial triggered', 'Stop navigation'}
textos = ['Project', 'Robot', 'Camera', 'TMS', 'Left Fiducial', 'Nasion', 'Right Fiducial', 'Left Tragus', 'Nose', 'Right Tragus', 'Target', 'Coil', 'Moving', 'Trials', 'Navigation stopped']
labels: dict[str, Label] = {}

@dataclass
class Dashboard():
    def __init__(self):
        # screen features
        self.project_set = False
        self.camera_set = False
        self.robot_set = False
        self.tms_set = False
        self.image_NA_set = False
        self.image_RE_set = False
        self.image_LE_set = False
        self.tracker_NA_set = False
        self.tracker_RE_set = False
        self.tracker_LE_set = False
        self.matrix_set = False
        self.target_set = False
        self.robot_moving = False
        self.at_target = False
        self.trials_started = False
        # navigation pointers
        self.displacement = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.probe_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.head_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.coil_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.target_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64) # to be implemented and or confirmed
        # experiment metadata holders 
        self.experimentName = 'Paired pulse, dual site, bilateral, leftM1-rightPMv'
        self.experiment_description = 'Dual site paired bilateral TMS stimulation, with 2 channel EMG acquisition. 80 trials, 4 experimental conditions, 200 pulses'
        self.start_date = '2025-01-31'
        self.end_date = '2024-02-01'
        self.experiment_details = 'Paired pulse contralateral conditioning. Paradigm with motor mapping totaling 80 trials with 20 pulses/condition. Target muscle: APB. Inter-pulse interval: 7 to 10 s.'
        # stimulation metadata holders 
        self.conditioning_stimulus = 'right ventral premotor cortex (rPMv)' # Conditioning stimulus location
        self.test_stimulus = 'left M1' # Test stimulus location
        self.number_intervals = '30' # Number of intervals
        self.interval_step = '15' # Interval step (ms)
        self.number_trials = '120' # Number of trials
        self.number_conditions = '4' # Number of conditions
        self.trials_conditon = '30' # Trials per condition 
        self.intertrial_interval = '12' # Trials per condition

# Função para gravar no CSV
def gravar_dados():
    agora = datetime.now()
    data_formatada = agora.strftime('%Y-%m-%d %H:%M:%S')
    
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Data atual", eName.label, eDescription.label, sDate.label, eDate.label, eDetails.label, cStim.label, tStim.label,\
                    nInt.label, iSteps.label, nTrials.label, nConditions.label, tConditons.label, itInterval.label])
            writer.writerow([data_formatada, eName.value, eDescription.value, sDate.value, eDate.value, eDetails.value, cStim.value, tStim.value,\
                            nInt.value, iSteps.value, nTrials.value, nConditions.value, tConditons.value, itInterval.value])
        ui.notify('Dados gravados com sucesso!')
    else:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([data_formatada, eName.value, eDescription.value, sDate.value, eDate.value, eDetails.value, cStim.value, tStim.value,\
                            nInt.value, iSteps.value, nTrials.value, nConditions.value, tConditons.value, itInterval.value])
        ui.notify('Dados gravados com sucesso!') 

# Função para definir cor padrão (vermelho p=alido)
def estilo_padrao(bg: str = '#E8F5E9') -> str:
    return (
        f'font-size: 1.5rem; font-weight: 500; padding: 16px; '
        f'background-color: {bg}; width: 100%; text-align: center; color: #000;'
    )

# Função para definir cor específica
def mudar_cor(texto_alvo: str, nova_cor: str):
    #print(f'Trocando cor de "{texto_alvo}" para "{nova_cor}"')
                
    cores = {
        'green': '#CDFFD2',
        'red': '#FFD2CD',
        'blue': '#CDD2FF',
        'grey': '#9E9E9E',
        }

    if texto_alvo in labels:
        cor = cores.get(nova_cor, '#9E9E9E')  # cor padrão se não for válida
        label: Label = labels[texto_alvo]
        label.style(estilo_padrao(cor))
        label.update()

# Função para atualizar dados do dashboard
def update_dashboard():
    mudar_cor("Project", 'red' if dashboard.project_set == False else 'green')
    mudar_cor("Camera", 'red' if dashboard.camera_set == False else 'green')
    mudar_cor("Robot", 'red' if dashboard.robot_set == False else 'green')
    mudar_cor("TMS", 'red' if dashboard.tms_set == False else 'green')
    mudar_cor("Nasion", 'red' if dashboard.image_NA_set == False else 'green')
    mudar_cor("Right Fiducial", 'red' if dashboard.image_RE_set == False else 'green')
    mudar_cor("Left Fiducial", 'red' if dashboard.image_LE_set == False else 'green')
    mudar_cor("Nose", 'red' if dashboard.tracker_NA_set == False else 'green')
    mudar_cor("Right Tragus", 'red' if dashboard.tracker_RE_set == False else 'green')
    mudar_cor("Left Tragus", 'red' if dashboard.tracker_LE_set == False else 'green')
    mudar_cor("Transformation matrix set", 'red' if dashboard.matrix_set == False else 'green')
    mudar_cor("Target", 'red' if dashboard.target_set == False else 'green')
    mudar_cor("Moving", 'red' if dashboard.robot_moving == False else 'green')
    mudar_cor("Coil", 'red' if dashboard.at_target == False else 'green')
    mudar_cor("Trials", 'red' if dashboard.trials_started == False else 'green')

# Classe de conexão ao socket
class RemoteControl:
    
    def __init__(self, remote_host):
        self.__buffer = []
        self.__remote_host = remote_host
        self.__connected = False
        self.__sio = socketio.Client(reconnection_delay_max=5)

        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('to_robot', self.__on_message_receive)

        self.__lock = Lock()

    def __on_connect(self):
        print("Connected to {}".format(self.__remote_host))
        self.__connected = True

    def __on_disconnect(self):
        print("Disconnected")
        self.__connected = False

    def __on_message_receive(self, msg):
        self.__lock.acquire(timeout=1)
        self.__buffer.append(msg)
        self.__lock.release()


    def get_buffer(self):
        self.__lock.acquire(timeout=1)
        res = self.__buffer.copy()
        self.__buffer = []
        self.__lock.release()
        return res

    def connect(self):
        self.__sio.connect(self.__remote_host, wait_timeout = 1)

        while not self.__connected:
            print("Connecting...")
            time.sleep(1.0)

# Função que verifica a mensagem entrante e atualiza variáveis
def get_navigation_status():
    global target_status
    #global fiducial_counter
    global distance_0
    global distance_x
    global distance_y
    global distance_z
    buf = rc1.get_buffer()

    #print(buf)
    if len(buf) == 0:
        pass
    elif any(item in [d['topic'] for d in buf] for item in robot_messages):
        topic = [d['topic'] for d in buf]
        
        for i in range(len(buf)):
            if topic[i] in robot_messages:
                target_status = buf[i]["data"]
                #if topic[i] == "Neuronavigation to Robot: Update displacement to target":
                    #print(topic[i])
                    #print(target_status)
                    #print(buf[i]["data"])
                    #print(buf)

                match topic[i]:
                    case 'Set image fiducial':
                        #target_status = buf[i]["data"]
                        #print(target_status)
                        #print("Nome do fiducial: " + target_status['fiducial_name'] + 
                        #    " Posição x: " + str(target_status['position']))
                        
                        if target_status != "":
                            #_msgs.append(target_status['fiducial_name'])
                            #print(len(_msgs))
                            
                            if str(target_status['position']) == "nan":
                                match target_status['fiducial_name']:
                                    case 'NA':
                                        dashboard.image_NA_set = False
                                    case 'RE':
                                        dashboard.image_RE_set = False
                                    case 'LE':
                                        dashboard.image_LE_set = False
                            else:
                                match target_status['fiducial_name']:
                                    case 'NA':
                                        dashboard.image_NA_set = True
                                    case 'RE':
                                        dashboard.image_RE_set = True
                                    case 'LE':
                                        dashboard.image_LE_set = True
                    case 'Reset image fiducials': # local no código: invesalius/navigation/image.py
                        dashboard.image_NA_set = False
                        dashboard.image_RE_set = False
                        dashboard.image_LE_set = False
                    case 'Project loaded successfully': # local no código: invesalius/control.py
                        dashboard.project_set = True
                    case 'Close Project': # local no código: invesalius/control.py
                        dashboard.project_set = False
                    case 'From Neuronavigation: Update tracker poses': # local no código: invesalius3/invesalius/data/coordinates.py (lines 206 ...)
                        dashboard.probe_location = (target_status['poses'][0][0], target_status['poses'][0][1], target_status['poses'][0][2], np.degrees(target_status['poses'][0][3]), np.degrees(target_status['poses'][0][4]), np.degrees(target_status['poses'][0][5])) # coil
                        dashboard.head_location = (target_status['poses'][1][0], target_status['poses'][1][1], target_status['poses'][1][2],np.degrees(target_status['poses'][1][3]), np.degrees(target_status['poses'][1][4]), np.degrees(target_status['poses'][1][5])) # probe
                        dashboard.coil_location = (target_status['poses'][2][0], target_status['poses'][2][1], target_status['poses'][2][2], np.degrees(target_status['poses'][2][3]), np.degrees(target_status['poses'][2][4]), np.degrees(target_status['poses'][2][5])) # head
                        dashboard.target_location = (target_status['poses'][3][0], target_status['poses'][3][1], target_status['poses'][3][2], np.degrees(target_status['poses'][3][3]), np.degrees(target_status['poses'][3][4]), np.degrees(target_status['poses'][3][5])) # coil
                        #distance = (distance_x + distance_y + distance_z) /3
                        #print("target >>>>>" + str(abs(distance)))
                        #print("target_x >>>>>" + str(abs(distance_x)))
                        #print("target_y >>>>>" + str(abs(distance_y)))
                        #print("target_z >>>>>" + str(abs(distance_z)))
                        dashboard.robot_moving = True
                    case 'Neuronavigation to Robot: Update displacement to target': # local no código: invesalius3/invesalius/data/viewer_volume.py
                        dashboard.displacement = list(map(lambda x: target_status['displacement'][x], range(6)))  # Updates displacement values
                        distance_x = dashboard.displacement[0]
                        distance_y = dashboard.displacement[1]
                        distance_z = dashboard.displacement[2]
                        distance_0 = (distance_x + distance_y + distance_z) /3
                        dashboard.robot_moving = True
                    case 'Tracker changed': #invesalius3/invesalius/gui/task_navigator.py
                        dashboard.camera_set = False
                    case 'Tracker fiducials set': #invesalius3/invesalius/gui/task_navigator.py
                        dashboard.tracker_LE_set = True
                        dashboard.tracker_RE_set = True
                        dashboard.tracker_NA_set = True
                    case 'Reset tracker fiducials': #invesalius3/invesalius/gui/task_navigator.py
                        dashboard.tracker_NA_set = False
                        dashboard.tracker_RE_set = False
                        dashboard.tracker_LE_set = False
                    case 'Open navigation menu':  #invesalius3/invesalius/gui/task_navigator.py
                        # test with "Update object registration" or "Neuronavigation to Robot: Connect to robot" or "Neuronavigation to Robot: Set robot transformation matrix"
                        dashboard.robot_set = True
                        dashboard.matrix_set = True
                    case 'Neuronavigation to Robot: Set target': #invesalius3/invesalius/gui/task_navigator.py or invesalius/navigation/robot.py (ln 201)
                        dashboard.target_location = (target_status['target'][0][3], target_status['target'][1][3], target_status['target'][2][3])
                        print(dashboard.target_location)
                        dashboard.target_set = True
                    case 'Unset target': # invesalius/navigation/robot.py
                        dashboard.target_set = False
                    case 'Start navigation': # invesalius/navigation/robot.py
                        dashboard.robot_moving = True
                    case 'Coil at target': # local no código: invesalius/data/viewer_volume.py
                        if target_status['state'] == True:
                            dashboard.at_target = True
                            dashboard.robot_moving = False
                        else:
                            dashboard.at_target = False
                    case 'Trial triggered':
                        #if target_status['data'] == "True":
                        print (target_status)
                        print (str(dashboard.trials_started))
                        dashboard.trials_started = True
                    case 'Stop navigation': # invesalius/control.py
                        dashboard.robot_moving = False

# Função que busca o status da navegação e atualiza a thread 
def message_nav():
    while True:
        time.sleep(0.5)
        mensagem = get_navigation_status()
        #print(mensagem)
        #if mensagem != None:
        r.put((mensagem))
        update_dashboard()


# start

dashboard = Dashboard()  # Inicializa o dashboard em variável local
rc1 = RemoteControl("http://127.0.0.1:5000") # Define a conexão com uma porta local ou servidor
#rc1 = RemoteControl("http://192.168.200.203:5000")
#rc2 = RemoteControl("http://192.168.200.201:5000")
#rc1 = RemoteControl("http://169.254.100.20:5000")
rc1.connect()
#clean buffer
print("Conectado à rede local")

r = queue.Queue() # Define a fila para o threading

threading.Thread(
    target=message_nav,
    daemon=None).start() # Inicia o threading

# Título da página
with ui.row().classes('items-center q-pa-md w-full'):
    ui.image('static/biomag_logo.jpg').classes('w-12 h-12')
    ui.label('Biomag TMS Dashboard').classes('text-h4')

# Detalhes do experimento
with ui.expansion('Experiment details', icon='expand_more'):
    ui.label('Edit the experiment details')

    eName = ui.input('Experiment_name', value = dashboard.experimentName)
    eDescription = ui.input('Experiment_description', value = dashboard.experiment_description)
    sDate = ui.input('Start_date', value = dashboard.start_date)
    eDate = ui.input('End_date', value = dashboard.end_date)
    eDetails = ui.input('Experiment_details', value = dashboard.experiment_details)
    
    ui.button('Save', on_click=gravar_dados)

# Expansor com as principais funções
with ui.expansion('Dashboard Main Functions', icon='expand_more'):
    
    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Connections')
        two = ui.tab('Transformation')
        three = ui.tab('Control')
        four = ui.tab('Navigation')
        five = ui.tab('Stimulation')
        six = ui.tab('Info')

    with ui.tab_panels(tabs, value=two).classes('w-full'):
        with ui.tab_panel(one):
            with ui.splitter(horizontal=False, value=50, limits=[20, 100]).classes('w-full') as splitter:
                with splitter.before:
                    ui.image('static/computer_icon.jpg').classes('w-18 h-18')
                    label = ui.label('Project').style(estilo_padrao('#FFFFFF'))
                    labels['Project'] = label
                    ui.image('static/robot_icon.jpg').classes('w-18 h-18')
                    label = ui.label('Robot').style(estilo_padrao('#FFFFFF'))
                    labels['Robot'] = label
                with splitter.after:
                    ui.image('static/cam_icon.jpg').classes('w-18 h-18 full-height')
                    label = ui.label('Camera').style(estilo_padrao('#FFFFFF'))
                    labels['Camera'] = label
                    ui.image('static/TMS_icon.jpg').classes('w-18 h-18')
                    label = ui.label('TMS').style(estilo_padrao('#FFFFFF'))
                    labels['TMS'] = label

        with ui.tab_panel(two):
            ui.label('Image fiducials')
            with ui.row().classes('w-full no-wrap'):
                
                # Coluna da esquerda
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    label = ui.label('Left Fiducial').style(estilo_padrao('#FFFFFF'))
                    labels['Left Fiducial'] = label

                # Coluna do meio
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 60%; height: 300px'):
                    label = ui.label('Nasion').style(estilo_padrao('#FFFFFF'))
                    labels['Nasion'] = label
                    ui.image('static/head.jpg').classes('rounded')

                # Coluna da direita
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    label = ui.label('Right Fiducial').style(estilo_padrao('#FFFFFFFFCDD2'))
                    labels['Right Fiducial'] = label
            
            ui.label('Real world landmarks')
            with ui.row().classes('w-full'):
                
                # Coluna da esquerda
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    label = ui.label('Left Tragus').style(estilo_padrao('#FFFFFF'))
                    labels['Left Tragus'] = label

                # Coluna do meio
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 60%; height: 300px'):
                    label = ui.label('Nose').style(estilo_padrao('#FFFFFF'))
                    labels['Nose'] = label
                    ui.image('static/head.jpg').classes('rounded')

                # Coluna da direita
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    label = ui.label('Right Tragus').style(estilo_padrao('#FFFFFF'))
                    labels['Right Tragus'] = label

        with ui.tab_panel(three):
            ui.label('Robot control')
            with ui.splitter(horizontal=False, value=50, limits=[20, 100]).classes('w-full') as splitter:
                with splitter.before:
                    ui.image('static/target_icon.jpg').classes('w-18 h-18')
                    label = ui.label('Target').style(estilo_padrao('#FFFFFF'))
                    labels['Target'] = label
                    ui.image('static/coil_icon.jpg').classes('w-18 h-18')
                    label = ui.label('Coil').style(estilo_padrao('#FFFFFF'))
                    labels['Coil'] = label
                with splitter.after:
                    ui.image('static/move_icon.jpg').classes('w-18 h-18 full-height')
                    label = ui.label('Moving').style(estilo_padrao('#FFFFFF'))
                    labels['Moving'] = label
                    ui.image('static/trials_icon.jpg').classes('w-18 h-18')
                    label = ui.label('Trials').style(estilo_padrao('#FFFFFF'))
                    labels['Trials'] = label

        with ui.tab_panel(four):
            ui.label('Ongoing navigation')
            with ui.splitter() as splitter:
                with splitter.before:
                    # inclui uma cena 3D para representação do alvo e da bobina
                    class CoordinateSystem(ui.scene.group):

                        def __init__(self, name: str, *, length: float = 1.0, model_path: str = None) -> None:
                            super().__init__()

                            with self:
                                for label, color, rx, ry, rz in [
                                    ('x', '#ff0000', 0, 0, -math.pi / 2),
                                    ('y', '#00ff00', 0, 0, 0),
                                    ('z', '#0000ff', math.pi / 2, 0, 0),
                                ]:
                                    with ui.scene.group().rotate(rx, ry, rz):
                                        ui.scene.cylinder(0.02 * length, 0.02 * length, 0.8 * length) \
                                            .move(y=0.4 * length).material(color)
                                        ui.scene.cylinder(0, 0.1 * length, 0.2 * length) \
                                            .move(y=0.9 * length).material(color)
                                        ui.scene.text(label, style=f'color: {color}') \
                                            .move(y=1.1 * length)
                                ui.scene.text(name, style='color: #808080')
                            
                    with ui.scene().classes('w-full h-64') as scene:
                        scene.axes_helper()
                        origin = CoordinateSystem('Target')
                        custom_frame = CoordinateSystem('TMS coil')

                    # Timer que atualiza o frame 3D a cada 0.05s
                    def update_frame():
                        # Deslocamento linear (x, y, z)
                        distance_x = dashboard.displacement[0]
                        distance_y = dashboard.displacement[1]
                        distance_z = dashboard.displacement[2]

                        # Deslocamento angular (rx, ry, rz) em radianos
                        rotation_x = dashboard.displacement[3]
                        rotation_y = dashboard.displacement[4]
                        rotation_z = dashboard.displacement[5]

                        custom_frame.move(distance_x, distance_y, distance_z)
                        custom_frame.rotate(rotation_x, rotation_y, rotation_z)

                    ui.timer(0.05, update_frame) # atualiza as coordenadas dos gizmos no gráfico 3D

                with splitter.after:
                    line_plot = ui.line_plot(n=3, limit=20, figsize=(4, 3), update_every=5) \
                        .with_legend(['X', 'Y', 'Z'], loc='upper center', ncol=3)

                    def update_line_plot() -> None:
                        now = datetime.now()
                        x = now.timestamp()
                        if dashboard.robot_moving != True:
                            y1 = math.sin(x)*10
                            y2 = math.cos(x)*10
                            y3 = math.tan(x)*10
                        else:
                            y1 = dashboard.displacement[0] /5
                            y2 = dashboard.displacement[1] /5
                            y3 = dashboard.displacement[2] /5

                        line_plot.push([now], [[y1], [y2], [y3]], y_limits=(-10, 10))

                    line_updates = ui.timer(0.05, update_line_plot, active=False)
                    line_checkbox = ui.checkbox('active').bind_value(line_updates, 'active')


                    with ui.scene().classes('w-full h-64') as scene:
                        '''scene.axes_helper()
                        scene.sphere().material('#4488ff').move(2, 2)
                        scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)
                        scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(2, -1)

                        with scene.group().move(z=2):
                            scene.box().move(x=2)
                            scene.box().move(y=2).rotate(0.25, 0.5, 0.75)
                            scene.box(wireframe=True).material('#888888').move(x=2, y=2)

                        scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')
                        scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, 0, 0]).material('#008800')'''

                        logo = 'https://avatars.githubusercontent.com/u/2843826'
                        scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],
                                            [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -3)

                        probe_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/stylus.stl'
                        probe = scene.stl(probe_url).scale(0.02).move(-2, -3, 0.5)

                        head_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/head.stl'
                        head = scene.stl(head_url).scale(0.02).move(-3, 4, 1).rotate(1.57, 0, 0)

                        coil_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/magstim_fig8_coil.stl'
                        coil = scene.stl(coil_url).scale(0.02).move(-2, -3, 0.5)

                        target_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/aim.stl'
                        target = scene.stl(target_url).scale(0.2).move(-2, -3, 0.5)

                        #scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)
                        scene.text3d('TMS setup', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)

                        #ui.timer(0.05, lambda: head.move(distance_x, distance_y, distance_z))

                                            # Timer que atualiza o frame 3D a cada 0.05s
                    def update_positions():
                        # Posição dos objetos (x, y, z)
                        probe_position = dashboard.probe_location[:3]
                        head_position = dashboard.head_location[:3]
                        #print(head_position)
                        coil_position = dashboard.coil_location[:3]
                        target_position = dashboard.target_location[:3]

                        # Rotação dos objetos (rx, ry, rz) em radianos
                        probe_rotation = dashboard.probe_location[3:]
                        head_rotation = dashboard.head_location[3:]
                        #print(head_rotation)
                        coil_rotation = dashboard.coil_location[3:]

                        probe.move(int(probe_position[0]), int(probe_position[1]), int(probe_position[2]))
                        probe.rotate(int(probe_rotation[0]), int(probe_rotation[1]), int(probe_rotation[2]))
                        head.move(int(head_position[0]), int(head_position[1]), int(head_position[2]))
                        head.rotate(int(head_rotation[0]), int(head_position[1]), int(head_position[2]))
                        coil.move(int(dashboard.displacement[0]), int(dashboard.displacement[1]),int(dashboard.displacement[2]))
                        coil.rotate(int(dashboard.displacement[3]), int(dashboard.displacement[4]), int(dashboard.displacement[5]))
                        target.move(int(target_position[0]), int(target_position[1]),int(target_position[2]))

                    ui.timer(0.1, update_positions) # atualiza as posições e rotações dos objetos no gráfico 3D

        with ui.tab_panel(five):
            ui.label('Stimulation setup')
            cStim = ui.input('Conditioning stimulus (%)', value = dashboard.conditioning_stimulus)
            tStim = ui.input('Test stimulus (%)', value = dashboard.test_stimulus)
            nInt = ui.input('Number of intervals', value = dashboard.number_intervals).props('type=number')
            iSteps = ui.input('Interval step (ms)', value = dashboard.interval_step)
            nTrials = ui.input('Number of trials', value = dashboard.number_trials)
            nConditions = ui.input('Number of conditions', value = dashboard.number_conditions)             
            tConditons = ui.input('Trials per condition', value = dashboard.trials_conditon)
            itInterval = ui.input('Inter_trial_interval (ms)', value = dashboard.intertrial_interval)
            ui.button('Gravar', on_click=gravar_dados, icon='save')
        
        with ui.tab_panel(six):
            ui.label('Stimulation info')

            ui.button('Computer → verde', on_click=lambda: mudar_cor('Computer', 'green'))
            ui.button('Robot → verde', on_click=lambda: mudar_cor('Robot', 'green'))
            ui.button('Camera → verde', on_click=lambda: mudar_cor('Nose', 'green'))
            ui.button('Texto C → azul', on_click=lambda: mudar_cor('Left Tragus', 'blue'))
ui.fullscreen()
ui.run(port=8084)

update_dashboard()
#ui.run(reload=False)