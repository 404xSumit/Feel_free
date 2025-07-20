# # from my_api import API_KEY, genai
# # import nltk
# # from nltk.stem import PorterStemmer
# # stemmer = PorterStemmer()
# # genai.configure(api_key=API_KEY)
# # model = genai.GenerativeModel("gemini-1.5-flash")

# # # Define mental health-related keywords
# # mental_health_keywords = [
# #     "anxiety", "depression", "stress", "therapy", "mental health", "counseling",
# #     "panic", "sleep", "sad", "unmotivated", "lonely", "anger", "wellbeing",
# #     "self-esteem", "motivation", "overwhelmed", "confidence", "burnout",
# #     "self care", "mood", "trauma", "grief", "personal health", "feel", "emotions",
# #     "support", "talk", "mental", "how to cope", "frustrated", "cry", "depressed", 
# #     "anxious", "lonely", "alone", "unmotivated", "burnout", "suicide", "loser", "embarrasing","scold","fight", "feel", "relative" ,"passed","die"
# # ]

# # stemmed_keywords = [stemmer.stem(word.lower()) for word in mental_health_keywords]


# # exit_commands = ["bye", "thank you", "ok", "thanks"]

# # # Check if input is related to mental health
# # def is_mental_health_related(text):
# #     text = text.lower()
# #     words = nltk.word_tokenize(text)
# #     stemmed_input = [stemmer.stem(word) for word in words]
# #     return any(stemmed_word in stemmed_input for stemmed_word in stemmed_keywords)

# # def empathetic_response(text, is_first_response):
# #     if "sad" in text:
# #         return (
# #             "I'm so sorry you're feeling sad. It must be really tough right now. "
# #             "It's okay to feel this way, and it's important to give yourself the time you need to process your emotions. "
# #             "Take care of yourself during this time."
# #         ) if is_first_response else (
# #             "I'm here for you. I understand that feeling sad can be overwhelming, but please remember that you're not alone."
# #         )
# #     elif "anxious" in text:
# #         return (
# #             "It sounds like you're feeling really anxious, and I want you to know that your feelings are valid. "
# #             "It can be overwhelming when anxiety takes hold, but you're not alone in this. "
# #             "Remember, you're strong, and it's okay to take things one step at a time."
# #         ) if is_first_response else (
# #             "I can imagine how overwhelming anxiety can be. Take your time, and remember you're capable of managing it, step by step."
# #         )
# #     elif "depressed" in text:
# #         return (
# #             "I'm really sorry you're feeling this way. Depression can feel isolating, but you're not alone. "
# #             "It's okay to take things one step at a time. Please be kind to yourself, and don't hesitate to reach out when you're ready."
# #         ) if is_first_response else (
# #             "Depression can be really tough, but you're not alone. Be gentle with yourself, and know that it's okay to feel this way."
# #         )
# #     elif "lonely" in text:
# #         return (
# #             "I'm so sorry you're feeling lonely right now. Loneliness can be incredibly hard to bear, but it doesn't mean you're alone. "
# #             "I'm here with you, and I want to remind you that you are worthy of connection and care."
# #         ) if is_first_response else (
# #             "Loneliness can be so hard, but you're not truly alone. I'm here, and I’m happy to listen if you need me."
# #         )
# #     elif "burnout" in text:
# #         return (
# #             "Burnout can leave you feeling drained and overwhelmed. It's okay to feel exhausted, and you don't have to carry that weight alone. "
# #             "Please remember that it's important to take a break and recharge. You've been working hard, and it's okay to pause."
# #         ) if is_first_response else (
# #             "I understand that burnout can be overwhelming. It's okay to step back and take time for yourself to rest and recharge."
# #         )
# #     else:
# #         return model.generate_content(text).text

# # print("Hi, I'm feelfree. I'm here to support your personal wellbeing. Type 'bye', 'thank you', or 'ok' to exit.\n")


# # first_response = True

# # while True:
# #     user_input = input("You: ").strip().lower()

# #     if user_input in exit_commands:
# #         print("feelfree: Goodbye! Take care of yourself.")
# #         break

