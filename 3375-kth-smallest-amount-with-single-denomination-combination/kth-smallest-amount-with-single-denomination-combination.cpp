
#include <vector>
#include <numeric>
#include <algorithm>

class Solution {
public:
    long long findKthSmallest(std::vector<int>& coins, int k) {
        int n = coins.size();
        int num_subsets = 1 << n;
        
        // Precompute LCM and subset size parity
        std::vector<std::pair<long long, int>> subsets;
        subsets.reserve(num_subsets - 1);
        
        for (int mask = 1; mask < num_subsets; ++mask) {
            long long current_lcm = 1;
            int bit_count = 0;
            for (int i = 0; i < n; ++i) {
                if ((mask >> i) & 1) {
                    current_lcm = std::lcm(current_lcm, (long long)coins[i]);
                    bit_count++;
                }
            }
            int sign = (bit_count % 2 == 1) ? 1 : -1;
            subsets.push_back({current_lcm, sign});
        }
        
        // Function to count multiples <= mid
        auto countMultiples = [&](long long mid) -> long long {
            long long total = 0;
            for (const auto& [lcm_val, sign] : subsets) {
                total += sign * (mid / lcm_val);
            }
            return total;
        };
        
        long long low = 1;
        long long min_coin = *std::min_element(coins.begin(), coins.end());
        long long high = min_coin * k;
        long long ans = high;
        
        while (low <= high) {
            long long mid = low + (high - low) / 2;
            if (countMultiples(mid) >= k) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        
        return ans;
    }
};