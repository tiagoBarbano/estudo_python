SELECT id, create_time, arr.item_object->>'name' as Name, 
        arr.item_object->>'price' as Price, 
        arr.item_object->>'productid' as Productid
FROM apolice, jsonb_array_elements(apolice.detalhe)
with ordinality arr(item_object, position) 
WHERE item_object->>'productid' = '1'
ORDER BY id;
                 
select a.id,
a.create_time, 
a.detalhe
from apolice as a
where a.detalhe->>'productid' = '1';


SELECT apolice.detalhe AS apolice_detalhe
FROM apolice
WHERE CAST((apolice.detalhe -> ('productid')) AS TEXT) = '7';

SELECT a.id, a.create_time, arr.position, arr.item_object
FROM apolice as a,
jsonb_array_elements(detalhe) with ordinality arr(item_object, position) 
WHERE id=2;

SELECT arr.item_object
FROM apolice, jsonb_array_elements(detalhe) with ordinality arr(item_object, position) 
WHERE id=2 and arr.position=2;

SELECT arr.item_object
FROM apolice, jsonb_array_elements(detalhe) with ordinality arr(item_object, position) 
WHERE id=2 and arr.position=Cast((select arr.position  FROM apolice, jsonb_array_elements(detalhe) with ordinality arr(item_object, position) 
WHERE id=2 and arr.item_object->>'productid' = '2') as int);


SELECT a.id, a.create_time, arr.item_object, arr.item_object->>'price' as Price
FROM apolice as a,
jsonb_array_elements(detalhe) with ordinality arr(item_object, position) 
WHERE id=2
and arr.item_object->>'price' = Cast((Select max(item_prices.price) as p
FROM apolice, jsonb_to_recordset(apolice.detalhe) as item_prices(price int)
WHERE id=2) as varchar);