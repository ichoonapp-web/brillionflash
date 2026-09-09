import 'package:flutter_test/flutter_test.dart';
import 'package:brillionflash/main.dart';

void main() {
  testWidgets('Brillionflash App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const BrillionflashApp());
    expect(find.text('Brillionflash'), findsOneWidget);
  });
}
