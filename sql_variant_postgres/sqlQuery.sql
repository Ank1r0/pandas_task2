WITH RECURSIVE bom_chain AS (

    SELECT
        mp.plant_id,
        mp.year,
        mp.month,
        mp.produced_material                   AS fin_material_id,
        0                                      AS depth,
        mp.produced_material,
        mp.produced_material_release_type,
        mp.produced_material_production_type,
        mp.produced_material_quantity,
        mp.component_material,
        mp.component_material_release_type,
        mp.component_material_production_type,
        mp.component_material_quantity,
        ARRAY[mp.produced_material]            AS visited
    FROM material_production mp
    WHERE mp.produced_material_release_type = 'FIN'

    UNION ALL

    SELECT
        bom.plant_id,
        bom.year,
        mp.month,
        bom.fin_material_id,
        bom.depth + 1,
        mp.produced_material,
        mp.produced_material_release_type,
        mp.produced_material_production_type,
        mp.produced_material_quantity,
        mp.component_material,
        mp.component_material_release_type,
        mp.component_material_production_type,
        mp.component_material_quantity,
        bom.visited || mp.produced_material
    FROM material_production mp
    JOIN bom_chain bom
        ON  mp.plant_id          = bom.plant_id
        AND mp.year              = bom.year
        AND mp.month             = bom.month
        AND mp.produced_material = bom.component_material
    WHERE mp.produced_material_release_type <> 'FIN'
      AND mp.produced_material <> ALL(bom.visited)
)

SELECT
    plant_id                           AS plant,
    year,
    month,
    fin_material_id,
    depth,
    produced_material                  AS material,
    produced_material_release_type     AS release_type,
    produced_material_production_type  AS production_type,
    produced_material_quantity         AS production_quantity,
    component_material                 AS component,
    component_material_release_type    AS component_release_type,
    component_material_production_type AS component_production_type,
    component_material_quantity        AS component_quantity
FROM bom_chain
ORDER BY plant_id, year, month, fin_material_id, depth,
         component_material_release_type DESC, component_material;