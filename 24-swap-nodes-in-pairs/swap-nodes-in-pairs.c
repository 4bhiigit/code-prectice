/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode* swapPairs(struct ListNode* head) {
    // Base case: if list has 0 or 1 node, no swap needed
    if (!head || !head->next) {
        return head;
    }

    struct ListNode dummy;
    dummy.next = head;
    struct ListNode* prev = &dummy;

    while (prev->next && prev->next->next) {
        struct ListNode* first = prev->next;
        struct ListNode* second = prev->next->next;

        // Perform pointer reassignment
        first->next = second->next;
        second->next = first;
        prev->next = second;

        // Move prev two nodes ahead for the next pair
        prev = first;
    }

    return dummy.next;
}
