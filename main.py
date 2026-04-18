import argparse
import subprocess
import logging
import sys


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stdout
    )
    return logging.getLogger(__name__)


def run_command(command: str):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description="Simple QC command runner")

    parser.add_argument("--command", required=True, help="Command to execute")
    parser.add_argument("--on_ok", help="Command to run if exit code is 0")
    parser.add_argument("--on_fail", help="Command to run if exit code is non-zero")

    args = parser.parse_args()
    logger = setup_logger()
    
	logger.info(f"Running command: {args.command}")
    
    exit_code, stdout, stderr = run_command(args.command)

    if exit_code == 0:
        logger.info(f"Command succeeded (exit=0)")
        if stdout:
            logger.info(stdout.strip())

        if args.on_ok:
            logger.info(f"Running on_ok command: {args.on_ok}")
            run_command(args.on_ok)

    else:
        logger.error(f"Command failed (exit={exit_code})")
        if stdout:
            logger.error(stdout.strip())
        if stderr:
            logger.error(stderr.strip())

        if args.on_fail:
            logger.error(f"Running on_fail command: {args.on_fail}")
            run_command(args.on_fail)


if __name__ == "__main__":
    main()