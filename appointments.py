# Shippo Programming Assignment
# Kevin Chau

import sys
import cmd
import sched
import time
import calendar
import datetime

class appointments(cmd.Cmd):
    """Appointment Scheduler"""
    
    intro = "Welcome to your appointment scheduler! Type 'help' to start."
    prompt = "(Enter Command) "

    # dictionary of appointments
    # key: date and time
    # value: appointment type
    schedule = {}

    def do_List(self, args):
        """List all future appointments.
        Usage: List
        """
        for key in appointments.schedule:
            print appointments.schedule[key], key.ctime()

    def do_Schedule(self, args):
        """Schedule a 'Haircut' or 'Shampoo&Haircut' appointment.
        
        Usage: Schedule [appointment_type] [year-month-day] [time]
        
        Examples:
            Schedule haircut 2016-10-31 10:30
            Schedule haircut&shampoo 2016-11-1 17:15
        """

        arg_list = args.split()

        try:
            appointment_type, date, time = arg_list[0], arg_list[1], arg_list[2]
        except IndexError:
            print "Incorrect number of arguments."
            print "Usage: Schedule [appointment_type] [date or day] [time]"
            return

        today = datetime.date.today()

        try:
            year, month, day = date.split('-')
        except ValueError:
            print "Invalid date."
            return

        try:
            d = datetime.date(int(year), int(month), int(day))
        except ValueError:
            print "Invalid date."
            return

        try:
            hour, minute = time.split(':')
        except ValueError:
            print "Invalid time."
            return

        t = datetime.time(int(hour),int(minute))

        # Appointments must be schedules at 15-minute offsets from the hour
        if t.minute % 15 != 0:
            print "Invalid appointment time. Must be at 15-minute offsets."
            return

        dt = datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)

        appointment_type = appointment_type.lower()

        if appointments.check_for_conflicts(self, dt, appointment_type):
            return
        else:
            appointments.schedule[dt] = appointment_type
    
    def check_for_conflicts(self, dt, appointment_type):
        # check for no conflicting appointments
        # conflicts: haircut in previous 15 mins
        #            haircut&shampoo in previous 15,30,45 mins
        #            any appointment in the next 15 minutes
        #            this appointment is haircut&shampoo, any appointment in next 30 or 45 mins

        prev_15_dt = dt - datetime.timedelta(minutes=15)
        prev_30_dt = dt - datetime.timedelta(minutes=30)
        prev_45_dt = dt - datetime.timedelta(minutes=45)
        next_15_dt = dt + datetime.timedelta(minutes=15)
        next_30_dt = dt + datetime.timedelta(minutes=30)
        next_45_dt = dt + datetime.timedelta(minutes=45)

        if appointments.schedule.has_key(dt):
            print "Appointment already booked for this time."

        if appointments.schedule.has_key(prev_15_dt) and appointments.schedule[prev_15_dt] == "haircut":
            print "Conflict with previous appointment."
            return 1

        if appointments.schedule.has_key(prev_15_dt) and appointments.schedule[prev_15_dt] == "haircut&shampoo":
            print "Conflict with previous appointment."
            return 1

        if appointments.schedule.has_key(prev_30_dt) and appointments.schedule[prev_30_dt] == "haircut&shampoo":
            print "Conflict with previous appointment."
            return 1

        if appointments.schedule.has_key(prev_45_dt) and appointments.schedule[prev_45_dt] == "haircut&shampoo":
            print "Conflict with previous appointment."
            return 1

        if appointments.schedule.has_key(next_15_dt):
            print "Conflict with next appointment."
            return 1

        if appointments.schedule.has_key(next_30_dt) and appointment_type == "haircut&shampoo":
            print "Conflict with next appointment."
            return 1

        if appointments.schedule.has_key(next_45_dt) and appointment_type == "haircut&shampoo":
            print "Conflict with next appointment."
            return 1

        if appointment_type != "haircut" and appointment_type != "haircut&shampoo":
            print "Invalid appointment type."
            return 1

        return 0

    def do_Cancel(self, appointment):
        """Cancel an appointment
        Usage: Cancel [year-month-day] [time]
        
        Examples:
            Cancel 2016-10-31 10:30
            Cancel 2016-11-1 17:15
        """
        arg_list = appointment.split()

        try:
            date, time = arg_list[0], arg_list[1]
        except IndexError:
            print "Incorrect number of arguments."
            print "Usage: Cancel [date or day] [time]"
            return

        try:
            year, month, day = date.split('-')
        except ValueError:
            print "Invalid date."
            return

        try:
            hour, minute = time.split(':')
        except ValueError:
            print "Invalid time."
            return

        dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))

        if appointments.schedule.pop(dt, None) == None:
            print "Appointment does not exist."
            return

    def do_Exit(self, args):
        """Exit the scheduler, destroying all appointments.
        Usage: Exit
        """
        print "Exiting... Destroying schedule."
        return True


    ### Lowercase commands ###
    def do_list(self, args):
        """See List."""
        appointments.do_List(self, args)

    def do_schedule(self, args):
        """See Schedule."""
        appointments.do_Schedule(self, args)

    def do_cancel(self, appointment):
        """See Cancel"""
        appointments.do_Cancel(self, appointment)

    def do_exit(self, args):
        """See Exit."""
        appointments.do_Exit(self, args)
        return True


    # Ctrl-D or EOF will close the interpreter
    def do_EOF(self, args):
        """Closes the interpreter."""
        return True

if __name__ == '__main__':
    appointments().cmdloop()


##       TODO:
##       Write Tests, test log output
##       Documentation/ README

