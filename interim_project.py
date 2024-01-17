# Importing modules
import pypyodbc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore') # Added to ignore some unnecessary errors

# Inserting data from SQL and connecting with this .py file
conn = pypyodbc.connect('Driver={SQL Server};' # Connected server type
                      'Server=DESKTOP-HGT8A4D\SQLEXPRESS01;' # Location and name of the connected server
                      'Database=AdventureWorks2019;' # Database connected to the selected server
                      'Trusted_Connection=yes;') # This enables the connection without entering a trusted key or password

cursor = conn.cursor()


'''
*******************************************************************
                         Question 1
    What are the regional sales in the best performing country?
*******************************************************************
'''

# The query to be executed in the database is defined
# This query finds the best performing country
query = '''
SELECT CountryRegionCode, COUNT(*) AS NumStores 
FROM AdventureWorks2019.Sales.vStoreWithAddresses AS S 
INNER JOIN AdventureWorks2019.Person.CountryRegion AS C 
    ON C.Name = S.CountryRegionName 
GROUP BY CountryRegionName, CountryRegionCode 
ORDER BY NumStores DESC
'''

# Reads the data from query to pandas dataframe 
stores = pd.read_sql(query, conn)

# Creats the bar plot
bars = plt.bar(stores.countryregioncode, stores.numstores)

# Adds labels and title
plt.xlabel('Country')
plt.ylabel('Number of Stores')
plt.title('Number of Stores Per Country')

# Function to show the plot
plt.show()

# The query to be executed in the database is defined
# This query finds the levels of revenue for each region in the US
query = '''
SELECT TerritoryID, Name, CountryRegionCode, SalesYTD, SalesLastYear 
FROM AdventureWorks2019.Sales.SalesTerritory 
WHERE CountryRegionCode = 'US' 
ORDER BY SalesYTD DESC
'''

# Reads the data from query to pandas dataframe
RegionalSales = pd.read_sql(query, conn, index_col = 'territoryid')

# Creats the bar plot
plt.bar(RegionalSales.name, RegionalSales.salesytd, color = 'blue')

# Adds labels and title
plt.xlabel('Region')
plt.ylabel('Sales YTD (USD)')
plt.title('Total Regional Sales for the US')

# Function to show the plot
plt.show()

# The query to be executed in the database is defined
query = '''
SELECT CountryRegionCode, SUM(SalesYTD) AS TotalSales 
FROM AdventureWorks2019.Sales.SalesTerritory 
GROUP BY CountryRegionCode ORDER BY TotalSales DESC
'''

# Reads the data from query to pandas dataframe
countries = pd.read_sql(query, conn)

# Creats the bar plot
bars = plt.bar(countries['countryregioncode'], countries['totalsales'])

# Adds color to the bars
bars[0].set_color('blue')
bars[1].set_color('darkviolet')
bars[2].set_color('darkorange')
bars[3].set_color('chocolate')
bars[4].set_color('green')
bars[5].set_color('r')

# Adds labels and title
plt.xlabel('Countries')
plt.ylabel('Total Sales YTD (USD)')
plt.title('Total Sales Per Country')

# Function to show the plot
plt.show()


'''
**********************************************************************
                        Question 2
    What is the relationship between annual leave taken and bonus?
**********************************************************************
'''

# The query to be executed in the database is defined
# This query fetches records where the bonus for the salesperson is not equal to 0
query = '''
SELECT Vacation.BusinessEntityID, Bonus.Bonus,Vacation.VacationHours 
FROM AdventureWorks2019.HumanResources.Employee AS Vacation 
JOIN AdventureWorks2019.Sales.SalesPerson AS Bonus 
    ON Vacation.BusinessEntityID = Bonus.BusinessEntityID 
WHERE Bonus != 0
'''

# Reads the data from query to pandas dataframe
employee = pd.read_sql(query, conn, index_col = 'businessentityid' )

# Founds the correlation
a=np.corrcoef(employee.vacationhours, employee.bonus)[0,1]

# Function to create scatter plot
plt.scatter(employee.vacationhours, employee.bonus,color ='green', marker='o' )

# Adds labels and title
plt.xlabel('Vacation Hours')
plt.ylabel('Bonus($)')
plt.title('Sales Team Annual Leave (excluding managers)')

# Adds a line of best fit.np.polyfit is used to calculate the coefficients of the linear regression line, and np.polyval is used to evaluate the line at each x value. The resulting line is then plotted on top of the scatter plot.
coefficients = np.polyfit(employee.vacationhours, employee.bonus, 1)
line = np.polyval(coefficients, employee.vacationhours)
plt.plot(employee.vacationhours, line, color='orange', label=f'Line of Best Fit (Corr Coef: {a:.2f})')

