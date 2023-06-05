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
        if tracker.get_slot('get_punched'):
            #and tracker.get_slot('location_cell')
                #and 0 == infirmary_count:
            dispatcher.utter_message(text="Now you are in the Infirmary")
            dispatcher.utter_message(text="you are lying on a patient bed, a trainee nurse is taking care of you")
            infirmary_count = 1
            return [SlotSet("location_Infirmary", True), SlotSet("location_cell", False), SlotSet('get_punched', False)]
        else:
            dispatcher.utter_message(text="You are not able in to Infirmary")

class AbleCheck(Action):
    def name(self) -> Text:
        return "able_check_infirmary"

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
            #return [SlotSet("nurse_away", False)]
        else:
            dispatcher.utter_message(text="You can't check infirmary, you are not alone sofar")



class Get_sedative(Action):
    def name(self) -> Text:
        return "get_sedative"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Infirmary'):
            entities = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'ingredients']
            print(entities)
            if len(entities) != 4:
                dispatcher.utter_message(text='It failed! You need to give four ingredients')
            else:
                if 'Lavender' in entities and 'Sunflower' in entities and 'Cayenne Pepper' in entities and 'Bioluminescent Algae' in entities:
                    dispatcher.utter_message(text='Now you get the sedative!')
                    dispatcher.utter_message(text='As you know the laundry room direct near from the infirmary')
                    dispatcher.utter_message(text='Now you are able to check locations, plan for the next step')
                    return [SlotSet('get_sedative', True),  SlotSet("location_Infirmary", False), SlotSet("location_cell", True)]
                else:
                    dispatcher.utter_message(text='You guess the wrong ingredients!')
        else:
            dispatcher.utter_message(text='You can not do this, because you are not in the Infirmary')


class ShowLaundryRoom(Action):
    def name(self) -> Text:
        return "show_Laundry_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='Now you are alone in the laundry room')
        dispatcher.utter_message(text='Here you can see some lockers, some washing machines, and a dirty clothes basket')
        dispatcher.utter_message(text='Check them for finding useful things!')
        return [SlotSet('location_Laundry_room', True), SlotSet("location_Infirmary", False),SlotSet("location_cell", False)]


class Show_locker_puzzles_or_other_unuseful_items(Action):
    def name(self) -> Text:
        return "show_locker_puzzles_or_other_unuseful_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Laundry_room'):
            checkitem = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'items_in_Laundry_room']
            print(checkitem)
            if 'washing machines' in checkitem:
                dispatcher.utter_message(text='they are nothing specials')
            elif 'lockers' in checkitem:
                dispatcher.utter_message(text='The lockers are locked. Inside should be something important')
                dispatcher.utter_message(text='Please give 5 digits code for open lockers')

            elif 'clothes basket' in checkitem:
                dispatcher.utter_message(text='In the dirty clothes basket you find a note left behind" There are five riddles on the note')
                dispatcher.utter_message(text='Clue 1: "The first digit is the square root of 16."')
                dispatcher.utter_message(text='Clue 2: "The second digit is the sum of 3 and 5."')
                dispatcher.utter_message(text='Clue 3: "The third digit is one less than the fourth digit."')
                dispatcher.utter_message(text='Clue 4: "The fourth digit is twice the second digit."')
                dispatcher.utter_message(text='Clue 5: "The fifth digit is the difference between the third digit and the first digit."')
            else:
                dispatcher.utter_message(text='No such item in the laundry room, pls try again')
        else:
            dispatcher.utter_message(text="You can't do this, you are not in laundry room")


class OpenLockers(Action):
    def name(self) -> Text:
        return "vertification_locker_puzzles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Laundry_room'):
            code = [e['value'] for e in tracker.latest_message['entities'] if
                         e['entity'] == 'numbercode']
            print(code)
            if len(code) != 5:
                dispatcher.utter_message('Please give 5 digits code')
            elif code == ['4','8','15','8','11']:
                dispatcher.utter_message('You give the correct codes. Now the locker is opened.')
                dispatcher.utter_message('You get the guards uniforms!')
                dispatcher.utter_message('Nothing else is nessesary in the laundry room. You are back to your cell')
                return [SlotSet('location_Laundry_room', False),SlotSet("location_cell", True), SlotSet('get_uniform', True)]
            else:
                dispatcher.utter_message('You gives the wrong code')
        else:
            dispatcher.utter_message(text="You can't do this, you are not in laundry room")


class Gokitchen(Action):
    def name(self) -> Text:
        return "show_Kitchen_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('get_uniform') == True:
            dispatcher.utter_message('You need to guess the correct vegetables from puzzle to open the door')
            dispatcher.utter_message("In the kitchen's realm of scraps and remains, seek the food that the dogs will claim. A taste of delight, they yearn to savor, find the dish that matches their favorite flavor. Look to the label, it holds the key, the name of the food that sets them free. It's not a meat, but something green, a vegetable that makes them keen. Search high and low, with keen eyesight, and choose the food that feels just right. What am I?")
            dispatcher.utter_message('Please give the correct vegetable')
            return [SlotSet('location_Kitchen', True)]
        else:
            dispatcher.utter_message(' You ran into the patrol officers, you do not have any uniform cover, you are arrested')

class KitchenCode(Action):
    def name(self) -> Text:
        return "vertification_Kitchens_code_and_show_kitchen_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Kitchen'):
            kitchencode = [e['value'] for e in tracker.latest_message['entities'] if
                    e['entity'] == 'vegetables']
            if 'Brocolli' in kitchencode:
                dispatcher.utter_message('Pin correct! Know you are in the Kitchen')
                dispatcher.utter_message('You can see delicious food being cooked on the stove, which should be the food for the prison guards. You are now very tired and hungry. ')
                dispatcher.utter_message('Now make decision:')
                dispatcher.utter_message('drug: You want to drug the food with sedative')
                dispatcher.utter_message('eat: You want to fill yourself up first')
                return [SlotSet('kitchen_door', True)]
            else:
                dispatcher.utter_message('You give the wrong Pin')

        else:
            dispatcher.utter_message('You can not do this action now')

