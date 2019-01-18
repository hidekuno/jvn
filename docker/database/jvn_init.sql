create role kunohi with SUPERUSER LOGIN PASSWORD 'kunohi';
create database kunohi_db WITH TEMPLATE = template0 OWNER = kunohi encoding 'utf8' lc_collate 'ja_JP.utf8' lc_ctype 'ja_JP.utf8';
