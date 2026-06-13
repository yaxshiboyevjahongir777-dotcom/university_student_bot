from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_url = State()
    waiting_for_admin_id = State()
    waiting_for_excel = State()
    waiting_for_word = State()
    waiting_for_name = State()
    waiting_for_course = State()
    waiting_for_phone = State()
    
    # Mana shu qator sizda yetishmayotgan edi:
    waiting_for_universal = State()