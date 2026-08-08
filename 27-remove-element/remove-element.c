int removeElement(int* nums, int numsSize, int val) {
    int k = 0; // Pointer to place elements not equal to val

    for (int i = 0; i < numsSize; i++) {
        // If current element is not equal to val, copy it to index k
        if (nums[i] != val) {
            nums[k] = nums[i];
            k++;
        }
    }

    return k;
}