#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# for local server, start with: python.exe relay_server.py 127.0.0.1 5000
# for remote server, start with : python.exe  relay_server.py {remote_ip} 5000 
# start in terminal with:
# streamlit run ./web_UI_streamlit_trials.py

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import threading
import queue
import time
import socketio

import os
import csv

import PIL.ImageOps
from dataclasses import dataclass
from PIL import Image
from threading import Lock
from tweaker import st_tweaker
import altair as alt
#from streamlit_cropper import st_cropper

@dataclass
class Dashboard():
    def __init__(self):
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

def update_dashboard():
    global current_trial
    ColourWidgetText("Project", '#FF0000' if dashboard.project_set == False else '#00FF00')
    ColourWidgetText("Camera", '#FF0000' if dashboard.camera_set == False else '#00FF00')
    ColourWidgetText("Robot", '#FF0000' if dashboard.robot_set == False else '#00FF00')
    ColourWidgetText("TMS", '#FF0000' if dashboard.tms_set == False else '#00FF00')
    ColourWidgetText("NA", '#FF0000' if dashboard.image_NA_set == False else '#00FF00')
    ColourWidgetText("RE", '#FF0000' if dashboard.image_RE_set == False else '#00FF00')
    ColourWidgetText("LE", '#FF0000' if dashboard.image_LE_set == False else '#00FF00')
    ColourWidgetText("tNA", '#FF0000' if dashboard.tracker_NA_set == False else '#00FF00')
    ColourWidgetText("tRE", '#FF0000' if dashboard.tracker_RE_set == False else '#00FF00')
    ColourWidgetText("tLE", '#FF0000' if dashboard.tracker_LE_set == False else '#00FF00')
    ColourWidgetText("Transformation matrix set", '#FF0000' if dashboard.matrix_set == False else '#00FF00')
    ColourWidgetText("3D target set", '#FF0000' if dashboard.target_set == False else '#00FF00')
    ColourWidgetText("Robot moving", '#FF0000' if dashboard.robot_moving == False else '#00FF00')
    ColourWidgetText("Coil at target", '#FF0000' if dashboard.at_target == False else '#00FF00')
    ColourWidgetText("Trials started", '#FF0000' if dashboard.trials_started == False else '#00FF00')
    
class RemoteControl:
    
    def __init__(self, remote_host):
        self.__buffer = []
        self.__remote_host = remote_host
        self.__connected = False
        self.__sio = socketio.Client(reconnection_delay_max=5)

        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('to_robot', self.__on_message_receive)
        self.__sio.on('to_neuronavigation', self.__on_message_receive)

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

def get_navigation_status():
    global target_status
    global fiducial_counter
    global distance
    global current_trial
    global distance_factor

    buf = rc1.get_buffer()

    #print(buf)
    if len(buf) == 0:
        pass
    elif any(item in [d['topic'] for d in buf] for item in robot_messages):
        topic = [d['topic'] for d in buf]
        
        for i in range(len(buf)):
            if topic[i] in robot_messages:
                target_status = buf[i]["data"]
            #if topic[i] != "From Neuronavigation: Update tracker poses":
                #print(topic[i])
                #print(target_status)
                #print(buf)

                match topic[i]:
                    case 'Set image fiducial':
                        target_status = buf[i]["data"]
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
                    case 'Reset image fiducials':
                        dashboard.image_NA_set = False
                        dashboard.image_RE_set = False
                        dashboard.image_LE_set = False
                    case 'Project loaded successfully':
                        dashboard.project_set = True
                    case 'Close Project':
                        dashboard.project_set = False
                    case 'From Neuronavigation: Update tracker poses':
                        distance_x = (target_status['poses'][1][0] - target_status['poses'][2][0])# / (target_status['poses'][1][0]+0.0000001)
                        distance_y = (target_status['poses'][1][1] - target_status['poses'][2][1])# / (target_status['poses'][1][1]+0.0000001)
                        distance_z = (target_status['poses'][1][2] - target_status['poses'][2][2])# / (target_status['poses'][1][2]+0.0000001)
                        distance = (distance_x + distance_y + distance_z) / distance_factor
                        #print("target >>>>>" + str(distance))
                        dashboard.robot_moving = True
                    case 'Tracker changed':
                        dashboard.camera_set = False
                    case 'Tracker fiducials set':
                        dashboard.tracker_LE_set = True
                        dashboard.tracker_RE_set = True
                        dashboard.tracker_NA_set = True
                    case 'Reset tracker fiducials':
                        dashboard.tracker_NA_set = False
                        dashboard.tracker_RE_set = False
                        dashboard.tracker_LE_set = False
                    case 'Open navigation menu':
                        dashboard.robot_set = True
                        dashboard.matrix_set = True
                    case 'Set target mode':
                        dashboard.target_set = True
                    case 'Unset target':
                        dashboard.target_set = False
                    case 'Set objective':
                        dashboard.robot_moving = True
                    case 'Coil at target':
                        if target_status['state'] == True:
                            dashboard.at_target = True
                            dashboard.robot_moving = False
                        else:
                            dashboard.at_target = False
                            dashboard.robot_moving = True
                    case 'Trial triggered':
                        #if target_status['data'] == "True":
                        dashboard.trials_started = True
                        print (target_status)
                        print (str(dashboard.trials_started))
                        current_trial = target_status['number']
                        print("prova atual >>>>>>>> " + str(current_trial))
                        #st.session_state.current_trial = _current_trial
                        
