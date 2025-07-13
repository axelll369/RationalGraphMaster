import sympy as sp
from sympy import symbols, apart, limit, oo, solve, factor, cancel, Poly
import re

class GameLogic:
    def __init__(self):
        self.x = symbols('x')
    
    def check_answers(self, func_data, user_answers):
        """Check user answers against the correct function features"""
        correct_features = func_data['features']
        score = 0
        max_score = 500  # 100 points per feature
        feedback = {}
        
        # Check vertical asymptotes
        va_score, va_feedback = self._check_vertical_asymptotes(
            correct_features['vertical_asymptotes'], 
            user_answers['vertical_asymptotes']
        )
        score += va_score
        feedback['vertical_asymptotes'] = va_feedback
        
        # Check horizontal asymptote
        ha_score, ha_feedback = self._check_horizontal_asymptote(
            correct_features['horizontal_asymptote'], 
            user_answers['horizontal_asymptote']
        )
        score += ha_score
        feedback['horizontal_asymptote'] = ha_feedback
        
        # Check holes
        holes_score, holes_feedback = self._check_holes(
            correct_features['holes'], 
            user_answers['holes']
        )
        score += holes_score
        feedback['holes'] = holes_feedback
        
        # Check x-intercepts
        x_int_score, x_int_feedback = self._check_x_intercepts(
            correct_features['x_intercepts'], 
            user_answers['x_intercepts']
        )
        score += x_int_score
        feedback['x_intercepts'] = x_int_feedback
        
        # Check y-intercept
        y_int_score, y_int_feedback = self._check_y_intercept(
            correct_features['y_intercept'], 
            user_answers['y_intercept']
        )
        score += y_int_score
        feedback['y_intercept'] = y_int_feedback
        
        return score, feedback
    
    def _parse_numbers(self, input_str):
        """Parse comma-separated numbers from string"""
        if not input_str or input_str.lower().strip() in ['none', 'undefined', '']:
            return []
        
        try:
            # Remove spaces and split by comma
            numbers = []
            for item in input_str.split(','):
                item = item.strip()
                if item:
                    # Try to parse as fraction or decimal
                    if '/' in item:
                        parts = item.split('/')
                        numbers.append(float(parts[0]) / float(parts[1]))
                    else:
                        numbers.append(float(item))
            return sorted(numbers)
        except:
            return []
    
    def _check_vertical_asymptotes(self, correct, user_input):
        """Check vertical asymptotes"""
        user_vas = self._parse_numbers(user_input)
        correct_vas = sorted([float(va) for va in correct])
        
        if set(user_vas) == set(correct_vas):
            return 100, {
                'correct': True, 
                'message': f'Correct! Vertical asymptotes at x = {", ".join(map(str, correct_vas))}'
            }
        else:
            return 0, {
                'correct': False,
                'message': f'Incorrect. The vertical asymptotes are at x = {", ".join(map(str, correct_vas))}'
            }
    
    def _check_horizontal_asymptote(self, correct, user_input):
        """Check horizontal asymptote"""
        user_input = user_input.strip().lower()
        
        if correct is None:
            if user_input in ['none', 'undefined', '']:
                return 100, {'correct': True, 'message': 'Correct! No horizontal asymptote exists.'}
            else:
                return 0, {'correct': False, 'message': 'Incorrect. There is no horizontal asymptote.'}
        else:
            try:
                user_ha = float(user_input)
                if abs(user_ha - correct) < 0.001:
                    return 100, {'correct': True, 'message': f'Correct! Horizontal asymptote at y = {correct}'}
                else:
                    return 0, {'correct': False, 'message': f'Incorrect. The horizontal asymptote is y = {correct}'}
            except:
                return 0, {'correct': False, 'message': f'Incorrect. The horizontal asymptote is y = {correct}'}
    
    def _check_holes(self, correct, user_input):
        """Check holes"""
        user_holes = self._parse_numbers(user_input)
        correct_holes = sorted([float(hole[0]) for hole in correct]) if correct else []
        
        if set(user_holes) == set(correct_holes):
            if not correct_holes:
                return 100, {'correct': True, 'message': 'Correct! No holes in this function.'}
            else:
                return 100, {
                    'correct': True, 
                    'message': f'Correct! Holes at x = {", ".join(map(str, correct_holes))}'
                }
        else:
            if not correct_holes:
                return 0, {'correct': False, 'message': 'Incorrect. There are no holes in this function.'}
            else:
                return 0, {
                    'correct': False,
                    'message': f'Incorrect. The holes are at x = {", ".join(map(str, correct_holes))}'
                }
    
    def _check_x_intercepts(self, correct, user_input):
        """Check x-intercepts"""
        user_x_ints = self._parse_numbers(user_input)
        correct_x_ints = sorted([float(x_int) for x_int in correct]) if correct else []
        
        if set(user_x_ints) == set(correct_x_ints):
            if not correct_x_ints:
                return 100, {'correct': True, 'message': 'Correct! No x-intercepts for this function.'}
            else:
                return 100, {
                    'correct': True, 
                    'message': f'Correct! x-intercepts at x = {", ".join(map(str, correct_x_ints))}'
                }
        else:
            if not correct_x_ints:
                return 0, {'correct': False, 'message': 'Incorrect. There are no x-intercepts.'}
            else:
                return 0, {
                    'correct': False,
                    'message': f'Incorrect. The x-intercepts are at x = {", ".join(map(str, correct_x_ints))}'
                }
    
    def _check_y_intercept(self, correct, user_input):
        """Check y-intercept"""
        user_input = user_input.strip().lower()
        
        if correct is None:
            if user_input in ['none', 'undefined', '']:
                return 100, {'correct': True, 'message': 'Correct! No y-intercept (undefined at x=0).'}
            else:
                return 0, {'correct': False, 'message': 'Incorrect. The y-intercept is undefined.'}
        else:
            try:
                user_y_int = float(user_input)
                if abs(user_y_int - correct) < 0.001:
                    return 100, {'correct': True, 'message': f'Correct! y-intercept at y = {correct}'}
                else:
                    return 0, {'correct': False, 'message': f'Incorrect. The y-intercept is y = {correct}'}
            except:
                return 0, {'correct': False, 'message': f'Incorrect. The y-intercept is y = {correct}'}
    
    def get_hint(self, func_data, hint_number):
        """Provide hints based on hint number"""
        hints = [
            "💡 To find vertical asymptotes, look for values of x that make the denominator zero (but not the numerator).",
            "💡 For horizontal asymptotes, compare the degrees of the numerator and denominator polynomials.",
            "💡 Holes occur when both numerator and denominator have the same factor that cancels out.",
        ]
        
        if hint_number < len(hints):
            return hints[hint_number]
        else:
            return "💡 Remember to factor both numerator and denominator completely!"
