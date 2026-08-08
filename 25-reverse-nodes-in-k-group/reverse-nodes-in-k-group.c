/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode* reverseKGroup(struct ListNode* head, int k) {
    if (!head || k == 1) return head;

    struct ListNode dummy;
    dummy.next = head;
    struct ListNode* prevGroup = &dummy;

    while (1) {
        // Check if there are at least k nodes remaining
        struct ListNode* kth = prevGroup;
        for (int i = 0; i < k && kth != NULL; i++) {
            kth = kth->next;
        }
        if (!kth) break;

        struct ListNode* groupNext = kth->next;
        struct ListNode* prev = groupNext;
        struct ListNode* curr = prevGroup->next;

        // Reverse k nodes in-place
        while (curr != groupNext) {
            struct ListNode* nextNode = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nextNode;
        }

        // Connect previous group to the new head of this reversed group
        struct ListNode* newGroupTail = prevGroup->next;
        prevGroup->next = kth;
        prevGroup = newGroupTail;
    }

    return dummy.next;
}