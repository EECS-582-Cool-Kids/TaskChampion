"""
 *  Module Name: task.py
 *  Purpose: Module for the Task class, which is a class for creating a task object.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley
 *  Date: 2/15/2025
 *  Last Modified: 2/15/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""
from taskw_ng import task, fields
from typing import TypeAlias, Literal, cast

status_t: TypeAlias = Literal['pending', 'completed', 'deleted', 'waiting', 'recurring']
priority_t: TypeAlias = Literal['H', 'M', 'L'] | None

class Task(task.Task):
    def get_annotations(self) -> fields.AnnotationArrayField:
        return self['annotations']

    def get_depends(self) -> fields.CommaSeparatedUUIDField: 
        return self['depends']

    def get_description(self) -> fields.StringField:
        return self['description']

    def get_due(self) -> fields.DateField: 
        return self['due']

    def get_end(self) -> fields.DateField:
        return self['end']

    def get_entry(self)-> fields.DateField:
        return self['entry']

    def get_id(self) -> fields.NumericField:
        return self['id']

    def get_imask(self) -> fields.NumericField:
        return self['imask']

    def get_mask(self) -> fields.StringField:
        return self['mask']

    def get_modified(self) -> fields.DateField:
        return self['modified']

    def get_parent(self) -> fields.StringField:
        return self['parent']

    def get_priority(self) -> priority_t:
        return cast(priority_t, str(self['priority']))

    def get_project(self) -> fields.StringField:
        return self['project']

    def get_recur(self) -> fields.StringField:
        return self['recur']

    def get_scheduled(self) -> fields.DateField:
        return self['scheduled']

    def get_start(self) -> fields.DateField:
        return self['start']

    def get_status(self) -> status_t:
        return cast(status_t, str(self['status']))

    def get_tags(self) -> fields.ArrayField:
        return self['tags']

    def get_until(self) -> fields.DateField:
        return self['until']

    def get_urgency(self) -> fields.NumericField:
        return self['urgency']

    def get_uuid(self) -> fields.UUIDField:
        return self['uuid']

    def get_wait(self) -> fields.DateField:
        return self['wait']
    
    

