import calendar
import time
from datetime import datetime
import schedule
import containerChecks


def generatePreviews(container, config):
    cmdToRun = "pihole updateGravity"

    print(f"Now running the command `{cmdToRun}` in the pihole container for updating the adblock lists!! This may take a while..")
    container.exec_run(cmd=cmdToRun)
    print(f"FINISHED: with updating the lists. See you at the next scheduled time. ;)")


def mainLastDayOfMonth():
    # check to see if it is in fact the last day of the month - and if so, then allow the schedule to take place
    today = datetime.today()
    curDay = today.day
    daysInCurMonth = calendar.monthrange(today.year, today.month)[1]

    if (daysInCurMonth - 7) < curDay:
        startMainProcess()


def handleScheduling(config):
    if config.dailySchedule is not None:
        schedule.every().day.at(config.dailySchedule.time).do(startMainProcess)
    if config.weeklySchedule is not None:
        if config.weeklySchedule.day == "MON":
            schedule.every().monday.at(config.weeklySchedule.time).do(startMainProcess)
        if config.weeklySchedule.day == "TUE":
            schedule.every().tuesday.at(config.weeklySchedule.time).do(startMainProcess)
        if config.weeklySchedule.day == "WED":
            schedule.every().wednesday.at(config.weeklySchedule.time).do(startMainProcess)
        if config.weeklySchedule.day == "THU":
            schedule.every().thursday.at(config.weeklySchedule.time).do(startMainProcess)
        if config.weeklySchedule.day == "FRI":
            schedule.every().friday.at(config.weeklySchedule.time).do(startMainProcess)
        if config.weeklySchedule.day == "SAT":
            schedule.every().saturday.at(config.weeklySchedule.time).do(startMainProcess)
        if config.weeklySchedule.day == "SUN":
            schedule.every().sunday.at(config.weeklySchedule.time).do(startMainProcess)
    if config.lastDayOfMonthSchedule is not None:
        if config.lastDayOfMonthSchedule.day == "MON":
            schedule.every().monday.at(config.lastDayOfMonthSchedule.time).do(mainLastDayOfMonth)
        if config.lastDayOfMonthSchedule.day == "TUE":
            schedule.every().tuesday.at(config.lastDayOfMonthSchedule.time).do(mainLastDayOfMonth)
        if config.lastDayOfMonthSchedule.day == "WED":
            schedule.every().wednesday.at(config.lastDayOfMonthSchedule.time).do(mainLastDayOfMonth)
        if config.lastDayOfMonthSchedule.day == "THU":
            schedule.every().thursday.at(config.lastDayOfMonthSchedule.time).do(mainLastDayOfMonth)
        if config.lastDayOfMonthSchedule.day == "FRI":
            schedule.every().friday.at(config.lastDayOfMonthSchedule.time).do(mainLastDayOfMonth)
        if config.lastDayOfMonthSchedule.day == "SAT":
            schedule.every().saturday.at(config.lastDayOfMonthSchedule.time).do(mainLastDayOfMonth)
        if config.lastDayOfMonthSchedule.day == "SUN":
            schedule.every().sunday.at(config.lastDayOfMonthSchedule.time).do(mainLastDayOfMonth)


def startMainProcess():
    print("\n\nCOMMENCING THE SCHEDULED TASK TO UPDATE GRAVITY..\n")
    container, config = containerChecks.mainChecks()
    generatePreviews(container, config)


def main():
    print("STARTING SCRIPT!")
    container, config = containerChecks.mainChecks()

    handleScheduling(config)
    while True:
        schedule.run_pending()
        time.sleep(1)


main()
