class Solution {
public:
    vector<int> nodesBetweenCriticalPoints(ListNode* head) {
        if (!head || !head->next || !head->next->next) {
            return {-1, -1};
        }

        int firstCriticalIndex = -1;
        int prevCriticalIndex = -1;
        int minDistance = INT_MAX;
        
        ListNode* prev = head;
        ListNode* curr = head->next;
        int currentIndex = 1; // 0-based index for head, 1 for head->next

        while (curr->next != nullptr) {
            // Check for local maxima or local minima
            bool isLocalMaxima = (curr->val > prev->val && curr->val > curr->next->val);
            bool isLocalMinima = (curr->val < prev->val && curr->val < curr->next->val);

            if (isLocalMaxima || isLocalMinima) {
                if (firstCriticalIndex == -1) {
                    firstCriticalIndex = currentIndex;
                } else {
                    minDistance = min(minDistance, currentIndex - prevCriticalIndex);
                }
                prevCriticalIndex = currentIndex;
            }

            prev = curr;
            curr = curr->next;
            currentIndex++;
        }

        // If fewer than two critical points are found
        if (minDistance == INT_MAX) {
            return {-1, -1};
        }

        int maxDistance = prevCriticalIndex - firstCriticalIndex;
        return {minDistance, maxDistance};
    }
};