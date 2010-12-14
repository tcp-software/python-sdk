ShiftPlanning Python SDK
================

The [ShiftPlanning API](http://www.shiftplanning.com/api/) allows you to call modules within the ShiftPlanning [employee scheduling software](http://www.shiftplanning.com/) that respond in REST style JSON & XML.

This repository contains the open source Python SDK that allows you to utilize the
above on your website. Except as otherwise noted, the ShiftPlanning Python SDK
is licensed under the Apache Licence, Version 2.0
(http://www.apache.org/licenses/LICENSE-2.0.html)


Usage
-----

The following are a good place to start. The minimal you'll need to
have is:

    if __name__ == "__main__":
        key = "your token goes here"
        username = 'username'
        pwd = 'password'
        s = shift_planning.ShiftPlanning(key,username,pwd)

To make [API] calls:
        Following is an example
	shift_planning_obj.create_message({'message':'this is a beautiful day.','subject':'weather','to':'14320'})
        
To Login

	shift_planning_obj.do_login()
and logout
        shift_planning_obj.do_logout()

[API]: http://www.shiftplanning.com/api/


Feedback
--------

We are relying on the [GitHub issues tracker][issues] linked from above for
feedback. File bugs or other issues [here][issues].

