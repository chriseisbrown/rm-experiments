INSERT INTO raremark.article values(999, 'test_url', "PMID", "test title include's apostrophe",
 1, "1.0", "journal name", "1967-06-01");
 
 INSERT INTO raremark.article values(101, 'http://www.ncbi.nlm.nih.gov/pubmed/25385939', 'PMID', 'something',
 1, '1.2', 'journal of something', '2014-01-03');

INSERT INTO raremark.article_abstract values(1, "the abstract text");

select * from raremark.article as a WHERE a._id=24582695;
select * from raremark.article_abstract;
select * from raremark.article order by journal;


select * from raremark.article;
 
SELECT a._id, a.publish_date, a.title, a.URL, ab.abstract_text
FROM article AS a
   LEFT JOIN article_abstract AS ab ON ab._id = a._id
WHERE a._id=996   24582695