import yaml
from dataclasses import dataclass
import sys
from os import path
import util


@dataclass
class ConfSchedule:
    day: str
    time: str


@dataclass
class Config:
    piholeContainerName: str
    weeklySchedule: ConfSchedule
    dailySchedule: ConfSchedule
    lastDayOfMonthSchedule: ConfSchedule


conf = Config(None, None, None, None)


def checkMandatoryFields():
    if conf.piholeContainerName is None:
        print("ERROR: Name of the pihole container must be inputted! Now exiting!")
        sys.exit(0)
    if conf.weeklySchedule is None and conf.dailySchedule is None and conf.lastDayOfMonthSchedule is None:
        print("ERROR: At least one backup schedule must be setup in order for the script to work! Now exiting!")
        sys.exit(0)
    if conf.weeklySchedule is not None and (conf.weeklySchedule.time is None or conf.weeklySchedule.day is None):
        print("ERROR: Weekly Schedule must have TIME and DAY setup! Now exiting!")
        sys.exit(0)
    if conf.lastDayOfMonthSchedule is not None and (
            conf.lastDayOfMonthSchedule.time is None or conf.lastDayOfMonthSchedule.day is None):
        print("ERROR: Last Day Of Month Schedule must have TIME and DAY setup! Now exiting!")
        sys.exit(0)
    if conf.dailySchedule is not None and conf.dailySchedule.time is None:
        print("ERROR: Daily Schedule must have TIME field setup! Now exiting!")
        sys.exit(0)


def printSetConfig():
    resultStr = "The following config params were set:\n"
    resultStr += f"- pihole_container_name = {conf.piholeContainerName}\n"

    resultStr += f"Backup Schedule:\n"
    if conf.weeklySchedule is not None:
        resultStr += f"- weekly.day = {conf.weeklySchedule.day}\n"
        resultStr += f"- weekly.time = {conf.weeklySchedule.time}\n"
    if conf.dailySchedule is not None:
        resultStr += f"- daily.time = {conf.dailySchedule.time}\n"
    if conf.lastDayOfMonthSchedule is not None:
        resultStr += f"- last_day_of_month.day = {conf.lastDayOfMonthSchedule.day}\n"
        resultStr += f"- last_day_of_month.time = {conf.lastDayOfMonthSchedule.time}\n"

    print(resultStr)


def initConfig():
    try:
        if path.exists('/yaml/config.yml'):
            with open('/yaml/config.yml') as f:
                docs = yaml.load_all(f, Loader=yaml.FullLoader)

                for doc in docs:
                    for k, v in doc.items():
                        if k == "general_settings" and v is not None:
                            for generalKey, generalVal in v.items():
                                if generalKey == "pihole_container_name" and generalVal != "<INSERT YOUR PIHOLE CONTAINER NAME HERE>":
                                    conf.piholeContainerName = generalVal

                        # Backup Schedule
                        if k == "backup_schedule" and v is not None:
                            for backupKey, backupVal in v.items():
                                if backupKey == "weekly" and backupVal is not None:
                                    weeklySchedule = ConfSchedule(None, None)
                                    for weeklyKey, weeklyVal in backupVal.items():
                                        if weeklyKey == "day":
                                            if weeklyVal in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]:
                                                weeklySchedule.day = weeklyVal
                                            else:
                                                print(
                                                    "ERROR: Weekly schedule's day is not set properly - Please use MON, TUE, WED, THU, FRI, SAT or SUN to specify the day. Now exiting!")
                                                sys.exit(0)
                                        if weeklyKey == "time":
                                            if util.isTimeFormat(weeklyVal):
                                                weeklySchedule.time = weeklyVal
                                            else:
                                                print(
                                                    "ERROR: Weekly time format is not valid! Please use HH:mm format! Now exiting!")
                                                sys.exit(0)

                                    conf.weeklySchedule = weeklySchedule

                                if backupKey == "daily" and backupVal is not None:
                                    dailySchedule = ConfSchedule(None, None)
                                    for dailyKey, dailyVal in backupVal.items():
                                        if dailyKey == "time":
                                            if util.isTimeFormat(dailyVal):
                                                dailySchedule.time = dailyVal
                                            else:
                                                print(
                                                    "ERROR: Daily time format is not valid! Please use HH:mm format! Now exiting!")
                                                sys.exit(0)

                                    conf.dailySchedule = dailySchedule

                                if backupKey == "last_day_of_month" and backupVal is not None:
                                    lastDaySchedule = ConfSchedule(None, None)
                                    for lastDayKey, lastDayVal in backupVal.items():
                                        if lastDayKey == "day":
                                            if lastDayVal.upper() in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]:
                                                lastDaySchedule.day = lastDayVal
                                            else:
                                                print(
                                                    "ERROR: Last Day Of Month schedule's day is not set properly - Please use MON, TUE, WED, THU, FRI, SAT or SUN to specify the day. Now exiting!")
                                                sys.exit(0)
                                        if lastDayKey == "time":
                                            if util.isTimeFormat(lastDayVal):
                                                lastDaySchedule.time = lastDayVal
                                            else:
                                                print(
                                                    "ERROR: Last Day Of Month time format is not valid! Please use HH:mm format! Now exiting!")
                                                sys.exit(0)

                                    conf.lastDayOfMonthSchedule = lastDaySchedule

            checkMandatoryFields()
            printSetConfig()
            return conf

        else:
            print(
                "ERROR: config.yml file not found (please bind the volume that contains the config.yml file) - now exiting!")
            sys.exit(0)

    except Exception as e:
        print("ERROR: config.yml file is not a valid yml file - now exiting!", e)
        sys.exit(0)
