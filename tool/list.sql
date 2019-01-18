select 'root';
select 'root|' || vname
from jvn_vendor  v
order by v.vid;
select 'root|' || vname || '|' || pname
from jvn_vendor  v,
     jvn_product p
where v.vid = p.vid
order by v.vid,p.pid;
select 'root|' || vname || '|' || pname ||'|' || identifier
from jvn_vendor  v,
     jvn_product p,
     jvn_vulnerability_detail d
where v.vid = p.vid
and   p.cpe = d.cpe
order by v.vid,p.pid,d.identifier;
