import argparse
import os
import dotenv
from datetime import date, datetime

# Load the environment variables from a .env (dotenv) file.
# This is done prior to importing other modules such that all variables,
# also the ones accessed in those modules, can be set in the dotenv file.
dotenv.load_dotenv()

def load_variable(env_var, secrets_file):
    """Load a variable from an environment variable or from a secrets file"""
    # Try to read the value from the secrets file. Silently fail if the file
    # cannot be read and use an empty value
    try:
        with open(secrets_file, encoding='utf-8') as secret:
            value = secret.read().strip("\n")
    except OSError:
        value = ""

    # Load variable from environment if it exists, otherwise use the
    # value read from the secrets file.
    return os.getenv(env_var, value)


GARMIN_USERNAME = load_variable('GARMIN_USERNAME', "/run/secrets/garmin_username")
GARMIN_PASSWORD = load_variable('GARMIN_PASSWORD', "/run/secrets/garmin_password")
TRAINERROAD_USERNAME = load_variable('TRAINERROAD_USERNAME', "/run/secrets/trainerroad_username")
TRAINERROAD_PASSWORD = load_variable('TRAINERROAD_PASSWORD', "/run/secrets/trainerroad_password")

def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description=(
            "A tool for synchronisation of Withings "
            "(ex. Nokia Health Body) to Garmin Connect"
            " and Trainer Road or to provide a json string."
        )
    )

    def date_parser(date_string):
        return datetime.strptime(date_string, "%Y-%m-%d")

    parser.add_argument("--server",
                        action="store_true",
                        help="Run server mode"
    )
    
    parser.add_argument("--port",
                        nargs='?',
                        type= int,
                        default=8000,
                        help="Choose on which port run server mode"
    )

    parser.add_argument(
        "--garmin-username",
        "--gu",
        default=GARMIN_USERNAME,
        type=str,
        metavar="GARMIN_USERNAME",
        help="Username to log in to Garmin Connect.",
    )
    parser.add_argument(
        "--garmin-password",
        "--gp",
        default=GARMIN_PASSWORD,
        type=str,
        metavar="GARMIN_PASSWORD",
        help="Password to log in to Garmin Connect.",
    )

    parser.add_argument(
        "--trainerroad-username",
        "--tu",
        default=TRAINERROAD_USERNAME,
        type=str,
        metavar="TRAINERROAD_USERNAME",
        help="Username to log in to TrainerRoad.",
    )

    parser.add_argument(
        "--trainerroad-password",
        "--tp",
        default=TRAINERROAD_PASSWORD,
        type=str,
        metavar="TRAINERROAD_PASSWORD",
        help="Password to log in to TrainerRoad.",
    )

    parser.add_argument(
        "--fromdate", "-f",
        type=date_parser,
        metavar="DATE",
        help="Date to start syncing from. Ex: 2023-12-20",
    )

    parser.add_argument(
        "--todate", "-t",
        type=date_parser,
        default=date.today(),
        metavar="DATE",
        help="Date for the last sync. Ex: 2023-12-30",
    )

    parser.add_argument(
        "--to-fit", "-F",
        action="store_true",
        help="Write output file in FIT format.",
    )

    parser.add_argument(
        "--to-json",
        "-J",
        action="store_true",
        help="Write output file in JSON format.",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        metavar="BASENAME",
        help="Write downloaded measurements to file.",
    )

    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Won't upload to Garmin Connect or TrainerRoad.",
    )

    parser.add_argument(
        "--features",
        nargs='+',
        default=[],
        metavar="BLOOD_PRESSURE",
        help="Enable Features like BLOOD_PRESSURE."
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Run verbosely."
    )

    return parser.parse_args()

ARGS = get_args()
