from flask import Blueprint, request, jsonify
import json
from DrinksRobot.API.Helpers.logger import get_logger
from DrinksRobot.API.BLL.LogLogic import LogLogic


def create_robot_controller(robot_logic):
    RobotController = Blueprint('RobotController', __name__)
    log = get_logger("RobotController")
    log_db = LogLogic()

    @RobotController.route('/mixdrink', methods=['POST'])
    def create_drink():
        try:
            data = request.get_json()
            bottle_ids = data.get('bottles')
            if not bottle_ids:
                return jsonify({"error": "Missing 'bottles' in request"}), 400

            log.info("Queue mixdrink bottles=%s", bottle_ids)
            try:
                log_db.create_logs(f"Queue mixdrink bottles={bottle_ids}", "info")
            except Exception:
                pass

            robot_logic.run_program(bottle_ids)
            return jsonify({"status": "success"}), 200

        except Exception as e:
            log.exception("Error in create_drink")
            try:
                log_db.create_logs(f"Error mixdrink: {e}", "error")
            except Exception:
                pass
            return jsonify({"error": str(e)}), 500


    @RobotController.route('/pause', methods=['POST'])
    def pause_robot():
        ok = robot_logic.pause()
        msg = {"status": "paused", "ok": bool(ok)}
        log.info("Pause requested -> %s", msg)
        try:
            log_db.create_logs(f"Pause -> {msg}", "info" if ok else "error")
        except Exception:
            pass
        return jsonify(msg), (200 if ok else 500)

    @RobotController.route('/resume', methods=['POST'])
    def resume_robot():
        ok = robot_logic.resume()
        msg = {"status": "resumed", "ok": bool(ok)}
        log.info("Resume requested -> %s", msg)
        try:
            log_db.create_logs(f"Resume -> {msg}", "info" if ok else "error")
        except Exception:
            pass
        return jsonify(msg), (200 if ok else 500)

    @RobotController.route('/mix_self', methods=['POST'])
    def mix_self():
        data = request.get_json(silent=True) or {}
        script = data.get('script', 'self_mix.urp')
        log.info("Queue mix_self script=%s", script)
        try:
            log_db.create_logs(f"Queue mix_self script={script}", "info")
        except Exception:
            pass
        robot_logic.run_single_program(script)
        return jsonify({"status": "queued"}), 200

    @RobotController.route('/run_program', methods=['POST'])
    def run_program():
        data = request.get_json(silent=True) or {}
        script = data.get('script')
        if not script:
            return jsonify({"error": "Missing 'script' in body"}), 400
        log.info("Queue run_program script=%s", script)
        try:
            log_db.create_logs(f"Queue run_program script={script}", "info")
        except Exception:
            pass
        robot_logic.run_single_program(script)
        return jsonify({"status": "queued", "script": script}), 200

    return RobotController