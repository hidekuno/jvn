create role hideki with SUPERUSER LOGIN PASSWORD 'hideki';
create database hideki_db WITH TEMPLATE = template0 OWNER = hideki encoding 'utf8' lc_collate 'ja_JP.utf8' lc_ctype 'ja_JP.utf8';
