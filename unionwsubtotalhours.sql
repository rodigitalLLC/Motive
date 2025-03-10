select
d1.EmployeeID
,d1.LastName
,d1.FirstName
,SUM(d1.HrsWorkedPast12Months)
,d1.HrsWorkedPast12Months
,d1.`Job Title`
,d1.TermDate
-- ,`d1.Associate ID`
FROM
demo AS d1
--LEFT JOIN demo as d2
--ON
--d1.`Associate ID`=d2.`Associate ID`
-- WHERE d1.LastName='Hartman'
GROUP BY `d1.Associate ID`
ORDER BY d1.LastName;

select
d1.EmployeeID
,d1.LastName
,d1.FirstName
,SUM(d1.HrsWorkedPast12Months)
-- ,d1.HrsWorkedPast12Months
,d1.`Job Title`
,d1.TermDate
,d1.`Associate ID`
FROM demo d1
GROUP BY d1.`Associate ID` 
UNION ALL
select
d2.EmployeeID
,d2.LastName
,d2.FirstName
--,'' AS 'SUM'
,d2.HrsWorkedPast12Months
,d2.`Job Title`
,d2.TermDate
,d2.`Associate ID`
FROM demo d2
-- WHERE d2.TermDate!=''
WHERE d2.TermDate IS NOT NULL
ORDER BY `Associate ID`;

select
d1.EmployeeID
,d1.LastName
,d1.FirstName
,SUM(d1.HrsWorkedPast12Months)
,d1.HrsWorkedPast12Months
,d1.`Job Title`
,d1.TermDate
,d1.`Associate ID`
FROM demo d1
JOIN (SELECT `Associate ID` FROM demo
WHERE d1.`Associate ID`=d2.`Associate ID` 
GROUP BY d1.`Associate ID` 
ORDER BY d1.LastName);


select 
d1.EmployeeID
,d1.LastName
,d1.FirstName
,SUM(d1.HrsWorkedPast12Months)
,d1.HrsWorkedPast12Months
,d1.`Job Title`
,d1.TermDate
,d1.`Associate ID`
FROM demo d1
GROUP BY d1.`Associate ID`
ORDER BY `Associate ID`;