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
                dispatcher.utter_message(text="A: Correct guess my new friend! As a former prison guard, I dedicated my life to upholding justice behind those cold, steel bars. However, fate took a cruel twist, and now I find myself trapped within the very system I once patrolled, facing the consequences of false accusations.")
                dispatcher.utter_message(text="I assume you are trying to escape , if so include me I can help .There are 6 important locations in the prisons")
                dispatcher.utter_message(text="I can tell you about the next one , which is the infirmery you can get sedatives and other drugs from there . And there is also the Laundry room , here you can find fresh or dirty guard outfits , this would be crucial to get in any escape room.")
                dispatcher.utter_message(text="There are 4 other rooms but I the other two cellmates know more about them")
                if 'room1' not in collect_infos_from_cellmates and 'room2' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room1')
                    collect_infos_from_cellmates.append('room2')
            elif talked_person == 'B' and B == guess:
                dispatcher.utter_message(text="B: Right on point new fish, As a dedicated janitor, I meticulously scrubbed away the stains of the prison's daily life, an invisible presence in the shadows. But now, I am condemned to dwell within the very walls I once maintained, grappling with the harsh reality of being a prisoner.")
                dispatcher.utter_message(text="As your reward for guessing right , I will tell you about the two next rooms you asked about. The 3rd room is the kitchen , it is where all the food is stored including the yummy food that guards and warden eat. The fourth room is the warden's office , That room is the best one , it has a phone , computer and most importantly a lot of fancy whiskey bottles , I used to take a sip of each , whenever I was cleaning there until I got caught and thrown in here :'(")
                dispatcher.utter_message(text="That was all I know..Now go away I have stuff to do")
                if 'room3' not in collect_infos_from_cellmates and 'room4' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room3')
                    collect_infos_from_cellmates.append('room4')
            elif talked_person == 'C' and C == guess:
                dispatcher.utter_message(text="C: Right on Target, inmate. Once a skilled aviator, I soared through the boundless skies, embracing the thrill of flight and the art of navigation. Yet now, destiny has landed me in the confines of a prison cell, wrestling with the paradox of being a prisoner within a world where I once commanded the cockpit. God what I would do to get myself inside an airlplanes cockpit one more time  ")
                dispatcher.utter_message(text="I heard you gathering info about the rooms in the prison , I know what you are up to , don'T worry though I won't tell , well maybe who knows. Anyway the only way to get out of here is by air . This means fly out , so you need to get a helicopter . I saw a heli pad outside the warden'S office just under the window . Maybe we can figure out how to get an airplane in there")
                dispatcher.utter_message(text="It will be a challenge and require a lot of time. It's like we are going anywhere right ? hahaha ")
                if 'room5' not in collect_infos_from_cellmates and 'room6' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room5')
                    collect_infos_from_cellmates.append('room6')
            else:
                dispatcher.utter_message(text="Wrong！Game Over")
        else:
            dispatcher.utter_message(text="I didn't understand you sorry. Could you please say that in a different manner ?")

        if len(collect_infos_from_cellmates) == 6:
            dispatcher.utter_message(text="You have now collected all the info needed for the rooms and unlocked the a Map. to check the map at any time just type in Map")
            dispatcher.utter_message(
                text="Now that you have a plan to escape you need to select which inamtes you want and need to escape with you . Choose wisely your very freedom depend on it .")
            return [SlotSet('select_member', True)]
        else:
            dispatcher.utter_message(text="You don't have all the rooms info. To get more info about different rooms ask all the different inamtes")
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
                text="You have successfuly recruited all the inmates, You also have the Map unlocked , you can now proceed with your escape")
            return []
        else:
            dispatcher.utter_message(
                text="Game over! The inmates you didn't recruit heard your plan and ratted you out for a reduced sentence.")
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
                text="the rooms in this Prison are as follow: | Cell |, | Infirmary |, | Kitchen | , | Laundry Room |, | Warden's office | , | Heli Pad |, which do you plan to access next")
        else:
            dispatcher.utter_message(text="You cannot view the Map at the moment ")


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
            dispatcher.utter_message(text="You wake up in a bed staring at a white ceiling , with a strong headache and your face feels swollen? what happened to me ? oh right I got punched ")
            dispatcher.utter_message(text="As you lie in the bed , a trainee nurse comes to check on you and patch you up. You need to say something to the nurse to get her to leave the room")
            infirmary_count = 1
            return [SlotSet("location_Infirmary", True), SlotSet("location_cell", False), SlotSet('get_punched', False)]
        else:
            dispatcher.utter_message(text="You cannot go into the Infirmary at the moment ")

