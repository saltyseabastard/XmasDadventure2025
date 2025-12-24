import random

# python
class HackerGame:

    def __init__(self):
        self.answered_count = 0
        self.max_questions = 10
        self.current_question = None
        self.current_answer = None
        self.awaiting_answer = False

    def start_game(self):
        self.answered_count = 0
        self.current_question = None
        self.current_answer = None
        self.awaiting_answer = False
        return self.next_question()

    def next_question(self):
        if self.answered_count >= self.max_questions:
            return None, "COMPLETE"

        # If a question is still awaiting an answer, return it again
        if self.awaiting_answer and self.current_question is not None:
            return self.current_question, "ACTIVE"

        # Generate a new question and mark it as awaiting an answer
        ops = ['+', '-', '*', '/']
        op = random.choice(ops)

        if op == '+':
            a = random.randint(10, 100)
            b = random.randint(10, 100)
            ans = a + b
        elif op == '-':
            a = random.randint(20, 100)
            b = random.randint(10, a)
            ans = a - b
        elif op == '*':
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            ans = a * b
        elif op == '/':
            b = random.randint(2, 12)
            ans = random.randint(2, 12)
            a = b * ans

        self.current_answer = ans
        self.current_question = f"{a} {op} {b} = ?"
        self.awaiting_answer = True

        return self.current_question, "ACTIVE"

    def check_answer(self, user_answer):
        try:
            val = int(user_answer.strip())
            correct = val == self.current_answer
        except ValueError:
            correct = False

        # Consume the current question (whether correct or not)
        self.awaiting_answer = False
        self.answered_count += 1

        return correct


