### Import Modules

import datetime as dt
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def new_alert_message(sensor_index, verified_number = True):
    '''
    Get a message for a new alert at a sensor_index
    # Composes and returns a single message
    '''
    
        
    # Short version (1 segment)
    
    message = '''SPIKE ALERT!
Air quality may be unhealthy in your area'''
    
    # URLs cannot be sent until phone number is verified
    if verified_number:
        message = message + f'''
map.purpleair.com/?select={int(sensor_index)}/44.9723/-93.2447'''
    else:
        message = message + '''
        Please see PurpleAir'''
        
    message = message + '''
    
Text STOP to unsubscribe'''
        
    return message


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def end_alert_message(duration, max_reading, report_id, base_report_url, verified_number = True):
    '''
    Get a list of messages to send when an alert is over

    inputs:
    duration = integer (number of minutes)
    max_reading = float
    report_id = string
    base_report_url is a string links directly to REDCap comment survey
    
    Returns a message (string)
    '''
        
    message = f'''Alert Over
Duration: {int(duration)} minutes 
Max value: {max_reading} ug/m3

Report here - '''
    
    # URLs cannot be sent until phone number is verified
    if verified_number:
        message = message + f"{base_report_url+ '&report_id=' + report_id}"
    else:
        message = message + f'URL coming soon... Report ID: {report_id}'
    # See https://help.redcap.ualberta.ca/help-and-faq/survey-parameters for filling in variable in url
        
    return message
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def afterhour_ended_alert_message(start_time, duration, max_reading, report_id, base_report_url, verified_number = True):
    '''
    Get a list of messages to send when an alert is over

    inputs:
    duration = integer (number of minutes)
    max_reading = float
    report_id = string
    base_report_url is a string links directly to REDCap comment survey
    
    Returns a message (string)
    '''
    
    time_string = start_time.strftime('%H:%M') + '-' + (start_time + dt.timedelta(minutes=duration)).strftime('%H:%M')
    message = f'''Overnight Alert
Timespan {time_string}
Max value: {max_reading} ug/m3

Report here - '''
    
    # URLs cannot be sent until phone number is verified
    if verified_number:
        message = message + f"{base_report_url+ '&report_id=' + report_id}"
    else:
        message = message + f'URL coming soon... Report ID: {report_id}'
    # See https://help.redcap.ualberta.ca/help-and-faq/survey-parameters for filling in variable in url
        
    return message
    
def no_location(signUp_url):
    '''
    Composes a message informing a user of misentered locations 
    '''
    
    message = f'''Hello, this is SpikeAlerts. 

We're sorry, no location was entered in your form. Please resubmit.

{signUp_url}'''

    return message
    
def welcome_message():
    '''
    Composes a message welcoming a new user!
    '''

    message = '''Welcome to SpikeAlerts! 

We will text 8am-9pm when air quality seems unhealthy (using 24 hour Standard) within 1 kilometer of your survey location.

Consider alerts as a caution and stay vigilant!

For questions see SpikeAlerts.github.io/Website

Reply STOP to end this service. Msg&Data Rates May Apply'''

    return message
