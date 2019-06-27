# fastapi-locations

Testing serving GeoJSON using https://github.com/tiangolo/fastapi

Test dataset:  100k records, each with a coordinate location, resembling data from https://apps.nrs.gov.bc.ca/gwells

These endpoints can be explored on your own system using `docker-compose up` and manually adding the following table
(using `docker exec -it fastapi-locations_db /bin/bash`):

```sql
CREATE TABLE well (
  well_tag_number serial primary key,
  geom Geometry(POINT)
);
```

Visit the auto-generated documentation at localhost:8000/docs.

## Methods:

### Psycopg2 and forming GeoJSON using python `geojson` package

  * [locations.py get_wells()](https://github.com/stephenhillier/fastapi-locations/blob/master/locations.py#L25-L56)
  
Time:  ~25 seconds

### returning GeoJSON using PostGIS:

  * [locations.py get_wells_geojson_from_db()](https://github.com/stephenhillier/fastapi-locations/blob/master/locations.py#L59-L118)
  
  Query only time (using explain analyze):  ~3 seconds