# Function add a legend
plt.legend()

# Function to show the plot
plt.show()


'''
*********************************************************************
                            Question 3
        What is the relationship between Country and Revenue?
*********************************************************************
'''

# The query to be executed in the database is defined
# This query finds the best performing country
query = '''
SELECT CountryRegionCode, COUNT(*) AS NumStores 
FROM AdventureWorks2019.Sales.vStoreWithAddresses AS S 
INNER JOIN AdventureWorks2019.Person.CountryRegion AS C 
    ON C.Name = S.CountryRegionName 
GROUP BY CountryRegionName, CountryRegionCode 
ORDER BY NumStores DESC
'''

# Reads the data from queries to pandas dataframe
stores = pd.read_sql(query, conn)

# Creats the bar plot
bars = plt.bar(stores.countryregioncode, stores.numstores)

# Adds labels and title
plt.xlabel('Country')
plt.ylabel('Number of Stores')
plt.title('Number of Stores Per Country')

# Function to show the plot
plt.show()

# The query to be executed in the database is defined
# This query finds the number of store in different countries
query ='''
SELECT CountryRegionCode, COUNT(*) AS NumStores
FROM AdventureWorks2019.Sales.vStoreWithAddresses AS S 
INNER JOIN AdventureWorks2019.Person.CountryRegion AS C ON C.Name = S.CountryRegionName 
GROUP BY CountryRegionName, CountryRegionCode
ORDER BY 
    CASE 
        WHEN CountryRegionCode = 'US' THEN 1
        WHEN CountryRegionCode = 'CA' THEN 2
        WHEN CountryRegionCode = 'MX' THEN 3
        WHEN CountryRegionCode = 'FR' THEN 4
        WHEN CountryRegionCode = 'DE' THEN 5
        WHEN CountryRegionCode = 'AU' THEN 6
        ELSE 7
    END
'''

# The query to be executed in the database is defined
query2 = '''
SELECT CountryRegionCode, SUM(SalesYTD) AS TotalSales 
FROM AdventureWorks2019.Sales.SalesTerritory 
GROUP BY CountryRegionCode 
ORDER BY 
    CASE 
        WHEN CountryRegionCode = 'US' THEN 1
        WHEN CountryRegionCode = 'CA' THEN 2
        WHEN CountryRegionCode = 'MX' THEN 3
        WHEN CountryRegionCode = 'FR' THEN 4
        WHEN CountryRegionCode = 'DE' THEN 5
        WHEN CountryRegionCode = 'AU' THEN 6
        ELSE 7
    END
'''

# Reads the data from queries to pandas dataframe
stores = pd.read_sql(query, conn)
totalsales = pd.read_sql(query2, conn)

# Creates the bar plot for number of store
bars = plt.bar(stores.countryregioncode, stores.numstores)

# Adds labels and title
plt.xlabel('Country')
plt.ylabel('Number of Stores')
plt.title('Number of Stores Per Country')

# Functions to show the plot
plt.show()

# Creates the bar plot for total sales
bars_2 = plt.bar(totalsales['countryregioncode'], totalsales['totalsales'])
for i, bar in enumerate(bars_2):
    if totalsales['countryregioncode'][i] == 'US':
        bar.set_color('blue') 
    else:
        bar.set_color('lightgray')

# Adds labels and title		
plt.xlabel('Countries')
plt.ylabel('Total Sales')
plt.title('Total Sales Per Country')

# Function to show the plot
plt.show()

# Creates the donut chart for number of store
# Colors
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

# Explosion 
explode = None
plt.pie(stores['numstores'], colors=colors, labels=stores['countryregioncode'], autopct='%1.1f%%', startangle=270, pctdistance=0.85, explode=explode, shadow=False)

# Draws circle
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')  
plt.tight_layout()
plt.title('Percentage of Stores per Country (YTD)',color='black')
plt.legend()

# Function to show the plot
plt.show()

# Create the donut chart for total sales
# Colors
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

# Explosion 
explode = None
plt.pie(totalsales['totalsales'], colors=colors, labels=totalsales['countryregioncode'], autopct='%1.1f%%', startangle=270, pctdistance=0.85, explode=explode, shadow=False)

# Draws circle
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')  
plt.tight_layout()
plt.title('Percentage of Sales per Country (YTD)',color='black')
plt.legend()

# Function to show the plot
plt.show()