# #     if is_mental_health_related(user_input):
# #         response = empathetic_response(user_input, first_response)  # Pass first_response flag
# #         print("feelfree:", response)
        
# #         # After the first response, we don't want to ask similar questions again
# #         first_response = False
# #     else:
# #         print("feelfree: Sorry, I am here to have conversations related to your personal wellbeing only.")

# # #return model.generate_content(text).text

# from my_api import API_KEY, genai
# import nltk
# from nltk.stem import PorterStemmer

# class FeelFreeChatbot:
#     def __init__(self):
#         self.stemmer = PorterStemmer()
#         genai.configure(api_key=API_KEY)
#         self.model = genai.GenerativeModel("gemini-1.5-flash")
#         self.first_response = True
        
#         # Define mental health keywords
#         self.mental_health_keywords = [
#      "anxiety", "depression", "stress", "therapy", "mental health", "counseling",
#      "panic", "sleep", "sad", "unmotivated", "lonely", "anger", "wellbeing",
#      "self-esteem", "motivation", "overwhelmed", "confidence", "burnout",
#      "self care", "mood", "trauma", "grief", "personal health", "feel", "emotions",
#      "support", "talk", "mental", "how to cope", "frustrated", "cry", "depressed", 
#      "anxious", "lonely", "alone", "unmotivated", "burnout", "suicide", "loser", "embarrasing","scold","fight", "feel", "relative" ,"passed","die"
#         ]
#         self.stemmed_keywords = [self.stemmer.stem(word.lower()) for word in self.mental_health_keywords]
#         self.exit_commands = ["bye", "thank you", "ok", "thanks"]

#     def is_mental_health_related(self, text):
#         text = text.lower()
#         words = nltk.word_tokenize(text)
#         stemmed_input = [self.stemmer.stem(word) for word in words]
#         return any(stemmed_word in stemmed_input for stemmed_word in self.stemmed_keywords)

#     def empathetic_response(self, text, is_first_response):
#         # ... (keep your existing empathetic_response logic) ...
#         pass
    
#     class FeelFreeChatbot:
#      def __init__(self):
#         self.stemmer = PorterStemmer()
#         genai.configure(api_key=API_KEY)
#         self.model = genai.GenerativeModel("gemini-1.5-flash")
#         self.first_response = True
        
#         # Define mental health keywords
#         self.mental_health_keywords = [
#      "anxiety", "depression", "stress", "therapy", "mental health", "counseling",
#      "panic", "sleep", "sad", "unmotivated", "lonely", "anger", "wellbeing",
#      "self-esteem", "motivation", "overwhelmed", "confidence", "burnout",
#      "self care", "mood", "trauma", "grief", "personal health", "feel", "emotions",
#      "support", "talk", "mental", "how to cope", "frustrated", "cry", "depressed", 
#      "anxious", "lonely", "alone", "unmotivated", "burnout", "suicide", "loser", "embarrasing","scold","fight", "feel", "relative" ,"passed","die"
#         ]
#         self.stemmed_keywords = [self.stemmer.stem(word.lower()) for word in self.mental_health_keywords]
#         self.exit_commands = ["bye", "thank you", "ok", "thanks"]

#     def is_mental_health_related(self, text):
#         text = text.lower()
#         words = nltk.word_tokenize(text)
#         stemmed_input = [self.stemmer.stem(word) for word in words]
#         return any(stemmed_word in stemmed_input for stemmed_word in self.stemmed_keywords)

#     def empathetic_response(self, text, is_first_response):
#         # ... (keep your existing empathetic_response logic) ...
#         pass

#     # def get_response(self, user_input):
#     #     user_input = user_input.strip().lower()
        
#     #     if user_input in self.exit_commands:
#     #         return {
#     #             'response': "Goodbye! Take care of yourself.",
#     #             'exit': True
#     #         }
        
#     #     if self.is_mental_health_related(user_input):
#     #         response = self.empathetic_response(user_input, self.first_response)
#     #         self.first_response = False
#     #         return {
#     #             'response': response,
#     #             'exit': False
#     #         }
#     #     else:
#     #         return {
#     #             'response': "Sorry, I am here to have conversations related to your personal wellbeing only.",
#     #             'exit': False
#     #         }
#     def get_response(self, user_input, is_first_response=True):
#      user_input = user_input.strip().lower()

