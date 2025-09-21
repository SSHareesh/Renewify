import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:location/location.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'map_page.dart';
import 'dashboard.dart';
import 'solarservices.dart';
import 'complaint.dart';
import 'shop.dart';
import 'subsidies.dart';
import 'monitoring.dart';

class SolarCenters extends StatefulWidget {
  const SolarCenters({Key? key}) : super(key: key);

  @override
  State<SolarCenters> createState() => _SolarCentersState();
}

class _SolarCentersState extends State<SolarCenters> {
  List<Map<String, dynamic>> nearbyShops = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchNearestShops();
  }

Future<void> _fetchNearestShops() async {
  try {
    Location location = Location();

    // Request service & permissions
    bool serviceEnabled = await location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await location.requestService();
      if (!serviceEnabled) throw 'Location service disabled';
    }

    PermissionStatus permissionGranted = await location.hasPermission();
    if (permissionGranted == PermissionStatus.denied) {
      permissionGranted = await location.requestPermission();
      if (permissionGranted != PermissionStatus.granted) throw 'Location permission denied';
    }

    // Get current location
    LocationData locationData = await location.getLocation();
    double? lat = locationData.latitude;
    double? lng = locationData.longitude;
    if (lat == null || lng == null) throw 'Could not get location';

    // Send location to Django server
    const String serverUrl = 'https://90da77df8790.ngrok-free.app/api/nearest-centers/';
    final response = await http.post(
      Uri.parse(serverUrl),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'latitude': lat, 'longitude': lng}),
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);

      setState(() {
        // Only take the 'nearest' list
        nearbyShops = List<Map<String, dynamic>>.from(data['nearest']);
        isLoading = false;
      });
    } else {
      throw 'Server error: ${response.statusCode}';
    }
  } catch (e) {
    setState(() => isLoading = false);
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text('Error fetching shops: $e')));
    print('Error fetching nearest shops: $e');
  }
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green.shade300,
        title: const Text('Contact Solar Centers'),
        actions: [IconButton(icon: const Icon(Icons.person), onPressed: () {})],
      ),
      drawer: _buildDrawer(context),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : nearbyShops.isEmpty
              ? const Center(child: Text('No nearby solar centers found'))
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: nearbyShops.length,
                  itemBuilder: (context, index) {
                    final shop = nearbyShops[index];
                    return _buildContactCenter(
  shop['name'] ?? '',
  shop['address'] ?? '',
  shop['phone'] ?? '',
  (shop['latitude'] as num?)?.toDouble() ?? 0.0,
  (shop['longitude'] as num?)?.toDouble() ?? 0.0,
  context,
);

                  },
                ),
    );
  }

  Drawer _buildDrawer(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(color: Colors.green),
            child: Text('RENEWIFY', style: TextStyle(color: Colors.white, fontSize: 24)),
          ),
          ListTile(
            leading: const Icon(Icons.home),
            title: const Text('Home'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const Dashboard())),
          ),
          ListTile(
            leading: const Icon(Icons.wb_sunny),
            title: const Text('Solar'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SolarServices())),
          ),
          ListTile(
            leading: const Icon(Icons.attach_money),
            title: const Text('Subsidies/Loans'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SubsidiesPage())),
          ),
          ListTile(
            leading: const Icon(Icons.warning_rounded),
            title: const Text('Complaints'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ComplaintPage())),
          ),
          ListTile(
            leading: const Icon(Icons.electric_bolt),
            title: const Text('Electricity'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => SolarElectricityMonitoringPage())),
          ),
          ListTile(
            leading: const Icon(Icons.shopping_cart),
            title: const Text('Energy Market'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ShopPage())),
          ),
        ],
      ),
    );
  }

  // Updated contact card with Map, Phone, and Book button
  Widget _buildContactCenter(String name, String address, String phone, double latitude, double longitude, BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 12.0),
      padding: const EdgeInsets.all(12.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        boxShadow: const [
          BoxShadow(color: Colors.black26, blurRadius: 4, offset: Offset(2, 2)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(name, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 6),
          Text(address),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              // Phone icon
              IconButton(
                icon: const Icon(Icons.phone, color: Colors.green),
                onPressed: () => _launchUrl('tel:$phone'),
                tooltip: phone,
              ),
              // Map icon
              IconButton(
                icon: const Icon(Icons.location_on, color: Colors.green),
                onPressed: () => _launchMap(latitude, longitude),
                tooltip: 'Navigate to $name',
              ),
              // Book button
              ElevatedButton(
                onPressed: () => _showBookingDialog(context, name, address),
                style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                child: const Text('Book'),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // Launch Google Maps or OSM
 Future<void> _launchMap(double latitude, double longitude) async {
  final Uri googleMapsUri = Uri.parse(
      'https://www.google.com/maps/dir/?api=1&destination=$latitude,$longitude');
  final Uri osmUri = Uri.parse(
      'https://www.openstreetmap.org/?mlat=$latitude&mlon=$longitude&zoom=16');

  if (await canLaunchUrl(googleMapsUri)) {
    await launchUrl(googleMapsUri, mode: LaunchMode.externalApplication);
  } else if (await canLaunchUrl(osmUri)) {
    await launchUrl(osmUri, mode: LaunchMode.externalApplication);
  } else {
    ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Could not launch map for coordinates.')));
  }
}


  Future<void> _launchUrl(String url) async {
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }
}

// Booking dialog unchanged
void _showBookingDialog(BuildContext context, String name, String address) {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      TextEditingController nameController = TextEditingController();
      TextEditingController phoneController = TextEditingController();

      return AlertDialog(
        title: const Text('Booking Form'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: nameController,
              decoration: const InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: phoneController,
              decoration: const InputDecoration(labelText: 'Phone Number'),
              keyboardType: TextInputType.phone,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () async {
              String nameInput = nameController.text;
              String phone = phoneController.text;

              if (nameInput.isNotEmpty && phone.isNotEmpty) {
                await _sendDataToServer(context, nameInput, phone);
                Navigator.of(context).pop();
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Please fill in all fields')),
                );
              }
            },
            child: const Text('Submit'),
          ),
        ],
      );
    },
  );
}

Future<void> _sendDataToServer(BuildContext context, String name, String phone) async {
  try {
    Location location = Location();

    bool serviceEnabled = await location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await location.requestService();
      if (!serviceEnabled) throw 'Location services are disabled.';
    }

    PermissionStatus permissionGranted = await location.hasPermission();
    if (permissionGranted == PermissionStatus.denied) {
      permissionGranted = await location.requestPermission();
      if (permissionGranted != PermissionStatus.granted) throw 'Location permission is denied.';
    }

    LocationData locationData = await location.getLocation();
    double? latitude = locationData.latitude;
    double? longitude = locationData.longitude;

    if (latitude == null || longitude == null) throw 'Unable to fetch location coordinates.';

    final locationUrl = 'https://maps.google.com/?q=$latitude,$longitude';
    Map<String, dynamic> requestData = {
      'name': name,
      'phone': phone,
      'location': locationUrl,
    };

    const String serverUrl = 'http://192.168.29.45:8000/request_installation';
    final response = await http.post(
      Uri.parse(serverUrl),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(requestData),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Data successfully sent to the server!')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to send data. Status: ${response.statusCode}')),
      );
    }
  } catch (e) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Error: $e')),
    );
    print('Error: $e');
  }
}
