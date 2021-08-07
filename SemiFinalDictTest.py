from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore

class DictTest(App):
    def build(self):
        #returns a window object with all it's widgets
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # image widget
        self.window.add_widget(Image(source="logo.png"))

        # label widget
        self.greeting = Label(
                        text= "What's the word?",
                        font_size= 18,
                        color= '#00FFCE'
                        )
        self.window.add_widget(self.greeting)

        # text input widget
        self.user = TextInput(
                    multiline= False,
                    padding_y= (20,20),
                    size_hint= (1, 0.5)
                    )

        self.window.add_widget(self.user)

        # button widget
        self.button = Button(
                      text= "CHECK SPELLING",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#00FFCE',
                      #remove darker overlay of background colour
                      # background_normal = ""
                      )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, instance):
        # change label text to "Hello + user name!"
        store = JsonStore('filo_dict.json')
        if store.exists((self.user.text).lower()):
            self.greeting.text = "The word" + " " + self.user.text + " " + "exists."
        else:
            #Suggested Words
            searched_word = (self.user.text).lower()
            tested_word_letters = []
            searched_word_letters = []
            tested_word = ""

            for letter in searched_word: #This allows the letters to revert to the original input after going through all the alternatives
                searched_word_letters.append(letter)

            for letter in searched_word: #This is what's actually being tested down there \/
                tested_word_letters.append(letter)

            print(tested_word_letters)
            print(searched_word_letters)
            suggested_words = []

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

            vowel_approximate = {
                "a": "eiou",
                "e": "aiou",
                "i": "aeou",
                "o": "aeiu",
                "u": "aeio"
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
                                suggested_words.append(tested_word)
                            else:
                                pass
            #------------------------------------------------------------------------
                tested_word_letters = searched_word_letters.copy() #Reset tested list to original

            #----------- Checking for mispells due to mixing vowels around ----------             
                for y, z in vowel_approximate.items():
                    if tested_word_letters[a] == y:
                        print("detected")
                        for approx_vowel in z:
                            tested_word_letters = searched_word_letters.copy()
                            tested_word_letters[a] = approx_vowel
                            tested_word = ""
                            for h in tested_word_letters:
                                tested_word = tested_word + h
                            print(tested_word)
                            if store.exists(tested_word):
                                suggested_words.append(tested_word)
                            else:
                                pass
            #------------------------------------------------------------------------
                tested_word_letters = searched_word_letters.copy() #Reset tested list to original

            suggested_words = list(set(suggested_words))
            self.greeting.text = "The word " + self.user.text + " does not exist."
            print(f"Perhaps you meant to type {suggested_words}")
            
    

# run Say Hello App Calss
if __name__ == "__main__":
    DictTest().run()
