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
            "Growth plus twelve percent, decline minus three point five percent. Item number five is ready.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Budget USD 12.50, cost EUR 3, yen JPY 100."),
            "Budget twelve dollars fifty cents, cost three euros, yen one hundred yen.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Budget 12 USD, cost 3 EUR, fee 5 GBP."),
            "Budget twelve dollars, cost three euros, fee five pounds.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Visit www.example.com and docs.example.org/path. Timezone UTC+8 and GMT-5."),
            "Visit www dot example dot com and docs dot example dot org slash path. "
            "Timezone UTC plus eight and GMT minus five.",
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
            "and IPv six two zero zero one colon zero D B eight colon colon one. "
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
            "The event is on january second twenty twenty six and january second twenty twenty six.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Date 2026.06.15, deadline 2026.6.5, version 2026.06."),
            "Date June fifteenth twenty twenty six, deadline June fifth twenty twenty six, "
            "version two thousand twenty six point zero six.",
        )
        self.assertEqual(
            _prepare_en_tn_input("The meeting is June 15, 2026 and Jun. 16, 2026."),
            "The meeting is June fifteenth twenty twenty six and June sixteenth twenty twenty six.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Valid 2026-06-15 - 2026-06-20."),
            "Valid june fifteenth twenty twenty six to june twentieth twenty twenty six.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Ch. 1, Sec. 2, Fig. 3, Eq. 4, No. 5."),
            "chapter one, section two, figure three, equation four, number five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Room 201, Ch. 12, p. 2, pp. 3-5, No. 5."),
            "Room two zero one, chapter twelve, page two, pages three to five, number five.",
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
            "Area eighty square meters, parcel one thousand two hundred square meters, "
            "price one thousand two hundred and thirty four dollars fifty six cents.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Area is 80 m², rent is $12/m², volume is 3 m³."),
            "Area is eighty square meters, rent is twelve dollars per square meter, volume is three cubic meters.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Area 80 sq m, lot 2 sq km, room 120 sq ft."),
            "Area eighty square meters, lot two square kilometers, room one hundred and twenty square feet.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature 23C, temp -5F, area 80 sq yd. Price 12.50 dollars."),
            "Temperature twenty three degrees Celsius, temp minus five degrees Fahrenheit, "
            "area eighty square yards. Price twelve dollars fifty cents.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature 36.5C ±2C, humidity 40%-60%."),
            "Temperature thirty six point five degrees Celsius plus or minus two degrees Celsius, "
            "humidity forty to sixty percent.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature 20-30C, body temperature 36.5-37.2°C."),
            "Temperature twenty to thirty degrees Celsius, body temperature thirty six point five "
            "to thirty seven point two degrees Celsius.",
        )
        self.assertEqual(
            _prepare_en_tn_input("The temp is -3C. Temperature is 72F."),
            "The temp is minus three degrees Celsius. Temperature is seventy two degrees Fahrenheit.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Temperature -3°C, feels like -5F."),
            "Temperature minus three degrees Celsius, feels like minus five degrees Fahrenheit.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Rating 4.8/5, score 9/10, NPS 8/10."),
            "Rating four point eight out of five, score nine out of ten, NPS eight out of ten.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Open Mon-Fri and Sat-Sun."),
            "Open Monday to Friday and Saturday to Sunday.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Range 10%-20%, price $10-$20, weight 5-10kg."),
            "Range ten to twenty percent, price ten to twenty dollars, weight five to ten kilograms.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Tolerance ±0.5mm, temperature ±3°C, x≈5."),
            "Tolerance plus or minus zero point five millimeters, temperature plus or minus three degrees Celsius, "
            "x approximately equal to five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Account 6222 1234 5678 9012 and card number 4111-1111-1111-1111."),
            "Account six two two two one two three four five six seven eight nine zero one two "
            "and card number four one one one one one one one one one one one one one one one.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Density is 5kg/m². Users 3.5K."),
            "Density is five kilograms per square meter. Users three point five thousand.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Gas is 400ppm, glucose is 5.6mmol/L, pressure is 101kPa."),
            "Gas is four hundred parts per million, glucose is five point six millimoles per liter, "
            "pressure is one hundred and one kilopascals.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Vitamin D is 25IU/L, drug is 2µg/mL, sample is 20µL."),
            "Vitamin D is twenty five international units per liter, drug is two micrograms per milliliter, "
            "sample is twenty microliters.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Noise is 30dB, irradiance is 80W/m², torque is 5N·m, battery is 5000mAh."),
            "Noise is thirty decibels, irradiance is eighty watts per square meter, "
            "torque is five newton meters, battery is five thousand milliampere hours.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Rate rose 25bp, users 1.2M, revenue 3B."),
            "Rate rose twenty five basis points, users one point two million, revenue three billion.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Resistance is 10Ω, current is 2A, voltage is 3.3mV, capacitance is 47µF."),
            "Resistance is ten ohms, current is two amperes, voltage is three point three millivolts, "
            "capacitance is forty seven microfarads.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "Force is 5N, pressure is 101Pa, stress is 0.1MPa, acceleration is 9.8m/s², "
                "speed is 3000rpm, flow is 2L/min."
            ),
            "Force is five newtons, pressure is one hundred and one pascals, stress is zero point one megapascals, "
            "acceleration is nine point eight meters per second squared, speed is three thousand revolutions per minute, "
            "flow is two liters per minute.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Resolution is 1920x1080, size is 10x20cm."),
            "Resolution is nineteen twenty by ten eighty, size is ten by twenty centimeters.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Growth is 2pp, error is 1e-5, speed is 3x10^8m/s, coordinate is 39.9°N."),
            "Growth is two percentage points, error is one times ten to the minus five, "
            "speed is three times ten to the eight meters per second, coordinate is thirty nine point nine degrees north.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Q2 2026 revenue grew. 2026 Q3 outlook improved. FY2026 budget is ready."),
            "second quarter twenty twenty six revenue grew. third quarter twenty twenty six outlook improved. "
            "fiscal year twenty twenty six budget is ready.",
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
            "Support one eight hundred five five five zero one two three, order number one two three four five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Unit price $12.50/kg, fee $3/hour."),
            "Unit price twelve dollars fifty cents per kilogram, fee three dollars per hour.",
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
            "zip one zero zero zero one dash one two three four.",
        )
        self.assertEqual(
            _prepare_en_tn_input("x>=5 and y<=10."),
            "x greater than or equal to five and y less than or equal to ten.",
        )
        self.assertEqual(
            _prepare_en_tn_input("x!=5 and y≠10."),
            "x not equal to five and y not equal to ten.",
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
            "Distance five meters, speed ten meters per second, size sixteen gigabytes, voltage two hundred and twenty volts.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Power 3kW, energy 5kWh, storage 512MB, cache 128KB, volume 500mL."),
            "Power three kilowatts, energy five kilowatt hours, storage five hundred and twelve megabytes, "
            "cache one hundred and twenty eight kilobytes, volume five hundred milliliters.",
        )
        self.assertEqual(
            _prepare_en_tn_input(
                "Length 30cm, width 5mm, capacity 1L, ratio 3:2, range 3-5 days, formula 20/4=5."
            ),
            "Length thirty centimeters, width five millimeters, capacity one liter, "
            "ratio three to two, range three to five days, formula twenty divided by four equals five.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Score 3:2. The ratio is 1:2."),
            "Score three to two. The ratio is one to two.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Room B-1208. Price HK$7. Meet at 3:30 p.m. Price."),
            "Room B dash one two zero eight. Price seven Hong Kong dollars. Meet at three thirty PM. Price.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Meet 3pm-4:30pm."),
            "Meet three PM to four thirty PM.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Throughput 120MB/s, frame rate 60fps, latency 12ms, memory 2GiB."),
            "Throughput one hundred and twenty megabytes per second, frame rate sixty frames per second, "
            "latency twelve milliseconds, memory two gibibytes.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Duration 2h 30min 45s, angle 90deg, frequency 44.1kHz."),
            "Duration two hours thirty minutes forty five seconds, angle ninety degrees, "
            "frequency forty four point one kilohertz.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Duration 1h30min, wait 2min30s."),
            "Duration one hour thirty minutes, wait two minutes thirty seconds.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Height 6ft, length 12in, weight 5lb, volume 2oz, distance 3mi."),
            "Height six feet, length twelve inches, weight five pounds, volume two ounces, distance three miles.",
        )
        self.assertEqual(
            _prepare_en_tn_input("Error 1‰, rate 3.5‰."),
            "Error one per mille, rate three point five per mille.",
        )


if __name__ == "__main__":
    unittest.main()
