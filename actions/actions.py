from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher



class CheckGuessAction(Action):
    def name(self) -> Text:
        return "action_check_guess"

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
            if talked_person == 'Maverick' and C == guess:
                dispatcher.utter_message(text="""Maverick: "Correct guess my new friend! I assume you are trying to escape - if so, you might find me useful for your schemes. You can find sedatives and other drugs in the <i>Infirmary</i>. But be vigilant! Nurse Rose guards the infirmary fiercely. However, she cares for the ill and injured, so you can distract her by <b>claiming hunger or thirst</>. There is also the <i>Laundry Room</i>, which has staff uniforms effective for disguise. That's all I know... Ask the other two dirtbags about the rest of the rooms." """)
                if tracker.get_slot("guess_b") and tracker.get_slot("guess_c"):
                    dispatcher.utter_message(
                        text="You have now collected all the information needed for an escape plan, congrats! But you still need to select which of the inmates you want to escape with. Choose wisely... Your very freedom depends on it!")
                    return SlotSet("guess_a", True)
                else:
                    dispatcher.utter_message(
                        text="You still don't have all the necessary information to form an escape plan, yet. Ask your inmates - they might know more...")
                    return [SlotSet("guess_a", True)]
            elif talked_person == 'Mr.Clean' and B == guess:
                dispatcher.utter_message(text="""Mr.Clean: "Spot-on, newbie!! As your reward for guessing right, I will tell you about 2 rooms of the prison. The 3rd room is the <i>Kitchen</i>, storing delicious food for guards and wardens. The <i>Warden's Office</i> is room 4, my personal favorite. It's equipped with a phone, a computer, and a stash of fancy whiskey. Used to sneak a sip until I got caught... Anyway, that was all I know. Now go away, I have other stuff to do." """)
                if tracker.get_slot("guess_a") and tracker.get_slot("guess_c"):
                    dispatcher.utter_message(
                        text="You have now collected all the information needed for an escape plan, congrats! But you still need to select which of the inmates you want to escape with. Choose wisely... Your very freedom depends on it!")
                    return SlotSet("guess_b", True)
                else:
                    dispatcher.utter_message(
                        text="You still don't have all the necessary information to form an escape plan, yet. Ask your inmates - they might know more...")
                    return [SlotSet("guess_b", True)]
            elif talked_person == 'Jailer Jake' and A == guess:
                dispatcher.utter_message(text="""Jailer Jake: "Right on target, inmate! Heard you're gathering info about the rooms in this hellhole. I might keep your secret, or maybe not, who knows. Anyway, the only way to get out of here is by air. I saw a <i>helicopter pad</i> outside the warden's office just under the window. If you let me join you, I will give you the phone number to of my friend to call a helicopter to this location. OK, that's all I know. Go bother somebody else now." """)
                if tracker.get_slot("guess_b") and tracker.get_slot("guess_a"):
                    dispatcher.utter_message(
                        text="You have now collected all the information needed for an escape plan, congrats! But you still need to select which of the inmates you want to escape with. Choose wisely... Your very freedom depends on it!")
                    return SlotSet("guess_c", True)
                else:
                    dispatcher.utter_message(
                        text="You still don't have all the necessary information to form an escape plan, yet. Ask your inmates - they might know more...")
                    return [SlotSet("guess_c", True)]
            else:
                dispatcher.utter_message(text="Wrong guess, buddy！Try again.")
        else:
            dispatcher.utter_message(text="Sorry, I didn't get you. Could you say that in a different manner?")


class CheckSelectAction(Action):
    def name(self) -> Text:
        return "action_check_asked_mates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'person']
        entities2 = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'all']
        if ('Maverick' in entities and 'Mr.Clean' in entities and 'Jailer Jake' in entities) or 'everyone' in entities2 or 'all' in entities2:
            dispatcher.utter_message(text="""
            You and your newfound mates sit down to discuss the escape plan in hushed voices. After hours of less than cordial deliberations, you have agreed to the following:
            <ol>
            <li>Go to the <i>infirmary</i> and get a strong sedative, which you will later mix into the food eaten by the prison guards.</li>
            <li>Enter the <i>kitchen</i> and disguise yourself as an employee of the facility. The <i>laundry room</i> might have some spare guard uniforms that will fit you.</li>
            <li>After sedating the guards, you need to call the helicopter to your location. B mentioned that the <i>warden</i> has a phone in her office.</li>
            <li>Get to the <i>Heli pad</i>, and you're as good as free.</li>
            </ol>

            Now off you go – time waits for no one! You can look at the map (type in "<i>Map</i>" to access).
            """)
            return [SlotSet('select_member', True)]
        else:
            dispatcher.utter_message(
                text="The inmates you didn't recruit heard your plan and ratted you out for a reduced sentence!")
            return []


