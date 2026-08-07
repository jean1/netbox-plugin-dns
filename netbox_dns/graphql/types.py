from typing import Annotated

import strawberry
import strawberry_django

from ipam.graphql.types import IPAddressType, PrefixType
from netbox.graphql.scalars import BigInt
from netbox.graphql.types import PrimaryObjectType
from netbox_dns.models import (
    DNSSECKeyTemplate,
    DNSSECPolicy,
    NameServer,
    Record,
    RecordTemplate,
    Registrar,
    RegistrationContact,
    View,
    Zone,
    ZoneTemplate,
)
from tenancy.graphql.types import TenantType

from .filters import (
    NetBoxDNSDNSSECKeyTemplateFilter,
    NetBoxDNSDNSSECPolicyFilter,
    NetBoxDNSNameServerFilter,
    NetBoxDNSRecordFilter,
    NetBoxDNSRecordTemplateFilter,
    NetBoxDNSRegistrarFilter,
    NetBoxDNSRegistrationContactFilter,
    NetBoxDNSViewFilter,
    NetBoxDNSZoneFilter,
    NetBoxDNSZoneTemplateFilter,
)


@strawberry_django.type(
    NameServer,
    fields="__all__",
    filters=NetBoxDNSNameServerFilter,
    pagination=True,
)
class NetBoxDNSNameServerType(PrimaryObjectType):
    name: str
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    soa_zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]


@strawberry_django.type(
    View,
    fields="__all__",
    filters=NetBoxDNSViewFilter,
    pagination=True,
)
class NetBoxDNSViewType(PrimaryObjectType):
    name: str
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    prefixes: list[Annotated["PrefixType", strawberry.lazy("ipam.graphql.types")]]
    ip_address_filter: str | None
    zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]


