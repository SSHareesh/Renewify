from django.core.management.base import BaseCommand
from dijkstra.models import SolarInstallationCenter

# Paste your full 30-center JSON list here.
CENTERS_JSON = [
  # === Sriperumbudur ===
  {
    "id": 1,
    "name": "GreenTech Solar Solutions",
    "address": "Plot 12, SIPCOT Industrial Area, Sriperumbudur, Chennai",
    "phone": "9445001122",
    "latitude": 12.9632,
    "longitude": 79.9449
  },
  {
    "id": 2,
    "name": "SunPower Solar Hub",
    "address": "No. 45, Bangalore Highway, Sriperumbudur, Chennai",
    "phone": "9445002233",
    "latitude": 12.9641,
    "longitude": 79.9502
  },
  {
    "id": 3,
    "name": "Solar Future Energy",
    "address": "Industrial Estate, Sriperumbudur, Chennai",
    "phone": "9445003344",
    "latitude": 12.9610,
    "longitude": 79.9400
  },
  {
    "id": 4,
    "name": "EcoLite Solar Systems",
    "address": "NH48, Sriperumbudur Toll Plaza, Chennai",
    "phone": "9445004455",
    "latitude": 12.9672,
    "longitude": 79.9470
  },
  {
    "id": 5,
    "name": "BrightSun Solar Services",
    "address": "Mettu Street, Sriperumbudur, Chennai",
    "phone": "9445005566",
    "latitude": 12.9690,
    "longitude": 79.9435
  },

  # === Poonamallee ===
  {
    "id": 6,
    "name": "Bright Solar Services",
    "address": "Mount Poonamallee Road, Poonamallee, Chennai",
    "phone": "9445101122",
    "latitude": 13.0487,
    "longitude": 80.0945
  },
  {
    "id": 7,
    "name": "EcoSun Solar Tech",
    "address": "No. 17, Main Road, Poonamallee, Chennai",
    "phone": "9445102233",
    "latitude": 13.0500,
    "longitude": 80.1000
  },
  {
    "id": 8,
    "name": "Sunrise Solar Systems",
    "address": "Opp. Bus Stand, Poonamallee, Chennai",
    "phone": "9445103344",
    "latitude": 13.0520,
    "longitude": 80.0970
  },
  {
    "id": 9,
    "name": "SolarWorld Power",
    "address": "Avadi Road, Poonamallee, Chennai",
    "phone": "9445104455",
    "latitude": 13.0540,
    "longitude": 80.0930
  },
  {
    "id": 10,
    "name": "SunEdge Solutions",
    "address": "Karayanchavadi, Poonamallee, Chennai",
    "phone": "9445105566",
    "latitude": 13.0515,
    "longitude": 80.0902
  },

  # === Koyambedu ===
  {
    "id": 11,
    "name": "SolarCare India",
    "address": "No. 9, 100 Feet Road, Koyambedu, Chennai",
    "phone": "9445201122",
    "latitude": 13.0702,
    "longitude": 80.1950
  },
  {
    "id": 12,
    "name": "FutureGreen Solar",
    "address": "Koyambedu Wholesale Market Complex, Chennai",
    "phone": "9445202233",
    "latitude": 13.0725,
    "longitude": 80.2033
  },
  {
    "id": 13,
    "name": "SolarTech Power Solutions",
    "address": "Near CMBT Metro, Koyambedu, Chennai",
    "phone": "9445203344",
    "latitude": 13.0710,
    "longitude": 80.2005
  },
  {
    "id": 14,
    "name": "BrightFuture Solar",
    "address": "100 Feet Ring Road, Koyambedu, Chennai",
    "phone": "9445204455",
    "latitude": 13.0730,
    "longitude": 80.1970
  },
  {
    "id": 15,
    "name": "Sunline Energy",
    "address": "OMR Exit, Koyambedu, Chennai",
    "phone": "9445205566",
    "latitude": 13.0695,
    "longitude": 80.1930
  },

  # === Ambattur ===
  {
    "id": 16,
    "name": "Loom Solar Distributor",
    "address": "62, Ambattur Red Hills Rd, Pudur, Ambattur, Chennai",
    "phone": "9440045678",
    "latitude": 13.1261,
    "longitude": 80.1782
  },
  {
    "id": 17,
    "name": "SolarMax Energy Systems",
    "address": "Ambattur Industrial Estate, Chennai",
    "phone": "9445301122",
    "latitude": 13.1150,
    "longitude": 80.1700
  },
  {
    "id": 18,
    "name": "EcoSolar Ambattur",
    "address": "MTH Road, Ambattur, Chennai",
    "phone": "9445302233",
    "latitude": 13.1185,
    "longitude": 80.1802
  },
  {
    "id": 19,
    "name": "Sunway Solar Systems",
    "address": "Near Ambattur O.T. Bus Stand, Chennai",
    "phone": "9445303344",
    "latitude": 13.1220,
    "longitude": 80.1775
  },
  {
    "id": 20,
    "name": "Bright Energy Solutions",
    "address": "Ambattur Main Road, Chennai",
    "phone": "9445304455",
    "latitude": 13.1200,
    "longitude": 80.1740
  },

  # === Central (Egmore / Park Town) ===
  {
    "id": 21,
    "name": "Central Solar Hub",
    "address": "Egmore High Road, Chennai Central",
    "phone": "9445401122",
    "latitude": 13.0827,
    "longitude": 80.2707
  },
  {
    "id": 22,
    "name": "Bright Future Solar",
    "address": "Opp. Chennai Central Station, Chennai",
    "phone": "9445402233",
    "latitude": 13.0835,
    "longitude": 80.2720
  },
  {
    "id": 23,
    "name": "SolarWay Systems",
    "address": "Park Town, Chennai Central",
    "phone": "9445403344",
    "latitude": 13.0842,
    "longitude": 80.2745
  },
  {
    "id": 24,
    "name": "EcoLight Solar",
    "address": "Near Egmore Railway Station, Chennai",
    "phone": "9445404455",
    "latitude": 13.0785,
    "longitude": 80.2630
  },
  {
    "id": 25,
    "name": "Sunshine Power",
    "address": "Kilpauk High Road, Chennai",
    "phone": "9445405566",
    "latitude": 13.0805,
    "longitude": 80.2590
  },

  # === Parrys Corner ===
  {
    "id": 26,
    "name": "Parrys Corner Solar Solutions",
    "address": "No. 20, NSC Bose Road, Parrys, Chennai",
    "phone": "9445501122",
    "latitude": 13.0925,
    "longitude": 80.2870
  },
  {
    "id": 27,
    "name": "EcoSun Parrys Energy",
    "address": "Broadway, Parrys, Chennai",
    "phone": "9445502233",
    "latitude": 13.0945,
    "longitude": 80.2885
  },
  {
    "id": 28,
    "name": "SunPower Parrys",
    "address": "Opp. High Court Metro, Parrys, Chennai",
    "phone": "9445503344",
    "latitude": 13.0952,
    "longitude": 80.2900
  },
  {
    "id": 29,
    "name": "BrightSolar Trading",
    "address": "Near Parrys Bus Terminus, Chennai",
    "phone": "9445504455",
    "latitude": 13.0932,
    "longitude": 80.2855
  },
  {
    "id": 30,
    "name": "Solar Energy Mart",
    "address": "NSC Bose Road, Chennai",
    "phone": "9445505566",
    "latitude": 13.0910,
    "longitude": 80.2830
  }
]

class Command(BaseCommand):
    help = 'Load hardcoded solar installation centers into database (id mapped to external_id).'

    def handle(self, *args, **options):
        created, updated = 0, 0
        for c in CENTERS_JSON:
            obj, was_created = SolarInstallationCenter.objects.update_or_create(
                external_id=c['id'],
                defaults={
                    'name': c.get('name', ''),
                    'address': c.get('address', ''),
                    'phone': c.get('phone', ''),
                    'latitude': c.get('latitude'),
                    'longitude': c.get('longitude'),
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Load complete — total: {len(CENTERS_JSON)} (created: {created}, updated: {updated})'
        ))
