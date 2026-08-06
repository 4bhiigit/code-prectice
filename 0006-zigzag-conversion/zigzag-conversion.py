class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # Edge case: if only 1 row or string length is less than numRows
        if numRows == 1 or numRows >= len(s):
            return s

        # Initialize rows
        rows = [''] * numRows
        current_row = 0
        going_down = False

        # Traverse characters in s
        for char in s:
            rows[current_row] += char
            
            # Reverse direction at top or bottom boundary
            if current_row == 0 or current_row == numRows - 1:
                going_down = not going_down
            
            # Move up or down
            current_row += 1 if going_down else -1

        # Combine all rows into a single string
        return "".join(rows)