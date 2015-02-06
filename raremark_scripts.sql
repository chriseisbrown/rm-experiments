INSERT INTO raremark.article values(999, 'test_url', "PMID", "test title include's apostrophe",
 1, "1.0", "journal name", "1967-06-01");
 
 INSERT INTO raremark.article values(101, 'http://www.ncbi.nlm.nih.gov/pubmed/25385939', 'PMID', 'something',
 1, '1.2', 'journal of something', '2014-01-03');

INSERT INTO raremark.article_abstract values(1, "the abstract text");

select * from raremark.article as a WHERE a._id=24582695;
select * from raremark.article_abstract;
select * from raremark.article order by journal;
select * from raremark.disease;
select * from raremark.mesh_term;

truncate table raremark.disease;

truncate table raremark.article_id;
truncate table raremark.article;
truncate table raremark.article_abstract;

select count(*) from raremark.article;
 
SELECT a._id, a.publish_date, a.title, a.URL, ab.abstract_text
FROM article AS a
   LEFT JOIN article_abstract AS ab ON ab._id = a._id
WHERE a._id=23350580;

commit;

Proximal spinal muscular atrophy
INSERT INTO raremark.disease values(1, "Fabry's disease", "Fabry");
INSERT INTO raremark.disease values(2, "Huntingdon's disease", "Huntingdon");
INSERT INTO raremark.disease values(3, "Muscular Atrophy, Spinal", "SMA");
INSERT INTO raremark.disease values(4, "Duchenne muscular dystrophy", "Duchenne");
INSERT INTO raremark.disease values(5, "Behcet disease", "Behcet");
INSERT INTO raremark.disease values(6, "Gaucher disease", "Gaucher");
INSERT INTO raremark.disease values(7, "Myelofibrosis", "Myelofibrosis");


INSERT INTO raremark.mesh_term values(1, 1, "Anderson-Fabry Disease");
INSERT INTO raremark.mesh_term values(2, 1, "alpha-Galactosidase A Deficiency Disease");
INSERT INTO raremark.mesh_term values(3, 1, "Fabry Disease");
INSERT INTO raremark.mesh_term values(4, 3, "Muscular Atrophy, Spinal");
INSERT INTO raremark.mesh_term values(5, 1, "Fabry's disease");
INSERT INTO raremark.mesh_term values(6, 2, "Huntington's Disease");


insert into raremark.article_id(_id) values("12611534") on duplicate key update _id=values(_id);

INSERT INTO raremark.article(_id,disease,URL,id_type,title,version,doc_version,journal,publish_date) values(
'25565388'
,'some name',
'http://www.ncbi.nlm.nih.gov/pubmed/25565388',
'PMID',
'Hypothalamic-pituitary-adrenal axis functioning in Huntington\'s disease and its association with depressive symptoms and suicidality.',1,'1','Journal of neuroendocrinology',
'2015-01-06') 
ON DUPLICATE KEY UPDATE 
_id =VALUES(_id),disease=(disease),URL =VALUES(URL),id_type =VALUES(id_type),title =VALUES(title),version =VALUES(version),             doc_version =VALUES(doc_version),journal =VALUES(journal),publish_date =VALUES(publish_date)
