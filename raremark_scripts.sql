INSERT INTO raremark.article values(999, 'test_url', "PMID", "test title include's apostrophe",
 1, "1.0", "journal name", "1967-06-01");
 
 INSERT INTO raremark.article values(101, 'http://www.ncbi.nlm.nih.gov/pubmed/25385939', 'PMID', 'something',
 1, '1.2', 'journal of something', '2014-01-03');

INSERT INTO raremark.article_abstract values(1, "the abstract text");

select * from raremark.article as a WHERE a._id=24582695;
select * from raremark.article_abstract;
select * from raremark.article order by journal;
select * from raremark.disease;
select * from raremark.mesh_term order by disease_id;

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


INSERT INTO raremark.disease values(1, "Fabry's disease", "Fabry");
INSERT INTO raremark.disease values(2, "Huntingdon's disease", "Huntingdon");
INSERT INTO raremark.disease values(3, "Muscular Atrophy, Spinal", "SMA");
INSERT INTO raremark.disease values(4, "Duchenne muscular dystrophy", "Duchenne");
INSERT INTO raremark.disease values(5, "Behcet syndrome", "Behcet");
INSERT INTO raremark.disease values(6, "Gaucher disease", "Gaucher");
INSERT INTO raremark.disease values(7, "Myelofibrosis", "Myelofibrosis");

INSERT INTO raremark.mesh_term values(1, 1, "Anderson-Fabry Disease");
INSERT INTO raremark.mesh_term values(2, 1, "alpha-Galactosidase A Deficiency Disease");
INSERT INTO raremark.mesh_term values(3, 1, "Fabry Disease");
INSERT INTO raremark.mesh_term values(4, 3, "Muscular Atrophy, Spinal");
INSERT INTO raremark.mesh_term values(5, 1, "Fabry's disease");
INSERT INTO raremark.mesh_term values(6, 2, "Huntington's Disease");

INSERT INTO raremark.mesh_term values(7, 1, "alpha Galactosidase A Deficiency Disease");
INSERT INTO raremark.mesh_term values(8, 1, "Anderson Fabry Disease");
INSERT INTO raremark.mesh_term values(9, 1, "Angiokeratoma Diffuse");
INSERT INTO raremark.mesh_term values(10, 1, "Ceramide Trihexosidase Deficiency");
INSERT INTO raremark.mesh_term values(11, 1, "Deficiency, Ceramide Trihexosidase");
INSERT INTO raremark.mesh_term values(12, 1, "Fabry's Disease");
INSERT INTO raremark.mesh_term values(13, 1, "GLA Deficiency");
INSERT INTO raremark.mesh_term values(14, 1, "Deficiency, GLA");
INSERT INTO raremark.mesh_term values(15, 1, "Hereditary Dystopic Lipidosis");
INSERT INTO raremark.mesh_term values(16, 1, "Lipidosis, Hereditary Dystopic");
INSERT INTO raremark.mesh_term values(17, 1, "alpha-Galactosidase A Deficiency");
INSERT INTO raremark.mesh_term values(18, 1, "Deficiency, alpha-Galactosidase A");
INSERT INTO raremark.mesh_term values(19, 1, "alpha Galactosidase A Deficiency");
INSERT INTO raremark.mesh_term values(20, 1, "Angiokeratoma, Diffuse");
INSERT INTO raremark.mesh_term values(21, 1, "Diffuse Angiokeratoma");
INSERT INTO raremark.mesh_term values(22, 1, "Angiokeratoma Corporis Diffusum");


