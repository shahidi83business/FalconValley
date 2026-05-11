
import random
import math

def calculate_prisoner_payoff(player_move, opponent_move, params):
    """
    player_move/opponent_move: 0 برای همکاری (Cooperate)، 1 برای خیانت (Defect)
    params: { 'R': 3, 'T': 5, 'S': 0, 'P': 1, 'rho': 1.0 }
    """
    R, T, S, P = params['R'], params['T'], params['S'], params['P']
    rho = params.get('rho', 1.0) # ضریب ریسک‌پذیری
    matrix = {
        (0, 0): (R, R), # هر دو همکاری
        (0, 1): (S, T), # بازیکن همکاری، رقیب خیانت
        (1, 0): (T, S), # بازیکن خیانت، رقیب همکاری
        (1, 1): (P, P)  # هر دو خیانت
    }

    p1_raw, p2_raw = matrix[(player_move, opponent_move)]

    p1_final = p1_raw * rho if p1_raw > P else p1_raw / rho
    
    return p1_final, p2_raw

def update_trust(current_trust, player_move, opponent_move, params):
    """
    params: { 'gain': 0.1, 'penalty': 0.4, 'forgiveness': 0.05 }
    """
    gain = params['gain']           
    penalty = params['penalty']   
    forgiveness = params.get('forgiveness', 0.0)

    new_trust = current_trust

    if player_move == 0 and opponent_move == 0:
        new_trust += gain
    elif opponent_move == 1: 
        new_trust -= penalty
    elif player_move == 1 and opponent_move == 0: # بازیکن خیانت کرده
        new_trust -= (penalty / 2) # اعتماد رقیب به بازیکن کم می‌شود

    if player_move == 0 and opponent_move == 1:
        new_trust += forgiveness 

    return max(0, min(1, new_trust)) # مقدار بین 0 و 1

def calculate_reputation(move_history, params):
    """
    move_history: لیستی از 0 و 1 ها (0=cooperate)
    params: { 'window': 10, 'weight_recent': True }
    """
    if not move_history:
        return 50 # شهرت اولیه متوسط

    window = params.get('window', 10)
    relevant_moves = move_history[-window:]
    
    # محاسبه درصد همکاری (تعداد 0 ها)
    cooperation_count = relevant_moves.count(0)
    base_score = (cooperation_count / len(relevant_moves)) * 100

    # اگر وزن دهی به فالیت‌های اخیر فعال باشد
    if params.get('weight_recent'):
        # حرکت آخر ۲ برابر وزن دارد
        recent_bonus = 10 if move_history[-1] == 0 else -10
        base_score = max(0, min(100, base_score + recent_bonus))

    return base_score

def predict_player_behavior(player_history, params):
    """
    خروجی: احتمال همکاری بازیکن در راند بعدی (0 تا 1)
    params: { 'strategy': 'memory_based', 'depth': 3 }
    """
    if not player_history:
        return 0.5 # پیش‌فرض: خنثی

    depth = params.get('depth', 3)
    recent_moves = player_history[-depth:]
    

    coop_rate = recent_moves.count(0) / len(recent_moves)
    
    noise = params.get('noise', 0.05)
    prediction = coop_rate + (noise if coop_rate < 0.5 else -noise)

    return max(0, min(1, prediction))

def risk_utility(outcomes, probabilities, params):
    """
    outcomes: لیست سود/زیان‌ها
    probabilities: لیست احتمال‌ها (جمع = 1)
    params: { 'risk_aversion': 0.5 }
    """

    rho = params.get('risk_aversion', 0.5)

    utility = 0
    for x, p in zip(outcomes, probabilities):
        # تابع utility ریسک‌گریز
        if x >= 0:
            u = math.pow(x, 1 - rho)
        else:
            u = -math.pow(abs(x), 1 - rho)

        utility += p * u

    return utility

def apply_uncertainty(value, params):
    """
    params: { 'noise_level': 0.1 }
    """
    noise = params.get('noise_level', 0.1)
    deviation = random.uniform(-noise, noise)
    return value + deviation

def risk_adjusted_payoff(base_payoff, risk_score, params):
    """
    risk_score: بین 0 و 1
    """
    penalty = params.get('risk_penalty', 0.3)
    return base_payoff * (1 - penalty * risk_score)

def perceived_risk(real_risk, params):
    """
    real_risk: عددی بین 0 تا 1
    params: { 'sensitivity': 1.5 }
    """
    sensitivity = params.get('sensitivity', 1.0)
    return min(1, real_risk ** sensitivity)


def prospect_theory(outcomes, probabilities, params):
    """
    params:
    {
      'alpha': 0.88,
      'beta': 0.88,
      'lambda': 2.25
    }
    """

    alpha = params.get('alpha', 0.88)
    beta = params.get('beta', 0.88)
    lambd = params.get('lambda', 2.25)

    value = 0
    for x, p in zip(outcomes, probabilities):
        if x >= 0:
            v = x ** alpha
        else:
            v = -lambd * (abs(x) ** beta)

        value += p * v

    return value
