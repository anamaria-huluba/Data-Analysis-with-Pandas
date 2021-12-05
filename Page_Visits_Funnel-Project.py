# Page Visits Funnel

# Cool T-Shirts Inc. has asked you to analyze data on visits to their website. Your job is to build a funnel, which is a description of how many people continue to the next step of a multi-step process.

# In this case, our funnel is going to describe the following process:

#1. A user visits CoolTShirts.com
#2. A user adds a t-shirt to their cart
#3. A user clicks “checkout”
#4. A user actually purchases a t-shirt

# Funnel for Cool T-Shirts Inc.

# 1. Inspect the DataFrames using print and head:

#- visits lists all of the users who have visited the website
#- cart lists all of the users who have added a t-shirt to their cart
#- checkout lists all of the users who have started the checkout
#- purchase lists all of the users who have purchased a t-shirt

import pandas as pd

visits = pd.read_csv('visits.csv',
                     parse_dates=[1])

print(visits.head())
# returns:

#	user_id	                                visit_time
# 0	943647ef-3682-4750-a2e1-918ba6f16188	2017-04-07 15:14:00
# 1	0c3a3dd0-fb64-4eac-bf84-ba069ce409f2	2017-01-26 14:24:00
# 2	6e0b2d60-4027-4d9a-babd-0e7d40859fb1	2017-08-20 08:23:00
# 3	6879527e-c5a6-4d14-b2da-50b85212b0ab	2017-11-04 18:15:00
# 4	a84327ff-5daa-4ba1-b789-d5b4caf81e96	2017-02-27 11:25:00   
                 
cart = pd.read_csv('cart.csv',
                   parse_dates=[1])

print(cart.head())
# returns: 

#    user_id	                            cart_time
# 0	2be90e7c-9cca-44e0-bcc5-124b945ff168	2017-11-07 20:45:00
# 1	4397f73f-1da3-4ab3-91af-762792e25973	2017-05-27 01:35:00
# 2	a9db3d4b-0a0a-4398-a55a-ebb2c7adf663	2017-03-04 10:38:00
# 3	b594862a-36c5-47d5-b818-6e9512b939b3	2017-09-27 08:22:00
# 4	a68a16e2-94f0-4ce8-8ce3-784af0bbb974	2017-07-26 15:48:00 

checkout = pd.read_csv('checkout.csv',
                       parse_dates=[1])

print(checkout.head())
# returns:

#    user_id	                            checkout_time
# 0	d33bdc47-4afa-45bc-b4e4-dbe948e34c0d	2017-06-25 09:29:00
# 1	4ac186f0-9954-4fea-8a27-c081e428e34e	2017-04-07 20:11:00
# 2	3c9c78a7-124a-4b77-8d2e-e1926e011e7d	2017-07-13 11:38:00
# 3	89fe330a-8966-4756-8f7c-3bdbcd47279a	2017-04-20 16:15:00
# 4	3ccdaf69-2d30-40de-b083-51372881aedd	2017-01-08 20:52:00

purchase = pd.read_csv('purchase.csv',
                       parse_dates=[1])

print(purchase.head())
# returns:

# 	user_id	                                purchase_time
# 0	4b44ace4-2721-47a0-b24b-15fbfa2abf85	2017-05-11 04:25:00
# 1	02e684ae-a448-408f-a9ff-dcb4a5c99aac	2017-09-05 08:45:00
# 2	4b4bc391-749e-4b90-ab8f-4f6e3c84d6dc	2017-11-20 20:49:00
# 3	a5dbb25f-3c36-4103-9030-9f7c6241cd8d	2017-01-22 15:18:00
# 4	46a3186d-7f5a-4ab9-87af-84d05bfd4867	2017-06-11 11:32:00

#2. Combine visits and cart using a left merge.

visits_cart = pd.merge(visits, cart, how='left')

#3. How long is your merged DataFrame?

visits_cart_rows = len(visits_cart)
print(visits_cart_rows)
# returns: 2000

# 4. How many of the timestamps are null for the column cart_time?

null_cart_time = len(visits_cart[visits_cart.cart_time.isnull()])
print(null_cart_time)
# returns: 1652

# What do these null rows mean?

# The null rows means that 1652 out of the 2000 users did not add anything into their carts.

# 5. What percent of users who visited Cool T-Shirts Inc. ended up not placing a t-shirt in their cart?

# Note: To calculate percentages, it will be helpful to turn either the numerator or the denominator into a float, by using float(), with the number to convert passed in as input. Otherwise, Python will use integer division, which truncates decimal points.

print(float(null_cart_time) / visits_cart_rows)
# returns:0.826

# This means the 82.6% of all users who visited Cool T-Shirts Inc. ended up not placing a t-shirt in their cart.

#6. Repeat the left merge for cart and checkout and count null values. 

cart_checkout = pd.merge(cart, checkout, how='left')
cart_checkout_rows = len(cart_checkout)
print(cart_checkout_rows)
# returns: 482
null_checkout_time = len(cart_checkout[cart_checkout.checkout_time.isnull()])
print(null_checkout_time)
# returns: 122

#What percentage of users put items in their cart, but did not proceed to checkout?

print(float(null_checkout_time) / cart_checkout_rows)
# returns: 0.253112033195

# This means that 25.31% percent of users put items in their cart, but did not proceed to checkout.

#7. Merge all four steps of the funnel, in order, using a series of left merges. Save the results to the variable all_data.

# Examine the result using print and head.

all_data = visits.merge(cart, how='left')\
                .merge(checkout, how='left')\
                .merge(purchase, how='left')

print(all_data.head())

#8. What percentage of users proceeded to checkout, but did not purchase a t-shirt?

checkout_purchase = pd.merge(checkout, purchase, how='left')
checkout_purchse_rows = len(checkout_purchase)
null_purchase_time = len(checkout_purchase[checkout_purchase.purchase_time.isnull()])
#print(null_purchase_time)
print(float(null_purchase_time) / checkout_purchse_rows)
# returns: 0.16889632107

# This means that 16.89% percent of customers end up to checkout but don't end up making a purchase.

# 9. Which step of the funnel is weakest (i.e., has the highest percentage of users not completing it)?

# Looking at all out findings, 80% of all users don't add anything to their cart, 25% of all users 
# ad items to cart but don't end up to checkout and finally 16% of all users end up at checkput but don't purchase anything. 

#The highest percentage of users is at 80%, which is the first step in the process and  they don't add anything to cart. 

# Average Time to Purchase

# 10. Using the giant merged DataFrame all_data that you created, let’s calculate the average time from initial visit to final purchase. Start by adding the following column to your DataFrame:

all_data['time_to_purchase'] = \
    all_data.purchase_time - \
    all_data.visit_time

# 11. Examine the results.

print(all_data.time_to_purchase)

# 12. Calculate the average time to purchase.

print(all_data.time_to_purchase.mean())
# returns: 0 days 00:43:53.360160

# In this project I used pandas to build a funnel which will provide insight into which parts of the website needed to be improved. 
# I used merges to investigate the specific combinations of data and to store information along the way.Merging is an impi=ortant part of
# the data analysis because it allows us to store data in smaller, more managable data frames without losing any of the functionalities 
# of scaling a large dataframe. 