INSERT INTO raremark.mesh_term values(23, 3, "Adult Spinal Muscular Atrophy");
INSERT INTO raremark.mesh_term values(24, 3, "Adult-Onset Spinal Muscular Atrophy");
INSERT INTO raremark.mesh_term values(25, 3, "Amyotrophy, Neurogenic Scapuloperoneal, New England Type");
INSERT INTO raremark.mesh_term values(26, 3, "Bulbospinal Neuronopathy");
INSERT INTO raremark.mesh_term values(27, 3, "Distal Spinal Muscular Atrophy");
INSERT INTO raremark.mesh_term values(28, 3, "Hereditary Motor Neuronopathy");
INSERT INTO raremark.mesh_term values(29, 3, "Muscular Atrophy, Adult Spinal");
INSERT INTO raremark.mesh_term values(30, 3, "Myelopathic Muscular Atrophy");
INSERT INTO raremark.mesh_term values(31, 3, "Myelopathic Muscular Atrophy, Progressive");
INSERT INTO raremark.mesh_term values(32, 3, "Oculopharyngeal Spinal Muscular Atrophy");
INSERT INTO raremark.mesh_term values(33, 3, "Progressive Muscular Atrophy");
INSERT INTO raremark.mesh_term values(34, 3, "Progressive Myelopathic Muscular Atrophy");
INSERT INTO raremark.mesh_term values(35, 3, "Progressive Proximal Myelopathic Muscular Atrophy");
INSERT INTO raremark.mesh_term values(36, 3, "Proximal Myelopathic Muscular Atrophy, Progressive");
INSERT INTO raremark.mesh_term values(37, 3, "Scapuloperoneal Form of Spinal Muscular Atrophy");
INSERT INTO raremark.mesh_term values(38, 3, "Scapuloperoneal Spinal Muscular Atrophy");
INSERT INTO raremark.mesh_term values(39, 3, "Spinal Amyotrophy");
INSERT INTO raremark.mesh_term values(40, 3, "Spinal Muscular Atrophy");
INSERT INTO raremark.mesh_term values(41, 3, "Spinal Muscular Atrophy, Distal");
INSERT INTO raremark.mesh_term values(42, 3, "Spinal Muscular Atrophy, Oculopharyngeal");
INSERT INTO raremark.mesh_term values(43, 3, "Spinal Muscular Atrophy, Scapuloperoneal");
INSERT INTO raremark.mesh_term values(44, 3, "Spinal Muscular Atrophy, Scapuloperoneal Form");