class ShowLocationAction(Action):
    def name(self) -> Text:
        return "action_show_collection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Heli_Pad'):
            dispatcher.utter_message('You are now in the Heli Pad')
        elif tracker.get_slot('location_cell'):
            dispatcher.utter_message('You are now in the cell ')
        elif tracker.get_slot('location_Infirmary'):
            dispatcher.utter_message('You are now in the Infirmary ')
        elif tracker.get_slot('location_Laundry_room'):
            dispatcher.utter_message('You are now in the Laundry room ')
        elif tracker.get_slot('location_Kitchen'):
            dispatcher.utter_message('You are now in the Kitchen ')
        elif tracker.get_slot('location_office'):
            dispatcher.utter_message("You are now in the Warden's office"  )
        print(tracker.get_slot('select_member'))
        if tracker.get_slot('select_member'):
            dispatcher.utter_message(
                text="The rooms in this prison are as follows: | Cell | , | Infirmary | , | Kitchen | , | Laundry Room | , | Warden's office | , | Heli Pad | , which do you plan to access next?")
        else:
            dispatcher.utter_message(text="You cannot view the Map at the moment")


#infirmary_count = 0


class AccessLocationInfirmary(Action):
    def name(self) -> Text:
        return "action_access_infirmary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      #  print(tracker.get_slot('get_punched'))
       # global infirmary_count
        if tracker.get_slot('get_punched'):
            #and tracker.get_slot('location_cell')
                #and 0 == infirmary_count:
            dispatcher.utter_message(text="You wake up in a makeshift hospital bed staring at a white ceiling eluminated by harsh fluorescent light. Besides the swollen cheek and a killer headache you feel fine. Guess the plan worked - <b>you are indeed in the infirmary</b>.  A small, black-haired woman, likely Nurse Rose, enters the room and scrutinizes your condition. To steal the sedatives, you'll need to find a way to get her out of the infirmary. You remember Maverick's advice to <b>ask for food or water</b>")
            infirmary_count = 1
            return [SlotSet("location_Infirmary", True), SlotSet("location_cell", False), SlotSet('get_punched', False)]
        else:
            dispatcher.utter_message(text="You cannot go into the infirmary at the moment.")

class AbleCheck(Action):
    def name(self) -> Text:
        return "action_able_check_infirmary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot('nurse_away'))
        if tracker.get_slot('location_Infirmary') and tracker.get_slot('nurse_away'):
            dispatcher.utter_message(text="Time is crucial now. Alone in the room, you find a cabinet with five ingredients: Lavender, Sunflower, Cayenne Pepper, and Bioluminescent Algae. A forgotten recipe for a potent sedative lies on the counter. Guess the four anesthetic components in the correct order by solving riddles. ")
            dispatcher.utter_message(text="RECIPE: <ol><li>I am fragrant and purple, bringing relaxation and calm. What am I?</li><li>I am tall and bright, a flower so cheery, with petals golden, and seeds you can eat, oh so seedy.</li><li>Spicy and red, I add the heat. Guess my name, this pepper so neat.</li><li>In the depths of the ocean, a magical sight. Multiple words describe my light.</li></ol>")
            #return [SlotSet("nurse_away", False)]
        else:
            dispatcher.utter_message(text="The trainee nurse is still in the infirmary. You should be alone to look around if you don't want to get caught!")



class Get_sedative(Action):
    def name(self) -> Text:
        return "action_get_sedative"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Infirmary'):
            entities = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'ingredients']
            print(entities)
            if len(entities) != 4:
                dispatcher.utter_message(text='Nothing happened, you need 4 ingredients')
            else:
                if 'Lavender' in entities and 'Sunflower' in entities and 'Cayenne Pepper' in entities and 'Bioluminescent Algae' in entities:
                    dispatcher.utter_message(text='A new potent chemical is formed , just the smell is making you sleepy. Nice, you acquired the sedative! Grab to go next location!')
                    return [SlotSet('get_sedative', True),  SlotSet("location_Heli_Pad", False), SlotSet("location_cell", False),SlotSet("location_Kitchen", False),SlotSet("location_Laundry_room", False),SlotSet("location_office", False)]
                else:
                    dispatcher.utter_message(text='The ingredients you guessed are wrong. Try again before your potion explodes!')
        else:
            dispatcher.utter_message(text='You cannot do this since you are not in the infirmary')


