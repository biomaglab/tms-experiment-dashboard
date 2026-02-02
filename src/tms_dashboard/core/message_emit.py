class Message2Server():
    def __init__(self, socket_client, dashboard):
        self.__socket_client = socket_client
        self.__event_name = "from_robot"
        self.dashboard

    def __send_message(self, topic, data = None):
        payload = {'topic': topic, 'data': {} if data is None else {data}}
        success = self.__socket_client.emit_event(self.__event_name, payload)
        return success

    def create_marker(self, data = None):
        return self.__send_message(topic='Create marker')
    
    def free_drive_robot(self):
        return self.__send_message(topic='Neuronavigation to Robot: Set free drive', data= not self.dashboard.free_drive_robot_pressed)

    def move_upward_robot(self):
        return self.__send_message(topic='Press move away button', data= not self.dashboard.move_upward_robot_pressed)

    def active_robot(self):
        return self.__send_message(topic="Press robot button", data= not self.dashboard.active_robot_pressed)