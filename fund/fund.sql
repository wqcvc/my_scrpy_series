# test
CREATE TABLE fund.student1(
  id INT PRIMARY KEY AUTO_INCREMENT COMMENT '学号',
  name VARCHAR(200) COMMENT '姓名',
  age    int COMMENT '年龄'
) COMMENT='学生信息';
show create table fund.student1;
drop table fund.student1;
alter table fund.student1 modify name VARCHAR(215) COMMENT '姓名';

select * from fund.student1;
INSERT INTO fund.student1(name, age) VALUES ('wq', 28);
DELETE FROM fund.student1 WHERE name='wq';
UPDATE fund.student1 SET age='22' WHERE name='wq';

# fund库
CREATE SCHEMA `fund` ;

select * from fund.funds_use_list limit 10000; where 基金代码=163406;
#drop table fund.funds_use_list;

select * from fund.funds_full_info limit 10000;
#drop table fund.funds_full_inf0;

select * from fund.funds_company_info;



