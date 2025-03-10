select A,B, SUM(B) OVER(PARTITION BY A) AS C FROM T ;

select 
LastName
,FirstName
,`Associate ID`
,HrsWorkedPast12Months
,TermDate
,SUM(HrsWorkedPast12Months) 
OVER(PARTITION BY `Associate ID`) AS C 
FROM demo 
ORDER BY `Associate ID`;

select 
LastName
,FirstName
,`Associate ID`
,HrsWorkedPast12Months
,TermDate
,CASE WHEN TermDate IS NULL THEN SUM(HrsWorkedPast12Months) OVER(PARTITION BY `Associate ID`) ELSE HrsWorkedPast12Months END AS C
FROM demo 
ORDER BY `Associate ID`;

select 
*
,CASE WHEN TermDate IS NULL THEN SUM(HrsWorkedPast12Months) OVER(PARTITION BY `Associate ID`) ELSE HrsWorkedPast12Months END AS C
FROM demo 
ORDER BY `Associate ID`;

