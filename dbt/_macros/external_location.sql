{% macro external_location(relation, config) %}
    {%- set bucket = 'prod' if target.name == 'prod' else 'dev' -%}
    {%- set domain = model.fqn[1] -%}
    {%- set layer = {'marts': 'mart', 'intermediate': 'int'}.get(model.fqn[2], model.fqn[2]) -%}
    {%- set fmt = config.get('format', 'parquet') -%}
    {%- set path = 's3://' ~ bucket ~ '/' ~ domain ~ '/' ~ layer ~ '/' ~ relation.identifier ~ '.' ~ fmt -%}
    {{ return(path) }}
{% endmacro %}