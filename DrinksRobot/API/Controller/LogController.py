from flask import Blueprint, request, jsonify


from DrinksRobot.API.BLL.LogLogic import LogLogic

log_logic = LogLogic()

LogController = Blueprint('LogController', __name__)

@LogController.route('/logs', methods=['GET'])
def get_logs():
    logs = log_logic.get_logs()
    return jsonify(logs), 200

@LogController.route('/logsbytype', methods=['GET'])
def get_logs_by_type():
    log_type = request.args.get('type')
    if not log_type:
        return jsonify({"error": "Missing 'type' query parameter"}), 400
    logs = log_logic.get_log_by_type(log_type)
    return jsonify(logs), 200

@LogController.route('/createlog', methods=['POST'])
def create_log():
    data = request.get_json(silent=True) or {}
    log_msg = data.get('log_msg')
    log_type = data.get('log_type')
    if not log_msg or not log_type:
        return jsonify({"error": "'log_msg' and 'log_type' required"}), 400
    log_logic.create_logs(log_msg, log_type)
    return jsonify({"status": "created"}), 201
