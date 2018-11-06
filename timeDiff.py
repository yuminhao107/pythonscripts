import datetime
stra='2015-04-07 04:30:03'
strb='2015-04-07 05:30:03'
a=datetime.strptime(stra,"%Y-%m-%d %H:%M:%S")
b=datetime.strptime(strb,"%Y-%m-%d %H:%M:%S")
(b-a).seconds
