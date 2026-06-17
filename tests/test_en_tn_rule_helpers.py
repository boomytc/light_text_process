from __future__ import annotations

import unittest

from light_text_process.rules.en_tn import (
    _prepare_en_tn_input,
    _space_en_tn_letter_decimal_versions,
    _verbalize_en_tn_dotted_versions,
    _verbalize_en_tn_negative_currency,
    _verbalize_en_tn_number_abbreviations,
)


class EnglishTNRuleHelperTests(unittest.TestCase):
    def test_en_tn_helpers_normalize_operational_tokens(self) -> None:
        self.assertEqual(
            _verbalize_en_tn_negative_currency("I paid -$12.50 and -€3.05."),
            "I paid minus $12.50 and minus €3.05.",
        )
        self.assertEqual(_verbalize_en_tn_number_abbreviations("No. 5 is ready."), "number 5 is ready.")
        self.assertEqual(
            _prepare_en_tn_input("Growth +12%, decline -3.5%. Item #5 is ready."),
            "Growth plus 12 percent, decline -3.5%. Item number 5 is ready.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Budget USD 12.50, cost EUR 3, yen JPY 100."),
            "Budget $12.50, cost €3, yen ¥100.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Budget 12 USD, cost 3 EUR, fee 5 GBP."),
            "Budget $12, cost €3, fee £5.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Visit www.example.com and docs.example.org/path. Timezone UTC+8 and GMT-5."),
            "Visit www dot example dot com and docs dot example dot org slash path. "
            "Timezone UTC plus 8 and GMT minus 5.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "File report_v2.0.pdf, path /data/input-01/test.csv, handle @light_user, hashtag #AI2026."
            ),
            "File report underscore v two point zero dot p d f, path slash data slash input dash zero one "
            "slash test dot c s v, handle at light underscore user, hashtag hash A I two zero two six.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Link https://example.com/a-b?q=hello_world&n=123#top."),
            "Link HTTPS colon slash slash example dot com slash a dash b question mark q equals "
            "hello underscore world ampersand n equals one two three hash top.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "MAC AA:BB:CC:DD:EE:FF, UUID 550e8400-e29b-41d4-a716-446655440000, color #FF5733."
            ),
            "MAC A A colon B B colon C C colon D D colon E E colon F F, "
            "UUID five five zero e eight four zero zero dash e two nine b dash four one d four "
            "dash a seven one six dash four four six six five five four four zero zero zero zero, "
            "color hash F F five seven three three.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "Server 127.0.0.1:8080 and IPv6 2001:0db8::1. "
                "ISBN 978-1-4028-9462-6, DOI 10.1000/xyz123."
            ),
            "Server one two seven dot zero dot zero dot one colon eight zero eight zero "
            "and IPv6 two zero zero one colon zero D B eight colon colon one. "
            "ISBN nine seven eight dash one dash four zero two eight dash nine four six two dash six, "
            "DOI one zero point one zero zero zero slash X Y Z one two three.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Version v2.0.1-beta.3."),
            "Version v two point zero point one dash beta point three.",
        )
        self.assertEqual(
            _prepare_en_tn_input("The API returned HTTP 404, port 8080, deadline 2026-06-15T14:30:05Z."),
            "The API returned HTTP four zero four, port eight zero eight zero, "
            "deadline two zero two six dash zero six dash one five T one four colon three zero colon zero five Z.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Press Ctrl+C, then Cmd+Shift+P and Alt+F4."),
            "Press control plus C, then command plus shift plus P and alt plus F four.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Deadline 2026-06-15 14:30:05."),
            "Deadline two zero two six dash zero six dash one five one four colon three zero colon zero five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Meeting at 14:30 and backup at 07:05."),
            "Meeting at fourteen thirty and backup at seven oh five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Office hours 09:00-18:30, meeting 14:30~15:45."),
            "Office hours nine o'clock to eighteen thirty, meeting fourteen thirty to fifteen forty five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("The event is on 1/2/2026 and 2026/01/02."),
            "The event is on January 2 2026 and January 2 2026.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Date 2026.06.15, deadline 2026.6.5, version 2026.06."),
            "Date June fifteenth 2026, deadline June fifth 2026, version 2026.06.",
        )
        self.assertEqual(
            _prepare_en_tn_input("The meeting is June 15, 2026 and Jun. 16, 2026."),
            "The meeting is June fifteenth 2026 and June sixteenth 2026.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Valid 2026-06-15 - 2026-06-20."),
            "Valid 2026-06-15 to 2026-06-20.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Ch. 1, Sec. 2, Fig. 3, Eq. 4, No. 5."),
            "chapter 1, section 2, figure 3, equation 4, number 5.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Room 201, Ch. 12, p. 2, pp. 3-5, No. 5."),
            "Room two zero one, chapter 12, page 2, pages 3 to 5, number 5.",
        )
        self.assertEqual(
            _prepare_en_tn_input("The 21st century, 3rd floor, 12th grade, 1st place."),
            "The twenty first century, third floor, twelfth grade, first place.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Rank 1st-3rd, floors 2nd-5th."),
            "Rank first to third, floors second to fifth.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Area 80㎡, parcel 1,200m², price $1,234.56."),
            "Area 80 square meters, parcel 1200 square meters, price $1234.56.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Area is 80 m², rent is $12/m², volume is 3 m³."),
            "Area is 80 square meters, rent is $12 per square meter, volume is 3 m³.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Area 80 sq m, lot 2 sq km, room 120 sq ft."),
            "Area 80 square meters, lot 2 square kilometers, room 120 square feet.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature 23C, temp -5F, area 80 sq yd. Price 12.50 dollars."),
            "Temperature 23 degrees Celsius, temp -5 degrees Fahrenheit, area 80 square yards. Price $12.50.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature 36.5C ±2C, humidity 40%-60%."),
            "Temperature 36.5 degrees Celsius plus or minus 2 degrees Celsius, humidity 40 to 60 percent.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature 20-30C, body temperature 36.5-37.2°C."),
            "Temperature 20 to 30 degrees Celsius, body temperature 36.5 to 37.2 degrees Celsius.",
        )
        self.assertEqual(
            _prepare_en_tn_input("The temp is -3C. Temperature is 72F."),
            "The temp is -3 degrees Celsius. Temperature is 72 degrees Fahrenheit.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature -3°C, feels like -5F."),
            "Temperature -3 degrees Celsius, feels like -5 degrees Fahrenheit.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Rating 4.8/5, score 9/10, NPS 8/10."),
            "Rating 4.8 out of 5, score 9 out of 10, NPS 8 out of 10.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Open Mon-Fri and Sat-Sun."),
            "Open Monday to Friday and Saturday to Sunday.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Range 10%-20%, price $10-$20, weight 5-10kg."),
            "Range 10 to 20 percent, price 10 to 20 dollars, weight 5 to 10 kilograms.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Tolerance ±0.5mm, temperature ±3°C, x≈5."),
            "Tolerance plus or minus 0.5 millimeters, temperature plus or minus 3 degrees Celsius, "
            "x approximately equal to 5.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Account 6222 1234 5678 9012 and card number 4111-1111-1111-1111."),
            "Account six two two two one two three four five six seven eight nine zero one two "
            "and card number four one one one one one one one one one one one one one one one.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Density is 5kg/m². Users 3.5K."),
            "Density is 5 kilograms per square meter. Users 3.5 thousand.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Gas is 400ppm, glucose is 5.6mmol/L, pressure is 101kPa."),
            "Gas is 400 parts per million, glucose is 5.6 millimoles per liter, "
            "pressure is 101 kilopascals.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Vitamin D is 25IU/L, drug is 2µg/mL, sample is 20µL."),
            "Vitamin D is 25 international units per liter, drug is 2 micrograms per milliliter, "
            "sample is 20 microliters.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Noise is 30dB, irradiance is 80W/m², torque is 5N·m, battery is 5000mAh."),
            "Noise is 30 decibels, irradiance is 80 watts per square meter, "
            "torque is 5 newton meters, battery is 5000 milliampere hours.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Rate rose 25bp, users 1.2M, revenue 3B."),
            "Rate rose 25 basis points, users 1.2 million, revenue 3 billion.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Resistance is 10Ω, current is 2A, voltage is 3.3mV, capacitance is 47µF."),
            "Resistance is 10 ohms, current is 2 amperes, voltage is 3.3 millivolts, "
            "capacitance is 47 microfarads.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "Force is 5N, pressure is 101Pa, stress is 0.1MPa, acceleration is 9.8m/s², "
                "speed is 3000rpm, flow is 2L/min."
            ),
            "Force is 5 newtons, pressure is 101 pascals, stress is 0.1 megapascals, "
            "acceleration is 9.8 meters per second squared, speed is 3000 revolutions per minute, "
            "flow is 2 liters per minute.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Resolution is 1920x1080, size is 10x20cm."),
            "Resolution is 1920 by 1080, size is 10 by 20 centimeters.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Growth is 2pp, error is 1e-5, speed is 3x10^8m/s, coordinate is 39.9°N."),
            "Growth is 2 percentage points, error is 1 times 10 to the minus 5, "
            "speed is 3 times 10 to the 8 meters per second, coordinate is 39.9 degrees north.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Q2 2026 revenue grew. 2026 Q3 outlook improved. FY2026 budget is ready."),
            "second quarter 2026 revenue grew. third quarter 2026 outlook improved. "
            "fiscal year 2026 budget is ready.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "Order AB-1234, invoice INV-2026-001, tracking SF1234567890, phone 415-555-0123 ext. 45."
            ),
            "Order A B dash one two three four, invoice I N V dash two zero two six dash zero zero one, "
            "tracking S F one two three four five six seven eight nine zero, "
            "phone four one five five five five zero one two three extension four five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Call 1-800-555-0123 and call +1 415-555-0123."),
            "Call one eight hundred five five five zero one two three and "
            "call plus one four one five five five five zero one two three.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Support 1-800-555-0123, order #12345."),
            "Support one eight hundred five five five zero one two three, order number 12345.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Unit price $12.50/kg, fee $3/hour."),
            "Unit price $12.50 per kilogram, fee $3 per hour.",
        )
        self.assertEqual(
            _prepare_en_tn_input("License plate ABC-123, VIN 1HGCM82633A004352, passport E12345678."),
            "License plate A B C dash one two three, "
            "VIN one H G C M eight two six three three A zero zero four three five two, "
            "passport E one two three four five six seven eight.",
        )
        self.assertEqual(_prepare_en_tn_input("Model X-200."), "Model X dash two zero zero.")
        self.assertEqual(
            _prepare_en_tn_input("Room 1208, Ste. 305, Apt. 5B, ZIP 10001-1234."),
            "Room one two zero eight, suite three zero five, apartment five B, "
            "ZIP one zero zero zero one dash one two three four.",
        )
        self.assertEqual(
            _prepare_en_tn_input("x>=5 and y<=10."),
            "x greater than or equal to 5 and y less than or equal to 10.",
        )
        self.assertEqual(
            _prepare_en_tn_input("x!=5 and y≠10."),
            "x not equal to 5 and y not equal to 10.",
        )

    def test_en_tn_helper_spaces_letter_decimal_versions(self) -> None:
        self.assertEqual(
            _space_en_tn_letter_decimal_versions("Version v2.0 and V10.3."),
            "Version v 2.0 and V 10.3.",
        )
        self.assertEqual(
            _verbalize_en_tn_dotted_versions("Version 2.0.1 and v2.0.1 and IP 192.168.0.1"),
            "Version 2 point 0 point 1 and v 2 point 0 point 1 and IP 192.168.0.1",
        )
        self.assertEqual(
            _prepare_en_tn_input("Distance 5m, speed 10m/s, size 16GB, voltage 220V."),
            "Distance 5 meters, speed 10 meters per second, size 16 gigabytes, voltage 220 volts.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Power 3kW, energy 5kWh, storage 512MB, cache 128KB, volume 500mL."),
            "Power 3 kilowatts, energy 5 kilowatt hours, storage 512 megabytes, cache 128 kilobytes, volume 500 milliliters.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "Length 30cm, width 5mm, capacity 1L, ratio 3:2, range 3-5 days, formula 20/4=5."
            ),
            "Length 30 centimeters, width 5 millimeters, capacity 1 liter, "
            "ratio 3 to 2, range 3 to 5 days, formula 20 divided by 4 equals 5.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Score 3:2. The ratio is 1:2."),
            "Score 3 to 2. The ratio is 1 to 2.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Room B-1208. Price HK$7. Meet at 3:30 p.m. Price."),
            "Room B dash one two zero eight. Price 7 Hong Kong dollars. Meet at three thirty PM. Price.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Meet 3pm-4:30pm."),
            "Meet three PM to four thirty PM.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Throughput 120MB/s, frame rate 60fps, latency 12ms, memory 2GiB."),
            "Throughput 120 megabytes per second, frame rate 60 frames per second, "
            "latency 12 milliseconds, memory 2 gibibytes.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Duration 2h 30min 45s, angle 90deg, frequency 44.1kHz."),
            "Duration 2 hours 30 minutes 45 seconds, angle 90 degrees, frequency 44.1 kilohertz.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Duration 1h30min, wait 2min30s."),
            "Duration 1 hour 30 minutes, wait 2 minutes 30 seconds.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Height 6ft, length 12in, weight 5lb, volume 2oz, distance 3mi."),
            "Height 6 feet, length 12 inches, weight 5 pounds, volume 2 ounces, distance 3 miles.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Error 1‰, rate 3.5‰."),
            "Error 1 per mille, rate 3.5 per mille.",
        )


if __name__ == "__main__":
    unittest.main()
