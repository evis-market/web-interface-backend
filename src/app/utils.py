def copy_instance(instance, instance_copy, exclude_fields=None):  # noqa: CCR001
    """
    Duplicate a model instance  into the other model instance, making copies of all foreign keys pointing to it.
    There are 3 steps that need to occur in order:

        1.  Enumerate the related child objects and m2m relations, saving in lists/dicts
        2.  Copy the parent object per django docs (doesn't copy relations)
        3a. Copy the child objects, relating to the copied parent object
        3b. Re-create the m2m relations on the copied parent object

    """

    fields_to_copy = {}
    related_objects_to_copy = []
    relations_to_set = {}
    # Iterate through all the fields in the parent object looking for related fields
    for field in instance._meta.get_fields():
        # Do not process the fields marked as excluded
        if exclude_fields and hasattr(field, 'attname') and field.attname in exclude_fields:
            continue

        # One to many field processing disabled
        if field.one_to_many:
            continue

        elif field.many_to_many:
            # Many to many fields are relationships where many parent objects
            # can be related to many child objects. Because of this the child
            # objects don't need to be copied when we copy the parent, we just
            # need to re-create the relationship to them on the copied parent.
            related_object_manager = getattr(instance, field.name)
            relations = list(related_object_manager.all())
            if relations:
                relations_to_set[field.name] = relations
        else:
            fields_to_copy[field.attname] = getattr(instance, field.attname)

    # Set values for the regular fields and foreign keys
    for field, value in fields_to_copy.items():
        setattr(instance_copy, field, value)

    # Save object before appending one_to_many and many_to_many relationships
    instance_copy.save()

    # Set the one-to-many objects and relate them to the copied object
    for related_object in related_objects_to_copy:
        # Iterate through the fields in the related object to find the one that
        # relates to the parent model.
        for related_object_field in related_object._meta.fields:
            if related_object_field.related_model == instance.__class__:
                # If the related_model on this field matches the parent
                # object's class, perform the copy of the child object and set
                # this field to the parent object, creating the new
                # child -> parent relationship.
                related_object.pk = None
                setattr(related_object, related_object_field.name, instance_copy)
                related_object.save()

                text = str(related_object)
                text = (text[:40] + '..') if len(text) > 40 else text

    # Set the many-to-many relations on the copied instance
    for field_name, relations in relations_to_set.items():
        # Get the field by name and set the relations, creating the new relationships
        field = getattr(instance_copy, field_name)
        field.set(relations)

        text_relations = []
        for relation in relations:
            text_relations.append(str(relation))

    return instance_copy


def copy_instance_fields(instance, fields_to_copy, destination_instance):
    for field in fields_to_copy:
        setattr(destination_instance, field, getattr(instance, field))
