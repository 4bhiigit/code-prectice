class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        # Ensure nums1 is the smaller array to minimize binary search range
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
            
        m, n = len(nums1), len(nums2)
        low, high = 0, m
        total_left = (m + n + 1) // 2
        
        while low <= high:
            i = (low + high) // 2       # Partition index in nums1
            j = total_left - i          # Partition index in nums2
            
            # Boundary values around partition in nums1
            max_left_1 = float('-inf') if i == 0 else nums1[i - 1]
            min_right_1 = float('inf') if i == m else nums1[i]
            
            # Boundary values around partition in nums2
            max_left_2 = float('-inf') if j == 0 else nums2[j - 1]
            min_right_2 = float('inf') if j == n else nums2[j]
            
            # Check if partition is valid
            if max_left_1 <= min_right_2 and max_left_2 <= min_right_1:
                # If total elements are odd
                if (m + n) % 2 == 1:
                    return float(max(max_left_1, max_left_2))
                # If total elements are even
                else:
                    return (max(max_left_1, max_left_2) + min(min_right_1, min_right_2)) / 2.0
            
            # Adjust binary search range
            elif max_left_1 > min_right_2:
                high = i - 1  # Move left in nums1
            else:
                low = i + 1   # Move right in nums1

        return 0.0