class AbleCheck(Action):
    def name(self) -> Text:
        return "able_check_infirmary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('nurse_away'))
        if tracker.get_slot('location_Infirmary') and tracker.get_slot('nurse_away'):
            dispatcher.utter_message(text="You are now alone in the infirmery, you can look around and do what you want . But you gotta do it fast cause the nurse might come back at any time")
            dispatcher.utter_message(text="In this room there is a cabinet with 7 different potions/ingredients: Lavender, Dandelion. Sunflower, Cayenne Pepper, Aloe Vera, Bioluminescent Algae, Rose")
            dispatcher.utter_message(text="A recipe with all instructions to making a very potent sedative fell off the pocket of the tarinee nurse when she reached down to grab the bandages")
            dispatcher.utter_message(text="Potent sedative recipe: There are four components of anesthetics, and you need to guess them correctly through riddles")
            dispatcher.utter_message(text="1 : In moonlit fields, I dance with grace, A bloom of beauty, a soothing embrace. With petals yellow and sweet perfume, I'm the first ingredient, brightening the room.")
            dispatcher.utter_message(text="2 : I'm forged in flames, a fiery birth, A spice so potent, I add zest to mirth. From the tropics, I bring the heat, A pinch of me makes the mixture complete.")
            dispatcher.utter_message(text="3 : A leafy treasure, green and grand, An herb that heals with a gentle hand. With calming scent and medicinal touch, I'm the herb you seek, the third as such.")
            dispatcher.utter_message(text="4 : From the depths of the ocean, I arise, A creature rare, hidden from prying eyes. With slimy skin and healing might, The final ingredient, glowing in the night.")
            dispatcher.utter_message(text="If you want to get the sedative, type the right ingredients in order one after the other")
            #return [SlotSet("nurse_away", False)]
        else:
            dispatcher.utter_message(text="The trainee nurse is also in the infirmery , You must be alone to look around")



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
                dispatcher.utter_message(text='Nothing happened, you need 4 ingredients ')
            else:
                if 'Lavender' in entities and 'Sunflower' in entities and 'Cayenne Pepper' in entities and 'Bioluminescent Algae' in entities:
                    dispatcher.utter_message(text='A new potent chemical is formed , just the smell is making you sleepy . you acquired the sedative.')
                    dispatcher.utter_message(text='Laundry room is just in front of the infirmery , it is easy to access from this position')
                    dispatcher.utter_message(text='The Map is available to you knwo , just type Map to see it')
                    return [SlotSet('get_sedative', True),  SlotSet("location_Infirmary", False), SlotSet("location_cell", True)]
                else:
                    dispatcher.utter_message(text='The ingredients you guessed are wrong')
        else:
            dispatcher.utter_message(text='You cannot do this, because you are not in the Infirmary')


class ShowLaundryRoom(Action):
    def name(self) -> Text:
        return "show_Laundry_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='Now you are alone in the laundry room')
        dispatcher.utter_message(text='You look around and  see some lockers, some washing machines, and a dirty clothes basket')
        dispatcher.utter_message(text='You can check those, who knows maybe you will find something useful')
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
                dispatcher.utter_message(text='Nothing special here')
            elif 'lockers' in checkitem:
                dispatcher.utter_message(text='The lockers are locked. Maybe something important is inside')
                dispatcher.utter_message(text='Please give The 5 digits code to opne the locker')

            elif 'clothes basket' in checkitem:
                dispatcher.utter_message(text='In the dirty clothes basket you find a note left behind" There are five riddles on the note')
                dispatcher.utter_message(text='Clue 1: "The first digit is the square root of 16."')
                dispatcher.utter_message(text='Clue 2: "The second digit is the sum of 3 and 5."')
                dispatcher.utter_message(text='Clue 3: "The third digit is the product of the numbers in the second clue."')
                dispatcher.utter_message(text='Clue 4: "The fourth digit is twice the first digit."')
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
                dispatcher.utter_message('Please give the 5 digits code')
            elif code == ['4','8','15','8','11']:
                dispatcher.utter_message('The codes worked and the locker is open now.')
                dispatcher.utter_message('You grab the guards uniforms!')
                dispatcher.utter_message('it does not look like there is anything else to do in the laundry room. You already got what need You should go back to your cell')
                return [SlotSet('location_Laundry_room', False),SlotSet("location_cell", True), SlotSet('get_uniform', True)]
            else:
                dispatcher.utter_message('You gave the wrong code')
        else:
            dispatcher.utter_message(text="You can't do this, you are not in laundry room")


