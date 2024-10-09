from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    question = State()
    a_var = State()
    b_var = State()
    c_var = State()
    d_var = State()
    correct_answer = State()
    kind = State()
    

class Adverts(StatesGroup):
    adverts = State()
    
class MessageAdmin(StatesGroup):
    user_text = State()
    
class AdminStates(StatesGroup):
    waiting_for_admin_message = State()
    waiting_for_reply_message = State()