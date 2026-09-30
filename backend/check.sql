.headers on
.mode column
.tables
SELECT incident_id, location_name, priority_score, priority_level, status FROM incidents;
SELECT resource_id, name, resource_type, capacity, status FROM resources;
SELECT assignment_id, incident_id, resource_id, approval_status FROM assignments;
