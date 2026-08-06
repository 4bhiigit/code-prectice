class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};
        
        vector<string> phoneMap = {
            "",     "",     "abc",  "def", 
            "ghi",  "jkl",  "mno", 
            "pqrs", "tuv",  "wxyz"
        };
        
        vector<string> result;
        string current = "";
        
        backtrack(0, digits, current, result, phoneMap);
        return result;
    }

private:
    void backtrack(int index, const string& digits, string& current, 
                   vector<string>& result, const vector<string>& phoneMap) {
        if (index == digits.length()) {
            result.push_back(current);
            return;
        }
        
        string letters = phoneMap[digits[index] - '0'];
        for (char c : letters) {
            current.push_back(c);
            backtrack(index + 1, digits, current, result, phoneMap);
            current.pop_back();
        }
    }
};