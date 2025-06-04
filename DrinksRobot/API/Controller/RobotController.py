from flask import Blueprint, request, jsonify
import json

def create_robot_controller(robot_logic):
    RobotController = Blueprint('RobotController', __name__)

    @RobotController.route('/mixdrink', methods=['POST'])
    def create_drink():
        try:
            data = request.get_json()
            bottle_ids = data.get('bottles')
            if not bottle_ids:
                return jsonify({"error": "Missing 'bottles' in request"}), 400

            print("Received bottle IDs:", bottle_ids)

            robot_logic.run_program(bottle_ids)
            return jsonify({"status": "success"}), 200

        except Exception as e:
            print("Error in create_drink:", e)
            return jsonify({"error": str(e)}), 500


    @RobotController.route('/pause', methods=['POST'])
    def pause_robot():
        robot_logic.pause()
        return jsonify({"status": "paused"}), 200

    @RobotController.route('/resume', methods=['POST'])
    def resume_robot():
        robot_logic.resume()
        return jsonify({"status": "resumed"}), 200

    return RobotController