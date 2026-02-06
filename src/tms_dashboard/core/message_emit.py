import time

from src.tms_dashboard.constants import BrainTargetModel

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
        self.check_robot_connection()
        if self.dashboard.robot_set:
            return self.__send_message2robot(topic='Neuronavigation to Robot: Set free drive', data= {'set': not self.dashboard.free_drive_robot_pressed})
        return False

    def move_upward_robot(self):
        self.check_robot_connection()
        if self.dashboard.robot_set:
            return self.__send_message2navigation(topic='Press move away button', data= {'pressed': not self.dashboard.move_upward_robot_pressed})
        return False
    def active_robot(self):
        self.check_robot_connection()
        if self.dashboard.robot_set:
            return self.__send_message2navigation(topic="Press robot button", data= {'pressed': not self.dashboard.active_robot_pressed})
        return False
    
    def check_robot_connection(self):
        self.__send_message2robot(topic="Neuronavigation to Robot: Check connection robot")

    def send_mep_value(self, meps: list):
        if self.dashboard.at_target:
            targets = []
            for mep in meps:
                target = BrainTargetModel()
                target.mep = mep
                targets.append(target.to_dict())
            
            self.__send_message2navigation(topic="Set brain targets", data={'brain_targets': targets})
        self.dashboard.status_new_mep = False

    def request_robot_config(self):
        self.__send_message2robot(topic="Neuronavigation to Robot: Request config")
    
    def send_robot_config(self, robot_config):
        """Send robot configuration to the robot control system.
        
        Args:
            robot_config: RobotConfigState instance with configuration parameters
            
        Returns:
            bool: True if message was sent successfully
        """
        self.__send_message2robot(
            topic='Neuronavigation to Robot: Update config', 
            data=robot_config.to_dict()
        )

        # self.__send_message2robot(
        #     topic='Neuronavigation to Robot: Update pid values', 
        #     data=robot_config.to_dict()
        # )

        return True

