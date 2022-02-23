import datetime
import json
import os
import pytz

from .singleton import Singleton
from .environment import Environment


class Summarisation(metaclass=Singleton):

    REL_PATH = "../../summary"
    FAIL_FILENAME = "fails.json"
    SUCCESS_FILENAME = "success.json"
    INFO_FILENAME = "info.json"

    def __init__(self):
        # check if summary path env variable set
        env_path = Environment().get(Environment.SUMMARY_PATH_KEY)
        if env_path:
            self.REL_PATH = env_path

        base = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(base, self.REL_PATH)

        # add datetime to path
        timezone = pytz.timezone('Pacific/Auckland')
        self.path = os.path.join(self.path, str(datetime.datetime.now(tz = timezone)))

        os.makedirs(self.path, exist_ok=True)

    def get_brand_path(self, brand_id):
        return os.path.join(self.path, str(brand_id))

    def get_fail_path(self, brand_id):
        return os.path.join(self.get_brand_path(brand_id), self.FAIL_FILENAME)

    def get_success_path(self, brand_id):
        return os.path.join(self.get_brand_path(brand_id), self.SUCCESS_FILENAME)

    def get_info_path(self, brand_id):
        return os.path.join(self.get_brand_path(brand_id), self.INFO_FILENAME)

    def create_brand_dir(self, brand_id):
        os.makedirs(self.get_brand_path(brand_id), exist_ok=True)

    def log_fail(self, brand_id, status, message, item_json):
        fail_file_path = self.get_fail_path(brand_id)
        exists = os.path.exists(fail_file_path)
        self.create_brand_dir(brand_id)
        item = json.dumps({"message": message, "status": status, "item": item_json})

        with open(fail_file_path, "a") as file:
            if exists:
                file.write(",\n")
            file.write(item)

    def log_success(self, brand_id, res_json):
        success_file_path = self.get_success_path(brand_id)
        exists = os.path.exists(success_file_path)
        self.create_brand_dir(brand_id)
        item = json.dumps(res_json)

        with open(success_file_path, "a") as file:
            if exists:
                file.write(",\n")
            file.write(item)

    def log_start(self, brand_id):
        self.create_brand_dir(brand_id)
        info_path = self.get_info_path(brand_id)
        item = {
            "startTime": str(datetime.datetime.now()),
            "endTime": None
        }
        with open(info_path, 'w') as file:
            json.dump(item, file)

    def log_end(self, brand_id):
        self.create_brand_dir(brand_id)
        info_path = self.get_info_path(brand_id)
        with open(info_path, 'r') as file:
            item = json.load(file)
            item['endTime'] = str(datetime.datetime.now())
        with open(info_path, 'w') as file:
            json.dump(item, file)
