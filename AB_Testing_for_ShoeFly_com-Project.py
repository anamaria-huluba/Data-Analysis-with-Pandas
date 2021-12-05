# A/B Testing for ShoeFly.com

# Our favorite online shoe store, ShoeFly.com is performing an A/B Test. They have two different versions of an ad, which they have placed in emails, as well as in banner ads 
# on Facebook, Twitter, and Google. They want to know how the two ads are performing on each of the different platforms on each day of the week. Help them analyze the data 
# using aggregate measures.

# Analyzing Ad Sources

# 1. Examine the first few rows of ad_clicks.

import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')
print(ad_clicks.head())

# user_id	                              utm_source	 day	        ad_click_timestamp	experimental_group
# 0	008b7c6c-7272-471e-b90e-930d548bd8d7	google	  6 - Saturday  	7:18	             A
# 1	009abb94-5e14-4b6c-bb1c-4f4df7aa7557	facebook  7 - Sunday	    nan	                 B
# 2	00f5d532-ed58-4570-b6d2-768df5f41aed	twitter	  2 - Tuesday	    nan	                 A
# 3	011adc64-0f44-4fd9-a0bb-f1506d2ad439	google	  2 - Tuesday	    nan	                 B
# 4	012137e6-7ae7-4649-af68-205b4702169c	facebook  7 - Sunday	    nan	                 B

# 2. Your manager wants to know which ad platform is getting you the most views.

# How many views (i.e., rows of the table) came from each utm_source?

count_utm_sourse = ad_clicks.groupby('utm_source')['user_id'].count().reset_index() 
print(count_utm_sourse)
# returns: 

# #	utm_source	user_id
# 0	   email	255
# 1	 facebook	504
# 2	  google	680
# 3	 twitter	215

# 3. If the column ad_click_timestamp is not null, then someone actually clicked on the ad that was displayed.

# Create a new column called is_click, which is True if ad_click_timestamp is not null and False otherwise.

ad_clicks['is_click'] = ad_clicks.ad_click_timestamp.isnull()
print(ad_clicks.head())
# returns:

#    user_id	                           utm_source   day	              ad_click_timestamp	experimental_group	  is_click
# 0	008b7c6c-7272-471e-b90e-930d548bd8d7	google	    6 - Saturday	    7:18	                    A              False
# 1	009abb94-5e14-4b6c-bb1c-4f4df7aa7557	facebook	7 - Sunday	         nan	                    B           	True
# 2	00f5d532-ed58-4570-b6d2-768df5f41aed	twitter	    2 - Tuesday	         nan	                    A           	True
# 3	011adc64-0f44-4fd9-a0bb-f1506d2ad439	google	    2 - Tuesday	         nan	                    B           	True
# 4	012137e6-7ae7-4649-af68-205b4702169c	facebook	7 - Sunday	         nan	                    B           	True

# 4. We want to know the percent of people who clicked on ads from each utm_source.

# Start by grouping by utm_source and is_click and counting the number of user_id‘s in each of those groups. Save your answer to the variable clicks_by_source.

clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
print(clicks_by_source)
# returns:

#   utm_source	is_click	user_id
# 0	email	     False	     80
# 1	email	     True	     175
# 2	facebook	 False	     180
# 3	facebook	 True	     324
# 4	google	     False	     239
# 5	google	     True	     441
# 6	twitter	     False	     66
# 7	twitter	     True	     149

#5. Now let’s pivot the data so that the columns are is_click (either True or False), the index is utm_source, and the values are user_id.

#Save your results to the variable clicks_pivot.

clicks_pivot = clicks_by_source.pivot(columns='is_click', index= 'utm_source', values= 'user_id').reset_index()
print(clicks_pivot)
# returns: 

#   utm_source	False	True
# 0	email	    80   	175
# 1	facebook	180	    324
# 2	google	    239  	441
# 3	twitter	     66	    149

# 6. Create a new column in clicks_pivot called percent_clicked which is equal to the percent of users who clicked on the ad from each utm_source.

