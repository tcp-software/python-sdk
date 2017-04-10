# -*- coding: utf-8 -*-
"""
 * ShiftPlanning Python SDK
 * Version: 1.0
 * Date: 11/01/2010
 * http://www.humanity.com/api/
 
All methods are called using perform_request() method. Supplying correct 'key'
while initiating a ShiftPlanning object is important otherwise things won't work
as expected and an exception will be thrown. All successful HTTP responses from the
API are like following
{
  "success": "1",
  "data": {
    "employee": {
      "name": "Ryan Fyfe",
      "email": "ryan@humanity.com",
      "etc": "..."
    },
    "business": {
      "name": "ShiftPlanning Inc.",
      "etc": "..."
    }
  },
  "token": "xxxxxxx"
}
As you can see the actual data is present as the value of the key 'data'. So as
soon as you perform an API function via ShiftPlanning object you can always acess
this 'data' value by calling get_response_data(). So for example, if you call
shift_planning_obj.get_messages() and the call is successful then you can access the
'data' by calling shift_planning_obj.get_public_data().
Likewise, the whole response object (which is essentially a dictionary) is called
via shift_planning_obj.get_raw_response().
"""

import codecs
import mimetypes
import os
import simplejson
import types
import urllib
import urllib2

response_codes = {
    '-3':'Flagged API Key - Pemanently Banned',
    '-2' : 'Flagged API Key - Too Many invalid access attempts - contact us',
    '-1' : 'Flagged API Key - Temporarily Disabled - contact us',
    '1' : 'Success -',
    '2' : 'Invalid API key - App must be granted a valid key by ShiftPlanning',
    '3' : 'Invalid token key - Please re-authenticate',
    '4' :  'Invalid Method - No Method with that name exists in our API',
    '5' : 'Invalid Module - No Module with that name exists in our API',
    '6' : 'Invalid Action - No Action with that name exists in our API',
    '7' : 'Authentication Failed - You do not have permissions to access the service',
    '8' : 'Missing parameters - Your request is missing a required parameter',
    '9' :  'Invalid parameters - Your request has an invalid parameter type',
    '10' :'Extra parameters - Your request has an extra/unallowed parameter type',
    '12' :'Create Failed - Your CREATE request failed',
    '13' :'Update Failed - Your UPDATE request failed',
    '14' :'Delete Failed - Your DELETE request failed',
    '20' :'Incorrect Permissions - You don\'t have the proper permissions to access this',
    '90' :'Suspended API key - Access for your account has been suspended, please contact ShiftPlanning',
    '91' :'Throttle exceeded - You have exceeded the max allowed requests. Try again later.',
    '98' :'Bad API Paramaters - Invalid POST request. See Manual.',
    '99' :'Service Offline - This service is temporarily offline. Try again later.'
}

internal_errors = {
    '1':'The requested API method was not found in this SDK.',
    '2':'The ShiftPlanning API is not responding.',
    '3':'You must use the login method before accessing other modules of this API.',
    '4':'A session has not yet been established.',
    '5':'You must specify your Developer Key when using this SDK.',
    '6':'The ShiftPlanning SDK needs the CURL PHP extension.',
    '7':'The ShiftPlanning SDK needs the JSON PHP extension.',
    '8':'File doesn\'t exist.',
    '9':'Could not find the correct mime for the file supplied.',
}

