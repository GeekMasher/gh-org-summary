"""GitHub Advanced Security Organization CSV Exporter."""

from argparse import Namespace
from dataclasses import dataclass
import logging
import os
import csv
import json
from typing import Any, Optional

logger = logging.getLogger(__name__)

try:
    from ghastoolkit import (
        GitHub,
        Repository,
        Enterprise,
        Organization,
        CodeScanning,
        Dependabot,
        SecretScanning,
    )
    from ghastoolkit.utils.cli import CommandLine
except:
    print("Failed to load `ghastoolkit`")
    print("please install it")
    exit(1)

HEADERS = "owner,name,code_scanning,dependabot,secret_scanning"


def saveCache(path: str, data: dict):
    """Save the cache to a file."""
    logger.info(f"Saving cache to {path}")

    with open(path, "w") as f:
        f.write(json.dumps(data))


def loadCache(path: str) -> dict[str, dict[str, Any]]:
    """Load the cache from a file."""
    logger.info(f"Loading cache from {path}")
    if not os.path.exists(path):
        # create the file
        with open(path, "w") as f:
            f.write("{}")
        return {}
    with open(path, "r") as f:
        return json.loads(f.read())


@dataclass
class RepositoryData:
    owner: Optional[str] = None
    name: Optional[str] = None

    # counts
    code_scanning: Optional[int] = None
    dependabot: Optional[int] = None
    secret_scanning: Optional[int] = None

    error: Optional[str] = None

    def createRow(self, headers: list[str]) -> list[str]:
        """Create a row for the CSV file."""
        result = []
        for header in headers:
            if hasattr(self, header):
                result.append(getattr(self, header))
        return result

    def isError(self) -> bool:
        if (
            self.code_scanning is None
            or self.dependabot is None
            or self.secret_scanning is None
        ):
            return True

        if self.error:
            return True

        return False

    def __str__(self) -> str:
        if self.isError():
            return f"{self.owner}/{self.name} (error)"
        return f"{self.owner}/{self.name}"


class CLI(CommandLine):
    def arguments(self):
        """Add arguments to the parser."""
        parser = self.parser.add_argument_group("csv")
        parser.add_argument("--headers", default=HEADERS, help="CSV headers")
        parser.add_argument("--output", default="output.csv", help="CSV output file")

        parser_caching = self.parser.add_argument_group("caching")
        parser_caching.add_argument(
            "--cache-dir", default=".cache", help="Cache directory"
        )
        parser_caching.add_argument("--cache-ignore-errors", action="store_true")
        parser_caching.add_argument("--cache-frequency", default=1, type=int)

    def run(self, arguments: Namespace):
        ent = Enterprise(arguments.enterprise)

        logger.info(f"GitHub :: {GitHub.instance}")

        if not GitHub.token:
            logger.error("No token provided")
            GitHub.token = input("Please provide PAT: ")
            if not GitHub.token:
                logger.error("No token provided")
                exit(1)

        if arguments.owner:
            orgs = [Organization(arguments.owner)]
        else:
            logger.info("Getting all organizations on the enterprise")
            orgs = ent.getOrganizations()

        logger.debug(f"Organizations:  {len(orgs)}")

        skipped = 0
        results = []

        for organization in orgs:
            logger.info(f"Organization: {organization.name}")

            # caching
            cache_path = os.path.join(arguments.cache_dir, f"{organization.name}.json")
            cache_counter = 0
            os.makedirs(arguments.cache_dir, exist_ok=True)

            cache = loadCache(cache_path)

            try:
                result = organization.rest.get(f"/orgs/{organization.name}/repos")

                for repo in result:
                    repo = Repository.parseRepository(repo.get("full_name"))
                    # check cache
                    if cache.get(repo.repo):
                        result = RepositoryData(**cache.get(repo.repo))

                        if result.isError() and arguments.cache_ignore_errors:
                            print(f" - {result} (cached, error ignored)")
                            result.error = None
                        else:
                            if result.isError():
                                skipped += 1
                                print(f" - [E] {result}")
                            else:
                                print(f" - [C] {result}")
                            results.append(result)
                            continue

                    print(f" - [F] {repo}")

                    code_scanning = CodeScanning(repo)
                    dependabot = Dependabot(repo)
                    secret_scanning = SecretScanning(repo)

                    result = RepositoryData(owner=repo.owner, name=repo.repo)

                    try:
                        if code_scanning.isEnabled():
                            result.code_scanning = len(code_scanning.getAlerts())
                        else:
                            result.code_scanning = -1

                        if secret_scanning.isEnabled():
                            result.secret_scanning = len(secret_scanning.getAlerts())
                        else:
                            result.secret_scanning = -1

                        if dependabot.isEnabled():
                            result.dependabot = len(dependabot.getAlerts())
                        else:
                            result.dependabot = -1

                    except KeyboardInterrupt as err:
                        raise err

                    except Exception as e:
                        logger.error(f"Error getting alerts for {repo}")
                        if arguments.debug:
                            logger.error(e)
                        result.error = str(e)
                        skipped += 1

                    results.append(result)

                    cache_counter += 1
                    if cache_counter >= arguments.cache_frequency:
                        # save cache
                        cache[repo.repo] = result.__dict__
                        saveCache(cache_path, cache)
                        cache_counter = 0

            except KeyboardInterrupt:
                print("Halting...")
                break

            except Exception as e:
                logger.error(e)
                if arguments.debug:
                    raise e
            finally:
                # save cache
                saveCache(cache_path, cache)

        # write to csv
        headers = arguments.headers.split(",")
        logger.info(f"Writing CSV to {GitHub.repository.owner}.csv")

        with open(arguments.output, "w") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for result in results:
                writer.writerow(result.createRow(headers))

        logger.info(f"Skipped `{skipped}` repositories")


if __name__ == "__main__":
    try:
        cli = CLI()
        cli.run(cli.parse_args())
    except Exception as err:
        logger.error(err)
        exit(1)
