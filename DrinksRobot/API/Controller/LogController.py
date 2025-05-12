from flask import Blueprint


from DrinksRobot.API.BLL.LogLogic import LogLogic

log_logic = LogLogic()

LogController = Blueprint('LogController', __name__)

@LogController.route('/logs', methods=['GET'])
def get_logs():
    logs = log_logic.get_logs()
    return logs

@LogController.route('/logsbytype', methods=['GET'])
def get_logs_by_type(log_type):
    logs = log_logic.get_log_by_type(log_type)
    return logs

@LogController.route('/createlog', methods=['post'])
def create_log(log_msg, log_type):
    log_logic.get_log_by_type(log_msg, log_type)
