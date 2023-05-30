from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

collect_infos_from_cellmates = []


class CheckGuessAction(Action):
    def name(self) -> Text:
        return "check_guess"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 获取用户的猜测和角色信息
        guess = tracker.get_slot("profession")
        talked_person = tracker.get_slot("person")
        A = "Prison Guard"
        B = "Janitor"
        C = "Pilot"
        print(tracker.get_slot("profession"))
        print(tracker.get_slot("person"))
        if guess and talked_person:
            if talked_person == 'A' and A == guess:
                dispatcher.utter_message(text="A: Hi, you guess correct!")
                dispatcher.utter_message(text="There are 4 locations in the prisons")
                dispatcher.utter_message(text="Now I can tell you the location 1 and 2...")
                dispatcher.utter_message(text="That was all I know..")
                if 'room1' not in collect_infos_from_cellmates and 'room2' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room1')
                    collect_infos_from_cellmates.append('room2')
            elif talked_person == 'B' and B == guess:
                dispatcher.utter_message(text="B: Hi, you guess correct!")
                dispatcher.utter_message(text="I can tell you the location 3 and 4...")
                dispatcher.utter_message(text="That was all I know..")
                if 'room3' not in collect_infos_from_cellmates and 'room4' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room3')
                    collect_infos_from_cellmates.append('room4')
            elif talked_person == 'C' and C == guess:
                dispatcher.utter_message(text="C: Hi, you guess correct!")
                dispatcher.utter_message(text="I can tell you the location 5 and 6")
                dispatcher.utter_message(text="That was all I know..")
                if 'room5' not in collect_infos_from_cellmates and 'room6' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room5')
                    collect_infos_from_cellmates.append('room6')
            else:
                dispatcher.utter_message(text="Wrong！Game Over")
        else:
            dispatcher.utter_message(text="I don't understand you sorry.")

        if len(collect_infos_from_cellmates) == 6:
            dispatcher.utter_message(text="Now you have collect all the location information")
            dispatcher.utter_message(
                text="For the next step, you can choose Cellmates for join you to escape, which would you like to select")
            return [SlotSet('select_member', True)]
        else:
            dispatcher.utter_message(text="For more location infos you need ask other cellmates..")
        return [SlotSet("profession", None), SlotSet("person", None)]


class CheckSelectAction(Action):
    def name(self) -> Text:
        return "check_asked_mates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'person']
        if len(entities) == 3:
            dispatcher.utter_message(
                text="Now A, B and C are in your team! For the next step you can check the locations and plan to acess")
            return []
        else:
            dispatcher.utter_message(
                text="Game over! Because the mates know all your plan and intent, not selected mates ratted you out")
            return []


class ShowLocationAction(Action):
    def name(self) -> Text:
        return "show_collection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('select_member'))
        if tracker.get_slot('select_member'):
            dispatcher.utter_message(
                text="there are Cell, Infirmary, Kitchen, Laundry Room, Warden's office and Heli Pad, which do you plan to access next")
        else:
            dispatcher.utter_message(text="Now you are not able check all locations")


class AccessLocationInfirmary(Action):
    def name(self) -> Text:
        return "access_infirmary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('get_punched'))
        if tracker.get_slot('get_punched'):
            dispatcher.utter_message(
                text="Now you are in the Infirmary")
            return [SlotSet("location_Infirmary", True), SlotSet("location_cell", False), SlotSet('get_punched', False)]
        else:
            dispatcher.utter_message(text="You are not able in to Infirmary")