@strawberry_django.type(
    Zone,
    fields="__all__",
    filters=NetBoxDNSZoneFilter,
    pagination=True,
)
class NetBoxDNSZoneType(PrimaryObjectType):
    name: str
    status: str
    active: bool
    view: Annotated["NetBoxDNSViewType", strawberry.lazy("netbox_dns.graphql.types")]
    nameservers: list[
        Annotated[
            "NetBoxDNSNameServerType", strawberry.lazy("netbox_dns.graphql.types")
        ]
    ]
    default_ttl: BigInt
    soa_ttl: BigInt
    soa_mname: Annotated[
        "NetBoxDNSNameServerType", strawberry.lazy("netbox_dns.graphql.types")
    ]
    soa_rname: str
    soa_serial: BigInt
    soa_refresh: BigInt
    soa_retry: BigInt
    soa_expire: BigInt
    soa_minimum: BigInt
    soa_serial_auto: bool
    dnssec_policy: (
        Annotated[
            "NetBoxDNSDNSSECPolicyType", strawberry.lazy("netbox_dns.graphql.types")
        ]
        | None
    )
    inline_signing: bool | None
    parental_agents: list[str]
    registrar: (
        Annotated["NetBoxDNSRegistrarType", strawberry.lazy("netbox_dns.graphql.types")]
        | None
    )
    registry_domain_id: str | None
    registrant: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )
    admin_c: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )
    tech_c: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )
    billing_c: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )
    rfc2317_prefix: str | None
    rfc2317_parent_managed: str
    rfc2317_parent_zone: (
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
        | None
    )
    records: list[
        Annotated["NetBoxDNSRecordType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    rfc2317_child_zones: list[
        Annotated["NetBoxDNSRecordType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    arpa_network: str | None
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None


@strawberry_django.type(
    Record,
    fields="__all__",
    filters=NetBoxDNSRecordFilter,
    pagination=True,
)
class NetBoxDNSRecordType(PrimaryObjectType):
    name: str
    zone: Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    type: str
    value: str
    absolute_value: str
    status: str
    ttl: BigInt | None
    managed: bool
    ptr_record: (
        Annotated["NetBoxDNSRecordType", strawberry.lazy("netbox_dns.graphql.types")]
        | None
    )
    disable_ptr: bool
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    ip_address: str | None
    ipam_ip_address: (
        Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
    )
    rfc2317_cname_record: (
        Annotated["NetBoxDNSRecordType", strawberry.lazy("netbox_dns.graphql.types")]
        | None
    )
    address_records: list[
        Annotated["NetBoxDNSRecordType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    rfc2317_ptr_records: list[
        Annotated["NetBoxDNSRecordType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    external_rfc2317_zone: (
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
        | None
    )


@strawberry_django.type(
    DNSSECKeyTemplate,
    fields="__all__",
    filters=NetBoxDNSDNSSECKeyTemplateFilter,
    pagination=True,
)
class NetBoxDNSDNSSECKeyTemplateType(PrimaryObjectType):
    name: str
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    type: str
    lifetime: BigInt | None
    algorithm: str
    key_size: BigInt | None


@strawberry_django.type(
    DNSSECPolicy,
    fields="__all__",
    filters=NetBoxDNSDNSSECPolicyFilter,
    pagination=True,
)
class NetBoxDNSDNSSECPolicyType(PrimaryObjectType):
    name: str
    status: str
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    inline_signing: bool
    key_templates: list[
        Annotated[
            "NetBoxDNSDNSSECKeyTemplateType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
    ]
    dnskey_ttl: BigInt | None
    purge_keys: BigInt | None
    publish_safety: BigInt | None
    retire_safety: BigInt | None
    signatures_jitter: BigInt | None
    signatures_refresh: BigInt | None
    signatures_validity: BigInt | None
    signatures_validity_dnskey: BigInt | None
    max_zone_ttl: BigInt | None
    zone_propagation_delay: BigInt | None
    create_cdnskey: bool
    cds_digest_types: list[str]
    parent_ds_ttl: BigInt | None
    parent_propagation_delay: BigInt | None
    use_nsec3: bool
    nsec3_iterations: BigInt | None
    nsec3_opt_out: bool | None
    nsec3_salt_size: BigInt | None


@strawberry_django.type(
    RegistrationContact,
    fields="__all__",
    filters=NetBoxDNSRegistrationContactFilter,
    pagination=True,
)
class NetBoxDNSRegistrationContactType(PrimaryObjectType):
    name: str
    contact_id: str
    organization: str
    street: str
    city: str
    state_province: str
    postal_code: str
    country: str
    phone: str
    phone_ext: str
    fax: str
    fax_ext: str
    email: str
    registrant_zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    admin_c_zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    tech_c_zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]
    billing_c_zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]


@strawberry_django.type(
    Registrar,
    fields="__all__",
    filters=NetBoxDNSRegistrarFilter,
    pagination=True,
)
class NetBoxDNSRegistrarType(PrimaryObjectType):
    name: str
    iana_id: int
    referral_url: str
    whois_server: str
    address: str
    abuse_email: str
    abuse_phone: str
    zones: list[
        Annotated["NetBoxDNSZoneType", strawberry.lazy("netbox_dns.graphql.types")]
    ]


@strawberry_django.type(
    ZoneTemplate,
    fields="__all__",
    filters=NetBoxDNSZoneTemplateFilter,
    pagination=True,
)
class NetBoxDNSZoneTemplateType(PrimaryObjectType):
    name: str
    nameservers: list[
        Annotated[
            "NetBoxDNSNameServerType", strawberry.lazy("netbox_dns.graphql.types")
        ]
    ]
    soa_mname: (
        Annotated[
            "NetBoxDNSNameServerType", strawberry.lazy("netbox_dns.graphql.types")
        ]
        | None
    )
    soa_rname: str | None
    dnssec_policy: (
        Annotated[
            "NetBoxDNSDNSSECPolicyType", strawberry.lazy("netbox_dns.graphql.types")
        ]
        | None
    )
    parental_agents: list[str]
    record_templates: list[
        Annotated[
            "NetBoxDNSRecordTemplateType", strawberry.lazy("netbox_dns.graphql.types")
        ]
    ]
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    registrar: (
        Annotated["NetBoxDNSRegistrarType", strawberry.lazy("netbox_dns.graphql.types")]
        | None
    )
    registrant: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )
    admin_c: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )
    tech_c: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )
    billing_c: (
        Annotated[
            "NetBoxDNSRegistrationContactType",
            strawberry.lazy("netbox_dns.graphql.types"),
        ]
        | None
    )


@strawberry_django.type(
    RecordTemplate,
    fields="__all__",
    filters=NetBoxDNSRecordTemplateFilter,
    pagination=True,
)
class NetBoxDNSRecordTemplateType(PrimaryObjectType):
    name: str
    record_name: str
    type: str
    value: str
    ttl: BigInt | None
    disable_ptr: bool
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    zone_templates: list[
        Annotated[
            "NetBoxDNSZoneTemplateType", strawberry.lazy("netbox_dns.graphql.types")
        ]
    ]
