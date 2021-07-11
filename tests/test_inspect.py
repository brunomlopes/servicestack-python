"""Inspect APIs
"""

import operator
import unittest

import requests
from dataclasses_json import config, dataclass_json, Undefined

from servicestack.utils import *


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GithubRepo:
    name: str
    description: Optional[str] = None
    homepage: Optional[str] = None
    lang: Optional[str] = field(metadata=config(field_name="language"), default=None)
    watchers: Optional[int] = 0
    forks: Optional[int] = 0


class TestTechStacks(unittest.TestCase):

    def test_does_dump(self):
        org_name = "python"
        response = requests.get(f'https://api.github.com/orgs/{org_name}/repos')
        org_repos = GithubRepo.schema().loads(response.text, many=True)
        org_repos.sort(key=operator.attrgetter('watchers'), reverse=True)

        print(f'Top 3 {org_name} Repos:')
        printdump(org_repos[0:3])

        print(f'\nTop 10 {org_name} Repos:')
        printdumptable(org_repos[0:10], headers=['name', 'lang', 'watchers', 'forks'])

        inspect_vars({'org_repos': org_repos})