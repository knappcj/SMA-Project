def findMax(results_dict):
    max_tickers = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for i in results_dict:
        for j in range(1, 10):
            if max_tickers[j] == 0:
                max_tickers[j] = [i]
            elif len(max_tickers[j]) == 1:
                max_tickers[j] = [max_tickers[j][0], i]
            else:
                if results_dict[i][j] > results_dict[max_tickers[j][0]][j] or results_dict[i][j] > \
                        results_dict[max_tickers[j][1]][j]:
                    new_list = []
                    if results_dict[max_tickers[j][0]][j] > results_dict[max_tickers[j][1]][j]:
                        new_list.append(max_tickers[j][0])
                    else:
                        new_list.append(max_tickers[j][1])
                    new_list.append(i)
                    max_tickers[j] = new_list
    high_sum = 0
    high_day = 0
    for i in max_tickers:
        sum = results_dict[max_tickers[i][0]][i] + results_dict[max_tickers[i][1]][i]
        if sum > high_sum:
            high_sum = sum
            high_day = i
    return max_tickers[high_day], high_day+1
