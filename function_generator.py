import sympy as sp
from sympy import symbols, factor, expand, apart, limit, oo, solve, cancel, Poly
import random
from fractions import Fraction

class FunctionGenerator:
    def __init__(self):
        self.x = symbols('x')
        
    def generate_function(self, difficulty=1):
        """Generate a rational function based on difficulty level"""
        if difficulty == 1:
            return self._generate_simple_function()
        elif difficulty == 2:
            return self._generate_medium_function()
        else:
            return self._generate_complex_function()
    
    def _generate_simple_function(self):
        """Generate simple rational functions for beginners"""
        patterns = [
            self._simple_vertical_asymptote,
            self._simple_horizontal_asymptote,
            self._simple_with_hole
        ]
        
        pattern = random.choice(patterns)
        return pattern()
    
    def _generate_medium_function(self):
        """Generate medium difficulty functions"""
        patterns = [
            self._medium_multiple_asymptotes,
            self._medium_with_intercepts,
            self._medium_oblique_asymptote
        ]
        
        pattern = random.choice(patterns)
        return pattern()
    
    def _generate_complex_function(self):
        """Generate complex functions for advanced students"""
        patterns = [
            self._complex_multiple_features,
            self._complex_high_degree,
            self._complex_with_parameters
        ]
        
        pattern = random.choice(patterns)
        return pattern()
    
    def _simple_vertical_asymptote(self):
        """Create function with simple vertical asymptote"""
        # f(x) = 1/(x-a) or f(x) = k/(x-a)
        a = random.randint(-5, 5)
        k = random.choice([1, 2, 3, -1, -2])
        
        if a == 0:
            a = 1
        
        numerator = k
        denominator = self.x - a
        
        return self._create_function_data(numerator, denominator)
    
    def _simple_horizontal_asymptote(self):
        """Create function with horizontal asymptote"""
        # f(x) = (ax + b)/(cx + d) where deg(num) = deg(den)
        a, b = random.randint(1, 3), random.randint(-5, 5)
        c, d = random.randint(1, 3), random.randint(-5, 5)
        
        # Ensure denominator doesn't factor with numerator
        if b * c == a * d:
            d += 1
        
        numerator = a * self.x + b
        denominator = c * self.x + d
        
        return self._create_function_data(numerator, denominator)
    
    def _simple_with_hole(self):
        """Create function with a hole"""
        # f(x) = (x-a)(x-b)/(x-a)(x-c) -> hole at x=a, VA at x=c
        a = random.randint(-3, 3)
        b = random.randint(-4, 4)
        c = random.randint(-4, 4)
        
        # Ensure all values are different
        while b == a or c == a or c == b:
            b = random.randint(-4, 4)
            c = random.randint(-4, 4)
        
        numerator = (self.x - a) * (self.x - b)
        denominator = (self.x - a) * (self.x - c)
        
        return self._create_function_data(numerator, denominator)
    
    def _medium_multiple_asymptotes(self):
        """Create function with multiple vertical asymptotes"""
        # f(x) = (ax + b)/((x-c)(x-d))
        a, b = random.randint(1, 3), random.randint(-3, 3)
        c = random.randint(-3, 3)
        d = random.randint(-3, 3)
        
        while d == c:
            d = random.randint(-3, 3)
        
        numerator = a * self.x + b
        denominator = (self.x - c) * (self.x - d)
        
        return self._create_function_data(numerator, denominator)
    
    def _medium_with_intercepts(self):
        """Create function with clear intercepts"""
        # f(x) = (x-a)(x-b)/(x-c)(x-d)
        a, b = random.randint(-2, 2), random.randint(-2, 2)
        c, d = random.randint(-3, 3), random.randint(-3, 3)
        
        # Ensure no common factors
        while c in [a, b] or d in [a, b] or c == d:
            c = random.randint(-3, 3)
            d = random.randint(-3, 3)
        
        numerator = (self.x - a) * (self.x - b)
        denominator = (self.x - c) * (self.x - d)
        
        return self._create_function_data(numerator, denominator)
    
    def _medium_oblique_asymptote(self):
        """Create function with oblique asymptote"""
        # f(x) = (ax^2 + bx + c)/(dx + e)
        a = random.randint(1, 2)
        b, c = random.randint(-3, 3), random.randint(-3, 3)
        d = random.randint(1, 2)
        e = random.randint(-3, 3)
        
        numerator = a * self.x**2 + b * self.x + c
        denominator = d * self.x + e
        
        return self._create_function_data(numerator, denominator)
    
    def _complex_multiple_features(self):
        """Create function with multiple features"""
        # f(x) = (x-a)(x-b)(x-c)/((x-d)(x-e)(x-a))
        a = random.randint(-2, 2)
        b, c = random.randint(-3, 3), random.randint(-3, 3)
        d, e = random.randint(-3, 3), random.randint(-3, 3)
        
        while d in [b, c] or e in [b, c, d]:
            d = random.randint(-3, 3)
            e = random.randint(-3, 3)
        
        numerator = (self.x - a) * (self.x - b) * (self.x - c)
        denominator = (self.x - d) * (self.x - e) * (self.x - a)
        
        return self._create_function_data(numerator, denominator)
    
    def _complex_high_degree(self):
        """Create higher degree rational function"""
        # Create polynomials of degree 2-3
        num_coeffs = [random.randint(1, 2)] + [random.randint(-2, 2) for _ in range(2)]
        den_coeffs = [random.randint(1, 2)] + [random.randint(-2, 2) for _ in range(random.randint(1, 2))]
        
        numerator = sum(coeff * self.x**i for i, coeff in enumerate(reversed(num_coeffs)))
        denominator = sum(coeff * self.x**i for i, coeff in enumerate(reversed(den_coeffs)))
        
        return self._create_function_data(numerator, denominator)
    
    def _complex_with_parameters(self):
        """Create function with parameters that create interesting behavior"""
        # Choose a complex pattern
        patterns = [
            lambda: self._create_function_data(
                (self.x**2 - 1), 
                (self.x**2 - 4)
            ),
            lambda: self._create_function_data(
                (self.x**2 + self.x - 2), 
                (self.x**3 - self.x)
            ),
            lambda: self._create_function_data(
                (2*self.x**2 - 3*self.x + 1), 
                (self.x**2 - 5*self.x + 6)
            )
        ]
        
        return random.choice(patterns)()
    
    def _create_function_data(self, numerator, denominator):
        """Create comprehensive function data including all features"""
        # Simplify the function
        simplified = cancel(numerator / denominator)
        
        # Get original expressions for analysis
        original_expr = numerator / denominator
        
        # Calculate all features
        features = self._analyze_function(numerator, denominator, simplified)
        
        # Create LaTeX representation
        latex = self._to_latex(numerator, denominator)
        
        return {
            'expression': simplified,
            'original_numerator': numerator,
            'original_denominator': denominator,
            'latex': latex,
            'features': features
        }
    
    def _analyze_function(self, numerator, denominator, simplified):
        """Analyze function to find all key features"""
        features = {
            'vertical_asymptotes': [],
            'horizontal_asymptote': None,
            'oblique_asymptote': None,
            'holes': [],
            'x_intercepts': [],
            'y_intercept': None
        }
        
        try:
            # Find vertical asymptotes and holes
            va_holes = self._find_vertical_asymptotes_and_holes(numerator, denominator)
            features['vertical_asymptotes'] = va_holes['vertical_asymptotes']
            features['holes'] = va_holes['holes']
            
            # Find horizontal/oblique asymptotes
            features['horizontal_asymptote'] = self._find_horizontal_asymptote(numerator, denominator)
            
            # Find intercepts
            features['x_intercepts'] = self._find_x_intercepts(simplified)
            features['y_intercept'] = self._find_y_intercept(simplified)
            
        except Exception as e:
            # Fallback to safe defaults
            print(f"Error analyzing function: {e}")
            
        return features
    
    def _find_vertical_asymptotes_and_holes(self, numerator, denominator):
        """Find vertical asymptotes and holes"""
        result = {'vertical_asymptotes': [], 'holes': []}
        
        try:
            # Factor both numerator and denominator
            num_factors = factor(numerator)
            den_factors = factor(denominator)
            
            # Find zeros of denominator
            den_zeros = solve(denominator, self.x)
            
            for zero in den_zeros:
                try:
                    zero_val = float(zero)
                    
                    # Check if this zero is also a zero of numerator (hole)
                    num_at_zero = numerator.subs(self.x, zero)
                    
                    if num_at_zero == 0:
                        # It's a hole - find the y-coordinate
                        simplified = cancel(numerator / denominator)
                        y_val = float(simplified.subs(self.x, zero))
                        result['holes'].append((zero_val, y_val))
                    else:
                        # It's a vertical asymptote
                        result['vertical_asymptotes'].append(zero_val)
                        
                except:
                    continue
                    
        except Exception as e:
            print(f"Error finding VA/holes: {e}")
            
        return result
    
    def _find_horizontal_asymptote(self, numerator, denominator):
        """Find horizontal asymptote"""
        try:
            # Get degrees
            num_poly = Poly(numerator, self.x)
            den_poly = Poly(denominator, self.x)
            
            num_degree = num_poly.degree()
            den_degree = den_poly.degree()
            
            if num_degree < den_degree:
                return 0.0
            elif num_degree == den_degree:
                # Ratio of leading coefficients
                num_lead = float(num_poly.LC())
                den_lead = float(den_poly.LC())
                return num_lead / den_lead
            else:
                # No horizontal asymptote (might have oblique)
                return None
                
        except:
            return None
    
    def _find_x_intercepts(self, expression):
        """Find x-intercepts"""
        try:
            # Solve numerator = 0
            x_intercepts = []
            
            # Get numerator of the simplified expression
            num, _ = expression.as_numer_denom()
            zeros = solve(num, self.x)
            
            for zero in zeros:
                try:
                    x_intercepts.append(float(zero))
                except:
                    continue
                    
            return x_intercepts
            
        except:
            return []
    
    def _find_y_intercept(self, expression):
        """Find y-intercept"""
        try:
            y_val = expression.subs(self.x, 0)
            return float(y_val)
        except:
            return None
    
    def _to_latex(self, numerator, denominator):
        """Convert function to LaTeX format"""
        try:
            num_latex = sp.latex(numerator)
            den_latex = sp.latex(denominator)
            return f"f(x) = \\frac{{{num_latex}}}{{{den_latex}}}"
        except:
            return "f(x) = \\text{Error generating LaTeX}"
