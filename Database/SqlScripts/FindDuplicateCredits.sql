select MovieId, PersonId, Relationship, Count FROM (select c1.*, COUNT(*) AS Count from Credits c1
INNER JOIN Credits c2
WHERE c1.MovieId=c2.MovieId AND c1.PersonId=c2.PersonId AND c1.Relationship=c2.Relationship
GROUP BY c1.MovieId, c1.PersonId, c1.`Relationship`) A WHERE Count > 1