class ShiftPlanning(object):
    def __init__(self,key,username,password):
        self.session_identifier = "SP"
        self.api_endpoint = "https://www.humanity.com/api/"
        self.output_type = "json"
        self.request = None
        self.token = None
        self.response = None
        self.response_data = None
        self.callback = None
        self.username = username
        self.password = password
        try:
            self.key = key
        except:
            raise Exception(internal_errors['5'])
    
    def __repr__(self):
         return "<Shift-planning Python API: Endpoint=%s, Key=%s,Username=%s>" %\
            (self.api_endpoint,self.key,self.username)
    
    def set_callback(self,callback):
        """Returns a callback if callback is a valid function"""
        if type(callback) == types.FunctionType:
            self.callback = callback
            
        return (None, "Callback isn't a valid function")
    def get_public_data(self):
        if not self.response_data:
            return "Data was empty in the response object (no data was sent from server)."
        if self.token and self.response_data:
            return self.response_data
        
        return (None,"User hasn't been authenticated")
    
    def get_raw_resopsne(self):
        if self.response:
            return self.response
        return (None,"No raw response available")
    
    def get_app_token(self):
        if self.token:
            return self.token
        else:
            raise Exception(internal_errors[4])
            
    def do_login(self):
        params = {
            "module":"staff.login",
            "method":"GET",
            "username":self.username,
            "password":self.password
        }
        self.perform_request(params)
    def do_logout(self):
        params = {
            'module':'staff.logout',
            'method':'GET'
        }
        self.perform_request(params)
        
    def get_api_config(self):
        params = {
            'module':'api.config',
            'method':'GET'
        }
        self.perform_request(params)
        if self.response['status']['code'] == 1:
            self.token = None
            self.response_data = None
        
    def perform_request(self,params,filedata=None):
        """This method performs a HTTP request. If token isn't set and 'filedata' parameter isn't set
        then we make a login request otherwise this method make requests depending on how it's called.
        Uploading a file is different in that data of the file is sent in 'filedata' along side
        'data' POST variable. """
        data = ''
        if self.token and not filedata:
            data = urllib.urlencode([('data', simplejson.dumps({'token':self.token,'request':params}))])
        if filedata:#it's a file upload
            data = simplejson.dumps({'token':self.token,'request':params})
            data = urllib.urlencode([('data', data),('filedata',filedata)])
            
        if not self.token and not filedata:#this is a login request
            data = urllib.urlencode([('data', simplejson.dumps({'key':self.key,'request':params}))])
        
        req = urllib2.Request(self.api_endpoint,headers={'accept-charset':'UTF-8'})
        try:
            reader = urllib2.urlopen(req, data)
        except:
            raise Exception("Cannot open the URL, please make sure API endpoint is correct.")
        if reader.code != 200:
            raise Exception(internal_errors[2])
        response = reader.read()
        #print response
        if response == "":
            #self.response_data = {''
            return (None, "No JSON object received from server.")
        response = simplejson.loads(response)
        
        if response.has_key('error'):
            return {'error':response['error']}
        else:
            self.response_data = response['data']
            self.response = response
            if self.callback:
                self.callback()
        if params['module'] == 'staff.login':
            if response.has_key('token'):
                self.token = response['token']
        
        
    def get_content_type(self,file_path):
        return mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        
    def get_file_size(self,file_path):
        return os.path.getsize(file_path)
        
    def get_file_data(self,file_path):
        data= open(file_path,'r').read()
        return data
    
     
    def create_admin_file(self,file_path):
        """Expects a file path. Parameter 'file_path' can be calculated like
        file_path = os.path.normpath('c:\test.pdf'). Note that in params we're only setting
        filename, file-length and mimetype. Data of the file is sent to
        perform_request() where it's sent along side 'data' POST variable. """
        filename = os.path.basename(file_path)
        params = {
            'module':'admin.file',
            'method':'CREATE',
            'filename':filename,
            'filelength':self.get_file_size(file_path),
            'mimetype': self.get_content_type(file_path),
            
        }
        
        
        self.perform_request(params,self.get_file_data(filename))
    def get_api_methods(self):
        params = {
            'module':'api.methods',
            'method':'GET'
        }
        self.perform_request(params)
        
    
    def create_admin_backup(self,backup_details):
        if not backup_details: return None
        filename = backup_details
        #we expect filename, filelength and mimetype in backup_details
        params = {
            'module':'admin.backup',
            'method':'CREATE'
            
        }
        params.update(backup_details)
        self.perform_request(params,self.get_file_data(filename))
    
    def get_admin_backup_details(self,id):
        params = {
            'module':'admin.backup',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
        
    def get_admin_backups(self):
        params = {
            'module':'admin.backups',
            'method':'GET'
        }
        self.perform_request(params)
        
    
    def delete_admin_backup(self,id):
        params = {
            'module':'admin.backup',
            'method':'DELETE',
            'id':str(id)
            
        }
        self.perform_request(params)
    
    def delete_admin_file(self,id):
        params = {
            'module':'admin.file',
            'method':'DELETE',
            'id':str(id)
        }
        self.perform_request(params)
    def get_admin_file_details(self,id):
        params = {
            'module':'admin.file',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
    
    def get_admin_files(self):
        params = {
            'module':'admin.files',
            'method':'GET'
        }
        self.perform_request(params)
        
    
    def update_admin_file(self,id, details):
        if not details: return None
        params = {
            'module':'admin.file',
            'method':'UPDATE',
            'id':str(id)
        }
        params.update(details)
        self.perform_request(params)
        
    
    def update_admin_settings(self,settings):
        if not settings:  return None
        params = {
            'module':'admin.settings',
            'method':'UPDATE'
        }
        
        params.update(settings)
        self.perform_request(params)
        
        
    def get_admin_serttings(self):
        params = {
            'module':'admin.settings',
            'method':'GET'
        }
        self.perform_request(params)
        
    
    def get_scheduler_conflicts(self,time_period):
        if time_period: return None
        params = {
            'module':'schedule.conflicts',
            'method' :'GET'
        }
        
        params.update(time_period)
        self.perform_request(params)
        
    
    def delete_vacation_schedule(self,id):
        params = {
            'module':'schedule.vacation',
            'method':'DELETE',
            'id':str(id)
        }
        self.perform_request(params)
    def update_vacation_schedule(self,id,vacation_details):
        if not vacation_details: return None
        params = {
            'module':'schedule.vacation',
            'method':'UPDATE',
            'id':str(id)
        }
       
        params.update(vacation_details)
        self.perform_request(params)
            
    def create_vacation_schedule(self,vacation_details):
        """Creates a vacation schedule and the parameter 'vacation_details' might
        look something like {'start_date':'14 December 2010','end_date':'24 December 2010'}"""
        if not vacation_details: return None
        params = {
            'module':'schedule.vacation',
            'method': 'CREATE'
        }
        
        params.update(vacation_details)
        self.perform_request(params)
        
    def get_vacation_schedule_details(self,id):
        params = {
            'module':'schedule.vacation',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
        
    def get_vacation_schedules(self,time_period=None):
        params = {
            'module':'schedule.vacations',
            'method':'GET'
        }
        if time_period: params.update(time_period)
        self.perform_request(params)
        
    def delete_shift(self,id):
        params = {
            'module':'schedule.shift',
            'method':'DELETE',
            'id':str(id)
        }
        self.perform_request(params)
        
    def create_shift(self,shift_details):
        """Creates a shift and parameter 'shift_details' might look like
        {'start_time':'9:00 am','end_time':'12:00 pm','start_date':'24 December 2010',
        'end_date':'24 December 2010','schedule':'343434'}"""
        if not shift_details: return None
        params = {
            'module':'schedule.shift',
            'method':'CREATE'
        }
        
        params.update(shift_details)
        self.perform_request(params)
    def update_shift(self,id,shift_details):
        if not shift_details: return None
        params = {
            'module':'schedule.shift',
            'method':'UPDATE',
            'id':str(id)
        }
        
        params.update(shift_details)
        self.perform_request(params)
    
    def get_shift_details(self,id):
        params = {
            'module':'schedule.shift',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
        
    
    def get_shifts(self):
        params = {
            'module':'schedule.shifts',
            'method':'GET'
        }
        self.perform_request(params)
        
    
    def delete_schedule(self,id):
        params = {
            'module':'schedule.schedule',
            'method':'DELETE',
            'id':str(id)
        }
        self.perform_request(params)
    
    def update_schedule(self,id,schedule_details):
        if not schedule_details: return None
        params = {
            'module':'schedule.schedule',
            'method':'UPDATE',
            'id':str(id)
        }

        params.update(params)
        self.perform_request(params)
    def create_schedule(self,schedule_details):
        """Creates a schedule. Parameter 'schedule_details' expects a dictionary which
        might look something like {'name':'Very important architecture overview!'}"""
        if not schedule_details: return None
        params = {
            'module':'schedule.schedule',
            'method':'CREATE'
        }
        
        params.update(schedule_details)
        self.perform_request(params)
    def get_schedule_details(self,id):
        params = {
            'module':'schedule.schedule',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
        
    
    def get_schedules(self):
        params = {
            'module':'schedule.schedules',
            'method':'GET'
        }
        self.perform_request(params)
        
    
    def create_staff_ping(self,ping_data):
        """Creates a ping that goes to a staff member. Parameter 'ping_data' expects
        a dictionary which might look like {'to':'id-goes-here','message':'this is just a ping'}"""
        if not ping_data: return None
        params = {
            'module':'staff.ping',
            'method':'CREATE'
        }
        
        self.perform_request(ping_data)
    def delete_staff_skill(self,id):
        params = {
            'module':'staff.skill',
            'method':'DELETE',
            'id':str(id)
            
        }
        self.perform_request(params)
    
    def update_staff_skill(self,id,skill_details):
        if not skill_details: return None
        params = {
            'module':'staff.skill',
            'method':'UPDATE',
            'id':str(id)
        }
        params.update(skill_details)
        self.perform_request(params)
    
    def create_staff_skill(self,skill_details):
        """Creates staff skill. Parameter 'skill_details' is a dict and it might
        look like {'name':'technical leadership'}"""
        if not skill_details: return None
        params = {
            'module':'staff.skill',
            'method':'CREATE'
        }
        
        params.update(skill_details)
        self.perform_request(params)
    
    def get_staff_skill_details(self,id):
        params = {
            'module':'staff.skill',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
        
    def get_staff_skills(self):
        params = {
            'module':'staff.skill',
            'method':'GET'
        }
        self.perform_request(params)
        
    def delete_employee(self,id):
        params = {
            'module':'staff.employee',
            'method':'DELETE',
            'id':str(id)
        }
        self.perform_request(params)
    def create_employee(self,details):
        """Creates an employee. Parameter 'details' is a dictionary and it might
        look like {'name':'Ryan'}"""
        if not details:return None
        params = {
            'module':'staff.employee',
            'method':'CREATE'
        }
       
        params.update(details)
        self.perform_request(params)
    def update_employee(self,id,data):
        if not data: return None
        params = {
            'module':'staff.employee',
            'method':'UPDATE',
            'id':str(id)
        }
        
        params.update(data)
        self.perform_request(params)
    def get_employee_details(self,id):
        params = {
            'module':'staff.employee',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
        
    def get_employees(self):
        params = {
            'module':'staff.employees',
            'method':'GET'
        }
        self.perform_request(params)
        
        
    def delete_wall_message(self,id,details):
        if not details: return None
        params= {
            'module':'messaging.wall',
            'method':'DELETE',
            'id':str(id)
        }
        
        params.update(details)
        self.perform_request(params)
    
    def create_wall_message(self,message):
        """Creates a wall message. Paramter 'message' might look
        something like {'title':'fun weather','post':'cool weather'}"""
        if not message: return None
        params= {
            'module':'messaging.wall',
            'method':'CREATE'
        }
        params.update(message)
        self.perform_request(params)
    def get_wall_messages(self):
        params= {
            'module':'messaging.wall',
            'method':'GET'
        }
        self.perform_request(params)
        
    def delete_message(self,id):
        params= {
            'module':'messaging.message',
            'method':'DELETE',
            'id':str(id)
        }
        self.perform_request(params)
    def create_message(self,message):
        """Creates a messages. Parameter 'message' might look something like
        {'message':'this is a beautiful day.','subject':'weather','to':'here-goes-id'}"""
        if not message: return None
        params= {
            'module':'messaging.message',
            'method': 'CREATE'
        }
        params.update(message)
        self.perform_request(params)
            
    def get_message_details(self,id):
        params= {
            'module':'messaging.message',
            'method':'GET',
            'id':str(id)
        }
        self.perform_request(params)
        
    def get_messages(self):
        params= {
            'module':'messaging.messages',
            'method':'GET'
        }
        self.perform_request(params)
        
        
  
