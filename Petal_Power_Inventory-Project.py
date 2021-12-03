# Petal Power Inventory

# You’re the lead data analyst for a chain of gardening stores called Petal Power. Help them analyze their inventory!

# If you get stuck during this project or would like to see an experienced developer work through it, click “Get Unstuck“ to see a project walkthrough video.

# 1. Data for all of the locations of Petal Power is in the file inventory.csv. Load the data into a DataFrame called inventory.

import pandas as pd

inventory = pd.read_csv('inventory.csv')

# 2. Inspect the first 10 rows of inventory.

print(inventory.head(10))

#3. The first 10 rows represent data from your Staten Island location. Select these rows and save them to staten_island.

staten_island = inventory.head(10)

#4. A customer just emailed you asking what products are sold at your Staten Island location. Select the column product_description from staten_island and save it to the 
#variable product_request.

product_request = staten_island.product_description

#5. Another customer emails to ask what types of seeds are sold at the Brooklyn location.

#Select all rows where location is equal to Brooklyn and product_type is equal to seeds and save them to the variable seed_request.

seed_request = inventory[(inventory.location == 'Brooklyn') & (inventory.product_type =='seeds')]

#6. Add a column to inventory called in_stock which is True if quantity is greater than 0 and False if quantity equals 0.

inventory['in_stock'] = inventory.apply(lambda row: True if row['quantity'] > 0 else False, axis=1)
print(inventory.head(10))
# returns: 
# 0      True  
# 1      True  
# 2      True  
# 3      True  
# 4     False  
# 5      True  
# 6      True  
# 7      True  
# 8     False  
# 9      True  

# 7. Petal Power wants to know how valuable their current inventory is.

# Create a column called total_value that is equal to price multiplied by quantity.

inventory['total_value'] = inventory.apply(lambda row: row.price * row.quantity, axis=1)

# 8. The Marketing department wants a complete description of each product for their catalog.

# The following lambda function combines product_type and product_description into a single string:

combine_lambda = lambda row: \
    '{} - {}'.format(row.product_type,
                     row.product_description)

#9. Using combine_lambda, create a new column in inventory called full_description that has the complete description of each product.

inventory["full_description"] = inventory.apply(combine_lambda, axis=1)
