class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        
        # Take the first string as a reference
        for i, char in enumerate(strs[0]):
            # Check if this character matches across all other strings
            for string in strs[1:]:
                if i >= len(string) or string[i] != char:
                    return strs[0][:i]
                    
        return strs[0]