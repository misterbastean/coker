import os
import subprocess
import csv
import logging
import time
import sys
import random

# =====================================================
# CONFIG
# =====================================================
GAM = '/Users/homefolder/bin/gamadv-xtd/gam'  # Full path required; cannot use ~ for home directory
driveEmail = "backupdrive@company.com"  # This is where the Drive files will be transferred

# Setup Logging Config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # https://docs.python.org/3/library/logging.html#logging.Logger.setLevel
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')  # https://docs.python.org/3/library/logging.html#formatter-objects
fileHandler = logging.FileHandler('logs.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


# =====================================================
# FUNCTIONS
# =====================================================
def random_pass():
    s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    p = "".join(random.sample(s, 20))
    return p


def change_password(username):
    logger.info(f"Updating password for {username} to random string")
    print(f"Updating password for {username} to random password")
    logger.debug("Generating random password")
    new_pass = random_pass()
    result = os.system(f'{GAM} update user {username} password {new_pass}')
    if result == 0:
        logger.info(f"Successfully updated password for {username} to random string.")
        print(f"Successfully updated password for {username} to random string.")
    else:
        logger.error(f"Error updating password for {username} to random string. Process aborted.")
        logger.error(f"Errored password: {new_pass}")
        print(f"Error updating password for {username} to random string. Process aborted.")
        sys.exit()


def set_vacation(username, subject, message):
    logger.info('Starting vacation message process.')
    print('Starting vacation message process.')
    logger.debug(f'Subject: {subject}')
    logger.debug(f'Message: {message}')
    result = os.system(f'{GAM} user {username} vacation on subject "{subject}" message "{message}"')
    if result == 0:
        logger.info(f'Vacation message process complete.')
        print(f'Vacation message process complete.')
    else:
        logger.error("Error setting vacation email")
        print("Error setting vacation email")
        sys.exit()


def remove_forwarding(username):
    logger.info(f'Disabling email forwarding for {username}')
    print(f'Disabling email forwarding for {username}')
    result = os.system(f'{GAM} user {username} forward off')
    if result == 0:
        logger.info('Email forwarding disabled successfully.')
        print('Email forwarding disabled.')
    else:
        logger.error("Error removing email forwarding")
        print("Error removing email forwarding")
        sys.exit()


def forward_to_manager(username, manager_email):
    logger.info('Beginning forward to manager process')
    print('Beginning forward to manager process')
    if not manager_email:
        logger.info("No manager email included, so no forwarding will be enabled")
        print("No manager email included, so no forwarding will be enabled")
    else:
        logger.info(f"Forwarding email to {manager_email}")
        print(f"Forwarding email to {manager_email}")
        result_a = os.system(f'{GAM} user {username} add forwardingaddress {manager_email}')
        result_b = os.system(f'{GAM} user {username} forward on {manager_email} archive')
        if result_a == 0 and result_b == 0:
            logger.info('Forwarding email process complete')
            print('Forwarding email process complete')
        elif result_a != 0:
            logger.error(f"Error adding {manager_email} to forwarding addresses for {username}")
            print(f"Error adding {manager_email} to forwarding addresses for {username}")
        elif result_b != 0:
            logger.error(f"Error enabling forwarding to {manager_email}")
            print(f"Error enabling forwarding to {manager_email}")
        else:
            logger.error("Generic error setting up email forwarding. Aborting process.")
            print("Generic error setting up email forwarding. Aborting process.")
            sys.exit()


def remove_tokens(username):
    logger.info("Removing OAUTH tokens and 2FA backup codes")
    print('Removing OAUTH tokens and 2FA backup codes')
    result = os.system(f'{GAM} user {username} deprovision')
    if result == 0:
        logger.info("Successfully removed OAUTH tokens and 2FA backup codes")
        print("Successfully removed OAUTH tokens and 2FA backup codes")
    else:
        logger.error("Error removing OAUTH tokens and 2FA backup codes. Aborting process.")
        print("Error removing OAUTH tokens and 2FA backup codes. Aborting process.")
        sys.exit()


def transfer_drive(username, drive_transfer_recipient):  # DONE
    print(drive_transfer_recipient)
    if not drive_transfer_recipient:
        logger.info(f"Transferring Drive ownership to {driveEmail}")
        print(f"Transferring Drive ownership to {driveEmail}")
        result = os.system(f'{GAM} create datatransfer {username} drive {driveEmail} all')
        if result == 0:
            logger.info(f"Successfully transferred Drive ownership from {username} to {driveEmail}")
            print(f"Successfully transferred Drive ownership from {username} to {driveEmail}")
        else:
            logger.info(f"Error transferring Drive ownership to {driveEmail}. Aborting process.")
            print(f"Error transferring Drive ownership to {driveEmail}. Aborting process.")
            sys.exit()
    else:
        logger.info(f"Transferring Drive ownership to {drive_transfer_recipient}")
        print(f"Transferring Drive ownership to {drive_transfer_recipient}")
        result = os.system(f'{GAM} create datatransfer {username} drive {drive_transfer_recipient} all')
        if result == 0:
            logger.info(f"Successfully created data transfer from {username} to {drive_transfer_recipient}")
            print(f"Successfully created data transfer from {username} to {drive_transfer_recipient}")
        else:
            logger.error(f"Error transferring Drive ownership to {drive_transfer_recipient}. Process aborted.")
            print(f"Error transferring Drive ownership to {drive_transfer_recipient}. Process aborted.")
            sys.exit()


def remove_delegates(username):  # DONE
    logger.info("Removing email delegates")
    print("Removing email delegates")
    delegates_list = []
    cmd = f'{GAM} user {username} print delegates'
    try:
        output = subprocess.check_output(cmd, shell=True)
        logger.debug(f"output: {output}")
        delegates = output.decode().split("\n")
        logger.debug(f"delegates: {delegates}")
        logger.debug("Trimming delegates - 1st and last")
        del delegates[0]
        del delegates[-1]
        for delegate in delegates:
            delegate_email = delegate.split(",")[1]
            logger.debug(f"Deleting delegate: {delegate_email}")
            result = os.system(f'{GAM} user {username} delete delegate {delegate_email}')
            if result == 0:
                delegates_list.append(delegate_email)
                logger.debug(f"Successfully deleted delegate {delegate_email}")
            else:
                logger.error(f"Error deleting delegate {delegate_email}")
                print(f"Error deleting delegate {delegate_email}")
        logger.info(f'The following delegates were removed: {delegates_list}')
        print(f'The following delegates were removed: {delegates_list}')
    except OSError as e:
        logger.error(f"Error running {cmd}")
        print(f"Error running {cmd}")
        print(e)


def disable_imap_pop(username):  # DONE
    logger.info(f"Disabling IMAP and POP for {username}")
    print(f"Disabling IMAP and POP for {username}")
    result_1 = os.system(f'{GAM} user {username} imap off')
    result_2 = os.system(f'{GAM} user {username} pop off')
    if result_1 == 0 and result_2 == 0:
        logger.info(f"Successfully disabled IMAP and POP for {username}")
        print(f"Successfully disabled IMAP and POP for {username}")
    elif result_1 == 0 and result_2 != 0:
        logger.info(f"Successfully disabled IMAP for {username}")
        logger.error(f"Error disabling POP for {username}")
        print(f"Successfully disabled IMAP for {username}")
        print(f"Error disabling POP for {username}")
    elif result_1 != 0 and result_2 == 0:
        logger.error(f"Error disabling IMAP for {username}")
        logger.info(f"Successfully disabled POP for {username}")
        print(f"Error disabling IMAP for {username}")
        print(f"Successfully disabled POP for {username}")
    else:
        logger.error(f"Errors disabling both IMAP and POP for {username}")
        print(f"Errors disabling both IMAP and POP for {username}")


def hide_from_directory(username):
    logger.info(f'Hiding {username} from directory')
    print(f'Hiding {username} from directory')
    result = os.system(f'{GAM} update user {username} gal off')
    if result == 0:
        logger.info(f"Successfully hid {username} from directory")
        print(f"Successfully hid {username} from directory")
    else:
        logger.error(f"Error hiding {username} from directory")
        print(f"Error hiding {username} from directory")


def remove_from_groups(username):  # DONE
    logger.info(f'Removing {username} from all groups')
    print(f'Removing {username} from all groups')
    groups_list = []
    cmd = f'''{GAM} info user {username} | grep -A 10000 "Groups:"'''
    logger.debug(f'''{GAM} info user {username} | grep -A 10000 "Groups:"''')
    try:
        output = subprocess.check_output(cmd, shell=True)
        output_split = output.decode().split("\n")
        del output_split[0]
        del output_split[-1]
        logger.debug(f"output_split: {output_split}")
        for group in output_split:
            group_email = group.split(":")[1].strip()
            logger.debug(f"group_email: {group_email}")
            result = os.system(f'{GAM} update group {group_email} remove member {username}')
            if result == 0:
                groups_list.append(group_email)
                logger.debug(f"Successfully removed {username} from {group_email}")
                logger.debug(f"group_email ongoing: {group_email}")
            else:
                logger.error(f"Error removing {username} from {group_email}")
                print(f"Error removing {username} from {group_email}")
        logger.info(f"Successfully removed user from the following groups: {groups_list}")
        print(f"Successfully removed user from the following groups: {groups_list}")
    except Exception as e:
        logger.info(f'Did not remove {username} from any groups.')
        logger.info(e)
        print(f'Did not remove {username} from any groups.')
        print(e)


def suspend(username):
    logger.info(f'Suspending {username}')
    print(f'Suspending {username}')
    result = os.system(f'{GAM} update user {username} suspended on')
    if result == 0:
        logger.info(f"{username} suspended successfully.")
        print(f"{username} suspended successfully.")
    else:
        logger.error(f"Error attempting to suspend {username}. Process aborted.")
        print(f"Error attempting to suspend {username}. Process aborted.")
        sys.exit()


def unsuspend(username):
    logger.info(f'Unsuspending {username}')
    print(f'Unsuspending {username}')
    result = os.system(f'{GAM} update user {username} suspended off')
    if result == 0:
        logger.info(f"Successfully unsuspended {username}")
        print(f"Successfully unsuspended {username}")
    else:
        logger.error(f"Error attempting to unsuspend {username}. Process aborted.")
        print(f"Error attempting to unsuspend {username}. Process aborted.")
        sys.exit()


# =====================================================
# USER LEAVING (RUN FOR EACH LINE OF CSV)
# =====================================================
def user_leaving(username, remain_active, vacation_subject, vacation_message, manager_email, drive_transfer_recipient):
    # Tasks for all users
    change_password(username)
    remove_forwarding(username)
    remove_tokens(username)
    remove_delegates(username)
    disable_imap_pop(username)
    remove_from_groups(username)
    suspend(username)
    transfer_drive(username, drive_transfer_recipient)

    # Tasks for users whose email WILL remain active
    if remain_active.lower() == "y":
        set_vacation(username, vacation_subject, vacation_message)
        forward_to_manager(username, manager_email)
        unsuspend(username)

    # Tasks for users whose email will NOT remain active
    else:
        hide_from_directory(username)


# =====================================================
# MAIN
# =====================================================
def main():
    logger.info("Beginning bulk offboard process.")
    logger.debug("Opening users.csv file")
    with open('test_users.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                logger.debug('Skipping header row in csv')
                line_count += 1
            logger.info('=============================================')
            logger.info(f'Beginning offboard process for {row["email"]}')
            logger.info('=============================================')
            logger.debug(f'Data for row {line_count}: {row}')
            user_leaving(row["email"], row["remainActive"], row["vacationSubject"], row["vacationMessage"],
                         row["managerEmail"], row["driveTransferRecipient"])
            line_count += 1
            time.sleep(1)


if __name__ == '__main__':
    main()
