import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from os.path import dirname, abspath, join
import configparser
from GarageWarden import status


class InvalidConfigError(Exception):
    pass


# Get the path of this file, then get the directory from it, then the parent directory, then look for the file there
mailconfig_path = join(dirname(dirname(abspath(__file__))), 'mailconfig.ini')
__parser = configparser.ConfigParser()
__parser.read(mailconfig_path)
config = __parser['mail']

try:
    enabled = config.getboolean('enabled')
except Exception:
    raise InvalidConfigError("mail enabled is not a valid config boolean. "
                             "See https://docs.python.org/3/library/configparser.html#supported-datatypes")

if enabled:
    host = config['host']
    encryption = (config['encryption'] or '').lower()
    username = config['username']
    password = config['password']
    recipients = config['recipients']
    _from = config['from'] or 'GarageWarden'
    try:
        port = config.getint('port')
    except Exception:
        raise InvalidConfigError('mail port cannot be empty or is not a number')

    if not config['host']:
        raise InvalidConfigError('mail host cannot be empty')
    if not encryption or encryption not in ['ssl', 'tls', 'none']:
        raise InvalidConfigError("Unknown mail encryption")

    if not recipients:
        raise InvalidConfigError('no mail recipients set')

    # split the string and dump out any empty strings in case there are any
    recipients = [email.strip() for email in recipients.split(';') if email]

    if len(config['recipients']) < 1:
        raise InvalidConfigError('No mail recipients set, or recipients is invalid')


def send_mail(state, color, date):
    if not enabled:
        pass

    if encryption == 'ssl':
        smtp = smtplib.SMTP_SSL(host=host, port=port)
    else:
        smtp = smtplib.SMTP(host=host, port=port)

    if encryption == 'tls':
        smtp.starttls()

    if username and password:
        smtp.login(username, password)

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Garage " + state
    msg['From'] = _from
    msg['To'] = ", ".join(recipients)
    msg.attach(MIMEText(make_text(state, date), "plain"))
    msg.attach(MIMEText(make_html(state, color, date), "html"))
    smtp.sendmail(_from, recipients, msg)


def make_html(state, color, date):
    return "Garage was <span style='color: " + color + "'><strong>" + state + "</strong></span> at <i>" + date + "</i>"


def make_text(state, date):
    return "Garage was " + state + " at " + date


was_open = False
was_closed = False


def init_state():
    global was_closed, was_open
    was_open = status.garage_is_full_open()
    was_closed = status.garage_is_full_close()


def state_change_notify(channel):
    global was_open, was_closed
    now = datetime.now()
    now_str = now.strftime("%d-%b-%Y %H:%M:%S")
    print("State changed on channel:" + channel + " at" + now_str)
    is_closed = status.garage_is_full_close()
    is_open = status.garage_is_full_open()

    if is_open and was_closed:
        send_mail("Opened", "#f0ad4e", now_str)
    elif is_closed and was_open:
        send_mail("Closed", "#5cb85c", now_str)

    was_closed = is_closed
    was_open = is_open
