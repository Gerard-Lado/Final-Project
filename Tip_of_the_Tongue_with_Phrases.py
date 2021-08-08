# Import Kivy
from kivy.app import App
# Layout
from kivy.uix.gridlayout import GridLayout
# Label (Text)
from kivy.uix.label import Label
# Image (Logo)
from kivy.uix.image import Image
# Button
from kivy.uix.button import Button
# User Input
from kivy.uix.textinput import TextInput
# Spelling validation
from kivy.storage.jsonstore import JsonStore

class DictTest(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # Logo
        self.window.add_widget(Image(source="DictTestLogo.png"))

        # Text
        self.answer = Label(
                        text = "What's the word?",
                        font_size = 16,
                        color = "#00FFCE"
                        )
        self.window.add_widget(self.answer)

        # Results
        self.results1 = Label(
                        text= "",
                        font_size= 15,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.results1)

        self.results2 = Label(
                        text= "",
                        font_size= 15,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.results2)

        # Results for later
        self.results = Label(
                        text= "",
                        font_size= 16,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.results)

        # Asking for user input
        self.userinput = TextInput(
                    multiline= False,
                    padding_y= (20,20),
                    size_hint= (0.7, 0.8)
                    )
        self.window.add_widget(self.userinput)

        # Button
        self.button = Button(
                      text = "CHECK SPELLING",
                      size_hint = (0.6,0.6),
                      bold = True,
                      background_color ='#00FFCE',
                      )
        # For callback
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, instance):
        # Remove special characters from text input to not interfere with validation
        remove_chars = "&$@[].,'#()-\"!?’_"
        remove_chars2 = "\n"
        for character in remove_chars:
            self.userinput.text = (self.userinput.text).replace(character,"")
        for character in remove_chars2:
            self.userinput.text = (self.userinput.text).replace(character,"")

        # Define store so application knows what json file to refer to
        store = JsonStore('filo_dict.json')
        final_values = (self.userinput.text).split(" ")

        # If text input is a word
        if len(final_values) == 1:
            # If word exists in the Filipino dictionary:
            if store.exists((self.userinput.text).lower()):
                self.answer.text = "The word" + " " + (self.userinput.text).lower() + " " + "exists."
                self.results1.text = ""
                self.results2.text = ""

            # If word does not exist in the Filipino dictionary
            else:
                searched_word = (self.userinput.text).lower()
                tested_word_letters = []
                searched_word_letters = []
                tested_word = ""

                for letter in searched_word: #This allows the letters to revert to the original input after going through all the alternatives
                    searched_word_letters.append(letter)

                for letter in searched_word: #This is what's actually being tested down there \/
                    tested_word_letters.append(letter)

                ka_suggested_words = []
                va_sa_suggested_words = []

                #Accounts for misclicks, hasty and careless typing, or disproportionately large-handed people with disproportionately tiny keyboards
                keyboard_approximate = {
                    "a": "qwesxz",
                    "b": "vghn",
                    "c": "xdfv",
                    "d": "wersfxcv",
                    "e": "wsdfr",
                    "f": "ertdgcvb",
                    "g": "rtyfhvbn",
                    "h": "tyugjbnm",
                    "i": "ujklo",
                    "j": "yuihknm",
                    "k": "uiojlm",
                    "l": "kiop",
                    "m": "nhjkl",
                    "n": "bhjm",
                    "o": "iklp",
                    "p": "ol",
                    "q": "asw",
                    "r": "edfgt",
                    "s": "qazxcdew",
                    "t": "rfghy",
                    "u": "yhjki",
                    "v": "cfgb",
                    "w": "qasde",
                    "x": "zasdc",
                    "y": "tghju",
                    "z": "asx"
                    }

                #In case people get vowels mixed up
                vowel_approximate = {
                    "a": "eiou",
                    "e": "aiou",
                    "i": "aeou",
                    "o": "aeiu",
                    "u": "aeio"
                    }

                sound_approximate = {
                    "q": "kc",
                    "w": "uo",
                    "i": "ye",
                    "c": "kq",
                    "k": "qc",
                    "u": "w",
                    "y": "ie",
                    "e": "yi",
                    "o": "wu"
                    }


                for a in range(len(searched_word_letters)):

                    #------------ Checking for slight mispells due to misclicks -------------
                    for k, v in keyboard_approximate.items():
                        if tested_word_letters[a] == k:
                            for approx_letter in v:
                                tested_word_letters = searched_word_letters.copy()
                                tested_word_letters[a] = approx_letter
                                tested_word = ""
                                for i in tested_word_letters:
                                    tested_word = tested_word + i
                                if store.exists(tested_word):
                                    ka_suggested_words.append(tested_word)
                                else:
                                    pass
                #------------------------------------------------------------------------
                    tested_word_letters = searched_word_letters.copy() #Reset tested list to original

                #----------- Checking for mispells due to mixing vowels around ----------
                    for y, z in vowel_approximate.items():
                        if tested_word_letters[a] == y:
                            for approx_vowel in z:
                                tested_word_letters = searched_word_letters.copy()
                                tested_word_letters[a] = approx_vowel
                                tested_word = ""
                                for h in tested_word_letters:
                                    tested_word = tested_word + h
                                if store.exists(tested_word):
                                    va_sa_suggested_words.append(tested_word)
                                else:
                                    pass
                #------------------------------------------------------------------------

                    tested_word_letters = searched_word_letters.copy() #Reset tested list to original

                #------------------------------------------------------------------------

                #----------- Checking for mispells due to similar sounds ----------------
                    for j, p in sound_approximate.items():
                        if tested_word_letters[a] == j:
                            for homonym in p:
                                tested_word_letters = searched_word_letters.copy()
                                tested_word_letters[a] = homonym
                                tested_word = ""
                                for h in tested_word_letters:
                                    tested_word = tested_word + h
                                if store.exists(tested_word):
                                    va_sa_suggested_words.append(tested_word)
                                else:
                                    pass
                #------------------------------------------------------------------------
                tested_word_letters = searched_word_letters.copy() #Reset tested list to original


                ka_suggested_words = list(set(ka_suggested_words))
                va_sa_suggested_words = list(set(va_sa_suggested_words))



                self.answer.text = "The word " + self.userinput.text + " does not exist."
                if len(ka_suggested_words) > 0 and len(va_sa_suggested_words) > 0:
                    ka_suggestion_text = "Perhaps you meant to type these?: "
                    for i in range(len(ka_suggested_words)):
                        ka_suggestion_text += f"({i}) {ka_suggested_words[i]} "
                    self.results1.text = ka_suggestion_text
                    va_sa_suggestion_text = "Or maybe you misheard these: "
                    for r in range(len(va_sa_suggested_words)):
                        va_sa_suggestion_text += f"({r}) {va_sa_suggested_words[r] }"
                    self.results2.text = va_sa_suggestion_text

                elif len(ka_suggested_words) == 0 and len(va_sa_suggested_words) == 0:
                    self.results1.text = "No suggestions available"
                    self.results2.text = ""

                elif len(ka_suggested_words) > 0 and len(va_sa_suggested_words) == 0:
                    ka_suggestion_text = "Perhaps you meant to type these?: "
                    for i in range(len(ka_suggested_words)):
                        ka_suggestion_text += f"({i}) {ka_suggested_words[i]} "
                    self.results1.text = ka_suggestion_text
                    self.results2.text = ""
                else:
                    va_sa_suggestion_text = "Perhaps you misheard these: "
                    for r in range(len(va_sa_suggested_words)):
                        va_sa_suggestion_text += f"({r}) {va_sa_suggested_words[r]} "
                    self.results1.text = va_sa_suggestion_text
                    self.results2.text = ""

        # The number of words written exceeds the limit of application
        elif len(final_values) > 10:
            self.answer.text = "You have exceeded the word limit. Please delete at least " + str(len(final_values) - 10) + " words."
            self.results1.text = ""
            self.results2.text = ""

        # If text input is a phrase/sentence
        elif 1 < len(final_values) <= 10:
            suggestions_dict = {}
            final_suggestions_dict = {}
            word_checker = []
            misspelled_words_list = []

            # Know if each word in phrase/sentence is correctly spelled
            for word in final_values:
                if store.exists(word.lower()) == True:
                    word_checker.append("True")
                if store.exists(word.lower()) == False:
                    word_checker.append("False")

            # If there is at least one misspelled word
            if "False" in word_checker:
                searched_sentence = final_values
                tested_word = ""

                for test_word in searched_sentence:
                    if store.exists(test_word.lower()) == True:
                        pass
                    elif store.exists(test_word.lower()) == False:
                        misspelled_words_list.append(test_word)
                        searched_word_letters = []
                        searched_word = (self.userinput.text).lower()
                        tested_word_letters = []
                        for letter in test_word: #This allows the letters to revert to the original input after going through all the alternatives
                            searched_word_letters.append(letter)
                        tested_word_letters = []
                        for letter in test_word: #This is what's actually being tested down there \/
                            tested_word_letters.append(letter)

                        ka_suggested_words = []
                        va_sa_suggested_words= []

                        #Accounts for misclicks, hasty and careless typing, or disproportionately large-handed people with disproportionately tiny keyboards
                        keyboard_approximate = {
                            "a": "qwesxz",
                            "b": "vghn",
                            "c": "xdfv",
                            "d": "wersfxcv",
                            "e": "wsdfr",
                            "f": "ertdgcvb",
                            "g": "rtyfhvbn",
                            "h": "tyugjbnm",
                            "i": "ujklo",
                            "j": "yuihknm",
                            "k": "uiojlm",
                            "l": "kiop",
                            "m": "nhjkl",
                            "n": "bhjm",
                            "o": "iklp",
                            "p": "ol",
                            "q": "asw",
                            "r": "edfgt",
                            "s": "qazxcdew",
                            "t": "rfghy",
                            "u": "yhjki",
                            "v": "cfgb",
                            "w": "qasde",
                            "x": "zasdc",
                            "y": "tghju",
                            "z": "asx"
                            }

                        #In case people get vowels mixed up
                        vowel_approximate = {
                            "a": "eiou",
                            "e": "aiou",
                            "i": "aeou",
                            "o": "aeiu",
                            "u": "aeio"
                            }

                        sound_approximate = {
                            "q": "kc",
                            "w": "uo",
                            "i": "ye",
                            "c": "kq",
                            "k": "qc",
                            "u": "w",
                            "y": "ie",
                            "e": "yi",
                            "o": "wu"
                            }


                        for a in range(len(searched_word_letters)):

                        #------------ Checking for slight mispells due to misclicks -------------
                            for k, v in keyboard_approximate.items():
                                if tested_word_letters[a] == k:
                                    for approx_letter in v:
                                        tested_word_letters = searched_word_letters.copy()
                                        tested_word_letters[a] = approx_letter
                                        tested_word = ""
                                        for i in tested_word_letters:
                                            tested_word = tested_word + i
                                        if store.exists(tested_word.lower()):
                                            ka_suggested_words.append(tested_word)
                                        else:
                                            pass
                        #------------------------------------------------------------------------
                            tested_word_letters = searched_word_letters.copy() #Reset tested list to original

                        #----------- Checking for mispells due to mixing vowels around ----------
                            for y, z in vowel_approximate.items():
                                if tested_word_letters[a] == y:
                                    for approx_vowel in z:
                                        tested_word_letters = searched_word_letters.copy()
                                        tested_word_letters[a] = approx_vowel
                                        tested_word = ""
                                        for h in tested_word_letters:
                                            tested_word = tested_word + h
                                        if store.exists(tested_word.lower()):
                                            va_sa_suggested_words.append(tested_word)
                                        else:
                                            pass
                        #------------------------------------------------------------------------

                            tested_word_letters = searched_word_letters.copy() #Reset tested list to original

                        #------------------------------------------------------------------------

                        #----------- Checking for mispells due to similar sounds ----------------
                            for j, p in sound_approximate.items():
                                if tested_word_letters[a] == j:
                                    for homonym in p:
                                        tested_word_letters = searched_word_letters.copy()
                                        tested_word_letters[a] = homonym
                                        tested_word = ""
                                        for h in tested_word_letters:
                                            tested_word = tested_word + h
                                        if store.exists(tested_word):
                                            va_sa_suggested_words.append(tested_word)
                                        else:
                                            pass
                        #------------------------------------------------------------------------
                        tested_word_letters = searched_word_letters.copy() #Reset tested list to original

                        # Suggestions for specific word analyzed
                        indv_suggestion_list = []

                        if len(ka_suggested_words) == 0 and len(va_sa_suggested_words) == 0:
                            indv_suggestion_list.append("No suggestions available")
                            suggestions_dict[test_word] = indv_suggestion_list

                        else:
                            for i in range(len(ka_suggested_words)):
                                indv_suggestion_list.append(ka_suggested_words[i])
                            for r in range(len(va_sa_suggested_words)):
                                indv_suggestion_list.append(va_sa_suggested_words[r])

                            # Used so that \n can be placed later on
                            indv_suggestion_list.append("],/filler/")

                            suggestions_dict[test_word] = indv_suggestion_list

                    self.answer.text = "\n\n The following words do not exist: \n" + str(set(misspelled_words_list))
                    self.results1.text = "Suggestions:"

                    # To make appearance of answer neater
                    suggestions = str(suggestions_dict).replace("{","")
                    suggestions = suggestions.replace("}","")
                    suggestions = suggestions.replace("[","")
                    suggestions = suggestions.replace("]","")

                    if len(suggestions_dict) == 1:
                        suggestions = suggestions.replace(", ',/filler/'","")
                        suggestions = suggestions.replace(" available', "," available', \n")
                    if len(suggestions_dict) > 1:
                        suggestions = suggestions.replace(", ',/filler/', ","\n")
                        suggestions = suggestions.replace(" available', "," available', \n")
                        suggestions = suggestions.replace(", ',/filler/'","\n")

                    self.results2.text = suggestions

            else:
                # All words in the phrase/sentence are spelled correctly
                self.answer.text = "All words are spelled correctly."
                self.results1.text = ""
                self.results2.text = ""


# run program
if __name__ == "__main__":
    DictTest().run()
