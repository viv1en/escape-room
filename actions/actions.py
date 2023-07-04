from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

collect_infos_from_cellmates = []


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
            if talked_person == 'Maverick' and A == guess:
                dispatcher.utter_message(text="Maverick: Correct guess my new friend! As a former prison guard, I dedicated my life to upholding justice behind these old, cold walls. However, fate took a cruel twist, and now I find myself trapped within the very system I once helped to upkeep, facing the consequences of false accusations. I assume you are trying to escape - if so, you might find me useful for your schemes. There are 6 important locations in the prison and I can give you intel for 2 of them. The first one is the infirmary. Here you can find sedatives and other drugs. But be vigilant! Nurse Rose is guarding that room like a dragon. She does take good care of the ill and injured however. Telling her you are hungry or thirsty will send her on to the kitchen and out of the room. There is also the Laundry Room, here you can find uniforms of all the facility staff. They could function as an effective disguise during our escape. That's all I know... Ask the other two dirtbags about the rest of the rooms.")
                if 'room1' not in collect_infos_from_cellmates and 'room2' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room1')
                    collect_infos_from_cellmates.append('room2')
            elif talked_person == 'Mr.Clean' and B == guess:
                dispatcher.utter_message(text="Mr.Clean: Right on point new fish! As a dedicated janitor, I meticulously scrubbed away the stains of the prison's daily life, an invisible presence in the shadows. But now, I am condemned to use the very same sh*tters I so meticulously scrubbed a year go. As your reward for guessing right, I will tell you about the 2 next rooms. The 3rd room is the kitchen. That's where all the food is stored including the delicious food that guards and wardens get to gobble up every day. The fourth room is the warden's office. I like this one the best. It has has a phone, a computer and most importantly, lots of fancy whiskey... I used to take a sip of each, whenever I was cleaning there until I got caught and thrown in here. That was all I know. Now go away, I have other stuff to do.")
                if 'room3' not in collect_infos_from_cellmates and 'room4' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room3')
                    collect_infos_from_cellmates.append('room4')
            elif talked_person == 'Jailer Jake' and C == guess:
                dispatcher.utter_message(text="Jailer Jake: Right on Target, inmate! Once a skilled aviator, I soared through the boundless skies, embracing the thril of flight and the art of navigation. Yet now, destiny has landed me in the confines of a prison cell, wrestling with the paradox of being a prisoner within a world where once I was free as a bird. God what I would do to get myself inside an airlplanes cockpit one more time... I heard you gathering info about the rooms in this hell hole. I know what you are up to but don't worry I won't tell, well maybe? Who knows. Anyway the only way to get out of here is by air. I saw a helicopter pad outside the warden's office just under the window. If you let me join you, I will give you the phone number to of my friend to call a helicopter to this location. OK, that's all I know. Go bother somebody else now.")
                if 'room5' not in collect_infos_from_cellmates and 'room6' not in collect_infos_from_cellmates:
                    collect_infos_from_cellmates.append('room5')
                    collect_infos_from_cellmates.append('room6')
            else:
                dispatcher.utter_message(text="Wrong guess, buddy！Try again.")
        else:
            dispatcher.utter_message(text="Sorry, I didn't understand you. Could you say that in a different manner?")

        if len(collect_infos_from_cellmates) == 6:
            dispatcher.utter_message(text="You have now collected all the information needed for an escape plan. Congrats! But you still need to select which of the inmates you want to escape with. Choose wisely... Your very freedom depends on it!")
            return [SlotSet('select_member', True)]
        else:
            dispatcher.utter_message(text="You still don't have all the necessary information to form an escape plan, yet. Ask your inmates - they might know more...")
        return [SlotSet("profession", None), SlotSet("person", None)]


