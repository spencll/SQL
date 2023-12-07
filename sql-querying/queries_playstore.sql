-- Comments in SQL Start with dash-dash --

--1. SELECT * FROM analytics 
--WHERE id = 1880;

--2. SELECT id, app_name FROM analytics
--WHERE last_updated = '2018-08-01'

--3. SELECT category, COUNT(category) FROM analytics
--GROUP BY category 

--4. SELECT app_name, reviews FROM analytics
--ORDER BY rating DESC
--LIMIT 5;

--5. SELECT * FROM analytics WHERE rating>=4.8
--ORDER BY reviews DESC
--LIMIT 1;

--6. SELECT AVG(rating) FROM analytics
--GROUP BY category
--ORDER BY avg DESC

--7. SELECT app_name, price, rating FROM analytics WHERE rating<3
--ORDER BY price DESC
--LIMIT 1

--8. SELECT * FROM analytics
--WHERE min_installs<=50 AND rating>0
--ORDER BY rating DESC

--9. SELECT app_name FROM analytics
--WHERE rating<3 and reviews>10000;

--10. SELECT app_name, price FROM analytics
--WHERE price BETWEEN 0.10 AND 1
--ORDER BY reviews DESC
--LIMIT 10;

--11. SELECT app_name, last_updated FROM analytics
--ORDER BY last_updated
--LIMIT 1;

--12. SELECT app_name, price FROM analytics
--ORDER BY price DESC
--LIMIT 1;

--13. SELECT SUM(reviews) FROM analytics;

--14. SELECT category, COUNT(category) FROM analytics
--GROUP BY category
--HAVING COUNT(category)>300;

--15. SELECT app_name, reviews, min_installs, min_installs/reviews AS ratio FROM analytics
--WHERE min_installs>=100000
--ORDER BY min_installs/reviews DESC
--LIMIT 1;
