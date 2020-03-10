from datetime import datetime, timedelta
import csv

from chatbot.helper.constants import CSV_FILE
from configs.log_config import logger

log = logger()


class Helper:

    @staticmethod
    def determine_end_time(start_time, duration=None):
        if not duration:
            duration = 0
        else:
            duration = int(duration)
        # duration = 0 if not duration else int(duration)
        end_time = datetime.strptime(start_time, '%H:%M')
        end_time += timedelta(minutes=duration)
        return end_time.time()

    @staticmethod
    def write_history_log(question, answer, nowaday):
        try:
            history = [question, answer, nowaday]

            with open(CSV_FILE, 'a', encoding='utf-8') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(history)

            csvFile.close()
        except Exception as ex:
            log.error(ex)
