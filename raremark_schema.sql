DROP TABLE article;
DROP TABLE article_abstract;

CREATE TABLE `article` (
  `_id` int(10) unsigned NOT NULL,
  `URL` varchar(200) DEFAULT NULL,
  `id_type` varchar(20) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `doc_version` varchar(20) DEFAULT NULL,
  `journal` varchar(200) DEFAULT NULL,
  `publish_date` date DEFAULT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `_id_UNIQUE` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `article_abstract` (
  `_id` int(10) unsigned NOT NULL,
  `abstract_text` text,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `_id_UNIQUE` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;