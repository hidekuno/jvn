create role jvn with SUPERUSER LOGIN PASSWORD 'jvn';
create database jvn_db WITH TEMPLATE = template0 OWNER = jvn encoding 'utf8' lc_collate 'ja_JP.utf8' lc_ctype 'ja_JP.utf8';