class ShowLaundryRoom(Action):
    def name(self) -> Text:
        return "action_show_Laundry_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="The pungent smell of detergent and the noise of the whirring washing machines momentarily stuns you as you sneak into the next room. <b>This definitely the laundry room</b>. Looking around you can see <b>lockers</b> lining the wall, as well as some <b>washing machines</b> and a <b>dirty clothes basket</b>. You can check those - you might find something useful!")
        return [SlotSet('location_Laundry_room', True), SlotSet("location_Heli_Pad", False), SlotSet("location_cell", False),SlotSet("location_Kitchen", False),SlotSet("location_Infirmary", False),SlotSet("location_office", False)]


class Show_locker_puzzles_or_other_unuseful_items(Action):
    def name(self) -> Text:
        return "action_show_locker_puzzles_or_other_unuseful_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Laundry_room'):
            checkitem = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'items_in_Laundry_room']
            print(checkitem)
            if 'washing machines' in checkitem:
                dispatcher.utter_message(text='Nothing special here')
            elif 'clothes basket' in checkitem:
                dispatcher.utter_message(text= """
                    In the dirty clothes basket, you find a handwritten note left behind. This must be some kind of password that will be used later! 
                    <br>
                    <b>Clues:</b>
                    <ol>
                    <li>"I am the first digit in here, but the second prime"</li>
                    <li>"I am the second digit in here, but I am the first prime"</li>
                    <li>"I am the lucky prime number"</li>
                    <li>"I am the beginning but also the end, in addition I fade away and divided by I am infinity, I am neither positive nor negative but I am also both."</li>
                    <li>"In card games, people sometimes mistake me as 6"</li>
                    </ol>
                    """)
            elif 'lockers' in checkitem:
                dispatcher.utter_message(text= """
                    The lockers are locked and please give a <b>5-digit code</b> to open. Hint: The password must be in this room, did you find them?
                    """)
            else:
                dispatcher.utter_message(text='There is no such item in the laundry room. Please try again.')
        else:
            dispatcher.utter_message(text="You can't do this as you are not in laundry room.")


class OpenLockers(Action):
    def name(self) -> Text:
        return "action_vertification_locker_puzzles"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        if tracker.get_slot('location_Laundry_room'):
            # Extract the code as individual characters or numbers
            code = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'numbercode']
            # Concatenate the code into a single string
            code_string = ''.join(code)

            # Check if the code_string has 5 characters
            if len(code_string) != 5:
                dispatcher.utter_message('Please give the 5 digits code')
            # Check if the code is correct
            elif code_string == '32709':
                dispatcher.utter_message("You hear a soft click before the locker finally swings open. As you had hoped, you find a guard uniform inside and quickly put it on. You don't have much time left before the guards go on lunch break. Better hurry!")
                return [SlotSet('location_Laundry_room', False), SlotSet("location_Heli_Pad", False),SlotSet("location_Kitchen", False),SlotSet("location_Infirmary", False),SlotSet("location_office", False), SlotSet("location_cell", True), SlotSet('get_uniform', True)]
            else:
                dispatcher.utter_message('You wait a few seconds, but nothing happens. Looks like you have typed in the wrong code...')
        else:
            dispatcher.utter_message(text="You can't do this, you are not in the laundry room.")

#action_show_Kitchen_code
class Gokitchen(Action):
    def name(self) -> Text:
        return "action_in_kitchen"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('get_uniform') == True:
            dispatcher.utter_message("On the way you escaped the guards' patrol in your uniform and you successfully accessed the kitchen.")
            dispatcher.utter_message('You can see delicious food being cooked on the stove, which should be the food for the prison guards. If you could have some kind of medicines to put in the food, you could make the guards faint and your further actions would be easier!')
            if tracker.get_slot('get_sedative'):
                dispatcher.utter_message('Great! You just got a sedative in the infirmary! You gently stir the pasta sauce as you mix in the sedatives. These guards will sleep like the dead.')
                dispatcher.utter_message('Where do you want to go to next?')

                return [SlotSet('guards_fainted',True),SlotSet('location_Kitchen', True),SlotSet('location_Laundry_room', False), SlotSet("location_Heli_Pad", False), SlotSet("location_cell", False),SlotSet("location_Infirmary", False),SlotSet("location_office", False)]
            else:
                dispatcher.utter_message('Search other locations first, you have nothing else to do in the Kitchen now')
                return [SlotSet('location_Kitchen', True),SlotSet('location_Laundry_room', False), SlotSet("location_Heli_Pad", False), SlotSet("location_cell", False),SlotSet("location_Infirmary", False),SlotSet("location_office", False)]

        else:
            dispatcher.utter_message('On the way you see a lot of prison guards patrolling, if you go to the kitchen now you will be arrested by them, please search another location first!.')

