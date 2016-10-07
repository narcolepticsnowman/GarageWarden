import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from django.http import HttpResponse
from GarageWarden import status, settingHelper, settingView, config, settings as gw_settings
import RPi.GPIO as GPIO

settings = None
settings_loaded = False


def reload_config():
    global settings, settings_loaded
    settings_loaded = True
    settings = settingHelper.values_for_prefix("email")


settingView.reload_methods['notify'] = reload_config


def send_mail(subject, text, html=None):
    
    if not get_setting('enabled'):
        print('email not enabled')
        return
    encryption = (get_setting('encryption') or '').lower()
    host = get_setting('host')
    port = int(get_setting('port'))
    if encryption == 'ssl':
        smtp = smtplib.SMTP_SSL(host=host, port=port)
    else:
        smtp = smtplib.SMTP(host=host, port=port)

    if encryption == 'tls':
        smtp.starttls()

    if get_setting('username') and get_setting('password'):
        smtp.login(get_setting('username'), get_setting('password'))

    _from = get_setting('from name') or 'GarageWarden'
    recipients = get_setting('recipients')
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = recipients
    if text:
        msg.attach(MIMEText(text, "plain"))
    if html:
        msg.attach(MIMEText(html, "html"))
    smtp.sendmail(_from, [r.strip() for r in recipients.split(',') if r], msg.as_string())


def send_state_change_mail(state, color, date):
    if get_setting('Status Notification'):
        send_mail("Garage " + state, make_text(state, date), make_html(state, color, date))
    else:
        print('status emails not enabled')


def make_html(state, color, date):
    return "Garage was <span style='color: " + color + "'><strong>" + state + "</strong></span> at <i>" + date + "</i>"


def make_text(state, date):
    return "Garage was " + state + " at " + date


def state_change():
    now = datetime.now()
    now_str = now.strftime("%d-%b-%Y %H:%M:%S")
    opened = status.garage_is_full_open()
    closed = status.garage_is_full_close()
    print("State changed to opened: "+str(opened)+" closed: "+str(closed)+" at" + now_str)

    if opened:
        send_state_change_mail("Opened", "#f0ad4e", now_str)
    elif closed:
        send_state_change_mail("Closed", "#5cb85c", now_str)


config.state_change_callbacks['notify'] = state_change


def test_email(request):
    global settings
    print('sending test emails')
    if not get_setting('enabled'):
        return HttpResponse("Email not enabled")
    send_state_change_mail("Test", "#5bc0de", datetime.now().strftime("%d-%b-%Y %H:%M:%S"))
    return HttpResponse("Test email sent")


def get_setting(setting):
    if not settings_loaded:
        reload_config()
    return settings[setting]


def start_beep():
    GPIO.output(gw_settings.BEEPER_PIN, True)


def stop_beep():
    GPIO.output(gw_settings.BEEPER_PIN, False)
