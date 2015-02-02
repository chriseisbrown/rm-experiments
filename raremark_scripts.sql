INSERT INTO raremark.article values(1, "test_url", "PMID", "test title",
 1, "1.0", "journal name", "1967-06-01");

INSERT INTO raremark.article_abstract values(1, "the abstract text");

select * from raremark.article;
select * from raremark.article_abstract;


select * from raremark.article;
 
SELECT a._id, a.publish_date, a.title, a.URL, ab.abstract_text
FROM article AS a
   LEFT JOIN article_abstract AS ab ON ab._id = a._id
WHERE a._id=1