class CheckSelectAction(Action):
    def name(self) -> Text:
        return "action_check_asked_mates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = [e['value'] for e in tracker.latest_message['entities'] if e['entity'] == 'person']
        if len(entities) == 3:
            dispatcher.utter_message(text="You and your newfound mates sit down to discuss the escape plan in hushed voices. After hours of less than cordial deliberations you have agreed to the following: To get to the helicopter pad you will first have to go to the infirmary and get a strong sedative, which you will later mix into the food eaten by the prison guards. Then, you get into the kitchen and disguise yourself as an employee of the facility – the laundry room might have some spare guard uniforms that will fit you. After sedating the guards, you need to call the helicopter to your location – B mentioned that the warden has a phone in her office. Afterward, you will just have to get to the pad and you’re as good as free. Now off you go – time waits for no one! Now that you have successfully recruited your team, you can look at the map (type in “Map” to access.)")
            return []
        else:
            dispatcher.utter_message(
                text="Game over! The inmates you didn't recruit heard your plan and ratted you out for a reduced sentence!")
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
            dispatcher.utter_message(text="You wake up in a makeshift hospital bed staring at a white ceiling eluminated by harsh fluorescent light. Besides the swollen cheek and a killer headache you feel fine. Guess the plan worked - you are indeed in the infirmary.")
            dispatcher.utter_message(text="As you sit up on the bed, a small, black haired woman walks into the room. You feel her eyes searching your face and body for any signs of discomfort. This must be nurse Rose A talked about. Without as much as a word she begins measuring your vitals and checking your injury. You need to get her out of the infirmary if you want to steal the sedatives. Maybe A's advice could help?")
            infirmary_count = 1
            return [SlotSet("location_Infirmary", True), SlotSet("location_cell", False), SlotSet('get_punched', False)]
        else:
            dispatcher.utter_message(text="You cannot go into the infirmary at the moment")

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
                    dispatcher.utter_message(text='A new potent chemical is formed , just the smell is making you sleepy. Nice, you acquired the sedative! Since the laundry room is just in front of the infirmary, it is quite easy to go there next.')
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
        dispatcher.utter_message(text='The pungent smell of detergent and the noise of the whirring washing machines momentarily stuns you as you sneak into the next room. This definitely the laundry room. Looking around you can see lockers lining the wall, as well as some washing machines and a dirty clothes basket. You can check those - who knows maybe you will find something useful?')
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
            elif 'lockers' in checkitem:
                dispatcher.utter_message(text='The lockers are locked. Something important might be inside? You need to give a 5 digits code to open the locker.')
            elif 'clothes basket' in checkitem:
                dispatcher.utter_message(text='In the dirty clothes basket you find a handwritten note left behind. There are 5 sentences on the note. Could these help you cracking the code?')
                dispatcher.utter_message(text='Clue 1: "I am the first digit in here, but the second prime"')
                dispatcher.utter_message(text='Clue 2: "I am the second digit in here, but I am the first prime"')
                dispatcher.utter_message(text='Clue 3: "I am the lucky prime number"')
                dispatcher.utter_message(text='Clue 4: "I am the beginning but also the end, in addition I fade away and devided by I am infinity, I am neither positive nor negative but I am also both."')
                dispatcher.utter_message(text='Clue 5: "In card games people sometimes mistake me as 6"')
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
                dispatcher.utter_message("You hear a soft click before the door of the locker finally swings open. As you had hoped, you find a guard uniform inside and quickly pull it on. Rolling up your sleeves, you check the watch mounted above the door. You don't have much time left before the guards go on lunch break. Better hurry!")
                return [SlotSet('location_Laundry_room', False), SlotSet("location_Heli_Pad", False),SlotSet("location_Kitchen", False),SlotSet("location_Infirmary", False),SlotSet("location_office", False), SlotSet("location_cell", True), SlotSet('get_uniform', True)]
            else:
                dispatcher.utter_message('You wait a few seconds, but nothing happens. Looks like you have typed in the wrong code...')
        else:
            dispatcher.utter_message(text="You can't do this, you are not in the laundry room.")


class Gokitchen(Action):
    def name(self) -> Text:
        return "action_show_Kitchen_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot('get_uniform') == True:
            dispatcher.utter_message("You pull the doorknob of the kitchen door but it won't budge. The note pinned to the door, and which you had mistakingly assumed to be a schedule, says the following: I am a green veggie which kids think I look like a tiny tree but they also do not like eating me, huhu. What am I?")
            return [SlotSet('location_Kitchen', True),SlotSet('location_Laundry_room', False), SlotSet("location_Heli_Pad", False), SlotSet("location_cell", False),SlotSet("location_Infirmary", False),SlotSet("location_office", False)]
        else:
            dispatcher.utter_message('You ran into the patrol officers and you got caught immediatly. Game Over.')

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
        if tracker.get_slot('guards_fainted') == False:
            dispatcher.utter_message("You got caught! Game Over")
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
                dispatcher.utter_message('You can use the phone to call someone for help. However, time is running out so you can make one crucial call. Make a choice, who do you want to call? It is either going to be the son of the pilot cellmate who is also a pilot or your rich best friend Stefan who you worked together as a lawyer with.')
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
                dispatcher.utter_message('After waiting for a few seconds, someone finally picks up: "Oh so YOU are the new mate my dad talked about! Well, well if you want my aid you first need to help me with my homework. Solve these riddles for me and in return, I get you the helicopter. An eye for an eye as Pops used to say!"')
                dispatcher.utter_message("Riddle 1: I am an ordered collection, with elements in line, in Excel I'm called a table, what am I?")
                dispatcher.utter_message("Riddle 2: To keep track of you task you create a To-Do what? the word you need starts with L.")
                dispatcher.utter_message("Riddle 3: In real life you can use a bottle to store some water , in programming, you use me, a handy holder of values, you see. What am I?")
                dispatcher.utter_message("Riddle 4: What do you call a line of people all waiting to buy something?")
                dispatcher.utter_message("Answer the riddlles in order. Type the answers one after the other ")
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
                if ['Array', 'List', 'Variable', 'Queue']==answers:
                    dispatcher.utter_message('"Nice, thank you! The helicopter will pick you up at the correct location soon, so hurry! Oh, and greet my dad for me." (Hint: you can pull out the Map to see where you should go to next)')
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
            dispatcher.utter_message("You are now in the Heli Pad. The helicopter is waiting you. Before getting on the helicopter, have a final confrontation with the mysterious person(M) to try to get the evidence to exonerate you. You threaten M: 'If you do not agree to give me the evidence immediately, I will not take you out of prison.'")
            dispatcher.utter_message("M: 'I must to escape before I can give you the evidence'")
            dispatcher.utter_message("Finally make a decision on how you will handle M")
            dispatcher.utter_message("Abandon him: You think this person is untrustworthy and don't need to waste your time.")
            dispatcher.utter_message("Confront: Keep spending time with him, insist that he produce evidence, and get on the plane together.")
            dispatcher.utter_message("Agree: You agree to let him board the plane and you are willing to believe that he will give you proof once he gets on the plane.")
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


