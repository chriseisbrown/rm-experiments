DROP TABLE article;
DROP TABLE article_id;
DROP TABLE article_abstract;
DROP TABLE disease;
DROP TABLE mesh_term;

CREATE TABLE `article_id` (
  `_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `_id_UNIQUE` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `article` (
  `_id` int(10) unsigned NOT NULL,
  `disease` varchar(200) DEFAULT NULL,
  `URL` varchar(200) DEFAULT NULL,
  `id_type` varchar(20) DEFAULT NULL,
  `title` varchar(400) DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `doc_version` varchar(20) DEFAULT NULL,
  `journal` varchar(200) DEFAULT NULL,
  `publish_date` date DEFAULT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `_id_UNIQUE` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `article_abstract` (
  `_id` int(10) unsigned NOT NULL,
  `abstract_text` text,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `_id_UNIQUE` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `disease` (
  `_id` int(10) unsigned NOT NULL,
  `disease_name` varchar(200),
  `short_name` varchar(200),
  PRIMARY KEY (`_id`),
  UNIQUE KEY `_id_UNIQUE` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `mesh_term` (
  `_id` int(10) unsigned NOT NULL,
  `disease_id` int(10) unsigned,
  `entry_term` varchar(200),
  PRIMARY KEY (`_id`),
  UNIQUE KEY `_id_UNIQUE` (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;