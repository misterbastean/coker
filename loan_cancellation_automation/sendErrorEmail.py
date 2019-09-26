import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, json

# Setup logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
fileHandler = logging.FileHandler('logs/sendErrorEmail.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


def sendErrorEmail():
    try:
        # Get login info from config.json
        logger.debug('Getting data from config.json')
        configData = {}
        try:
            with open('config.json') as jsonFile:
                data = json.load(jsonFile)
                configData['fromAddress'] = data['fromEmailAddress']
                configData['fromPassword'] = data['fromEmailPassword']
                configData['toAddress'] = data['toEmailAddress']
        except Exception as e:
            logger.error('There was a problem accessing data in config.json', exc_info=True)
            print('crap 2')

        # Build email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Error in Loan Cancellation Emailer'
        msg['From'] = configData['fromAddress']
        msg['To'] = configData['toAddress']
        bodyHtml = """\
        There was a problem with the loan cancellation emailer. Look at the logs.<br /><br />It's on the Informer server,
        in C:/Student_Accounts.<br /><br />Documentation is here: https://docs.google.com/document/d/1KG23DHmCp2YXrKCD65EqP8Dtauy9M5g4ttv8kFEGC2g
        """

        # Record MIME type - text/html
        emailText = MIMEText(bodyHtml, 'html')
        # Attach to message container
        msg.attach(emailText)

        logger.info('Connecting to gmail server to send error notification')
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        logger.info('Successfully connected to gmail server')

        # login and send email, then log out
        logger.info("Logging into gmail.")
        server_ssl.login(configData['fromAddress'], configData['fromPassword'])
        server_ssl.sendmail(configData['fromAddress'], configData['toAddress'], msg.as_string())
        server_ssl.close()
    except Exception as e:
        logger.error('Unable to send email.', exc_info=True)
        print('crap')