class Gokitchen(Action):
    def name(self) -> Text:
        return "show_Kitchen_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('get_uniform') == True:
            dispatcher.utter_message('You need to guess the correct vegetables from the puzzle to open the door')
            dispatcher.utter_message("In the kitchen's realm of scraps and remains, seek the food that the dogs will claim. A taste of delight, they yearn to savor, find the dish that matches their favorite flavor. Look to the label, it holds the key, the name of the food that sets them free. It's not a meat, but something green, a vegetable that makes them keen. Search high and low, with keen eyesight, and choose the food that feels just right. What am I?")
            dispatcher.utter_message('What is the correct vegtable ?')
            return [SlotSet('location_Kitchen', True)]
        else:
            dispatcher.utter_message(' You ran into the patrol officers, you got caught immediatly game over. What is the point of going through the trouble of stealing the guards uniforms if you are not going to use them -_-')

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
                dispatcher.utter_message('Pin correct! You now have access to the food area in the kitchen')
                dispatcher.utter_message('You can see delicious food being cooked on the stove, which should be the food for the prison guards. It is really not fair that you have to eat all the bad food while the guards eat only the bets of food. As you stare at the food you get hungrier and hungrier ')
                dispatcher.utter_message('Should you ruin the food and put the drugs in it or is it a waste and you should eat the food ?')
                dispatcher.utter_message('drug: You want to drug the food with sedative')
                dispatcher.utter_message('eat: You want to fill yourself up first')
                return [SlotSet('kitchen_door', True)]
            else:
                dispatcher.utter_message('You gave the wrong Pin')

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
                dispatcher.utter_message('You got caught, You started binging on the food and forgot the time and the chefs came back from their break ')
            elif 'drug' in kitchenfood:
                if tracker.get_slot('get_sedative'):
                    dispatcher.utter_message('You successfuly put the sedatives in the food , the guards should be asleep soon')
                    dispatcher.utter_message('Where do you want to go to next ?')
                    return [SlotSet('location_Kitchen',False),SlotSet('guards_fainted',True)]
                elif tracker.get_slot('get_sedative') == False:
                    dispatcher.utter_message("You don't have the sedative to lace the food")
                    dispatcher.utter_message("You need to get the sedative from another location first")
            else:
                dispatcher.utter_message('No this Choice')
        else:
            dispatcher.utter_message('You cannot do this action now')


class OfficeIn(Action):
    def name(self) -> Text:
        return "vertification_guards_fainted_and_show_office_or_getcaught"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('guards_fainted') == False:
            dispatcher.utter_message('The prison guards detect you, and catch you')
        else:
            dispatcher.utter_message('As the guards are all asleep including the warden you just walk into the wardens office .')
            dispatcher.utter_message('You look around and see a transparent cabinet, a telephone on the desk. There is a chair, and a desk lamp.')
            dispatcher.utter_message('try to find something useful')
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
            if 'telephone' in officeitem:
                dispatcher.utter_message('You can use the phone to call someone for help')
                dispatcher.utter_message('Time is running out only enough for one call is left')
                dispatcher.utter_message('Make a choice, to which Person you want to call')
                dispatcher.utter_message('Son: The son of the pilot cellmate, he is also a pilot')
                dispatcher.utter_message('Friend: Your best friend Stefan, he is also a lawyer, he is rich')

                return [SlotSet('phone_ready',True)]
            elif 'cabinet' in officeitem:
                dispatcher.utter_message('You found a huge check, the payer is hung up by link, the name can be vaguely seen with the beginning of S and end of n')
            else:
                dispatcher.utter_message('Nothing special')
        else:
            dispatcher.utter_message('You cannot do this, because you are not in the office')


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
                dispatcher.utter_message('Your friend is corrupt along with the warden and is involved in your framing he does not want you to get out')
                dispatcher.utter_message('He reported you, and you are locked up again')
            elif 'Son' in calledperson:
                dispatcher.utter_message("The call to the pilot's son went well, you explained the current situation and requested that he could fly a plane to the prison's Heli_Pad to rescue you.")
                dispatcher.utter_message("The pilot's son says he'll say yes if you can help him answer the following questions correctly")
                dispatcher.utter_message("Riddle 1: I'm a collection of elements, orderly arranged, With a fixed size and type, never to be changed. Sequential access is how I'm designed, Efficiency is key, in memory I'm confined. What am I?")
                dispatcher.utter_message("Riddle 2: I'm like a chain, linking nodes in a line, Traversing me forwards or backwards is fine. I'm flexible, dynamic, and efficient too, Adding or removing elements, I can easily do. What am I?")
                dispatcher.utter_message("Riddle 3: I'm a type, a blueprint of data and behavior, Encapsulating objects, I'm a powerful savior. Inheritance and polymorphism, I embrace, Creating instances, bringing code to life's embrace. What am I?")
                dispatcher.utter_message("Riddle 4: I'm a line, where elements wait in turn, First come, first serve, that's how I churn. Enqueue and dequeue, actions I take, Used in printing, processes, and more, give me a break. What am I?")
                dispatcher.utter_message("Answer the riddlles in order . Type the answers one after the other ")
                return [SlotSet('phone_son',True)]
            else:
                dispatcher.utter_message('Not this Choice')
        else:
            dispatcher.utter_message('You can not do this action')



