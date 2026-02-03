from tms_dashboard.constants import BrainTargetModel
from tms_dashboard.utils.signal_processing import p2p_from_time

class Message2Server():
    def __init__(self, socket_client, dashboard):
        self.__socket_client = socket_client
        self.dashboard = dashboard        

    def __send_message2navigation(self, topic: str, data: dict = None):
        payload = {'topic': topic, 'data': {} if data is None else dict(data)}
        success = self.__socket_client.emit_event('from_robot', payload)
        return success
    
    def __send_message2robot(self, topic: str, data: dict = None):
        payload = {'topic': topic, 'data': {} if data is None else dict(data)}
        success = self.__socket_client.emit_event('from_neuronavigation', payload)
        return success

    def create_marker(self):
        return self.__send_message2navigation(topic='Create marker')
    
    def free_drive_robot(self):
        return self.__send_message2robot(topic='Neuronavigation to Robot: Set free drive', data= {'set': not self.dashboard.free_drive_robot_pressed})

    def move_upward_robot(self):
        return self.__send_message2navigation(topic='Press move away button', data= {'pressed': not self.dashboard.move_upward_robot_pressed})

    def active_robot(self):
        return self.__send_message2navigation(topic="Press robot button", data= {'pressed': not self.dashboard.active_robot_pressed})
    
    def send_mep_value(self, series_meps: list):
        targets = []
        for mep in series_meps:
            mep_value = p2p_from_time(mep, self.dashboard.mep_sampling_rate, -10)
            target = BrainTargetModel()
            target.mep = mep_value
            targets.append(target.to_dict())
        
        self.dashboard.status_new_mep = False
        return self.__send_message2navigation(topic="Set brain targets", data={'brain_targets': targets})
