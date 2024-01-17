--*****************************************************************
--                       Question 1
-- What are the regional sales in the best performing country?
--*****************************************************************

--This query finds the best performing country
SELECT CountryRegionCode, COUNT(*) AS NumStores 
FROM [AdventureWorks2019].[Sales].[vStoreWithAddresses] AS S 
INNER JOIN [AdventureWorks2019].[Person].[CountryRegion] AS C 
    ON C.Name = S.CountryRegionName 
GROUP BY CountryRegionName, CountryRegionCode 
ORDER BY NumStores DESC;


--This query retrieves the top 1000 records of specific columns from the Sales.SalesTerritory table
--and it orders the results in descending order based on the SalesYTD column.
SELECT TOP (1000) [TerritoryID]
		,[Name]
		,[CountryRegionCode]
		,[SalesYTD]
		,[SalesLastYear]
FROM [AdventureWorks2019].[Sales].[SalesTerritory]
WHERE CountryRegionCode = 'US'
ORDER BY SalesYTD DESC;


--This query calculates the total sales for each distinct CountryRegionCode in the Sales.SalesTerritory table, 
--grouping the results by country code, and then orders the output in descending order 
--based on the calculated total sales.
SELECT [CountryRegionCode]
	,SUM([SalesYTD]) AS TotalSales
FROM [AdventureWorks2019].[Sales].[SalesTerritory]
GROUP BY CountryRegionCode
ORDER BY TotalSales DESC;


--*****************************************************************
--                       Question 2
-- What is the relationship between annual leave taken and bonus?
--*****************************************************************

--This query selects the BusinessEntityID, Bonus, JobTitle, and VacationHours columns 
--from the HumanResources.Employee table and the Sales.SalesPerson table. 
--The tables are joined on the BusinessEntityID,
--linking employees with their corresponding bonus information in the sales department.
SELECT [Vacation].[BusinessEntityID]
		,[Bonus][.Bonus]
		,[Vacation].[JobTitle]
		,[Vacation].[VacationHours]
FROM [AdventureWorks2019].[HumanResources].[Employee] AS Vacation
JOIN [AdventureWorks2019].[Sales].[SalesPerson] AS Bonus
	ON Vacation.BusinessEntityID = bonus.BusinessEntityID;


--This query selects the BusinessEntityID, Bonus, and VacationHours columns from the HumanResources.Employee
--table and the Sales.SalesPerson table. The tables are joined on the BusinessEntityID, 
--linking employees with their corresponding bonus information in the sales department. 
--The results are filtered to include only rows where the Bonus value is not equal to 0.
SELECT [Vacation].[BusinessEntityID]
		,[Bonus].[Bonus]
		,[Vacation].[VacationHours]
FROM [AdventureWorks2019].[HumanResources].[Employee] AS Vacation
JOIN [AdventureWorks2019].[Sales].[SalesPerson] AS Bonus
	ON Vacation.BusinessEntityID = bonus.BusinessEntityID
WHERE bonus != 0;


--The tables are joined on the BusinessEntityID, linking employees with their corresponding bonus information in the sales department. 
--The results are filtered to include only rows where the Bonus value is not equal to 0. 
--This query provides detailed information about employees and their associated salesperson bonuses in the AdventureWorks2019 database.
SELECT [Vacation].[BusinessEntityID]
		,Bonus.Bonus
		,Bonus.CommissionPct
		,Bonus.SalesYTD
		,Bonus.SalesLastYear
		,Vacation.VacationHours
		,Vacation.SickLeaveHours
FROM [AdventureWorks2019].[HumanResources].[Employee] AS Vacation
JOIN [AdventureWorks2019].[Sales].[SalesPerson] AS Bonus
	ON Vacation.BusinessEntityID = bonus.BusinessEntityID
WHERE bonus != 0


--*****************************************************************
--                       Question 3
-- What is the relationship between Country and Revenue?
--*****************************************************************

--This query retrieves the distinct CountryRegionName values from the Sales.vStoreWithAddresses view 
--and calculates the count of records for each region, naming the result column as NumStores. 
--The results are then grouped by CountryRegionName, and the output is ordered in descending order 
--based on the count of stores.
SELECT [CountryRegionName], COUNT(*) AS NumStores
FROM [AdventureWorks2019].[Sales].[vStoreWithAddresses]
GROUP BY CountryRegionName
ORDER BY NumStores DESC

