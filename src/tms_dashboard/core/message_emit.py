class Message2Server():
    def __init__(self, socket_client, dashboard):
        self.__socket_client = socket_client
        self.__event_name = "from_robot" # from_robot
        self.dashboard = dashboard        

    def __send_message2navigation(self, topic: str, data: dict = None):
        payload = {'topic': topic, 'data': {} if data is None else dict(data)}
        success = self.__socket_client.emit_event('from_robot', payload)
        return success
    
    def __send_message2robot(self, topic: str, data: dict = None):
        payload = {'topic': topic, 'data': {} if data is None else dict(data)}
        success = self.__socket_client.emit_event('from_neuronavigation', payload)
        return success

    def create_marker(self, data = None):
        return self.__send_message2navigation(topic='Create marker')
    
    def free_drive_robot(self):
        return self.__send_message2robot(topic='Neuronavigation to Robot: Set free drive', data= {'set': not self.dashboard.free_drive_robot_pressed})

    def move_upward_robot(self):
        return self.__send_message2navigation(topic='Press move away button', data= {'pressed': not self.dashboard.move_upward_robot_pressed})

    def active_robot(self):
        return self.__send_message2navigation(topic="Press robot button", data= {'pressed': not self.dashboard.active_robot_pressed})