from django.test import TestCase
from dns import name as dns_name

from netbox_dns.choices import RecordTypeChoices, ZoneStatusChoices
from netbox_dns.models import NameServer, Record, Zone


class RFC2317ExternalZoneTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.zone_data = {
            "soa_mname": NameServer.objects.create(name="ns1.example.com"),
            "soa_rname": "hostmaster.example.com",
        }

        cls.zones = (
            Zone(name="zone1.example.com", **cls.zone_data),
            Zone(name="0.0.10.in-addr.arpa", **cls.zone_data),
        )
        for zone in cls.zones:
            zone.save()

    def test_external_rfc2317_zone_25_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-127.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/25",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            128,
        )

    def test_external_rfc2317_zone_26_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-63.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/26",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            64,
        )

    def test_external_rfc2317_zone_27_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            32,
        )

    def test_external_rfc2317_zone_28_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-15.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/28",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            16,
        )

    def test_external_rfc2317_zone_29_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-7.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/29",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            8,
        )

    def test_external_rfc2317_zone_30_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-3.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/30",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            4,
        )

    def test_external_rfc2317_zone_31_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-1.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/31",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            2,
        )

    def test_external_rfc2317_zone_32_bit(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/32",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            1,
        )

    def test_delete_external_rfc2317_zone_remove_cnames(self):
        p_zone = self.zones[1]

        rfc2317_zone = Zone.objects.create(
            name="0-15.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/28",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
                external_rfc2317_zone=rfc2317_zone,
            ).count(),
            16,
        )

        rfc2317_zone.delete()

        self.assertEqual(
            Record.objects.filter(
                zone=p_zone,
                type=RecordTypeChoices.CNAME,
            ).count(),
            0,
        )

    def test_external_rfc2317_zone_no_ptr(self):
        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )
        f_record = Record.objects.create(
            name="test1",
            zone=self.zones[0],
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        self.assertIsNone(f_record.ptr_record)
        self.assertFalse(
            rfc2317_zone.records.filter(type=RecordTypeChoices.PTR).exists()
        )
        self.assertFalse(
            Record.objects.filter(type=RecordTypeChoices.PTR, zone=rfc2317_zone)
            .exclude(address_records__in=[f_record])
            .exists()
        )

    def test_external_rfc2317_zone_static_cname(self):
        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )
        f_record = Record.objects.create(
            name="test1",
            zone=self.zones[0],
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        cname_record = Record.objects.filter(
            zone=self.zones[1], fqdn=f_record.ip_address.reverse_dns
        ).first()
        self.assertIsNotNone(cname_record)
        self.assertEqual(cname_record.external_rfc2317_zone, rfc2317_zone)
        self.assertTrue(
            dns_name.from_text(cname_record.value).is_subdomain(
                dns_name.from_text(rfc2317_zone.fqdn)
            )
        )

    def test_active_rfc2317_zone_ptr(self):
        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )
        f_record = Record.objects.create(
            name="test1",
            zone=self.zones[0],
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        self.assertIsNone(f_record.ptr_record)

        rfc2317_zone.status = ZoneStatusChoices.STATUS_ACTIVE
        rfc2317_zone.save()

        f_record.refresh_from_db()
        r_record = Record.objects.get(type=RecordTypeChoices.PTR, value=f_record.fqdn)

        self.assertEqual(f_record.ptr_record, r_record)
        self.assertIn(f_record, f_record.ptr_record.address_records.all())

        self.assertEqual(r_record.rfc2317_cname_record.value, r_record.fqdn)

    def test_change_external_rfc2317_zone_to_active_ptr(self):
        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )
        f_record = Record.objects.create(
            name="test1",
            zone=self.zones[0],
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        self.assertIsNone(f_record.ptr_record)

        rfc2317_zone.status = ZoneStatusChoices.STATUS_ACTIVE
        rfc2317_zone.save()

        f_record.refresh_from_db()
        r_record = Record.objects.get(type=RecordTypeChoices.PTR, value=f_record.fqdn)

        self.assertEqual(f_record.ptr_record, r_record)
        self.assertIn(f_record, f_record.ptr_record.address_records.all())

    def test_change_external_rfc2317_zone_to_active_dynamic_cname(self):
        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_EXTERNAL,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )
        f_record = Record.objects.create(
            name="test1",
            zone=self.zones[0],
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        rfc2317_zone.status = ZoneStatusChoices.STATUS_ACTIVE
        rfc2317_zone.save()

        f_record.refresh_from_db()
        cname_record = Record.objects.filter(
            zone=self.zones[1], fqdn=f_record.ip_address.reverse_dns
        ).first()
        self.assertEqual(f_record.ptr_record.rfc2317_cname_record, cname_record)
        self.assertIn(f_record.ptr_record, cname_record.rfc2317_ptr_records.all())

    def test_change_active_rfc2317_zone_to_external_no_ptr(self):
        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_ACTIVE,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )
        f_record = Record.objects.create(
            name="test1",
            zone=self.zones[0],
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        cname_record = Record.objects.filter(
            zone=self.zones[1], fqdn=f_record.ip_address.reverse_dns
        ).first()
        self.assertEqual(f_record.ptr_record.rfc2317_cname_record, cname_record)
        self.assertIn(f_record.ptr_record, cname_record.rfc2317_ptr_records.all())

        rfc2317_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        rfc2317_zone.save()

        f_record.refresh_from_db()
        r_record = Record.objects.filter(
            type=RecordTypeChoices.PTR, value=f_record.fqdn
        ).first()

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(r_record)

    def test_change_active_rfc2317_zone_to_external_static_cname(self):
        rfc2317_zone = Zone.objects.create(
            name="0-31.0.0.10.in-addr.arpa",
            status=ZoneStatusChoices.STATUS_ACTIVE,
            rfc2317_prefix="10.0.0.0/27",
            rfc2317_parent_managed=True,
            **self.zone_data,
        )
        f_record = Record.objects.create(
            name="test1",
            zone=self.zones[0],
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        rfc2317_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        rfc2317_zone.save()

        f_record.refresh_from_db()
        cname_record = Record.objects.filter(
            zone=self.zones[1], fqdn=f_record.ip_address.reverse_dns
        ).first()

        self.assertIsNone(f_record.ptr_record)
        self.assertEqual(cname_record.external_rfc2317_zone, rfc2317_zone)
        self.assertFalse(cname_record.rfc2317_ptr_records.exists())
