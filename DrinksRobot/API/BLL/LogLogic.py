from DrinksRobot.API.DAL.LogContext import LogContext

log_context = LogContext()

class LogLogic:
    def get_logs(self):
        logs = log_context.get_all_logs()
        return logs

    def create_logs(self, log_msg, log_type):
        log_context.create_log(log_msg, log_type)

    def get_log_by_type(self, log_type):
        logs = log_context.get_logs_by_type(log_type)
        return logs