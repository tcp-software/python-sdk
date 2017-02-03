#!/usr/bin/env python
import os
import shift_planning
  
    
def say_hello():
    print('hi')
    
if __name__ == "__main__":
    key = "your token goes here"
    username = 'username'
    pwd = 'password'
    s = shift_planning.ShiftPlanning(key,username,pwd)
    s.set_callback(say_hello)
    s.do_login()
    #file upload test: make sure you've a test1.pdf in this directory
    file_path = os.path.normpath('test1.pdf')
    s.create_admin_file(file_path)
    creating and message
    s.create_message({'message':'this is a beautiful day.','subject':'weather','to':'14320'})
    s.get_messages()
    print(s.get_public_data())
    #creating a wall message
    s.create_wall_message({'title':'fun weather','post':'cool weather'})
    s.get_wall_messages()
    print(s.get_public_data())
    #creating an employee
    s.create_employee({'name':'Paul'})
    s.get_employees()
    print(s.get_public_data())
    s.get_employee_details('14304')
    print(s.get_public_data())
    #creating a staff skill
    s.create_staff_skill({'name':'technical leadership'})
    s.get_staff_skills()
    print(s.get_public_data())
    #creating a staff ping
    s.create_staff_ping({'to':'14304','message':'this is just a ping'})
    s.create_schedule({'name':'Very important architecture overview!'})
    s.get_schedules()
    print(s.get_public_data())
    #creating a shift
    s.create_shift({'start_time':'10:00 am','end_time':'11:00 pm','start_date':'24 December 2010',
                    'end_date':'25 December 2010','schedule':'99'})
    s.get_shifts()
    print(s.get_public_data())
    #creating a vacation schedule
    
    s.create_vacation_schedule({'start_date':'29 December 2010','end_date':'10 January 2011'})
    
    
    
    
