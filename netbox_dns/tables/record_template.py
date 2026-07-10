import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import (
    ActionsColumn,
    BooleanColumn,
    PrimaryModelTable,
    TagColumn,
    TemplateColumn,
)
from netbox_dns.models import RecordTemplate
from netbox_dns.utilities import value_to_unicode
from tenancy.tables import TenancyColumnsMixin

__all__ = (
    "RecordTemplateTable",
    "RecordTemplateDisplayTable",
)


class RecordTemplateTable(TenancyColumnsMixin, PrimaryModelTable):
    class Meta(PrimaryModelTable.Meta):
        model = RecordTemplate

        fields = (
            "status",
            "description",
        )

        default_columns = (
            "name",
            "record_name",
            "ttl",
            "type",
            "value",
            "tags",
        )

    name = tables.Column(
        verbose_name=_("Name"),
        linkify=True,
    )
    record_name = tables.Column(
        verbose_name=_("Record Name"),
    )
    type = tables.Column(
        verbose_name=_("Type"),
    )
    value = TemplateColumn(
        verbose_name=_("Value"),
        template_code="""
            <span title="{{ value }}">
               {{ value|truncatechars:48 }}
            </span>
        """,
    )
    unicode_value = TemplateColumn(
        verbose_name=_("Unicode Value"),
        template_code="""
            <span title="{{ value }}">
               {{ value|truncatechars:48 }}
            </span>
        """,
        accessor="value",
    )
    ttl = tables.Column(
        verbose_name=_("TTL"),
    )
    disable_ptr = BooleanColumn(
        verbose_name=_("Disable PTR"),
    )
    tags = TagColumn(
        url_name="plugins:netbox_dns:recordtemplate_list",
    )

    def render_unicode_value(self, value):
        return value_to_unicode(value)


class RecordTemplateDisplayTable(RecordTemplateTable):
    class Meta(PrimaryModelTable.Meta):
        model = RecordTemplate

        fields = (
            "status",
            "description",
        )

        default_columns = (
            "name",
            "record_name",
            "ttl",
            "type",
            "value",
        )

    actions = ActionsColumn(actions="")
