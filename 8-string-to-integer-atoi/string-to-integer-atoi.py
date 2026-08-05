class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.strip()  # 1. Skip leading whitespaces
        if not s:
            return 0
        
        sign = 1
        index = 0
        
        # 2. Check for sign
        if s[0] == '-':
            sign = -1
            index += 1
        elif s[0] == '+':
            index += 1
            
        res = 0
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31
        
        # 3. Read valid digits
        while index < len(s) and s[index].isdigit():
            res = res * 10 + int(s[index])
            index += 1
            
        res *= sign
        
        # 4. Clamp within 32-bit signed integer bounds
        if res < INT_MIN:
            return INT_MIN
        if res > INT_MAX:
            return INT_MAX
            
        return res