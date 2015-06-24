from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import FieldError

def object_relation_mixin_factory(
    prefix=None,
    prefix_verbose=None,
    add_related_name=False,
    limit_content_type_choices_to={},
    limit_object_choices_to={},
    is_required=False,
    ):
    """
    """
    if prefix:
        p = "%s_" % prefix
    else:
        p = ""

    content_type_field = "%scontent_type" %p
    object_id_field = "%sobject_id" % p
    content_object_field = "%scontent_object" % p

    class AClass(models.Model):
        class Meta:
            abstract = True

    if add_related_name:
        if not prefix:
            raise FieldError("if add_related_name is set to True," "a prefix must be given")
        related_name = prefix
    else:
        related_name = None

    content_type = models.ForeignKey(
        ContentType,
        verbose_name = (prefix_verbose and _("%s's type (model)") %\
                        prefix_verbose or _("Related object's type (model)")),
        related_name=related_name,
        blank=not is_required,
        null=not is_required,
        help_text=_("Please select the type (model) for the relation," "you want to build."),
        limit_choices_to=limit_content_type_choices_to,
    )

    object_id = models.CharField(
        (prefix_verbose or _("Related object")),
        blank=not is_required,
        null=False,
        help_text=_("Please enter the ID of the related object."),
        max_length=255,
        default="",
    )

    object_id.limit_choices_to = limit_object_choices_to

    content_object = generic.GenericForeignKey(
        ct_field=content_type_field,
        fk_field=object_id_field,
    )

    AClass.add_to_class(content_type_field, content_type)
    AClass.add_to_class(object_id_field, object_id)
    AClass.add_to_class(content_object_field, content_object)

    return AClass

