#!/usr/bin/env python

'''
Below is a working example of a server-side script, in Python. In our case the script is
in the file http://lab-perception.org/js/savedata.py. It can be used to receive the data
and store it in a file with a unique name (0001.dat, 0002.dat, etc.), together with a date
and time, and to optionally send the data to an email address. Similar scripts can of course
be written in PHP or other server scripting languages.

When testing, don't forget the set permissions (read and execute for the script, write for the
directory where the data files will go: in our case, ./data). Also make sure that your server
will execute the script. In my case (Apache 2), I added the following lines the configuration
file:
<Directory "/var/www/html/js">
	Require all granted
	Options +ExecCGI
	AddHandler cgi-script .cgi .py
</Directory>
<Directory "/var/www/html/js/data">
	Require all denied
</Directory>

Also note that if the server-side script isn't on the same site that served the client script
(for example, if you simply execute the client script from a file on your own machine), this
would be an example of Cross-Origin Resource Sharing (CORS), and needs to be handled carefully
(see https://web.dev/cross-origin-resource-sharing/).
'''

import cgi, os, datetime, re
import smtplib
from email.mime.text import MIMEText

DATA_DIR = './data'             # the directory in which to put the data file
SUFFIX = 'dat'
EMAIL_FROM = 'Mark Wexler <mark@lab-perception.org>'
EMAIL_SMTP = 'localhost'

dt = datetime.datetime.now()    # get current date and time (put it as a comment at the beginning of the data file)
millis = int(round(float(dt.microsecond)/1000.0))
now = dt.strftime('%Y-%m-%d-%H-%M-%S') + '-' + ('%03d' % millis)

fs = cgi.FieldStorage()         # get the data field
data = fs.getfirst('data')

os.chdir(DATA_DIR)              # get the next unused name for a data file
file_names = os.listdir('.')    # order is 0001.dat, 0002.dat, etc.
existing = []
for file_name in file_names:
    m = re.match(r'^([0-9]+)\.' + SUFFIX + r'$', file_name)
    if m:
        existing.append(int(m.group(1)))
if existing:
    n = max(existing) + 1
else:
    n = 1
data_fn = '%04d.%s' % (n, SUFFIX)

fp = open(data_fn, 'wt')        # save the data
fp.write('# ' + now + '\n')     # first the date and time as a comment
fp.write(data)                  # then the contents of the data field
fp.close()

# send the data by email, if we got an email address
if 'email' in fs:
    email = fs.getfirst('email').strip()
    if email:
        msg = MIMEText(data)
        msg['Subject'] = 'data from on-line experiment'
        msg['From'] = EMAIL_FROM
        msg['To'] = email
        s = smtplib.SMTP(EMAIL_SMTP)
        s.sendmail(EMAIL_FROM, [email], msg.as_string())
        s.quit()

print('Content-Type: text/html')    # you have to send something back
print('')                           # even if it won't be displayed
print('ok')
