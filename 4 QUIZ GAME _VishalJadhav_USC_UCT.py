import random

class QuizGame:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0

    def start_game(self):
        random.shuffle(self.questions)
        for index, question in enumerate(self.questions):
            print(f"Question {index + 1}: {question['text']}")
            if question.get('options'):
                self.display_options(question['options'])
            user_answer = input("Your answer: ")
            self.check_answer(user_answer, question['answer'])
            print()  # Add a line break after each question

        self.display_final_score()

    def display_options(self, options):
        for option in options:
            print(f"- {option}")
        print()

    def check_answer(self, user_answer, correct_answer):
        if user_answer.lower() == correct_answer.lower():
            print("Correct!")
            self.score += 1
        else:
            print("Incorrect!")

    def display_final_score(self):
        print("Quiz completed!")
        print(f"Your final score is: {self.score}/{len(self.questions)}")

# Example usage
questions = [
    {
        'text': 'What is the capital of India??',
        'options': ['a) Mumbai', 'b) New Delhi', 'c) Kolkata', 'd) Chennai'],
        'answer': 'b'
    },
    {
        'text': ' Which river is considered sacred by Hindus and is known as the "Ganges"?',
        'options': ['a) Yamuna','b) Brahmaputra','c) Godavari','d) Ganga'],
        'answer': 'd'
    },
    {
        'text': 'Which monument is a UNESCO World Heritage Site and is known as the symbol of love?',
        'options': ['a) Taj Mahal ','b) Red Fort','c) Qutub Mina','d) Hawa Mahal'],
        'answer': 'a'
    },

    {
        'text': 'Which Indian festival is widely celebrated with the lighting of oil lamps and symbolizes the victory of light over darkness?',
        'options': ['a) Holi', 'b) Diwali', 'c) Eid', 'd) Christmas'],
        'answer': 'b'
    },
    {
        'text': 'Which state in India is known for its backwaters, houseboat cruises, and Kathakali dance?',
        'options': ['a) Goa', 'b) Kerala', 'c) Tamil Nadu', 'd) Maharashtraa'],
        'answer': 'b'
    }
]

game = QuizGame(questions)
game.start_game()
