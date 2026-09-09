import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );
  runApp(const BrillionflashApp());
}

class BrillionflashApp extends StatelessWidget {
  const BrillionflashApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Brillionflash',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0D0D12),
        primaryColor: const Color(0xFFFFB300),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFFFFB300),
          secondary: Color(0xFFFF0080),
          surface: Color(0xFF161622),
        ),
        textTheme: GoogleFonts.plusJakartaSansTextTheme(ThemeData.dark().textTheme),
      ),
      home: const BrillionMainDashboard(),
    );
  }
}

class BrillionMainDashboard extends StatefulWidget {
  const BrillionMainDashboard({super.key});

  @override
  State<BrillionMainDashboard> createState() => _BrillionMainDashboardState();
}

class _BrillionMainDashboardState extends State<BrillionMainDashboard> {
  int _selectedTab = 0;
  double _kelvin = 5200;
  double _brightness = 90;
  double _red = 255;
  double _green = 225;
  double _blue = 210;
  bool _is120Fps = true;
  bool _is12kUpscale = true;
  bool _isBeatSync = false;
  int _dailyStreak = 4;
  int _userCredits = 105;
  String _activePreset = "K-Beauty Soft Glow";

  final List<Map<String, dynamic>> _starterPresets = [
    {"name": "K-Beauty Soft Glow", "kelvin": 5200.0, "r": 255.0, "g": 225.0, "b": 210.0, "icon": Icons.auto_awesome, "color": const Color(0xFFFF80AB)},
    {"name": "Golden Hour Studio", "kelvin": 3200.0, "r": 255.0, "g": 190.0, "b": 120.0, "icon": Icons.wb_sunny, "color": const Color(0xFFFFB300)},
    {"name": "Cyberpunk Neon", "kelvin": 8500.0, "r": 0.0, "g": 240.0, "b": 255.0, "icon": Icons.electric_bolt, "color": const Color(0xFF00E5FF)},
    {"name": "Soft Portrait", "kelvin": 5600.0, "r": 250.0, "g": 240.0, "b": 230.0, "icon": Icons.face, "color": const Color(0xFFFFD180)},
    {"name": "TikTok Streamer", "kelvin": 6000.0, "r": 255.0, "g": 210.0, "b": 240.0, "icon": Icons.videocam, "color": const Color(0xFFE040FB)},
  ];

  void _applyPreset(Map<String, dynamic> preset) {
    setState(() {
      _activePreset = preset["name"];
      _kelvin = preset["kelvin"];
      _red = preset["r"];
      _green = preset["g"];
      _blue = preset["b"];
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("? Active Preset: $_activePreset"),
        backgroundColor: const Color(0xFFFF0080),
        duration: const Duration(seconds: 1),
      ),
    );
  }