def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.5)
    
    yield pd.DataFrame(
        np.random.randn(5,10),
        columns=["a", "b","c","d","e","f","g","h","i","j"]
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.5)
def test_run():
    while True:
        time.sleep(0.2)
        val = x
        multiply = val * 10
        q.put((val, multiply))
def message_nav():
    global current_trial
    while True:
        time.sleep(0.2)
        mensagem = get_navigation_status()
        #print(mensagem)
        #if mensagem != None:
        r.put((mensagem))
# https://discuss.streamlit.io/t/changing-the-text-color-of-only-one-metric/35338/2
def ColourWidgetText(wgt_txt, wch_colour = '#000000'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        elements[i].style.color = ' """ + wch_colour + """ '; } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

@st.fragment
def save_file(file_name):
    time.sleep(2)  # Simulating a save operation that takes some time
    # Save logic in CSV format with quotes
    with open(file_name, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # Quote all fields
        # Write header
        writer.writerow(fields.keys())
        # Write data
        writer.writerow(fields.values())
    st.session_state.file_saved = True  # Mark that the file is saved

if __name__ == '__main__':
    
    path_images = "C:\\Users\\bioma\\Documents\\GitHub\\tms-experiment-dashboard\\images\\"

    rc1 = RemoteControl("http://127.0.1.1:5000")
    #rc1 = RemoteControl("http://192.168.200.240:5000") #Tesla
    #rc2 = RemoteControl("http://192.168.200.201:5000")
    #rc1 = RemoteControl("http://169.254.100.20:5000") #Thais
    #rc1 = RemoteControl("http://169.254.111.20:5000") #Thais
    #rc1 = RemoteControl("http://169.254.140.200:5000") #Victor
 
    rc1.connect()
    #rc2.connect()
    #clean buffer
    print("Conectado à rede local")

    texto = rc1.get_buffer()
    print(texto)
    print("Buffer capturado")

    if "file_saved" not in st.session_state:
        st.session_state.file_saved = False  # To track if file is saved

    dashboard = Dashboard()
    print("Dashboard inicializado")

    #plt.style.use('dark_background')

    global robot_messages 
    global ui_messages
    global image_fiducial_set
    global current_trial
    global distance
    global distance_factor

    distance = 0
    distance_factor = 420 # value to make relative the distance between coil and head 
    robot_messages = {'Set target mode', 'Open navigation menu', 'Close Project', 'Project loaded successfully', 'Set image fiducial', 'Reset image fiducials', 'Set robot transformation matrix', 'Set target', 'Tracker fiducials set', 'Set objective', 'Unset target', 'Remove sensors ID', 'Reset tracker fiducials', 'Robot connection status','Reset image fiducials', 'Disconnect tracker', 'Tracker changed', 'From Neuronavigation: Update tracker poses','Coil at target', 'Update displacement to target', 'Trials started', 'Trial triggered', 'From Neuronavigation: Update robot warning'}
    ui_messages = {"Alvo definido", "Navegação iniciada", "Projeto fechado", "Projeto carregado", "Fiducial na imagem definido", "Fiduciais resetados", "Robô conectado", "Alvo definido", "Fiduciais do robô definidos", "Trajetória definida", "Alvo não definido", "Camera desconectada", "Fiduciais do robô indefinidos", "Status do robô", "Fiduciais da imagem ressetados", "Câmera desconectada", "Câmera desconectada", "Câmera conectada", "Bobina no alvo", "Atualizando distância", "Inicio das provas", "Prova disparada", "Robô para altura segura"}
    

    
    _msgs = []

    q = queue.Queue()
    r = queue.Queue()
    counter = 1
    fiducial_counter = 0

    st.set_page_config(page_title="Biomag Dashboard",
                       page_icon = os.path.join(path_images, 'biomag_logo.jpeg'), 
                       layout="wide",
                       menu_items={'Get Help': 'mailto:biomag@hotmail.com?subject=Asking%20for%20help',
                        'Report a bug': "mailto:biomag@hotmail.com?subject=I%20found%20a%20bug",
                        'About': "# Dashboard for Invesalius Neuronavigator."})

    _LOREM_IPSUM = "Fiducial Nasion definido 1, 2, 3... Feito!"

    # creating initial data values of x and y
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    is_exit_target_if_main_exits = True

    threading.Thread(
        target=test_run,
        daemon=is_exit_target_if_main_exits).start()

    threading.Thread(
        target=message_nav,
        daemon=is_exit_target_if_main_exits).start()


    print("Threads iniciadas")

    col1, mid, col2 = st.columns([1,1,20])
    with col1:
        image = Image.open(path_images + 'biomag_logo.jpg')
        #inverted_image = PIL.ImageOps.invert(image)
        st.image(image, width=120)
    with col2:
        st.header('Biomag Neuronavigation Dashboard', divider='rainbow')

    # New expander for user input fields

    with st.expander("Experiment details", expanded=False):
        # Dictionary fields
        fields = {
            "Experiment_name": "Paired pulse, dual site, bilateral, leftM1-rightPMv",
            "Experiment_description": "Dual site paired bilateral TMS stimulation, with 2 channel EMG acquisition. 80 trials, 4 experimental conditions, 200 pulses",
            "Start_date": "2025-01-31",
            "End_date": "2024-02-01",
            "Experiment_title": "Paired pulse contralateral conditioning",
            "Experiment_description_details": "Paradigm with motor mapping totaling 80 trials with 20 pulses/condition. Target muscle: APB. Inter-pulse interval: 7 to 10 s."
            }

        # Input fields
        for key, value in fields.items():
            fields[key] = st.text_area(key.replace("_", " ").capitalize(), value, height=90)

        file_name = st.text_area("File name:", "experiment_details.csv", height=90)
        save_button =  st.button("Save", key="save_file_button")

        if save_button and not st.session_state.file_saved:
            result = save_file(file_name)  # Save file directly in the main thread
            
            st.session_state.file_saved = True
            st.success(result)
            
        if st.session_state.file_saved:
            st.success("User input saved successfully.")
            #st.session_state.file_saved = False

    # Expander for the dashboard Main Functions
    with st.expander("Dashboard Main Functions", expanded=True):
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Conections", "Transformation", "Control", "Navigation", "Stimulation", "Info"])

        with tab1: # Connections
            st.markdown("""
                <style>
                .centered {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                }
                </style>
                """, unsafe_allow_html=True)
        
            st.markdown("<h3 style='text-align:center'>Connections</h4>", unsafe_allow_html=True)
    
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([0.1,0.1,0.1,0.1])
                
                with col1:
                    st.markdown("<p style='text-align:center; font-size:20px; font-weight:bold;'>Project</p>", unsafe_allow_html=True)
                    image = Image.open(path_images + 'computer_icon.jpg')
                    st.image(image, width=80, use_container_width=True)

                with col2:
                    #st.image('/home/iana/tms-robot-control/camera_icon.jpg', width=100)
                    st.markdown("<p style='text-align:center; font-size:20px; font-weight:bold;'>Camera</p>", unsafe_allow_html=True)
                    image = Image.open(path_images + 'camera_icon.jpg')
                    st.image(image, width=80, use_container_width=True)

                with col3:
                    #st.image('/home/iana/tms-robot-control/robot_icon.jpg', width=100)
                    st.markdown("<p style='text-align:center; font-size:20px; font-weight:bold;'>Robot</p>", unsafe_allow_html=True)
                    image = Image.open( path_images + 'robot_icon.jpg')
                    st.image(image, width=80, use_container_width=True)

                with col4:
                    #st.image('/home/iana/tms-robot-control/TMS_icon.jpg', width=100)
                    st.markdown("<p style='text-align:center; font-size:20px; font-weight:bold;'>TMS</p>", unsafe_allow_html=True)
                    image = Image.open(path_images + 'TMS_icon.jpg')
                    st.image(image, width=80, use_container_width=True)

        with tab2: # Transformations
            st.markdown("<h3 style='text-align:center'>Transformation</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("<h4 style='text-align:center'>Image fiducials</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'>NA</p>", unsafe_allow_html=True)
                #st_tweaker.write("NA")
                
                subcol1, mid, subcol2 = st.columns([1,1,1])
                with subcol1:
                    st.markdown("<p style='text-align:right'>RE</p>", unsafe_allow_html=True)
                    #st_tweaker.write("RE")
                with mid:
                    image = Image.open(path_images + 'head.jpg')
                    #inverted_image = PIL.ImageOps.invert(image)
                    st.image(image)
                with subcol2:
                    st_tweaker.write("LE")

                st.markdown("<h5 style='text-align:center'>Transformation matrix set</h5>", unsafe_allow_html=True)

                st.markdown("<h4 style='text-align:center'>Tracker fiducials</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center'>tNA</p>", unsafe_allow_html=True)
                
                subcol3, mid2, subcol4 = st.columns([1,1,1])
                with subcol3:
                    st.markdown("<p style='text-align:right'>tRE</p>", unsafe_allow_html=True)
                    #st_tweaker.write("RE")
                with mid2:
                    image = Image.open(path_images + 'head.jpg')
                    #inverted_image = PIL.ImageOps.invert(image)
                    st.image(image)
                with subcol4:
                    st_tweaker.write("tLE")


                #preview_area = st.text_area(label="X", value=0, label_visibility='collapsed', on_change=None,
                #                    disabled=False, max_chars=5000)
                #st_tweaker.writetext(label = "My label", id = "my-element-id")

        with tab3: # 
            st.markdown("<h2 style='text-align:center'>Execution</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                col5, col6, col7, col8 = st.columns([0.1,0.1,0.1,0.1])

                with col5:
                    st.markdown("<p style='text-align:center; font-size:20px; font-weight:bold;'>3D target set</p>", unsafe_allow_html=True)
                    image = Image.open(path_images + 'target_icon.jpg')
                    st.image(image, width=80, use_container_width=True)

                with col6:
                    st.markdown("<p style='text-align:center; font-size:20px; font-weight:bold;'>Robot moving</p>", unsafe_allow_html=True)
                    image = Image.open(path_images + 'move_icon.jpg')
                    st.image(image, width=80, use_container_width=True)


                with col7:
                    st.markdown("<h5 style='text-align:center'>Coil at target</h5>", unsafe_allow_html=True)
                    image = Image.open(path_images + 'coil_icon.jpg')
                    st.image(image, width=80, use_container_width=True)

                with col8:
                    st.markdown("<h5 style='text-align:center'>Trials started</h5>", unsafe_allow_html=True)
                    image = Image.open(path_images + 'trials_icon.jpg')
                    st.image(image, width=80, use_container_width=True)

        with tab5: # Stimulation
            st.markdown("<h2 style='text-align:center'>Stimulation</h4>", unsafe_allow_html=True)
            with st.container(border=True):# Input for number of trials
                total_trials = st.number_input("Enter the total number of trials", min_value=1, max_value=1000, value=70)
                current_trial = 15
                # Initialize session state for current_trial
                if 'current_trial' not in st.session_state:
                    st.session_state.current_trial = current_trial

                # Button for incrementing the current trial
                #if st.button("Reset"):
                    #if st.session_state.current_trial < total_trials:
                    #st.session_state.current_trial += 1

                # Input to set the current trial manually (optional)
                #current_trial = st.slider("Select Current Trial", 1, total_trials, st.session_state.current_trial)
                
                # Create data for the bar chart
                trial_numbers = np.arange(1, total_trials + 1)
                colors = ["green" if trial <= current_trial else "red" for trial in trial_numbers]

                # Create a DataFrame to plot
                df = pd.DataFrame({
                    'Trial': trial_numbers,
                    'Color': colors,
                    'Count': np.ones(total_trials)  # placeholder for count or other metric
                })

                # Define the bar chart using Altair
                chart = alt.Chart(df).mark_bar().encode(
                    x=alt.X('Trial:O', title='Trial', axis=alt.Axis(labelAngle=0)),  # X-axis for trial numbers (ordinal)
                    y='Count:Q',  # Y-axis for count (quantity)
                    color=alt.Color('Color:N', scale=alt.Scale(domain=['red', 'green'], range=['red', 'green']), legend=None),  # Set colors to red and green, no legend
                    tooltip=['Trial', 'Color']  # Show trial number and color on hover
                ).properties(
                    width=1060,
                    height=110
                ).configure_axis(
                    grid=False,  # Disable grid lines
                    ticks=False,  # Disable axis ticks
                    domain=False  # Disable axis line for Y-axis
                ).configure_axisY(
                    title=None,  # Remove the title for the Y-axis
                    labels=False,  # Remove the labels for the Y-axis
                )

                # Display the chart
                #mensagem, current_trial = r.get_nowait()
                st.altair_chart(chart)

        with tab6: # Information
            st.markdown("""
                <style>
                .centered {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                }
                </style>
                """, unsafe_allow_html=True)
        
            st.markdown("<h3 style='text-align:center'>Information</h4>", unsafe_allow_html=True)

        with tab4: # Navigation
            st.markdown("<h2 style='text-align:center'>Navigation</h4>", unsafe_allow_html=True)
            with st.container(border=False):# Input for number of trials
                #fig, ax = plt.subplots()
                figure, ax = plt.subplots(figsize=(15, 7))
                line1, = ax.plot(x, y)
                
                # setting title
                plt.title("Distance to target", fontsize=20)

                
                # setting x-axis label and y-axis label
                plt.xlabel("Time (s)")
                plt.ylabel("Distance (cm)")

                # Set the background color to white for the current plot
                plt.style.use('default')  # Reset to the default style
                plt.rcParams.update({'axes.facecolor': 'white'})  # Set the figure background to white
                plt.rcParams.update({'figure.facecolor': 'white'})  # Set the figure background to white
                
                
                placeholder1 = st.empty()
                with placeholder1.container():
                    st.pyplot(figure)

                #placeholder2 = st.empty()
                #with placeholder2.container():
                    #col1, col2, col3 = st.columns(3)
                    #col1.metric(label="Distância atual:", value="")
                    #col2.metric(label="Multiplicada por 10: ", value="")
                    #col3.metric(label="Mensagem: ", value="")
                # Loop
                #for _ in range(50):
                    # creating new Y values
            
                while True:
                    try:
                        with placeholder1.container():
                            val, multiply = q.get_nowait()
                            new_last_y = np.sin(x+0.5 * val)[0] # first value of new graph 

                            if counter == 1:
                                new_y = np.sin(x+0.5 * val)
                                counter += 1
                                #pthread_kill(t1.ident, SIGTSTP)
                            else:
                                new_y = new_y[:-1] # delete last value
                                new_y = np.insert(new_y, 0, distance) # insert new on first position
                            #line1.set_xdata(x)
                            line1.set_ydata(new_y[::-1]) # write y in reverse order, last point is new
                            #line1.set_ydata(new_y)

                            figure.canvas.flush_events()
                            #figure.canvas.draw()
                            st.write(figure)
                            update_dashboard()
                            q.task_done()
                    except queue.Empty:
                        continue



