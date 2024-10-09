--
--  JVN Vulnerability Infomation Managed System
--
--  hidekuno@gmail.com
--

-- ========================================================================
-- オブジェクトのクリア
-- ========================================================================
DROP TABLE IF EXISTS jvn_vendor;
DROP TABLE IF EXISTS jvn_vendor_work;
DROP TABLE IF EXISTS jvn_product;
DROP TABLE IF EXISTS jvn_product_work;
DROP TABLE IF EXISTS jvn_vulnerability;
DROP TABLE IF EXISTS jvn_vulnerability_detail;
DROP TABLE IF EXISTS jvn_vulnerability_work;
DROP TABLE IF EXISTS jvn_vulnerability_detail_work;
DROP TABLE IF EXISTS jvn_account;
DROP TABLE IF EXISTS jvn_mainte_work;
DROP TABLE IF EXISTS jvn_cwe_work;
DROP TABLE IF EXISTS jvn_nvd;
DROP TABLE IF EXISTS jvn_nvd_work;

DROP INDEX IF EXISTS jvn_vendor_idx_1;
DROP INDEX IF EXISTS jvn_product_idx_1;
DROP INDEX IF EXISTS jvn_product_idx_2;
DROP INDEX IF EXISTS jvn_vulnerability_idx_1;
DROP INDEX IF EXISTS jvn_vulnerability_detail_idx_1;
DROP INDEX IF EXISTS jvn_vulnerability_detail_idx_2;
-- ========================================================================
-- Quattro テーブル作成(マスタ及びトランザクション系)
-- ========================================================================
-- ---------------------  ベンダ情報 -------------------------
CREATE TABLE    jvn_vendor (
  vid           int          NOT NULL,
  vname         text         NOT NULL,
  cpe           varchar(255) NOT NULL
);
CREATE TABLE    jvn_vendor_work (
  vid           int          NOT NULL,
  vname         text         NOT NULL,
  cpe           varchar(255) NOT NULL
);
-- ---------------------  製品情報 -------------------------
CREATE TABLE jvn_product (
  pid           int          NOT NULL,
  pname         text         NOT NULL,
  cpe           varchar(255) NOT NULL,
  vid           int          NOT NULL,
  fs_manage     varchar(16)  NOT NULL,
  edit          smallint
);
-- ---------------------  製品情報(ワークテーブル) ---------
CREATE TABLE jvn_product_work (
  pid           int,
  pname         text,
  cpe           varchar(255),
  vid           int
);

-- --------------------- 脆弱性情報 -------------------------
CREATE TABLE jvn_vulnerability (
  identifier    varchar(32)      NOT NULL PRIMARY KEY,
  title         text             NOT NULL,
  link          varchar(255)     NOT NULL,
  description   text             NOT NULL,
  issued_date   timestamp        NOT NULL,
  modified_date timestamp        NOT NULL,
  public_date   timestamp,
  cweid         varchar(32),
  cwetitle      text,
  ticket_modified_date timestamp
);
-- --------------------- 脆弱性情報(ワークテーブル) --------
CREATE TABLE jvn_vulnerability_work (
  identifier    varchar(32),
  title         text,
  link          varchar(255),
  description   text,
  issued_date   timestamp,
  modified_date timestamp
);

-- --------------------- 脆弱性情報詳細 --------------------
CREATE TABLE jvn_vulnerability_detail (
  identifier    varchar(32)     NOT NULL,
  cpe           varchar(255)    NOT NULL
);
-- --------------------- 脆弱性情報詳細(ワークテーブル) ---
CREATE TABLE jvn_vulnerability_detail_work (
  identifier    varchar(32),
  cpe           varchar(255)
);
-- --------------------- 脆弱性情報詳細(ワークテーブル) ---
CREATE TABLE jvn_mainte_work (
  identifier    varchar(32)      NOT NULL PRIMARY KEY,
  public_date   timestamp
);

-- --------------------- 脆弱性情報(ワークテーブル) --------
CREATE TABLE jvn_cwe_work (
  identifier    varchar(32),
  cweid         varchar(32),
  cwetitle      text
);
-- --------------------- NVD脆弱性情報 --------
CREATE TABLE jvn_nvd (
  identifier    varchar(32),
  cve           varchar(16),
  url           text
);
-- --------------------- NVD脆弱性情報(ワークテーブル) --------
CREATE TABLE jvn_nvd_work (
  identifier    varchar(32),
  cve           varchar(16),
  url           text
);
-- --------------------- アカウント情報 --------------------
CREATE TABLE jvn_account (
  user_id       varchar(32)    NOT NULL PRIMARY KEY,
  passwd        varchar(64),
  user_name     varchar(255),
  email         varchar(255),
  department    varchar(32),
  privs         varchar(8)
);

CREATE INDEX jvn_vendor_idx_1               ON jvn_vendor  (vid);
CREATE INDEX jvn_vendor_idx_2               ON jvn_vendor  (cpe);
CREATE INDEX jvn_product_idx_1              ON jvn_product (pid);
CREATE INDEX jvn_product_idx_2              ON jvn_product (cpe);
CREATE INDEX jvn_vulnerability_idx_1        ON jvn_vulnerability (modified_date);
CREATE INDEX jvn_vulnerability_idx_2 ON jvn_vulnerability(title text_pattern_ops);
CREATE INDEX jvn_vulnerability_detail_idx_1 ON jvn_vulnerability_detail (identifier);
CREATE INDEX jvn_vulnerability_detail_idx_2 ON jvn_vulnerability_detail (cpe);

truncate table jvn_account;
insert into jvn_account values
('admin','$2a$10$gWXneYLpHDjD239d5z/1ceaEiW5I1R3i3ZoBRVnoQ3HkK.xRJDHWW', 'あどみん','testtaro@gmail.com','開発部','admin'),
('guest' ,'$2a$10$WAcEDcJI5HQq8SiLj266BOoVtRF88U8/AI1nsugW3pXjnnnym433S', 'ゆーざー','testtaro@gmail.com','開発部','user');