  void _claimDailyReward() {
    setState(() {
      _dailyStreak += 1;
      _userCredits += 5;
    });
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2C),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        title: Row(
          children: const [
            Icon(Icons.stars, color: Color(0xFFFFB300)),
            SizedBox(width: 8),
            Text("Day Streak Claimed!", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          ],
        ),
        content: Text(
          "?? You claimed +5 Free AI Credits for Day $_dailyStreak streak!\n\nTotal Credits: $_userCredits",
          style: const TextStyle(fontSize: 14),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Awesome!", style: TextStyle(color: Color(0xFFFFB300))),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final Color currentLightColor = Color.fromRGBO(_red.toInt(), _green.toInt(), _blue.toInt(), 1.0);

    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            _buildTopAppBar(),
            _buildDailyStreakBanner(),
            Expanded(
              child: IndexedStack(
                index: _selectedTab,
                children: [
                  _buildStudioTab(currentLightColor),
                  _buildAiCreatorStudioTab(),
                  _buildMarketplaceTab(),
                  _buildAboutAndGuideTab(),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: _buildBottomNav(),
    );
  }

  Widget _buildTopAppBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: const BoxDecoration(
        color: Color(0xFF14141E),
        border: Border(bottom: BorderSide(color: Color(0xFF262638), width: 1)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [Color(0xFFFF0080), Color(0xFF00E5FF)]),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.flash_on, color: Colors.white, size: 20),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text("Brillionflash", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, letterSpacing: 0.5)),
                  Text("Global #1 AI Light Studio", style: TextStyle(fontSize: 11, color: Colors.grey)),
                ],
              ),
            ],
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: const Color(0xFF262638),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: const Color(0xFFFFB300), width: 1),
            ),
            child: Row(
              children: [
                const Icon(Icons.stars, color: Color(0xFFFFB300), size: 16),
                const SizedBox(width: 6),
                Text("$_userCredits Credits", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFFFFB300))),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDailyStreakBanner() {
    return Container(
      margin: const EdgeInsets.fromLTRB(16, 12, 16, 8),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            const Color(0xFFFF0080).withValues(alpha: 0.2),
            const Color(0xFF00E5FF).withValues(alpha: 0.2),
          ],
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              const Icon(Icons.local_fire_department, color: Color(0xFFFF3D00), size: 22),
              const SizedBox(width: 8),
              Text(
                "Daily Streak: Day $_dailyStreak ?? (+5 Credits Ready)",
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
              ),
            ],
          ),
          ElevatedButton(
            onPressed: _claimDailyReward,
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFFFB300),
              foregroundColor: Colors.black,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            ),
            child: const Text("Claim", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
          ),
        ],
      ),
    );
  }

  Widget _buildStudioTab(Color currentLightColor) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Container(
              width: 180,
              height: 180,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.black,
                boxShadow: [
                  BoxShadow(
                    color: currentLightColor.withValues(alpha: _brightness / 100.0),
                    blurRadius: 40,
                    spreadRadius: 15,
                  ),
                ],
                border: Border.all(color: currentLightColor, width: 14),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text("${_kelvin.toInt()}K", style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  Text("${_brightness.toInt()}% Glow", style: const TextStyle(fontSize: 12, color: Colors.grey)),
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(color: const Color(0xFF262638), borderRadius: BorderRadius.circular(8)),
                    child: Text(_activePreset, style: const TextStyle(fontSize: 10, color: Color(0xFFFFB300))),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),

          const Text("INSTANT 1-TAP GLOW PRESETS", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey, letterSpacing: 1.2)),
          const SizedBox(height: 10),
          SizedBox(
            height: 48,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: _starterPresets.length,
              itemBuilder: (context, index) {
                final preset = _starterPresets[index];
                final bool isSelected = _activePreset == preset["name"];
                return GestureDetector(
                  onTap: () => _applyPreset(preset),
                  child: Container(
                    margin: const EdgeInsets.only(right: 10),
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                    decoration: BoxDecoration(
                      color: isSelected ? preset["color"] : const Color(0xFF1E1E2C),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: isSelected ? Colors.white : Colors.white10),
                    ),
                    child: Row(
                      children: [
                        Icon(preset["icon"], color: isSelected ? Colors.black : preset["color"], size: 18),
                        const SizedBox(width: 8),
                        Text(
                          preset["name"],
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            color: isSelected ? Colors.black : Colors.white,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 24),

          _buildControlCard(
            title: "Kelvin Temperature (2000K - 10000K)",
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("2000K Warm Gold", style: TextStyle(fontSize: 11, color: Colors.amber)),
                    Text("${_kelvin.toInt()}K", style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFFFFB300))),
                    const Text("10000K Cool Blue", style: TextStyle(fontSize: 11, color: Colors.cyan)),
                  ],
                ),
                Slider(
                  value: _kelvin,
                  min: 2000,
                  max: 10000,
                  activeColor: Color.lerp(Colors.amber, Colors.cyan, (_kelvin - 2000) / 8000),
                  onChanged: (val) => setState(() => _kelvin = val),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),

          _buildControlCard(
            title: "Light Brightness & Intensity",
            child: Slider(
              value: _brightness,
              min: 0,
              max: 100,
              activeColor: const Color(0xFFFF0080),
              onChanged: (val) => setState(() => _brightness = val),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAiCreatorStudioTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildControlCard(
            title: "120FPS 12K ULTRA AI SUPER-RESOLUTION",
            child: Column(
              children: [
                SwitchListTile(
                  title: const Text("120 FPS Motion Smoothing", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
                  subtitle: const Text("Ultra-smooth video frames for budget smartphones", style: TextStyle(fontSize: 11, color: Colors.grey)),
                  value: _is120Fps,
                  activeThumbColor: const Color(0xFF00E5FF),
                  onChanged: (val) => setState(() => _is120Fps = val),
                ),
                const Divider(color: Colors.white10),
                SwitchListTile(
                  title: const Text("12K AI Super-Resolution Matrix", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
                  subtitle: const Text("Night vision noise filter with 99.2% clarity boost", style: TextStyle(fontSize: 11, color: Colors.grey)),
                  value: _is12kUpscale,
                  activeThumbColor: const Color(0xFFFF0080),
                  onChanged: (val) => setState(() => _is12kUpscale = val),
                ),
                const Divider(color: Colors.white10),
                SwitchListTile(
                  title: const Text("AI Audio Beat-Sync Pulse", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
                  subtitle: const Text("Pulse light synced to microphone audio beats", style: TextStyle(fontSize: 11, color: Colors.grey)),
                  value: _isBeatSync,
                  activeThumbColor: const Color(0xFFFFB300),
                  onChanged: (val) => setState(() => _isBeatSync = val),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          _buildControlCard(
            title: "AI AUTO-CAPTION & 1-TAP VIRAL SHARE",
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("Generated Viral Caption:", style: TextStyle(fontSize: 12, color: Colors.grey)),
                const SizedBox(height: 6),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(color: const Color(0xFF14141E), borderRadius: BorderRadius.circular(12)),
                  child: const Text(
                    "Brillionflash 12K AI Ring Light ????? ???? ?????? ?????? ??! ? #LitWithBrillionflashAI #Brillionflash #Viral",
                    style: TextStyle(fontSize: 13, height: 1.4),
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text("?? Opening TikTok with Auto-Caption & Floating Light!")),
                          );
                        },
                        icon: const Icon(Icons.share, size: 16),
                        label: const Text("Share to TikTok", style: TextStyle(fontSize: 12)),
                        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFFF0080)),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text("?? Opening Instagram Reels!")),
                          );
                        },
                        icon: const Icon(Icons.camera_alt, size: 16),
                        label: const Text("Reels Share", style: TextStyle(fontSize: 12)),
                        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF00E5FF), foregroundColor: Colors.black),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMarketplaceTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("CREATOR PRESET MARKETPLACE (70% REVENUE SHARE)", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey, letterSpacing: 1.2)),
          const SizedBox(height: 12),
          _buildMarketplaceCard("Korean K-Pop Idol Glow Pack", "By Designer Su-jin", "\$1.99", Icons.star, Colors.amber),
          _buildMarketplaceCard("Cyberpunk Neon Night Vlogger", "By Creator Alex", "\$2.49", Icons.flash_on, Colors.cyan),
          _buildMarketplaceCard("Golden Hour Sunset Portrait", "By Studio Pro", "FREE", Icons.check_circle, Colors.green),
        ],
      ),
    );
  }

  Widget _buildMarketplaceCard(String title, String creator, String price, IconData icon, Color accentColor) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: const Color(0xFF1E1E2C), borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.white10)),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Icon(icon, color: accentColor, size: 28),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                  Text(creator, style: const TextStyle(fontSize: 11, color: Colors.grey)),
                ],
              ),
            ],
          ),
          ElevatedButton(
            onPressed: () {},
            style: ElevatedButton.styleFrom(
              backgroundColor: accentColor,
              foregroundColor: Colors.black,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            child: Text(price, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
          ),
        ],
      ),
    );
  }

  Widget _buildAboutAndGuideTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildControlCard(
            title: "ABOUT BRILLIONFLASH & CREATOR GUIDE",
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text("1. Flagship 12K Quality on Normal Phones", style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFFFFB300))),
                SizedBox(height: 4),
                Text("120 FPS Motion Smoothing & 12K AI Super-Resolution brings \$1200 pro studio lighting to any budget phone.", style: TextStyle(fontSize: 12, color: Colors.grey)),
                SizedBox(height: 12),
                Text("2. Floating Ring Light Over ALL Apps", style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFFFF0080))),
                SizedBox(height: 4),
                Text("Floats a studio ring light over TikTok, Instagram, Camera, Zoom, and YouTube Shorts.", style: TextStyle(fontSize: 12, color: Colors.grey)),
                SizedBox(height: 12),
                Text("3. How Creators Earn Cash", style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF00E5FF))),
                SizedBox(height: 4),
                Text("Sell your custom presets on Brillionflash Marketplace and keep 70% of all revenues sent to your bank account.", style: TextStyle(fontSize: 12, color: Colors.grey)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildControlCard({required String title, required Widget child}) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E1E2C),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.grey, letterSpacing: 1.1)),
          const SizedBox(height: 12),
          child,
        ],
      ),
    );
  }

  Widget _buildBottomNav() {
    return BottomNavigationBar(
      currentIndex: _selectedTab,
      onTap: (index) => setState(() => _selectedTab = index),
      backgroundColor: const Color(0xFF14141E),
      selectedItemColor: const Color(0xFFFFB300),
      unselectedItemColor: Colors.grey,
      type: BottomNavigationBarType.fixed,
      items: const [
        BottomNavigationBarItem(icon: Icon(Icons.tune), label: "Studio Light"),
        BottomNavigationBarItem(icon: Icon(Icons.auto_awesome), label: "AI 12K Studio"),
        BottomNavigationBarItem(icon: Icon(Icons.store), label: "Marketplace"),
        BottomNavigationBarItem(icon: Icon(Icons.info), label: "Guide"),
      ],
    );
  }
}