class KitchenCode(Action):
    def name(self) -> Text:
        return "action_vertification_Kitchens_code_and_show_kitchen_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Kitchen'):
            kitchencode = [e['value'] for e in tracker.latest_message['entities'] if
                    e['entity'] == 'vegetables']
            if 'Brocolli' in kitchencode:
                dispatcher.utter_message('Pin correct! You now have access to the food storage area of the kitchen!')
                dispatcher.utter_message('You can see delicious food being cooked on the stove, which should be the food for the prison guards. It is really unfair that you have to eat all the bad food and leftovers while the guards eat only the best supplies. You can feel yourself starting to drool as you take a step closer towards the stove...')
                dispatcher.utter_message('You know you are on a tight schedule but having one or two bites surely wont harm anyone... Or should you just put in the sedatives right now and be done with it?')
                dispatcher.utter_message('drug: You want to drug the food with sedative.')
                dispatcher.utter_message('eat: You want to fill yourself up first!')
                return [SlotSet('kitchen_door', True)]
            else:
                dispatcher.utter_message('You hear an annoying buzzing sound, idicating that you have entered the wrong code. Try again')

        else:
            dispatcher.utter_message('You can not do this action right now!')

class KitchenFood(Action):
    def name(self) -> Text:
        return "action_vertification_Kitchen_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Kitchen') and tracker.get_slot('get_uniform'):

            kitchenfood = [e['value'] for e in tracker.latest_message['entities'] if
                               e['entity'] == 'dealwithfood']
            if 'eat' in kitchenfood:
                dispatcher.utter_message('You got caught: You started binging on the food and forgot the time.')
            elif 'drug' in kitchenfood:
                if tracker.get_slot('get_sedative'):
                    dispatcher.utter_message('You gently stir the pasta sauce as you mix in the sedatives. These guards will sleep like the dead.')
                    dispatcher.utter_message('Where do you want to go to next?')
                    return [SlotSet('guards_fainted',True)]
                elif tracker.get_slot('get_sedative') == False:
                    dispatcher.utter_message("You don't have the sedative to lace the food!")
                    dispatcher.utter_message("You need to get the sedative from another location first!")
            else:
                dispatcher.utter_message("You can't waste anymore time! Please select from the two options above.")
        else:
            dispatcher.utter_message('You cannot do this action right now!')


class OfficeIn(Action):
    def name(self) -> Text:
        return "action_vertification_guards_fainted_and_show_office_or_getcaught"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('get_uniform') and tracker.get_slot('guards_fainted') == False :
            dispatcher.utter_message("Entering the warden's office there are guards to verify identity, just wearing the guard's uniform is not enough, you are now dangerous to come here, search for other location first!")
        elif tracker.get_slot('get_uniform') == False and tracker.get_slot('guards_fainted') == False:
            dispatcher.utter_message("The way to the warden office is full of guards, we can't go to this place yet, let's search other location first!")
        else:
            dispatcher.utter_message('You can hear the snores of the guards eminating from the cafeteria as you make your way towards the wardens office. Once inside, you can see a transparent cabinet, a telephone on the desk and a fancy leather chair. Try to find something useful.')
            return [SlotSet('location_office', True),SlotSet('location_Laundry_room', False), SlotSet("location_Heli_Pad", False), SlotSet("location_cell", False),SlotSet("location_Kitchen", False),SlotSet("location_Infirmary", False)]


class OfficeItems(Action):
    def name(self) -> Text:
        return "action_show_phone_or_other_unuseful_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_office'):
            officeitem = [e['value'] for e in tracker.latest_message['entities'] if
                               e['entity'] == 'items_in_office']
            if 'telephone' in officeitem:
                dispatcher.utter_message('You can use the phone to call someone for help. However, time is running out so you can make one crucial call. Make a choice, <b>who do you want to call?</b> The <b>son of the pilot</b> cellmate who is also a pilot or your <b>rich best friend Stefan</b> who you worked together as a lawyer with.')
                return [SlotSet('phone_ready',True)]
            elif 'cabinet' in officeitem:
                dispatcher.utter_message('You found a huge check, the payer is hung up by link, the name can be vaguely seen with the beginning of S and end of n')
            else:
                dispatcher.utter_message('Nothing special here...')
        else:
            dispatcher.utter_message('You cannot do this, because you are not in the office!')


