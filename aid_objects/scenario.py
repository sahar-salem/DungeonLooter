from typing import List

from pydantic import BaseModel

from aid_objects.default_export_options import DEFAULT_LORE_CARD, DEFAULT_CHARACTER, DEFAULT_CHARACTER_DATA


class AID_StoryCard(BaseModel):
    type: str
    value: str
    keys: str
    title: str
    def to_lore(self, uid: int, **kwargs):
        result = {
            "uid": uid,
            "key": [key.strip() for key in self.keys.split(",")],
            "comment": self.title,
            "content": f"Type: {self.type}\nContent:{self.value[1:len(self.value)-1]}",
            **DEFAULT_LORE_CARD
        }
        for key,val in kwargs:
            if result.get(key):
                result[key] = val
        return result

class AID_scenario_state(BaseModel):
    prompt: str
    plotEssentials: str
    authorsNote: str


class AidScenario(BaseModel):
    image: str
    storyCards: List[AID_StoryCard] = []
    state: AID_scenario_state
    title: str
    tags: List[str]
    def get_lore_book(self, **kwargs):
        if not self.storyCards:
            return {"entries": {}}
        entries = {i: card.to_lore(i, **kwargs) for i, card in enumerate(self.storyCards)}
        return {
            "entries": entries
        }
    def get_character(self):
        plot_essentials = self.state.plotEssentials if self.state.plotEssentials else ""
        instructions = self.state.plotEssentials if self.state.plotEssentials else ""
        result = {
            "data": {
                "name": self.title,
                "personality": "This is a narrator for a scenario, with various characters:\n" + self.state.authorsNote,
                "scenario": "[Note: second person refers to the user.]\n" + self.state.plotEssentials,
                "first_mes": self.state.prompt,
                **DEFAULT_CHARACTER_DATA
            },
            "name": f"Narrator: {self.title}",
            "personality": "This is a narrator for a scenario, with various characters:\n" + self.state.authorsNote,
            "scenario": "[Note: second person refers to the user.]\n" + self.state.plotEssentials,
            "first_mes": self.state.prompt,
            "tags": self.tags,
            **DEFAULT_CHARACTER
        }
        return result
