class Message2Server():
    def __init__(self, socket_client):
        self.__socket_client = socket_client
        self.__event_name = "from_robot"

    def __send_message(self, topic, data = None):
        payload = {'topic': topic, 'data': {} if data is None else {data}}
        success = self.__socket_client.emit_event(self.__event_name, payload)
        return success

    def create_marker(self, data = None):
        return self.__send_message(topic='Create marker')