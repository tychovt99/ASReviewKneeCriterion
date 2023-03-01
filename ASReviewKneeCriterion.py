import pandas as pd

df = pd.read_csv('ASReviewLABprogressDensity2560.csv')
df.head()


def calculate_knee_values(k, rho, df):
    # Variables to store stopping values
    stop_i = -1
    stop_s = -1
    stop_relevant = -1
    slope_stop = -1

    for rank_s, relevant in zip(df["category"], df['Relevant records']):

        # If knee found, break
        if stop_s > 0:
            break

        # If number relevant less than k, do not even need to consider stopping
        if relevant < k:
            continue

        # Index (start=0) is one lower than rank (start=1)
        index_s = rank_s - 1

        # Loop over all i and compare slopes
        for rank_i in range(1, rank_s):

            # Calculate slope until i
            index_i = rank_i - 1
            num_relevant_i = df['Relevant records'][index_i]

            slope_i = num_relevant_i / rank_i

            # If slope until i is zero, cannot exceed cutoff
            if slope_i == 0:
                continue

            num_relevant_s = df['Relevant records'][index_s]

            # Calculate slope of s
            # Add 1 to numerator to avoid edge cases with i very close to s
            slope_s = (1 + num_relevant_s - num_relevant_i) / (rank_s - rank_i)

            # Calculate slope ratio
            slope_ratio = slope_i / slope_s

            # Check if slope_ratio greater than cutoff
            if slope_ratio > rho:
                stop_i = rank_i
                stop_s = rank_s
                stop_relevant = num_relevant_s
                slope_stop = slope_ratio
                break
    return stop_i, stop_s, stop_relevant, slope_stop

k = 10 # minimum target set size, maybe 1070 (10%) or k = 900
rho = 100 #based on Cormack & Grossman article, slope ratio cutoff

i, s, num_relevant, slope_ratio = calculate_knee_values(k, rho, df)

print('We stop at s=' + str(s) + ' since the slope from 0 to i='
      + str(i) + ' is ' + str(round(slope_ratio, 2)) + ' times higher '
     + 'than the intermediate slope between i and s.')


#We don't have random relevant, still in review process - Tycho
#R = df['Random relevant'].iat[-1] # number of relevant documents, generally unknown

#print('At the stopping point we have found ' + str(num_relevant)
#     + ' relevant papers. This corresponds to a recall of '
#     + str(round(num_relevant/R, 2)*100) + '%.')