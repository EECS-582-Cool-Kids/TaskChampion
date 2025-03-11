""" Prologue
 *  Module Name: task.py
 *  Purpose: Module for the Task class, which is a class for creating a task object.
 *  Inputs: None
 *  Outputs: None
 *  Additional code sources: None
 *  Developers: Ethan Berkley, Mo Morgan, Jacob Wilkus
 *  Date: 2/15/2025
 *  Last Modified: 2/25/2025
 *  Preconditions: None
 *  Postconditions: None
 *  Error/Exception conditions: None
 *  Side effects: None
 *  Invariants: None
 *  Known Faults: None encountered
"""

from taskw_ng import task, fields
from typing import TypeAlias, Literal, cast

# creating type aliases for the status and priority fields
status_t: TypeAlias = Literal['pending', 'completed', 'deleted', 'waiting', 'recurring'] | None
priority_t: TypeAlias = Literal['H', 'M', 'L'] | None

class Task(task.Task):
    def get_annotations(self) -> fields.AnnotationArrayField:
        return self['annotations']  # Return the annotations field.

    def get_depends(self) -> fields.CommaSeparatedUUIDField:
        return self['depends']  # Return the depends field.

    def get_description(self) -> fields.StringField:
        return self['description']  # Return the description field.

    def get_due(self) -> fields.DateField:
        if 'due' not in self:  # If the due field does not exist
            return None  # Return None
        else:  # If the due field exists
            return self['due']  # Return the due field.
    
    def set_due(self, due : str) -> None:
        self.set('due', due)  # Set the due field to the given due date.

    def get_end(self) -> fields.DateField:
        return self['end']  # Return the end field.

    def get_entry(self)-> fields.DateField:
        return self['entry']  # Return the entry field.

    def get_id(self) -> fields.NumericField:
        return self['id']  # Return the id field.

    def get_imask(self) -> fields.NumericField:
        return self['imask']  # Return the imask field.

    def get_mask(self) -> fields.StringField:
        return self['mask']  # Return the mask field.

    def get_modified(self) -> fields.DateField:
        return self['modified']  # Return the modified field.

    def get_parent(self) -> fields.StringField:
        return self['parent']  # Return the parent field.

    def get_priority(self) -> priority_t:
        try:  # Try to return the priority field.
            return cast(priority_t, str(self['priority']))  # Return the priority field.
        except KeyError:  # If the priority field does not exist
            return None  # Return None
        # return cast(priority_t, str(self['priority']))  # Return the priority field.
    
    def set_priority(self, priority : str) -> None:
        self.set("priority", priority)  # Set the priority field to the given priority.

    def _has_project(self) -> bool:  # Check if the project field exists.
        return 'project' in self

    def get_project(self) -> fields.StringField | None: 
        return self['project'] if self._has_project() else None  # Return the project field.

    def set_project(self, project : str) -> None:
        self.set("project", project)  # Set the project field to the given project.

    def get_recur(self) -> fields.StringField:
        return self['recur']  # Return the recur field.

    def set_recur(self, recur : str) -> None:
        self.set("recur", recur)  # Set the recur field to the given recurrence.

    def get_scheduled(self) -> fields.DateField:
        return self['scheduled']  # Return the scheduled field.

    def get_start(self) -> fields.DateField:
        return self['start']  # Return the start field.

    def get_status(self) -> status_t:  # Get the status of the task.
        return cast(status_t, str(self['status']))  # Return the status field.

    def _has_tags(self) -> bool:  # Check if the tags field exists.
        return 'tags' in self

    def get_tags(self) -> fields.ArrayField | None:
        return self['tags'] if self._has_tags() else None # Return the tags field.

    def get_until(self) -> fields.DateField:
        return self['until']  # Return the until field.

    def get_urgency(self) -> fields.NumericField:
        return self['urgency']  # Return the urgency field.

    def get_uuid(self) -> fields.UUIDField:
        return self['uuid']  # Return the uuid field.

    def get_wait(self) -> fields.DateField:
        return self['wait']  # Return the wait field.
    
    