'''
*******************************************************************************
                            Question 4
    What is the relationship between sick leave and Job Title (PersonType)?
*******************************************************************************
'''

# The query to be executed in the database is defined
# This query joins tables to understand which department the employees belong to
query = '''
SELECT SickLeaveHours, Name AS department_name
FROM AdventureWorks2019.HumanResources.EmployeeDepartmentHistory AS a
INNER JOIN AdventureWorks2019.HumanResources.Employee AS b 
    ON a.BusinessEntityID = b.BusinessEntityID
INNER JOIN AdventureWorks2019.HumanResources.Department AS c 
    ON a.DepartmentID = c.DepartmentID
'''

# The query to be executed in the database is defined
# This query counts the number of employees in each team
query2 = '''
SELECT Name AS department_name, count(Name) AS count
FROM AdventureWorks2019.HumanResources.EmployeeDepartmentHistory AS a
INNER JOIN AdventureWorks2019.HumanResources.Employee AS b 
    ON a.BusinessEntityID = b.BusinessEntityID
INNER JOIN AdventureWorks2019.HumanResources.Department AS c 
    ON a.DepartmentID = c.DepartmentID
GROUP BY name
'''

# Reads the data from queries to pandas dataframe 
Q4 = pd.read_sql(query, conn)
Q4_1 = pd.read_sql(query2, conn)

# Merges the two dataframes on 'department_name'
Q4_2 = pd.merge(Q4, Q4_1, on='department_name', how='left')
Q4_2['department_name_2'] = Q4_2['department_name'].astype(str) + ' (' + Q4_2['count'].astype(str) + ')'
print(Q4_2)

# Calculates medians for each department
medians = Q4_2.groupby('department_name_2')['sickleavehours'].median()
sorted_departments = medians.sort_values().index

# Function to create box plots in the sorted order
plt.boxplot([Q4_2[Q4_2['department_name_2'] == department]['sickleavehours'] for department in sorted_departments], labels=sorted_departments, vert=False)

# Adds labels and title
plt.xlabel('Sick Leave Hours')
plt.ylabel('Department Name')
plt.title('Boxplot of Department Name by Sick Leave Hours (Sorted by Median)')

# Adjusts the layout to fit the screen
plt.tight_layout()

# Function to show the plot
plt.show()

# The query to be executed in the database is defined
# This query finds employees' average sick leave
query = '''
SELECT d.Name AS DepName, AVG(e1.SickLeaveHours) AS AvgSickLeave 
FROM AdventureWorks2019.HumanResources.Employee AS e1 
INNER JOIN AdventureWorks2019.HumanResources.EmployeeDepartmentHistory AS e2 
    ON e1.BusinessEntityID = e2.BusinessEntityID 
INNER JOIN AdventureWorks2019.HumanResources.Department AS d 
    ON e2.DepartmentID = d.DepartmentID 
GROUP BY d.Name 
ORDER BY AvgSickLeave
'''

# Reads the data from query to pandas dataframe 
sickleave = pd.read_sql(query, conn)

# Creats the bar plot
plt.barh(sickleave.depname, sickleave.avgsickleave)

# Adds labels and title
plt.xlabel('Sick Leave (Avg/Hr)')
plt.ylabel('Department')
plt.title('Average Sick Leave Per Employee Per Department')

# Adjusts the layout to fit the screen
plt.tight_layout()

# Function to show the plot
plt.show()

# The query to be executed in the database is defined
# This query finds number of employees in each department
query = '''
SELECT d.Name AS DepName, COUNT(e1.BusinessEntityID) AS NumEmployees 
FROM AdventureWorks2019.HumanResources.Employee AS e1 
INNER JOIN AdventureWorks2019.HumanResources.EmployeeDepartmentHistory AS e2 
    ON e1.BusinessEntityID = e2.BusinessEntityID 
INNER JOIN AdventureWorks2019.HumanResources.Department AS d 
    ON e2.DepartmentID = d.DepartmentID 
GROUP BY d.Name 
ORDER BY NumEmployees
'''

# Reads the data from query to pandas dataframe 
bar = pd.read_sql(query, conn)

# Creats the bar plot
plt.barh(bar.depname, bar.numemployees)

# Adds labels and title
plt.xlabel('Number of Employees')
plt.ylabel('Department')
plt.title('Number of Employees per Department')

# Adjusts the layout to fit the screen
plt.tight_layout()

# Function to show the plot
plt.show()


'''
****************************************************************************
                            Question 5
    What is the relationship between store trading duration and revenue?
****************************************************************************
'''

