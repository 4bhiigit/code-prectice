class Solution:
    def stoneGameV(self, stoneValue: list[int]) -> int:
        n = len(stoneValue)
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + stoneValue[i]

        dp = [[0] * n for _ in range(n)]
        max_left = [[0] * n for _ in range(n)]
        max_right = [[0] * n for _ in range(n)]

        for i in range(n):
            max_left[i][i] = stoneValue[i]
            max_right[i][i] = stoneValue[i]

        for length in range(2, n + 1):
            k = 0
            for i in range(n - length + 1):
                j = i + length - 1
                total = pref[j + 1] - pref[i]

                while pref[k + 1] - pref[i] < pref[j + 1] - pref[k + 1]:
                    k += 1

                left_sum = pref[k + 1] - pref[i]
                right_sum = total - left_sum

                res = 0

                if left_sum == right_sum:
                    res = max(max_left[i][k], max_right[k + 1][j])
                else:
                    if k > i:
                        res = max(res, max_left[i][k - 1])
                    if k < j:
                        res = max(res, max_right[k + 1][j])

                dp[i][j] = res
                max_left[i][j] = max(max_left[i][j - 1], res + total)
                max_right[i][j] = max(max_right[i + 1][j], res + total)

        return dp[0][n - 1]