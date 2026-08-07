from django.test import TestCase

from netbox_dns.choices import RecordTypeChoices, ZoneStatusChoices
from netbox_dns.models import NameServer, Record, Zone


class ZoneExternalZoneTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nameserver = NameServer.objects.create(name="ns1.example.com")
        cls.zone_data = {
            "soa_mname": cls.nameserver,
            "soa_rname": "hostmaster.example.com",
        }

        cls.zones = (
            Zone(name="zone1.example.com", **cls.zone_data),
            Zone(name="0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa", **cls.zone_data),
            Zone(name="0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa", **cls.zone_data),
            Zone(name="0.0.10.in-addr.arpa", **cls.zone_data),
            Zone(name="0.10.in-addr.arpa", **cls.zone_data),
        )
        for zone in cls.zones:
            zone.save()

    def test_external_zone_inactive(self):
        zone = self.zones[0]

        self.assertTrue(zone.is_active)

        zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        zone.save()

        self.assertFalse(zone.is_active)

    def test_zone_external_no_ipv6_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[1]
        p_zone = self.zones[2]

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.AAAA,
            value="2001:db8::1",
        )

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

    def test_zone_external_to_active_ipv6_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[1]
        p_zone = self.zones[2]

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.AAAA,
            value="2001:db8::1",
        )

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

        r_zone.status = ZoneStatusChoices.STATUS_ACTIVE
        r_zone.save()

        f_record.refresh_from_db()
        r_record = Record.objects.get(
            zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertEqual(r_record, f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

    def test_zone_active_to_external_no_ipv6_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[1]
        p_zone = self.zones[2]

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.AAAA,
            value="2001:db8::1",
        )

        r_record = Record.objects.get(
            zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertEqual(r_record, f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record.refresh_from_db()

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

    def test_zone_external_to_inactive_ipv6_ptr_in_parent(self):
        f_zone = self.zones[0]
        r_zone = self.zones[1]
        p_zone = self.zones[2]

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.AAAA,
            value="2001:db8::1",
        )

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

        r_zone.status = ZoneStatusChoices.STATUS_RESERVED
        r_zone.save()

        f_record.refresh_from_db()
        r_record = Record.objects.get(
            zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertEqual(r_record, f_record.ptr_record)

    def test_zone_inactive_to_external_no_ipv6_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[1]
        p_zone = self.zones[2]

        r_zone.status = ZoneStatusChoices.STATUS_RESERVED
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.AAAA,
            value="2001:db8::1",
        )

        r_record = Record.objects.get(
            zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertEqual(r_record, f_record.ptr_record)

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record.refresh_from_db()

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

    def test_zone_external_no_ipv4_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[3]
        p_zone = self.zones[4]

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

    def test_zone_external_to_active_ipv4_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[3]
        p_zone = self.zones[4]

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

        r_zone.status = ZoneStatusChoices.STATUS_ACTIVE
        r_zone.save()

        f_record.refresh_from_db()
        r_record = Record.objects.get(
            zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertEqual(r_record, f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

    def test_zone_active_to_external_no_ipv4_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[3]
        p_zone = self.zones[4]

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        r_record = Record.objects.get(
            zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertEqual(r_record, f_record.ptr_record)

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record.refresh_from_db()

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

    def test_zone_external_to_inactive_ipv4_ptr_in_parent(self):
        f_zone = self.zones[0]
        r_zone = self.zones[3]
        p_zone = self.zones[4]

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )

        r_zone.status = ZoneStatusChoices.STATUS_RESERVED
        r_zone.save()

        f_record.refresh_from_db()
        r_record = Record.objects.get(
            zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertEqual(r_record, f_record.ptr_record)

    def test_zone_inactive_to_external_no_ipv4_ptr(self):
        f_zone = self.zones[0]
        r_zone = self.zones[3]
        p_zone = self.zones[4]

        r_zone.status = ZoneStatusChoices.STATUS_RESERVED
        r_zone.save()

        f_record = Record.objects.create(
            name="test1",
            zone=f_zone,
            type=RecordTypeChoices.A,
            value="10.0.0.1",
        )

        r_record = Record.objects.get(
            zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
        )

        self.assertIsNotNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertEqual(r_record, f_record.ptr_record)

        r_zone.status = ZoneStatusChoices.STATUS_EXTERNAL
        r_zone.save()

        f_record.refresh_from_db()

        self.assertIsNone(f_record.ptr_record)
        self.assertIsNone(
            Record.objects.filter(
                zone=r_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
        self.assertIsNone(
            Record.objects.filter(
                zone=p_zone, value=f_record.fqdn, type=RecordTypeChoices.PTR
            ).first()
        )