# The query to be executed in the database is defined
# This query finds information about the trading duration and average annual revenue of stores
query = '''
SELECT  2014 - YearOpened AS Store_Trading_Duration,AVG(AnnualRevenue) AS Average_Revenue
FROM AdventureWorks2019.Sales.vStoreWithDemographics
GROUP BY 2014 - YearOpened
''' 

# Reads the data from query to pandas dataframe 
Q5 = pd.read_sql(query, conn)
print(Q5)

# Function to create scatter plot
plt.scatter(Q5["store_trading_duration"], Q5["average_revenue"])

# Adds labels and title
plt.xlabel('Year of Opening')
plt.ylabel('Average Revenue')
plt.title('Store Trading Duration Against Revenue')

# Calculates correlation coefficient
correlation_coefficient = np.corrcoef(Q5["store_trading_duration"], Q5["average_revenue"])[0, 1]

# Fits a linear regression line
fit = np.polyfit(Q5["store_trading_duration"], Q5["average_revenue"], 1)
fit_fn = np.poly1d(fit)

# Plots the regression line
plt.plot(Q5["store_trading_duration"], fit_fn(Q5["store_trading_duration"]), color='red', label=f'Correlation Line (r = {correlation_coefficient:.2f})')

# Function add a legend
plt.legend()

# Adjusts the layout to fit the screen
plt.tight_layout()

# Function to show the plot
plt.show()

# The query to be executed in the database is defined
query = '''
SELECT  2014 - YearOpened AS store_trading_duration, AnnualRevenue AS annualrevenue
FROM AdventureWorks2019.Sales.vStoreWithDemographics
ORDER BY store_trading_duration DESC
'''

# Reads the data from query to pandas dataframe
data = pd.read_sql(query, conn, index_col='store_trading_duration')

bins = list(range(0, int(data.index.max()) + 6, 5))

# Set the maximum y-axis limit
max_frequency_limit = 65

# Create subplots for each distinct revenue value
revenue_values = data['annualrevenue'].unique()

fig, axes = plt.subplots(nrows=(len(revenue_values) + 1) // 2, ncols=2, figsize=(12, 8))
fig.tight_layout(pad=4.0)

for i, revenue_value in enumerate(revenue_values):
    row = i // 2
    col = i % 2
    subset = data[data['annualrevenue'] == revenue_value]
    axes[row, col].hist(subset.index, bins=bins, edgecolor='black')
    axes[row, col].set_title(f'Annual Revenue: {revenue_value}')
    axes[row, col].set_xlabel('Store Trading Duration')
    axes[row, col].set_ylabel('Frequency')
    axes[row, col].set_ylim(0, max_frequency_limit)  # Set common ylim for all subplots

# In case there's an odd number of unique revenue values, remove the empty subplot
if len(revenue_values) % 2 != 0:
    fig.delaxes(axes.flatten()[-1])

# Function to show the plot
plt.show()

'''
***************************************************************************************************
                                        Question 6     
    What is the relationship between the size of the stores, number of employees and revenue?                       
***************************************************************************************************
'''

# The query to be executed in the database is defined
# The query finds the specified demographic and financial details for each store
query = '''
SELECT BusinessEntityID, AnnualRevenue, SquareFeet, NumberEmployees 
FROM AdventureWorks2019.Sales.vStoreWithDemographics
''' 

# Reads the data from query to pandas dataframe
Q6 = pd.read_sql(query, conn)

# Scatter plot with different colors for each category
scatter = plt.scatter(Q6["numberemployees"], Q6["squarefeet"], c=Q6["annualrevenue"], cmap='coolwarm', label='Data points', s = 5, alpha = 0.4)

# Adds labels and title
plt.xlabel('Number of Employees')
plt.ylabel('SquareFeet')
plt.title('Correlation between the Number of Employees, Size of Store and Annual Revenue')

# Calculates correlation coefficient
correlation_coefficient = np.corrcoef(Q6["numberemployees"], Q6["squarefeet"])[0, 1]

# Fits a linear regression line
fit = np.polyfit(Q6["numberemployees"], Q6["squarefeet"], 1)
fit_fn = np.poly1d(fit)

# Plots the regression line, :.2f means to format the floating-point number with two decimal places
plt.plot(Q6["numberemployees"], fit_fn(Q6["numberemployees"]), color='red', label=f'Correlation Line between Number of Employees, Size of Store (r = {correlation_coefficient:.2f})')

# Adds a colorbar
plt.colorbar(scatter, label='Annual Revenue')

# Function add a legend
plt.legend()

# Adjusts the layout to fit the screen
plt.tight_layout()

# Function to show the plot
plt.show()
