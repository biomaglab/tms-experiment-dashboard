from nicegui import ui
import numpy as np
from matplotlib import pyplot as plt
import csv
import os
import math

# Define o caminho do arquivo CSV
CSV_FILE = 'nice_details.csv'

# Se o arquivo não existir ainda, cria com cabeçalho
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Nome', 'Email', 'Idade'])

# Função para gravar no CSV
def gravar_dados():
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([cStim.value, tStim.value, nInt.value, iSteps.value, nTrials.value, nConditions.value, tConditons.value, itInterval.value])
    ui.notify('Dados gravados com sucesso!')

with ui.row().classes('items-center q-pa-md'):
    ui.image(r'C:\Users\bioma\Documents\GitHub\tms-experiment-dashboard\images\biomag_logo.jpg').classes('w-12 h-12')
    ui.label('Biomag TMS Dashboard').classes('text-h4')

with ui.expansion('Experiment details', icon='expand_more'):
    ui.label('Edit the experiment details')

    eName = ui.input('Experiment_name', value='Paired pulse, dual site, bilateral, leftM1-rightPMv')
    eDescription = ui.input('Experiment_description', value='Dual site paired bilateral TMS stimulation, with 2 channel EMG acquisition. 80 trials, 4 experimental conditions, 200 pulses')
    sDate = ui.input('Start_date', value='2025-01-31')
    eDate = ui.input('End_date', value='2024-02-01')
    eDetails = ui.input('Experiment_details', value='Paired pulse contralateral conditioning. Paradigm with motor mapping totaling 80 trials with 20 pulses/condition. Target muscle: APB. Inter-pulse interval: 7 to 10 s.')

    ui.button('Save', on_click=gravar_dados)

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
                    ui.label('Computer').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                    ui.image('static/robot_icon.jpg').classes('w-18 h-18')
                    ui.label('Robot').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                with splitter.after:
                    ui.image('static/cam_icon.jpg').classes('w-18 h-18 full-height')
                    ui.label('Camera').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                    ui.image('static/TMS_icon.jpg').classes('w-18 h-18')
                    ui.label('TMS').classes('text-h5 q-pa-md bg-green-1 full-width text-center')

        with ui.tab_panel(two):
            ui.label('Image fiducials')
            with ui.row().classes('w-full no-wrap'):
                
                # Coluna da esquerda
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    ui.label('Left Fiducial').classes('text-h5 q-pa-md bg-green-1 full-width text-center')

                # Coluna do meio
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 60%; height: 300px'):
                    ui.label('Nasion').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                    ui.image('static/head.jpg').classes('rounded')

                # Coluna da direita
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    ui.label('Right Fiducial').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
            
            ui.label('Real world landmarks')
            with ui.row().classes('w-full no-wrap'):
                
                # Coluna da esquerda
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    ui.label(' Left Tragus ').classes('text-h5 q-pa-md bg-green-1 full-width text-center')

                # Coluna do meio
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 60%; height: 300px'):
                    ui.label('Nasion').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                    ui.image('static/head.jpg').classes('rounded')

                # Coluna da direita
                with ui.column().classes('items-center justify-center'):#.style('background-color: lightgreen; width: 20%; height: 300px'):
                    ui.label(' Right Tragus ').classes('text-h5 q-pa-md bg-green-1 full-width text-center')

        with ui.tab_panel(three):
            ui.label('Robot control')
            with ui.splitter(horizontal=False, value=50, limits=[20, 100]).classes('w-full') as splitter:
                with splitter.before:
                    ui.image('static/target_icon.jpg').classes('w-18 h-18')
                    ui.label('Target').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                    ui.image('static/coil_icon.jpg').classes('w-18 h-18')
                    ui.label('Coil').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                with splitter.after:
                    ui.image('static/move_icon.jpg').classes('w-18 h-18 full-height')
                    ui.label('Moving').classes('text-h5 q-pa-md bg-green-1 full-width text-center')
                    ui.image('static/trials_icon.jpg').classes('w-18 h-18')
                    ui.label('Trials').classes('text-h5 q-pa-md bg-green-1 full-width text-center')

        with ui.tab_panel(four):
            ui.label('Ongoing navigation')
            with ui.splitter() as splitter:
                with splitter.before:
                    with ui.pyplot(figsize=(3, 2)):
                        x = np.linspace(0.0, 5.0)
                        y = np.cos(2 * np.pi * x) * np.exp(-x)
                        plt.plot(x, y, '-')

                with splitter.after:
                    with ui.scene().classes('w-full h-64') as scene:
                        scene.axes_helper()
                        scene.sphere().material('#4488ff').move(2, 2)
                        scene.cylinder(1, 0.5, 2, 20).material('#ff8800', opacity=0.5).move(-2, 1)
                        scene.extrusion([[0, 0], [0, 1], [1, 0.5]], 0.1).material('#ff8888').move(2, -1)

                        with scene.group().move(z=2):
                            scene.box().move(x=2)
                            scene.box().move(y=2).rotate(0.25, 0.5, 0.75)
                            scene.box(wireframe=True).material('#888888').move(x=2, y=2)

                        scene.line([-4, 0, 0], [-4, 2, 0]).material('#ff0000')
                        scene.curve([-4, 0, 0], [-4, -1, 0], [-3, -1, 0], [-3, 0, 0]).material('#008800')

                        logo = 'https://avatars.githubusercontent.com/u/2843826'
                        scene.texture(logo, [[[0.5, 2, 0], [2.5, 2, 0]],
                                            [[0.5, 0, 0], [2.5, 0, 0]]]).move(1, -3)

                        teapot = 'https://upload.wikimedia.org/wikipedia/commons/9/93/Utah_teapot_(solid).stl'
                        scene.stl(teapot).scale(0.2).move(-3, 4)

                        avocado = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/Avocado/glTF-Binary/Avocado.glb'
                        scene.gltf(avocado).scale(40).move(-2, -3, 0.5)

                        scene.text('2D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(z=2)
                        scene.text3d('3D', 'background: rgba(0, 0, 0, 0.2); border-radius: 5px; padding: 5px').move(y=-2).scale(.05)

                    class CoordinateSystem(ui.scene.group):

                        def __init__(self, name: str, *, length: float = 1.0) -> None:
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

                    with ui.scene().classes('w-full h-64'):
                        CoordinateSystem('origin')
                        CoordinateSystem('custom frame').move(-2, -2, 1).rotate(0.1, 0.2, 0.3)
            
        with ui.tab_panel(five):
            ui.label('Stimulation setup')
            cStim = ui.input('Conditioning stimulus (%)', value='right ventral premotor cortex (rPMv)')
            tStim = ui.input('Test stimulus (%)', value='left M1')
            nInt = ui.input('Number of intervals', value='30').props('type=number')
            iSteps = ui.input('Interval step (ms)', value='15')
            nTrials = ui.input('Number of trials', value='120')
            nConditions = ui.input('Number of conditions', value='4')             
            tConditons = ui.input('Trials per condition', value='30')
            itInterval = ui.input('Inter_trial_interval (ms)', value='12')
            ui.button('Gravar', on_click=gravar_dados, icon='save')
        
        with ui.tab_panel(six):
            ui.label('Stimulation info')

ui.run(port=8082)
#ui.run(reload=False)