class KitchenFood(Action):
    def name(self) -> Text:
        return "vertification_Kitchen_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Kitchen') and tracker.get_slot('get_uniform'):

            kitchenfood = [e['value'] for e in tracker.latest_message['entities'] if
                               e['entity'] == 'dealwithfood']
            if 'eat' in kitchenfood:
                dispatcher.utter_message('You get caught, because you wast too many time for eating')
            elif 'drug' in kitchenfood:
                if tracker.get_slot('get_sedative'):
                    dispatcher.utter_message('Now you have successfully drug the food with sedatives, the guards will get fainted as they eat the food')
                    dispatcher.utter_message('You can select the next location you want to move on')
                    return [SlotSet('location_Kitchen',False),SlotSet('guards_fainted',True)]
                elif tracker.get_slot('get_sedative') == False:
                    dispatcher.utter_message("You don't have medical for drug the food")
                    dispatcher.utter_message("Please check other locations for getting drugs at first")
            else:
                dispatcher.utter_message('No this Choice')
        else:
            dispatcher.utter_message('You are not possible do this action')


class OfficeIn(Action):
    def name(self) -> Text:
        return "vertification_guards_fainted_and_show_office_or_getcaught"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('guards_fainted') == False:
            dispatcher.utter_message('The prison guards detect you, and catch you')
        else:
            dispatcher.utter_message('You are successfully in the office')
            dispatcher.utter_message('You can see a transparent cabinet, a telephone on the desk. There is a chair, and a desk lamp.')
            dispatcher.utter_message('Please check the useful item')
            return [SlotSet('location_office', True)]


class OfficeItems(Action):
    def name(self) -> Text:
        return "show_phone_or_other_unuseful_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_office'):
            officeitem = [e['value'] for e in tracker.latest_message['entities'] if
                               e['entity'] == 'items_in_office']
            if 'phone' in officeitem:
                dispatcher.utter_message('You can use the phone to call a important person')
                dispatcher.utter_message('Now the time runs, you can only call one person')
                dispatcher.utter_message('Make a choice, to which Person you want to call')
                dispatcher.utter_message('Son: The son of the pilot cellmate, he is also a pilot')
                dispatcher.utter_message('Friend: Your best friend Stefan, he is also a lawyer, he is rich')

                return [SlotSet('phone_ready',True)]
            elif 'cabinet' in officeitem:
                dispatcher.utter_message('You found a huge check, the payer is hung up by link, the name can be vaguely seen with the beginning of S and end of n')
            else:
                dispatcher.utter_message('Nothing specials')
        else:
            dispatcher.utter_message('You can not do this, because you are not in the office')


class OfficePhone(Action):
    def name(self) -> Text:
        return "vertification_call_with_npc_child_for_helicopter_and_show_puzzles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('phone_ready'):
            calledperson = [e['value'] for e in tracker.latest_message['entities'] if
                          e['entity'] == 'called_person']
            if 'Friend' in calledperson:
                dispatcher.utter_message('Your friend is the guy who makes the corruption to the prison warden with the check')
                dispatcher.utter_message('He reported you, and you are locked up again')
            elif 'Son' in calledperson:
                dispatcher.utter_message("The call to the pilot's son went well, you explained the current situation and requested that he could fly a plane to the prison's Heli_Pad to rescue you.")
                dispatcher.utter_message("The pilot's son says he'll say yes if you can help him answer the following questions correctly")
                dispatcher.utter_message("Riddle 1: I'm a collection of elements, orderly arranged, With a fixed size and type, never to be changed. Sequential access is how I'm designed, Efficiency is key, in memory I'm confined. What am I?")
                dispatcher.utter_message("Riddle 2: I'm like a chain, linking nodes in a line, Traversing me forwards or backwards is fine. I'm flexible, dynamic, and efficient too, Adding or removing elements, I can easily do. What am I?")
                dispatcher.utter_message("Riddle 3: I'm a type, a blueprint of data and behavior, Encapsulating objects, I'm a powerful savior. Inheritance and polymorphism, I embrace, Creating instances, bringing code to life's embrace. What am I?")
                dispatcher.utter_message("Riddle 4: I'm a line, where elements wait in turn, First come, first serve, that's how I churn. Enqueue and dequeue, actions I take, Used in printing, processes, and more, give me a break. What am I?")
                dispatcher.utter_message("Please give your answers in correct orders")
                return [SlotSet('phone_son',True)]
            else:
                dispatcher.utter_message('No this Choice')
        else:
            dispatcher.utter_message('You can not do this action')



class OfficePhone(Action):
    def name(self) -> Text:
        return "check_answer_to_son"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('phone_son'):
            answers = [e['value'] for e in tracker.latest_message['entities'] if
                          e['entity'] == 'answer_to_son']
            print(answers)
            if len(answers) == 4:
                if ['Array', 'Linked List', 'Class', 'Queue']==answers:
                    dispatcher.utter_message('You answer correctly, the Son of pilot cellmate promisse you He will pick you up in a helicopter in half an hour.')
                    dispatcher.utter_message('You can check locations, choose where you want to go as next')
                    return [SlotSet('get_helicopter',True)]
                else:
                    dispatcher.utter_message('You give the wrong answers')

            else:
                dispatcher.utter_message('Please give 4 answers')
        else:
            dispatcher.utter_message('You can not do this action')