# Was there a difference in click rates for each source?

clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])
print(clicks_pivot)
# returns:

# #  utm_source	False	True	percent_clicked
# 0	 email     	175	     80	    0.313725490196
# 1	 facebook	324	    180	    0.357142857143
# 2	 google	    441	    239	    0.351470588235
# 3	 twitter	149	     66	    0.306976744186

# Analyzing an A/B Test

#7. The column experimental_group tells us whether the user was shown Ad A or Ad B.

# Were approximately the same number of people shown both adds?

print(ad_clicks.groupby('experimental_group').user_id.count().reset_index())
# returns:

# 	experimental_group	user_id
# 0	               A	   827
# 1	               B	   827

#8. Using the column is_click that we defined earlier, check to see if a greater percentage of users clicked on Ad A or Ad B.

print(ad_clicks\
    .groupby(['experimental_group', 'is_click']).user_id\
        .count()\
        .reset_index()\
        .pivot(
            index= 'experimental_group', 
            columns= 'is_click', 
            values= 'user_id'
            )\
            .reset_index()
            )

# 	experimental_group	False	True
# 0	               A	517	    310
# 1	               B	572	    255

# 9. The Product Manager for the A/B test thinks that the clicks might have changed by day of the week.

# Start by creating two DataFrames: a_clicks and b_clicks, which contain only the results for A group and B group, respectively.

a_clicks = ad_clicks[ad_clicks.expererinetal_group == 'A']
b_clicks = ad_clicks[ad_clicks.expererinetal_group == 'B']

#10. For each group (a_clicks and b_clicks), calculate the percent of users who clicked on the ad by day.

a_clicks_pivot = a_clicks\
.groupby(['is_click', 'day']).user_id\
.count()\
.reset_index()\
.pivot(
  index = 'day',
  columns= 'is_click',
  values='user_id'
)\
.reset_index()

a_clicks_pivot['percent_cliked'] = a_clicks_pivot[True] / (a_clicks_pivot[True] + a_clicks_pivot[False])
print(a_clicks_pivot)
# returns:

#         day	     False	True	percent_cliked
# 0	1 - Monday      	70	43	    0.380530973451
# 1	2 - Tuesday	        76	43	    0.361344537815
# 2	3 - Wednesday	    86	38   	0.306451612903
# 3	4 - Thursday	    69	47	    0.405172413793
# 4	5 - Friday	        77	51	    0.3984375
# 5	6 - Saturday	    73	45	    0.381355932203
# 6	7 - Sunday	       66	43	    0.394495412844

b_clicks_pivot = b_clicks\
.groupby(['is_click', 'day']).user_id\
.count()\
.reset_index()\
.pivot(
  index = 'day',
  columns= 'is_click',
  values='user_id'
)\
.reset_index()

b_clicks_pivot['percent_cliked'] = b_clicks_pivot[True] / (b_clicks_pivot[True] + b_clicks_pivot[False])
print(b_clicks_pivot)
# returns:

#          day   	False	True	percent_cliked
# 0	1 - Monday     	81	    32  	0.283185840708
# 1	2 - Tuesday	    74	    45	    0.378151260504
# 2	3 - Wednesday	89	    35	    0.282258064516
# 3	4 - Thursday	87	    29	    0.25
# 4	5 - Friday	    90	    38	    0.296875
# 5	6 - Saturday	76	    42	    0.35593220339
# 6	7 - Sunday   	75	    34   	0.311926605505

# 11. Compare the results for A and B. What happened over the course of the week?

# Do you recommend that your company use Ad A or Ad B?

#11. The last two columns of the two adds, Ad A and Ad B, represents the percent clicked rate for every day of the week. This comparison makes it easier to notice the results 
# for the two ads. I notice the ads picked at diffrent times during the week. Ad A has a better rate than B on every day of the week except for Tuesday. Based on this data and
# all the other tables I looked at over the course of this project, I would recommend that your company uses Ad A. 
