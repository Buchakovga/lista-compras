

with tb_leg as (
    select 
        * ,
        lag(dt_compra) over (PARTITION BY produto order by dt_compra )  as dt_anterior
    from
        compras 

    order by produto, dt_compra
), tb_media as (
    select 
        produto,
        avg(julianday(dt_compra) - julianday(dt_anterior)) as Dif_Dias

    from 
        tb_leg 
    group by produto 
), tb_stats_produto as (

select 
    produto,
    max(dt_compra) as dt_ult_compra,
    avg(valor_produto) as valor_media_produto
    
from 
    compras

group by produto 

)
select 
    a.* ,
    b.Dif_Dias,
    julianday('now') - julianday(a.dt_ult_compra) as dias_ultima_compra
from 
    tb_stats_produto a 

    left join tb_media b 
        on a.produto = b.produto
    
