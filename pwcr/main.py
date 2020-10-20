import click
import subprocess
from datetime import datetime, timedelta
import csv

GAM_PATH = "/Users/joshuabastean/bin/gamadv-xtd3/gam"


@click.command()
@click.option('--months', '-m', default=1,
              help='Number of months to check, 1-6. Defaults to 1.')
@click.option('--changed/--not-changed', '-c/-nc', default=False, help="Find uses who have changed or not changed their password. Defaults to not-changed.")
@click.option('--out', '-o', help="[OPTIONAL] Filename for output (must be .csv)")
@click.argument('org_unit', type=click.STRING, default="/Students", required=False)
def main(org_unit, months, changed, out):
    """This tool checks G-Suite for users who have not updated their passwords in a given timeframe."""
    users = find_unchanged_users(org_unit, months)
    outfile = ""
    if out:
        if out.endswith(".csv"):
            outfile = out
        else:
            outfile = out + ".csv"
    if changed:
        if out:
            with open(outfile, 'w') as f:
                writer = csv.writer(f)
                writer.writerow("username")
                for user in users['changed']:
                    writer.writerow([user])
        else:
            click.echo(f"Total users who have changed their password in the last {months} month(s): {len(users['changed'])}")
            click.echo(users['changed'])
    else:
        if out:
            with open(outfile, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["username"])
                for user in users['not_changed']:
                    writer.writerow([user])
        else:
            click.echo(f"Total users who have not changed their password in the last {months} month(s): {len(users['not_changed'])}")
            click.echo(users['not_changed'])


def get_all_usernames(ou):
    """Returns all usernames for the given OU."""
    if ou != "/":
        sp = subprocess.Popen([GAM_PATH, "print", "users", "query", f"orgUnitPath={ou}"],
                              stdout=subprocess.PIPE)
        data = sp.stdout.readlines()
        output = []
        for user in data:
            output.append(user.decode()[:-1])
        return output
    else:
        sp = subprocess.Popen(
            [GAM_PATH, "print", "users"],
            stdout=subprocess.PIPE)
        data = sp.stdout.readlines()
        output = []
        for user in data:
            output.append(user.decode()[:-1])
        return output


def get_all_pw_users(months):
    """Gets the usernames for all password change events in the previous given months."""
    today = datetime.today()
    last = today - timedelta(days=30*months)
    sp = subprocess.Popen([GAM_PATH, "report", "admin", "user", "sada.admin", "event",
                           "CHANGE_PASSWORD", "range", last.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")],
                          stdout=subprocess.PIPE)
    all_events = sp.stdout.readlines()
    usernames = extract_usernames(all_events)
    return usernames


def extract_usernames(events):
    """Extracts the username from a list of password change events."""
    output = []
    for event in events:
        separate = event.decode().split(",")
        output.append(separate[1])
    return output


def find_unchanged_users(org_unit, months):
    """Returns a dict of users separated by if they have changed their password or not

    :param org_unit: A string of the full G-Suite org unit (e.g. "/Faculty/Adjunct"
    :param months: Number of months to include in search (API limits to 6)
    :return: Dict of users separated into "changed" and "not_changed"
    """
    users = sorted(get_all_usernames(org_unit))  # Get all usernames in the given OU
    pw_users = sorted(get_all_pw_users(months))  # Get all password change events in the last X month(s)
    return {
        "not_changed": set(users).difference(pw_users),
        "changed": set(users).intersection(pw_users)
    }


if __name__ == '__main__':
    main()