class OfficePhone(Action):
    def name(self) -> Text:
        return "action_vertification_call_with_npc_child_for_helicopter_and_show_puzzles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('phone_ready'):
            calledperson = [e['value'] for e in tracker.latest_message['entities'] if
                          e['entity'] == 'called_person']
            if 'Friend' in calledperson:
                dispatcher.utter_message('Your friend is corrupt along with the warden and is involved in your framing he does not want you to get out. He reported you, and you are locked up again')
            elif 'Son' in calledperson:
                dispatcher.utter_message("""After waiting for a few seconds, someone finally picks up: "Oh so YOU are the new mate my dad talked about! Well, well if you want my aid you first need to help me with my homework. <b>Solve these riddles for me</b> and in return, I get you the helicopter. An eye for an eye as Pops used to say!"
                            <ul>
                             <li>I am the capital of a country where baguettes and croissants are famous.</li>
                             <li>I am a colorful arc up in the sky, after rain, you'll see me up high.</li>
                             <li>I am a place where birds roam free, where you can feel the wind and be as you want to be.</li>
                             <li>I am an animal with a long neck, spotted coat, and can run very fast. </li>
                             '</ul>""")

                return [SlotSet('phone_son',True)]
            else:
                dispatcher.utter_message('Not this choice!')
        else:
            dispatcher.utter_message('You can not do this action!')



class OfficeSon(Action):
    def name(self) -> Text:
        return "action_check_answer_to_son"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('phone_son'):
            answers = [e['value'] for e in tracker.latest_message['entities'] if
                          e['entity'] == 'answer_to_son']
            print(answers)
            if len(answers) == 4:
                if ['Paris', 'Rainbow', 'Sky', 'Giraffe']==answers:
                    dispatcher.utter_message('"Nice, thank you! The helicopter will pick you up at the correct location soon, so hurry! Oh, and greet my dad for me." <i>(Hint: you can pull out the Map to see where you should go to next)</i>')
                    return [SlotSet('get_helicopter',True)]
                else:
                    dispatcher.utter_message('"I doubt that this is correct... Thought you want to escape? Try again!"')

            else:
                dispatcher.utter_message('"There need to be 4 answers though..."')
        else:
            dispatcher.utter_message('You can not do this action')


class GoHelipad(Action):
    def name(self) -> Text:
        return "action_vertification_go_helipad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('get_helicopter'):
            dispatcher.utter_message(""" You are now in the Heli Pad. The helicopter is waiting for you. Before getting on the helicopter, have a final confrontation with the mysterious person (M) to try to get the evidence to exonerate you. You threaten M: '<i>If you do not agree to give me the evidence immediately, I will not take you out of prison.</i>'
                                    M: '<i>I must escape before I can give you the evidence.</i>'
                                    Finally, make a decision on how you will handle M:
                                    <b>Abandon him:</b> You think this person is untrustworthy and don't need to waste your time.
                                    <b>Confront:</b> Keep spending time with him, insist that he produces evidence, and get on the helicopter together.""")
            return [SlotSet('location_Heli_Pad', True),SlotSet('location_Laundry_room', False), SlotSet("location_cell", False),SlotSet("location_Kitchen", False),SlotSet("location_Infirmary", False),SlotSet("location_office", False)]
        else:
            dispatcher.utter_message('The helicopter pad is empty, try to search another locations first!')



class Ending(Action):
    def name(self) -> Text:
        return "action_ending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('location_Heli_Pad'):
            deal_M = [e['value'] for e in tracker.latest_message['entities'] if
                       e['entity'] == 'deal_M']
            if 'Agree' in deal_M:
                dispatcher.utter_message('Your end: You successfully escaped from prison, but M did not keep his promise to give you the evidence you need to exonerate yourself, you have to spend the rest of your life in hiding , you successfuly completed the game and escaped prison , but you failed to escape your fate . So are you really free ? did you really escape then?')
            elif 'Confront' in deal_M:
                dispatcher.utter_message('Your end: As time gets tighter and tighter, M shows an anxious look and he finally pulls out the evidence for you and it turns out he was the one who the evil corporate hired to frame you. You gave him permission to board the helicopter. You managed to escape and were cleared of any guilt. Congrats you escaped both prison and your fate. This is the bets possible outcome!')
            elif 'Abandon' in deal_M:
                dispatcher.utter_message('Your end: You directly choose to abandon M and board the helicopter, completely enraging M. He yanked you right out of the plane and wrestled with you. The guards came looking for you soon after and the helicopter along with the other inmates left you behind. You were caught and sent to a max security prison. You failed the to escape the prison and lost the game and your freedom forever. Better luck next time!')
            else:
                dispatcher.utter_message('Please give a valid decision!')


        else:
            dispatcher.utter_message('You are not able to do this action')


