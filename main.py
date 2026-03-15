import sys

from aid_api.ai_dungeon_scenario_loader import AIDungeonAPI
from authentication.ai_dungeon_auth import AIDAuthenticator
from dungeon_looter import DungeonLooter

GUEST = "AIzaSyCnvo_XFPmAabrDkOKBRpbivp5UH8r_3mg"


def main():
    if not len(sys.argv) in (3, 4):
        print("Usage: main.py <url_id> <character_export_path> [lore_export_path]")
    auth = AIDAuthenticator(GUEST)
    api = AIDungeonAPI(auth)
    looter = DungeonLooter(api)
    looter.import_scenario(sys.argv[1], resolve_questions=True)
    looter.export_character(sys.argv[2])
    if len(sys.argv) == 4:
        looter.export_lore_book(sys.argv[3])


if __name__ == "__main__":
    main()