#      if user_input in self.exit_commands:
#         return {"response": "Goodbye! Take care of yourself.", "exit": True}

#      if self.is_mental_health_related(user_input):
#         if is_first_response:
#             response = self.first_empathetic_response(user_input)
#         else:
#             response = self.gemini_response(user_input)
#         return {"response": response, "exit": False}
#      else:
#         return {
#             "response": "Sorry, I am here to have conversations related to your personal wellbeing only.",
#             "exit": False
#         }



#     # def get_response(self, user_input):
#     #     user_input = user_input.strip().lower()
        
#     #     if user_input in self.exit_commands:
#     #         return {
#     #             'response': "Goodbye! Take care of yourself.",
#     #             'exit': True
#     #         }
        
#     #     if self.is_mental_health_related(user_input):
#     #         response = self.empathetic_response(user_input, self.first_response)
#     #         self.first_response = False
#     #         return {
#     #             'response': response,
#     #             'exit': False
#     #         }
#     #     else:
#     #         return {
#     #             'response': "Sorry, I am here to have conversations related to your personal wellbeing only.",
#     #             'exit': False
#     #         }

# import nltk
# from nltk.stem import PorterStemmer
# from my_api import API_KEY, genai

# # Ensure necessary NLTK resources are downloaded
# nltk.download('punkt')  # Download the necessary resources for tokenization

# class FeelFreeChatbot:
#     def __init__(self):
#         # Initialize the stemmer and the AI model
#         self.stemmer = PorterStemmer()
#         genai.configure(api_key=API_KEY)
#         self.model = genai.GenerativeModel("gemini-1.5-flash")
#         self.first_response = True
        
#         # Define mental health keywords
#         self.mental_health_keywords = [
#             "anxiety", "depression", "stress", "therapy", "mental health", "counseling",
#             "panic", "sleep", "sad", "unmotivated", "lonely", "anger", "wellbeing",
#             "self-esteem", "motivation", "overwhelmed", "confidence", "burnout",
#             "self care", "mood", "trauma", "grief", "personal health", "feel", "emotions",
#             "support", "talk", "mental", "how to cope", "frustrated", "cry", "depressed", 
#             "anxious", "lonely", "alone", "unmotivated", "burnout", "suicide", "loser", 
#             "embarrasing", "scold", "fight", "feel", "relative", "passed", "die"
#         ]
#         # Stemmed keywords to make it case insensitive and match words
#         self.stemmed_keywords = [self.stemmer.stem(word.lower()) for word in self.mental_health_keywords]
#         # Exit commands
#         self.exit_commands = ["bye", "thank you", "ok", "thanks"]

#     def is_mental_health_related(self, text):
#         # Tokenize and stem input text
#         text = text.lower()
#         words = nltk.word_tokenize(text)
#         stemmed_input = [self.stemmer.stem(word) for word in words]
#         # Check if any of the stemmed words match mental health keywords
#         return any(stemmed_word in stemmed_input for stemmed_word in self.stemmed_keywords)

#     def empathetic_response(self, text, is_first_response):
#         # Provide empathetic response based on whether it's the first response
#         if is_first_response:
#             return "I'm really sorry you're feeling this way. Can I help with anything specific?"
#         else:
#             return "I'm here to listen. Please share more about how you're feeling."

#     def get_response(self, user_input, first_response):
#         user_input = user_input.strip().lower()

#         # Handle exit commands
#         if user_input in self.exit_commands:
#             return {"response": "Goodbye! Take care of yourself.", "exit": True}

#         # Handle mental health-related input
#         if self.is_mental_health_related(user_input):
#             response = self.empathetic_response(user_input, self.first_response)
#             # After the first response, we set `first_response` to False
#             if self.first_response:
#                 self.first_response = False
#             return {"response": response, "exit": False}
#         else:
#             return {
#                 "response": "Sorry, I am here to have conversations related to your personal wellbeing only.",
#                 "exit": False
#             }

