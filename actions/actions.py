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


#infirmary_count = 0


class AccessLocationInfirmary(Action):
    def name(self) -> Text:
        return "access_infirmary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      #  print(tracker.get_slot('get_punched'))
       # global infirmary_count
        if tracker.get_slot('get_punched') and tracker.get_slot('location_cell'):
                #and 0 == infirmary_count:
            dispatcher.utter_message(text="Now you are in the Infirmary")
            dispatcher.utter_message(text="you are lying on a patient bed, a trainee nurse is taking care of you")
            infirmary_count = 1
            return [SlotSet("location_Infirmary", True), SlotSet("location_cell", False), SlotSet('get_punched', False)]
        else:
            dispatcher.utter_message(text="You are not able in to Infirmary")

class AbleCheck(Action):
    def name(self) -> Text:
        return "able_check"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('nurse_away'))
        if tracker.get_slot('location_Infirmary') and tracker.get_slot('nurse_away'):
            dispatcher.utter_message(text="Now you are alone")
            dispatcher.utter_message(text="In this room there is a cabinet with 7 potions ingredients: Lavender, Dandelion. Sunflower, Cayenne Pepper, Aloe Vera, Bioluminescent Algae, Rose")
            dispatcher.utter_message(text="A instructions for making sedative was left from the trainee nurse")
            dispatcher.utter_message(text="The instructions for making sedative was written: There are four components of anesthetics, and you need to guess them correctly through riddles")
            dispatcher.utter_message(text="1 : In moonlit fields, I dance with grace, A bloom of beauty, a soothing embrace. With petals yellow and sweet perfume, I'm the first ingredient, brightening the room.")
            dispatcher.utter_message(text="2 : I'm forged in flames, a fiery birth, A spice so potent, I add zest to mirth. From the tropics, I bring the heat, A pinch of me makes the mixture complete.")
            dispatcher.utter_message(text="3 : A leafy treasure, green and grand, An herb that heals with a gentle hand. With calming scent and medicinal touch, I'm the herb you seek, the third as such.")
            dispatcher.utter_message(text="4 : From the depths of the ocean, I arise, A creature rare, hidden from prying eyes. With slimy skin and healing might, The final ingredient, glowing in the night.")
            dispatcher.utter_message(text="If you want to get the sedative, choose the 4 correct ingredients please")
            return [SlotSet("nurse_away", False)]
        else:
            dispatcher.utter_message(text="You can't check infirmary, you are not alone sofar")



class Get_sedative(Action):
    def name(self) -> Text:
        return "get_sedative"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'ingredients']
        print(entities)
        if len(entities) != 4:
            dispatcher.utter_message(text='It failed! You need to give four ingredients')
        else:
            if 'Lavender' in entities and 'Sunflower' in entities and 'Cayenne Pepper' in entities and 'Bioluminescent Algae' in entities:
                dispatcher.utter_message(text='Now you get the sedative!')
                dispatcher.utter_message(text='After somedays, you getting well, and turnes back to the cell!')
                dispatcher.utter_message(text='Now you are able to check locations, plan for the next step')
                return [SlotSet('get_sedative', True),  SlotSet("location_Infirmary", False), SlotSet("location_cell", True)]
            else:
                dispatcher.utter_message(text='You guess the wrong ingredients!')