INSERT INTO raremark.mesh_term values(45, 4, "Becker Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(46, 4, "Becker's Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(47, 4, "Cardiomyopathy, Dilated, 3B");
INSERT INTO raremark.mesh_term values(48, 4, "Cardiomyopathy, Dilated, X-Linked");
INSERT INTO raremark.mesh_term values(49, 4, "Childhood Muscular Dystrophy, Pseudohypertrophic");
INSERT INTO raremark.mesh_term values(50, 4, "Childhood Pseudohypertrophic Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(51, 4, "Duchenne and Becker Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(52, 4, "Duchenne Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(53, 4, "Duchenne-Becker Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(54, 4, "Duchenne-Type Progressive Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(55, 4, "Muscular Dystrophy Pseudohypertrophic Progressive, Becker Type");
INSERT INTO raremark.mesh_term values(56, 4, "Muscular Dystrophy, Becker");
INSERT INTO raremark.mesh_term values(57, 4, "Muscular Dystrophy, Becker Type");
INSERT INTO raremark.mesh_term values(58, 4, "Muscular Dystrophy, Childhood, Pseudohypertrophic");
INSERT INTO raremark.mesh_term values(59, 4, "Muscular Dystrophy, Duchenne and Becker Types");
INSERT INTO raremark.mesh_term values(60, 4, "Muscular Dystrophy, Duchenne Type");
INSERT INTO raremark.mesh_term values(61, 4, "Muscular Dystrophy, Pseudohypertrophic");
INSERT INTO raremark.mesh_term values(62, 4, "Muscular Dystrophy, Pseudohypertrophic Progressive, Becker Type");
INSERT INTO raremark.mesh_term values(63, 4, "Muscular Dystrophy, Pseudohypertrophic Progressive, Duchenne Type");
INSERT INTO raremark.mesh_term values(64, 4, "Muscular Dystrophy, Pseudohypertrophic, Childhood");
INSERT INTO raremark.mesh_term values(65, 4, "Progressive Muscular Dystrophy, Duchenne Type");
INSERT INTO raremark.mesh_term values(66, 4, "Pseudohypertrophic Childhood Muscular Dystrophy");
INSERT INTO raremark.mesh_term values(67, 4, "Pseudohypertrophic Muscular Dystrophy, Childhood")INSERT INTO raremark.mesh_term values(68, 4, "Adamantiades-Behcet Disease");


INSERT INTO raremark.mesh_term values(68, 5, "Behcet Disease");
INSERT INTO raremark.mesh_term values(69, 5, "Behcet Triple Symptom Complex");
INSERT INTO raremark.mesh_term values(70, 5, "Behcet's Syndrome");
/*INSERT INTO raremark.mesh_term values(71, 5, "Behçet Disease");*/
INSERT INTO raremark.mesh_term values(72, 5, "Old Silk Route Disease");
INSERT INTO raremark.mesh_term values(73, 5, "Triple Symptom Complex");
INSERT INTO raremark.mesh_term values(74, 5, "Triple-Symptom Complex");

INSERT INTO raremark.mesh_term values(75,6,"Acid beta-Glucosidase Deficiency");
INSERT INTO raremark.mesh_term values(76,6,"Acid beta-Glucosidase Deficiency Disease");
INSERT INTO raremark.mesh_term values(77,6,"Acute Neuronopathic Gaucher Disease");
INSERT INTO raremark.mesh_term values(78,6,"Cerebroside Lipidosis Syndrome");
INSERT INTO raremark.mesh_term values(79,6,"Chronic Gaucher Disease");
INSERT INTO raremark.mesh_term values(80,6,"Gaucher Disease Type 1");
INSERT INTO raremark.mesh_term values(81,6,"Gaucher Disease Type 2");
INSERT INTO raremark.mesh_term values(82,6,"Gaucher Disease Type 3");
INSERT INTO raremark.mesh_term values(83,6,"Gaucher Disease, Acute Neuronopathic");
INSERT INTO raremark.mesh_term values(84,6,"Gaucher Disease, Acute Neuronopathic Type");
INSERT INTO raremark.mesh_term values(85,6,"Gaucher Disease, Chronic");
INSERT INTO raremark.mesh_term values(86,6,"Gaucher Disease, Chronic Neuronopathic Type");
INSERT INTO raremark.mesh_term values(87,6,"Gaucher Disease, Infantile");
INSERT INTO raremark.mesh_term values(88,6,"Gaucher Disease, Infantile Cerebral");
INSERT INTO raremark.mesh_term values(89,6,"Gaucher Disease, Juvenile");
INSERT INTO raremark.mesh_term values(90,6,"Gaucher Disease, Juvenile and Adult, Cerebral");
INSERT INTO raremark.mesh_term values(91,6,"Gaucher Disease, Neuronopathic");
INSERT INTO raremark.mesh_term values(92,6,"Gaucher Disease, Non-Neuronopathic Form");
INSERT INTO raremark.mesh_term values(93,6,"Gaucher Disease, Noncerebral Juvenile");
INSERT INTO raremark.mesh_term values(94,6,"Gaucher Disease, Subacute Neuronopathic Form");
INSERT INTO raremark.mesh_term values(95,6,"Gaucher Disease, Subacute Neuronopathic Type");
INSERT INTO raremark.mesh_term values(96,6,"Gaucher Disease, Type 1");
INSERT INTO raremark.mesh_term values(97,6,"Gaucher Disease, Type 2");
INSERT INTO raremark.mesh_term values(98,6,"Gaucher Disease, Type 3");
INSERT INTO raremark.mesh_term values(99,6,"Gaucher Disease, Type I");
INSERT INTO raremark.mesh_term values(100,6,"Gaucher Disease, Type II");
INSERT INTO raremark.mesh_term values(101,6,"Gaucher Disease, Type III");
INSERT INTO raremark.mesh_term values(102,6,"Gaucher Splenomegaly");
INSERT INTO raremark.mesh_term values(103,6,"Gaucher Syndrome");
INSERT INTO raremark.mesh_term values(104,6,"Gaucher's Disease");
INSERT INTO raremark.mesh_term values(105,6,"Gauchers Disease");
INSERT INTO raremark.mesh_term values(106,6,"GBA Deficiency");
INSERT INTO raremark.mesh_term values(107,6,"Glucocerebrosidase Deficiency");
INSERT INTO raremark.mesh_term values(108,6,"Glucocerebrosidase Deficiency Disease");
INSERT INTO raremark.mesh_term values(109,6,"Glucocerebrosidosis");
INSERT INTO raremark.mesh_term values(110,6,"Glucosyl Cerebroside Lipidosis");
INSERT INTO raremark.mesh_term values(111,6,"Glucosylceramidase Deficiency");
INSERT INTO raremark.mesh_term values(112,6,"Glucosylceramide Beta-Glucosidase Deficiency");
INSERT INTO raremark.mesh_term values(113,6,"Glucosylceramide Beta-Glucosidase Deficiency Disease");
INSERT INTO raremark.mesh_term values(114,6,"Glucosylceramide Lipidosis");
INSERT INTO raremark.mesh_term values(115,6,"Infantile Gaucher Disease");
INSERT INTO raremark.mesh_term values(116,6,"Kerasin Histiocytosis");
INSERT INTO raremark.mesh_term values(117,6,"Kerasin Lipoidosis");
INSERT INTO raremark.mesh_term values(118,6,"Kerasin thesaurismosis");
INSERT INTO raremark.mesh_term values(119,6,"Lipoid Histiocytosis (Kerasin Type)");
INSERT INTO raremark.mesh_term values(120,6,"Neuronopathic Gaucher Disease");
INSERT INTO raremark.mesh_term values(121,6,"Non-Neuronopathic Gaucher Disease");
INSERT INTO raremark.mesh_term values(122,6,"Subacute Neuronopathic Gaucher Disease");
INSERT INTO raremark.mesh_term values(123,6,"Type 1 Gaucher Disease");
INSERT INTO raremark.mesh_term values(124,6,"Type 2 Gaucher Disease");
INSERT INTO raremark.mesh_term values(125,6,"Type 3 Gaucher Disease");

INSERT INTO raremark.mesh_term values(126,7,"Agnogenic Myeloid Metaplasia");
INSERT INTO raremark.mesh_term values(127,7,"Bone Marrow Fibrosis");
INSERT INTO raremark.mesh_term values(128,7,"Chronic Idiopathic Myelofibrosis");
INSERT INTO raremark.mesh_term values(129,7,"Fibrosis, Bone Marrow");
INSERT INTO raremark.mesh_term values(130,7,"Idiopathic Myelofibrosis");
INSERT INTO raremark.mesh_term values(131,7,"Myelofibrosis");
INSERT INTO raremark.mesh_term values(132,7,"Myelofibrosis With Myeloid Metaplasia");
INSERT INTO raremark.mesh_term values(133,7,"Myeloid Metaplasia");
INSERT INTO raremark.mesh_term values(134,7,"Myelosclerosis");
INSERT INTO raremark.mesh_term values(135,7,"Myelosis, Nonleukemic");

INSERT INTO raremark.mesh_term values(136,2,"Akinetic-Rigid Variant of Huntington Disease");
INSERT INTO raremark.mesh_term values(137,2,"Chorea, Chronic Progressive Hereditary (Huntington)");
INSERT INTO raremark.mesh_term values(138,2,"Chronic Progressive Hereditary Chorea (Huntington)");
INSERT INTO raremark.mesh_term values(139,2,"Huntington Chorea");
INSERT INTO raremark.mesh_term values(140,2,"Huntington Chronic Progressive Hereditary Chorea");
INSERT INTO raremark.mesh_term values(141,2,"Huntington Disease, Akinetic-Rigid Variant");
INSERT INTO raremark.mesh_term values(142,2,"Huntington Disease, Juvenile");
INSERT INTO raremark.mesh_term values(143,2,"Huntington Disease, Juvenile-Onset");
INSERT INTO raremark.mesh_term values(144,2,"Huntington Disease, Late Onset");
INSERT INTO raremark.mesh_term values(145,2,"Huntington's Chorea");
INSERT INTO raremark.mesh_term values(146,2,"Huntington's Disease");
INSERT INTO raremark.mesh_term values(147,2,"Juvenile Huntington Disease");
INSERT INTO raremark.mesh_term values(148,2,"Juvenile-Onset Huntington Disease");
INSERT INTO raremark.mesh_term values(149,2,"Late-Onset Huntington Disease");
INSERT INTO raremark.mesh_term values(150,2,"Progressive Chorea, Chronic Hereditary (Huntington)");
INSERT INTO raremark.mesh_term values(151,2,"Progressive Chorea, Hereditary, Chronic (Huntington)");

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
