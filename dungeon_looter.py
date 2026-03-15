import json
import re
from typing import Optional

from aid_api.ai_dungeon_scenario_loader import AIDungeonAPI
from aid_objects.scenario import AidScenario


class DungeonLooter:
    def __init__(self, api: AIDungeonAPI):
        self.api = api
        self.scenario: Optional[AidScenario] = None

    def import_scenario(self, short_id: str, resolve_questions: bool = True):
        raw_scenario = self.api.import_scenario(short_id)
        if resolve_questions:
            raw_scenario = self.resolve_questions(raw_scenario)
        self.scenario = self.parse_scenario_schema(raw_scenario)

    def export_character(self, export_path: str) -> None:
        if not self.scenario:
            return
        file = open(export_path, "w")
        json.dump(self.scenario.get_character(), file)

    def export_lore_book(self, export_path: str) -> None:
        if not self.scenario:
            return
        file = open(export_path, "w")
        json.dump(self.scenario.get_lore_book(), file)

    @staticmethod
    def resolve_questions(raw_scenario: str):
        """
        Resolve scenario parameters that require user input, such as "What is your name?" and "Describe your appearance"
        :param raw_scenario: A string representing the scenario's prompt, plot essentials, character cards, author's
        note.
        :return: The updated string.
        """
        print("Resolving user input.")
        while (matched_str := re.search(r"\$\{([^}]+)\}", raw_scenario)):
            answer = input(matched_str.group(1) + "\n")
            raw_scenario = raw_scenario.replace(matched_str.group(0), answer, -1)
        return raw_scenario

    @staticmethod
    def parse_scenario_schema(raw_response: str) -> AidScenario:
        response_json = json.loads(raw_response)
        scenario_json = response_json["data"]["scenario"]
        return AidScenario.model_validate_json(json.dumps(scenario_json))