class OfficeSon(Action):
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
                    dispatcher.utter_message('You answer correctly, the Son of pilot  promisses you He will pick you up in a helicopter in half an hour.')
                    dispatcher.utter_message('You need to go where the helicopter will land and be ready , because you will not have much time . Hint: you can pull out the Map to see where you should go to next')
                    return [SlotSet('get_helicopter',True)]
                else:
                    dispatcher.utter_message('Wrong answers')

            else:
                dispatcher.utter_message('Please give 4 answers')
        else:
            dispatcher.utter_message('You can not do this action')


class GoHelipad(Action):
    def name(self) -> Text:
        return "vertification_go_helipad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('get_helicopter'):
            dispatcher.utter_message('You are now in the Heli Pad')
            dispatcher.utter_message('The halicopter is waiting you')
            dispatcher.utter_message('Before getting on the helicopter, have a final confrontation with the mysterious person(M) to try to get the evidence to exonerate you')
            dispatcher.utter_message("You threaten M: 'If you do not agree to give me the evidence immediately, I will not take you out of prison.'")
            dispatcher.utter_message("M: 'I must to escape before I can give you the evidence'")
            dispatcher.utter_message("Finally make a decision on how you will handle M")
            dispatcher.utter_message("Abandon him: You think this person is untrustworthy and don't need to waste your time.")
            dispatcher.utter_message("Confront: Keep spending time with him, insist that he produce evidence, and get on the plane together.")
            dispatcher.utter_message("Agree: You agree to let him board the plane and you are willing to believe that he will give you proof once he gets on the plane.")
            return [SlotSet('location_Heli_Pad', True)]
        else:
            dispatcher.utter_message('The Hali_Pad is empty, try to search another locations first')



class Ending(Action):
    def name(self) -> Text:
        return "ending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Heli_Pad'):
            deal_M = [e['value'] for e in tracker.latest_message['entities'] if
                       e['entity'] == 'deal_M']
            if 'Agree' in deal_M:
                dispatcher.utter_message('Your end: You successfully escaped from prison, but M did not keep his promise to give you the evidence you need to exonerate yourself, you have to spend the rest of your life in hiding , you successfuly completed the game and escaped prison , but you failed to escape your fate . So are you really free ? did you really escape then ?')
            elif 'Confront' in deal_M:
                dispatcher.utter_message('Your end: As time gets tighter and tighter, M shows an anxious look and he finally pulls out the evidence for you and it turns out he was the one who the evil corporate hired to frame you. You gave him permission to board the helicopter. You managed to escape and were cleared of any guilt. Congrats you escaped both prison and your fate . This is the bets possible outcome .')
            elif 'Abandon' in deal_M:
                dispatcher.utter_message('Your end: You directly choose to abandon M and board the helicopter, completely enraging M. He yanked you right out of the plane and wrestled with you. The guards came looking for you soon after and the helicopter along with the other inmates left you behind. You were caught and sent to a max security prison. You failed the to escape the prison and lost the game and your freedom forever. Better luck next time ')
            else:
                dispatcher.utter_message('Please give a valid decision')


        else:
            dispatcher.utter_message('You are not able to do this action')