--This query finds the number of store in different countries
SELECT [CountryRegionCode], COUNT(*) AS NumStores
FROM [AdventureWorks2019].[Sales].[vStoreWithAddresses] AS S 
INNER JOIN [AdventureWorks2019].[Person].[CountryRegion] AS C 
	ON C.Name = S.CountryRegionName 
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

--This query finds the number of sales in different countries
SELECT [CountryRegionCode], SUM(SalesYTD) AS TotalSales 
FROM [AdventureWorks2019].[Sales].[SalesTerritory]
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


--***************************************************************************
--                       Question 4
-- What is the relationship between sick leave and Job Title (PersonType)?
--***************************************************************************

--This query retrieves the average sick leave hours for employees in each department, 
--using the HumanResources.Employee, HumanResources.EmployeeDepartmentHistory, and HumanResources.Department tables. 
--The results are grouped by department name (DepName), with each group showing the average sick leave hours 
--for employees within that department.
SELECT d.Name AS DepName, AVG(e1.SickLeaveHours) AS AvgSickLeave
FROM [AdventureWorks2019].[HumanResources].[Employee] AS e1
INNER JOIN [AdventureWorks2019].[HumanResources].[EmployeeDepartmentHistory] AS e2
	ON e1.BusinessEntityID = e2.BusinessEntityID
INNER JOIN [AdventureWorks2019].[HumanResources].[Department] AS d
	ON e2.DepartmentID = d.DepartmentID
GROUP BY d.Name;;


--This query retrieves the count of employees (NumEmployees) in each department, 
--using the HumanResources.Employee, HumanResources.EmployeeDepartmentHistory, and HumanResources.Department tables. 
--The results are grouped by department name (DepName), and the output is ordered in descending order based on 
--the number of employees in each department.
SELECT d.Name AS DepName, COUNT(e1.[BusinessEntityID]) AS NumEmployees
FROM [AdventureWorks2019].[HumanResources].[Employee] AS e1
INNER JOIN [AdventureWorks2019].[HumanResources].[EmployeeDepartmentHistory] AS e2
	ON e1.BusinessEntityID = e2.BusinessEntityID
INNER JOIN [AdventureWorks2019].[HumanResources].[Department] AS d
	ON e2.DepartmentID = d.DepartmentID
GROUP BY d.Name
ORDER BY NumEmployees DESC;


--**********************************************************************
--                       Question 5
-- What is the relationship between store trading duration and revenue?
--**********************************************************************

--This query calculates the trading duration of stores (Store_Trading_Duration) by subtracting the YearOpened from 2014 
--and computes the average annual revenue (Average_Revenue) for each calculated trading duration. 
--The results are grouped by the trading duration, providing an average revenue for stores 
--that opened in the same year relative to 2014.
SELECT  2014 - [YearOpened] AS Store_Trading_Duration,AVG([AnnualRevenue]) AS Average_Revenue
FROM [AdventureWorks2019].[Sales].[vStoreWithDemographics]
GROUP BY 2014 - [YearOpened];


--This SQL query shows the trading duration (calculated as the difference between 2014 and the opening year) 
--and annual revenue of stores from the vStoreWithDemographics view, ordered by trading duration in descending order.
SELECT  2014 - [YearOpened] AS store_trading_duration, [AnnualRevenue] AS annualrevenue
FROM [AdventureWorks2019].[Sales].[vStoreWithDemographics]
ORDER BY store_trading_duration DESC;

--*********************************************************************************************
--                       Question 6
-- What is the relationship between the size of the stores, number of employees and revenue?
--*********************************************************************************************

--This  query selects the columns BusinessEntityID, AnnualRevenue, SquareFeet, and NumberEmployees from the view 
--Sales.vStoreWithDemographics, providing information about stores along with their demographic details in the AdventureWorks2019 database.
SELECT [BusinessEntityID]
      ,[AnnualRevenue]
      ,[SquareFeet]
      ,[NumberEmployees]
FROM [AdventureWorks2019].[Sales].[vStoreWithDemographics];
