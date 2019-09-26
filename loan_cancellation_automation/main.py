import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv, logging, sys
from sendErrorEmail import sendErrorEmail
from time import sleep

"""
TODO:
- Build the entire nested array of user data and write together instead of doing it row by row. This is to overcome 
API limits of 100 per second per user
    
Possible Problems:
1. Names with strange characters
"""

# Setup logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
fileHandler = logging.FileHandler('logs/main.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


def readCsv(inputCsv):
    logger.info('updateCsv function started')
    output = []
    logger.debug(f"Getting info from {inputCsv}")
    try:
        logger.debug(f"Opening csv file: {inputCsv}")
        with open(inputCsv, 'r') as file:
            logger.debug("csv file opened successfully")
            next(file)  # Skip the header row
            fileReader = csv.reader(file)
            for row in fileReader:
                newRow = row
                try:
                    # Format money string
                    logger.info(f'Formatting money on row: {row}')
                    rawAmount = row[3].replace(',','')
                    logger.debug(f'rawAmount: {rawAmount}')
                    floatAmount = float(rawAmount)
                    newAmount = '${:,.2f}'.format(floatAmount)
                    newRow[3] = newAmount
                    logger.debug('Finished formatting money')
                except:
                    logger.info("Problem formatting money. This probably means it's an empty field")
                logger.debug(f"Appending row: {newRow}")
                output.append(newRow)
                logger.debug('Row successfully appended')
        logger.debug(f"Info from {inputCsv} read")
        logger.info(f'Output from inputCsv: {output}')
        return output
    except Exception as e:
        logger.error("Exception occurred, stopping program", exc_info=True)
        sendErrorEmail()
        sys.exit()


def gSuite(data, key):
    logger.info('gSuite function started')
    logger.debug(f'Data: {data}')

    # G-Suite Auth
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    logger.debug(f'Google API scope set to: {scope}')
    logger.debug("Getting credentials from API_Keys.json")
    credentials = ServiceAccountCredentials.from_json_keyfile_name('API_Keys.json', scope)  # Add API Keys file downloaded from Google in the same directory
    try:
        logger.debug("Authorizing gspread with provided credentials")
        gc = gspread.authorize(credentials)
    except Exception as e:
        logger.error("Unable to authorize gspread, stopping program", exc_info=True)
        sendErrorEmail()
        sys.exit()

    # Get Correct Spreadsheet
    try:
        logger.debug(f"Accessing spreadsheet with id {key}")
        spreadsheet = gc.open_by_key(key)  # Update key to new Sheet if needed

        # Populate Google Sheet with new data
        spreadsheet.values_append(
            'data!A1',
            params={'valueInputOption': 'RAW'},
            body={'values': data}
        )
        logger.debug(f'Data appended: {data}')
    except Exception as e:
        logger.error('Error adding data to spreadsheet, stopping program', exc_info=True)
        sendErrorEmail()
        sys.exit()


def main(inputCsv, key):
    logger.info("=====STARTED MAIN FUNCTION=====")
    # Get raw data from csv
    data = readCsv(inputCsv)
    # Loop through data, merging email addresses
    i = 0
    logger.debug("Begin while loop")
    while i < len(data):
        try:
            if data[i+1][0] is '':
                # Add second email to first row
                newData = '|' + data[i+1][8]
                logger.debug(f'Adding email {data[i+1][8]} to {data[i][8]}')
                data[i][8] += newData
                # Delete second row
                logger.info(f'Deleting second row on iteration {i}')
                del data[i+1]
            i += 1
        except Exception as e:
            logger.error("Error in main while loop, stopping program", exc_info=True)
            sendErrorEmail()
            sys.exit()

    # Write data to sheet
    gSuite(data, key)


try:
    main('XBOL_Daily.csv', '1TIJMpx_hUJ-L0SbA3R0XlDBhISrdYJJ6prc1JsBSSA4')
    logger.info('=====MAIN FUNCTION RAN SUCCESSFULLY=====')
except Exception as e:
    logger.error('=====ERROR IN MAIN FUNCTION=====', exc_info=True)