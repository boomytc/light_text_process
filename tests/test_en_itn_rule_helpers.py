from __future__ import annotations

import unittest

from light_text_process.rules.en_itn import (
    finalize_outputs,
    _compact_en_itn_spacing,
    _normalize_en_itn_time_oh,
    _prepare_en_itn_input,
)


class EnglishITNRuleHelperTests(unittest.TestCase):
    def test_en_itn_helper_compacts_percent_spacing(self) -> None:
        self.assertEqual(_compact_en_itn_spacing("it is 23.5 and 60 %"), "it is 23.5 and 60%")
        self.assertEqual(
            _compact_en_itn_spacing("error one per mille rate 3.5 per mille"),
            "error 1‰ rate 3.5‰",
        )
        self.assertEqual(
            _compact_en_itn_spacing("I paid minus $12.50 and negative €3.05"),
            "I paid -$12.50 and -€3.05",
        )
        self.assertEqual(
            _compact_en_itn_spacing("unit price $12.50 per kilogram fee $3 per hour"),
            "unit price $12.50/kg fee $3/h",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "version v 2.0 .1 email t e s t at example.com ratio one half and three quarters"
            ),
            "version v 2.0.1 email test@example.com ratio 1/2 and 3/4",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "negative 12.5% negative 3.5 degrees celsius speed 100 mbps "
                "storage 512 mb cache 128 kb volume 500 ml energy 5 kwh"
            ),
            "-12.5% -3.5°C speed 100 Mbps "
            "storage 512 MB cache 128 KB volume 500 mL energy 5 kWh",
        )
        self.assertEqual(
            _compact_en_itn_spacing("the temp is negative three celsius and negative five fahrenheit"),
            "the temp is -3°C and -5°F",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "url f t p colon// files dot example dot org/a_b "
                "contact user dot name plus tag at example dot co.uk"
            ),
            "url ftp://files.example.org/a_b contact user.name+tag@example.co.uk",
        )
        self.assertEqual(
            _compact_en_itn_spacing("visit w w w dot example dot com and docs dot example dot org slash path"),
            "visit www.example.com and docs.example.org/path",
        )
        self.assertEqual(
            _compact_en_itn_spacing("visit example.com email a.b at example.com user @light_user"),
            "visit example.com email a.b@example.com user @light_user",
        )
        self.assertEqual(
            _compact_en_itn_spacing("meet at 07:05 oh nine and eight x growth"),
            "meet at 07:05:09 and 8x growth",
        )
        self.assertEqual(
            _compact_en_itn_spacing("meet at 03:30 p.m. price hk$7"),
            "meet at 03:30 PM price HK$7",
        )
        self.assertEqual(
            _compact_en_itn_spacing("the file is 1.5 mb and 2 gigabytes version 3.10"),
            "the file is 1.5 MB and 2 GB version 3.10",
        )
        self.assertEqual(
            _compact_en_itn_spacing("rent is $12 per square meter and fee is $2 per m²"),
            "rent is $12/m² and fee is $2/m²",
        )
        self.assertEqual(
            _compact_en_itn_spacing("call+1 area code 4155550123 and call area code 2125557890"),
            "call +1 415-555-0123 and call 212-555-7890",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "x greater than or equal to five and y less than or equal to ten growth is three x"
            ),
            "x>=5 and y<=10 growth is 3x",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "capacity one liter ratio is three to two range three to five days "
                "formula 3+5 equals eight and twenty divided by four equals five"
            ),
            "capacity 1 L ratio is 3:2 range 3-5 days formula 3+5=8 and 20/4=5",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                _prepare_en_itn_input(
                    "the date is june fifteenth twenty twenty six time is nine oh five a m "
                    "score three to two call plus eight six one three eight zero zero one three eight zero zero zero"
                )
            ),
            "the date is 2026-06-15 time is 09:05 AM score 3:2 call +8613800138000",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "growth plus 12% area twelve square centimeters volume four cubic centimeters "
                "capacity 3.5 liters chapter twelve page three number five"
            ),
            "growth +12% area 12 cm² volume 4 cm³ capacity 3.5 L chapter 12 page 3 number 5",
        )
        self.assertEqual(_compact_en_itn_spacing("users 3.5 k"), "users 3.5K")
        self.assertEqual(
            _compact_en_itn_spacing(
                'frame rate 60 frames per 2nd latency twelve milliseconds memory two gibibytes '
                'weight £5 length 12 "'
            ),
            "frame rate 60 fps latency 12 ms memory 2 GiB weight 5 lb length 12 in",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "gas is 400 parts per million glucose is 5.6 millimoles per liter "
                "cholesterol is 90 mg per deciliter blood pressure is 120 mm of mercury "
                "pressure is 101 kilopascals lead is twelve parts per billion"
            ),
            "gas is 400 ppm glucose is 5.6 mmol/L cholesterol is 90 mg/dL "
            "blood pressure is 120 mmHg pressure is 101 kPa lead is 12 ppb",
        )
        self.assertEqual(
            _compact_en_itn_spacing("drug is 2 μg/ml hormone is 50 nanograms per milliliter sample is 20 microliters"),
            "drug is 2 µg/mL hormone is 50 ng/mL sample is 20 µL",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "the p h is 7.4 noise is 30 decibels irradiance is eighty watts per square meter "
                "torque is five newton meters battery is 5000 milliampere hours"
            ),
            "the pH is 7.4 noise is 30 dB irradiance is 80 W/m² torque is 5 N·m battery is 5000 mAh",
        )
        self.assertEqual(
            _compact_en_itn_spacing("rate rose 25 basis points users 1.2 m revenue 3 b"),
            "rate rose 25 bps users 1.2M revenue 3B",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "resistance is 10 ω current is 2 amperes voltage is 3.3 millivolts "
                "capacitance is 47 microfarads power is 5 watts"
            ),
            "resistance is 10 Ω current is 2 A voltage is 3.3 mV capacitance is 47 µF power is 5 W",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "force is 5 newtons pressure is 101 pa stress is 0.1 mpa acceleration is 9.8 m/s squared "
                "speed is 3000 revolutions per minute flow is 2 liters per minute"
            ),
            "force is 5 N pressure is 101 Pa stress is 0.1 MPa acceleration is 9.8 m/s² "
            "speed is 3000 rpm flow is 2 L/min",
        )
        self.assertEqual(
            _compact_en_itn_spacing("resolution is 1920 by 1080 size is ten by 20 cm"),
            "resolution is 1920x1080 size is 10x20cm",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "growth is two percentage points error is one times ten to the minus five "
                "speed is three times ten to the 8 m/s coordinate is 39.9 degrees north 116.4 degrees east"
            ),
            "growth is 2 pp error is 1e-5 speed is 3e8 m/s coordinate is 39.9°N 116.4°E",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "tolerance plus or minus zero point five millimeters x approximately equal to five"
            ),
            "tolerance ±0.5 mm x≈5",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "price one thousand two hundred thirty four dollars and fifty six cents budget three euros"
            ),
            "price $1234.56 budget €3",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "range ten to 20% price ten to $20 weight five to 10 kg budget twelve usd cost three eur"
            ),
            "range 10-20% price $10-$20 weight 5-10 kg budget $12 cost €3",
        )

    def test_en_itn_helpers_normalize_spoken_operational_tokens(self) -> None:
        self.assertEqual(
            _prepare_en_itn_input(
                "the date is twenty twenty six dash zero six dash fifteen timezone UTC plus eight"
            ),
            "the date is 2026-06-15 timezone UTC+8",
        )
        self.assertEqual(
            _prepare_en_itn_input("q two twenty twenty six revenue fiscal year twenty twenty six budget"),
            "Q2 2026 revenue FY2026 budget",
        )
        self.assertEqual(
            _prepare_en_itn_input("call one eight hundred five five five zero one two three extension nine"),
            "call 1-800-555-0123 ext. 9",
        )
        self.assertEqual(
            _prepare_en_itn_input("phone number four one five five five five zero one two three last four zero one two three"),
            "phone number 415-555-0123 last four 0123",
        )
        self.assertEqual(
            _prepare_en_itn_input("support one eight hundred five five five zero one two three extension four five"),
            "support 1-800-555-0123 ext. 45",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "the file is one point five megabytes and two gigabytes version three point ten is ready"
            ),
            "the file is 1.5 MB and 2 GB version 3.10 is ready",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "file one point five gigabytes download one hundred twenty megabytes per second "
                "network one hundred megabits per second"
            ),
            "file 1.5 GB download 120 MB/s network 100 Mbps",
        )
        self.assertEqual(
            _prepare_en_itn_input("version three point ten point four build twenty twenty six point zero six"),
            "version 3.10.4 build 2026.06",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "order A B dash one two three four invoice I N V dash two zero two six dash zero zero one "
                "tracking S F one two three four five six seven eight nine zero extension four five"
            ),
            "order AB-1234 invoice INV-2026-001 tracking SF1234567890 ext. 45",
        )
        self.assertEqual(
            _compact_en_itn_spacing("date 2026/06/15 time 14 : 30 phone 415-555-0123 ext 007"),
            "date 2026/06/15 time 14:30 phone 415-555-0123 ext. 007",
        )
        self.assertEqual(
            _prepare_en_itn_input("date twenty twenty six point zero six point fifteen callback time fourteen thirty"),
            "date 2026.06.15 callback time 14:30",
        )
        self.assertEqual(
            _prepare_en_itn_input("issue id Q one two three priority P one"),
            "issue id Q123 priority P1",
        )
        self.assertEqual(
            _prepare_en_itn_input("parameter q equals hello underscore world ticket X underscore one two three"),
            "parameter q=hello_world ticket X underscore one two three",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "license plate A B C dash one two three vin one H G C M eight two six three three "
                "A zero zero four three five two passport E one two three four five six seven eight"
            ),
            "license plate ABC-123 vin 1HGCM82633A004352 passport E12345678",
        )
        self.assertEqual(
            _prepare_en_itn_input("room two oh one room A twelve seat B three gate C zero eight parking C dash zero eight"),
            "room 201 room A12 seat B3 gate C08 parking C-08",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "file report underscore v two point zero dot p d f path slash data slash input dash zero one "
                "slash test dot c s v handle at light underscore user hashtag hash A I two zero two six"
            ),
            "file report_v2.0.pdf path /data/input-01/test.csv handle @light_user hashtag #AI2026",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "link h t t p s colon slash slash example dot com slash a dash b question mark q equals "
                "hello underscore world ampersand n equals one two three hash top"
            ),
            "link https://example.com/a-b?q=hello_world&n=123#top",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "MAC A A colon B B colon C C colon D D colon E E colon F F "
                "UUID five five zero e eight four zero zero dash e two nine b dash four one d four "
                "dash a seven one six dash four four six six five five four four zero zero zero zero "
                "color hash F F five seven three three"
            ),
            "MAC AA:BB:CC:DD:EE:FF UUID 550e8400-e29b-41d4-a716-446655440000 color #FF5733",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "server one two seven dot zero dot zero dot one colon eight zero eight zero "
                "and ipv6 two zero zero one colon zero d b eight colon colon one "
                "ISBN nine seven eight dash one dash four zero two eight dash nine four six two dash six "
                "DOI one zero point one zero zero zero slash x y z one two three"
            ),
            "server 127.0.0.1:8080 and ipv6 2001:0db8::1 "
            "ISBN 978-1-4028-9462-6 DOI 10.1000/xyz123",
        )
        self.assertEqual(
            _prepare_en_itn_input("version v two point zero point one dash beta point three"),
            "version v2.0.1-beta.3",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "the api returned HTTP four zero four port eight zero eight zero "
                "deadline two zero two six dash zero six dash one five T one four colon three zero colon zero five Z"
            ),
            "the api returned HTTP 404 port 8080 deadline 2026-06-15T14:30:05Z",
        )
        self.assertEqual(
            _prepare_en_itn_input("press control plus C then command plus shift plus P and alt plus F four"),
            "press Ctrl+C then Cmd+Shift+P and Alt+F4",
        )
        self.assertEqual(
            _prepare_en_itn_input("meeting at fourteen thirty and backup at seven oh five"),
            "meeting at 14:30 and backup at 07:05",
        )
        self.assertEqual(
            _prepare_en_itn_input("meet at noon and leave at midnight"),
            "meet at 12:00 and leave at 00:00",
        )
        self.assertEqual(
            _prepare_en_itn_input("meeting at a quarter past three and reminder at a quarter to four"),
            "meeting at 03:15 and reminder at 03:45",
        )
        self.assertEqual(
            _prepare_en_itn_input("call at half past nine and callback time quarter past ten"),
            "call at 09:30 and callback time 10:15",
        )
        self.assertEqual(
            _prepare_en_itn_input("appointment at three thirty in the afternoon"),
            "appointment at 03:30 PM",
        )
        self.assertEqual(
            _prepare_en_itn_input("check by nine zero five in the morning and after seven thirty in the evening"),
            "check by 09:05 AM and after 07:30 PM",
        )
        self.assertEqual(
            _prepare_en_itn_input("duration one and a half hours distance two and a half miles"),
            "duration 1.5 hours distance 2.5 miles",
        )
        self.assertEqual(
            _prepare_en_itn_input("save twenty percent off buy two get one free limit three per person"),
            "save twenty percent off buy 2 get 1 free limit three per person",
        )
        self.assertEqual(
            _prepare_en_itn_input("rating four point eight out of five score nine out of ten n p s eight out of ten"),
            "rating 4.8/5 score 9/10 NPS 8/10",
        )
        self.assertEqual(
            _prepare_en_itn_input("open monday to friday and saturday to sunday"),
            "open monday-friday and saturday-sunday",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "office hours nine to six thirty meeting fourteen thirty to fifteen forty five"
            ),
            "office hours 09:00-18:30 meeting 14:30-15:45",
        )
        self.assertEqual(
            _prepare_en_itn_input("business hours nine to eighteen"),
            "business hours 09:00-18:00",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "temperature twenty to thirty degrees celsius "
                "body temperature thirty six point five to thirty seven point two degrees celsius"
            ),
            "temperature 20-30°C body temperature 36.5-37.2°C",
        )
        self.assertEqual(
            _prepare_en_itn_input("the event is january second twenty twenty six and february first twenty twenty six"),
            "the event is 2026-01-02 and 2026-02-01",
        )
        self.assertEqual(
            _prepare_en_itn_input("the meeting is june fifteen twenty twenty six and jun sixteen twenty twenty six"),
            "the meeting is 2026-06-15 and 2026-06-16",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "date twenty twenty six dot zero six dot fifteen "
                "deadline twenty twenty six dot six dot five due date twenty twenty six dot oh five dot o nine"
            ),
            "date 2026.06.15 deadline 2026.06.05 due date 2026.05.09",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "the deadline is fifteenth of june twenty twenty six and june fifteenth twenty twenty six"
            ),
            "the deadline is 2026-06-15 and 2026-06-15",
        )
        self.assertEqual(
            _prepare_en_itn_input("due on june the fifteenth twenty twenty six"),
            "due on 2026-06-15",
        )
        self.assertEqual(
            _prepare_en_itn_input("meeting on the fifteenth of june twenty twenty six"),
            "meeting on 2026-06-15",
        )
        self.assertEqual(
            _prepare_en_itn_input("deadline six fifteen twenty twenty six"),
            "deadline 2026-06-15",
        )
        self.assertEqual(
            _prepare_en_itn_input(
                "deadline two zero two six dash zero six dash one five one four colon three zero colon zero five"
            ),
            "deadline 2026-06-15 14:30:05",
        )
        self.assertEqual(
            _compact_en_itn_spacing("it is 72 degrees fahrenheit and 300 kelvin"),
            "it is 72°F and 300 K",
        )
        self.assertEqual(
            _compact_en_itn_spacing("it is 23.5 degrees celsius and negative 3.5 degrees celsius"),
            "it is 23.5°C and -3.5°C",
        )
        self.assertEqual(
            _compact_en_itn_spacing(
                "temperature 23 degrees celsius temp minus five degrees fahrenheit area 80 square yards"
            ),
            "temperature 23°C temp -5°F area 80 yd²",
        )
        self.assertEqual(
            _compact_en_itn_spacing("ratio 1/2 complete 3/4 probability one 8th"),
            "ratio 1/2 complete 3/4 probability 1/8",
        )
        self.assertEqual(_compact_en_itn_spacing("lot twelve hundred square feet"), "lot 1200 ft²")
        self.assertEqual(
            _prepare_en_itn_input(
                "room one two zero eight suite three zero five apartment five B "
                "floor twelve level three zip one zero zero zero one dash one two three four"
            ),
            "room 1208 suite 305 apartment 5B floor 12 level 3 zip 10001-1234",
        )
        self.assertEqual(
            _prepare_en_itn_input("invoice I N V dash twenty twenty six dash zero zero one"),
            "invoice INV-2026-001",
        )
        self.assertEqual(
            _prepare_en_itn_input("apartment five b building two unit three room five zero two"),
            "apartment 5B building 2 unit 3 room 502",
        )
        self.assertEqual(
            _prepare_en_itn_input("twenty first century third floor twelfth grade first place"),
            "21st century 3rd floor 12th grade 1st place",
        )
        self.assertEqual(
            _prepare_en_itn_input("rank first to third floors second to fifth"),
            "rank 1st-3rd floors 2nd-5th",
        )
        self.assertEqual(
            _prepare_en_itn_input("um I paid twelve bucks and fifty cents"),
            "I paid $12.50",
        )
        self.assertEqual(
            _prepare_en_itn_input("I have one buck zero five and two bucks fifty"),
            "I have $1.05 and $2.50",
        )
        self.assertEqual(
            _normalize_en_itn_time_oh("meet at seven oh five and eleven thirty pm"),
            "meet at seven o five and eleven thirty pm",
        )
        self.assertEqual(_normalize_en_itn_time_oh("meet at zero seven oh five"), "meet at seven o five")

    def test_en_itn_helper_normalizes_unit_prefix_words(self) -> None:
        self.assertEqual(
            _prepare_en_itn_input("energy five kilowatt hours current twenty milliamperes"),
            "energy five kilo watt hours current twenty milli amperes",
        )

    def test_en_itn_helper_normalizes_equals_sign_phrases(self) -> None:
        self.assertEqual(_prepare_en_itn_input("parameter q equals sign hello"), "parameter q=hello")

    def test_en_itn_finalize_outputs_restores_spoken_markup(self) -> None:
        self.assertEqual(
            finalize_outputs(["title: customer info new line phone number 415-555-0123"]),
            ["title: customer info\nphone number 415-555-0123"],
        )
        self.assertEqual(
            finalize_outputs(["status: pending dash waiting slash review"]),
            ["status: pending-waiting/review"],
        )
        self.assertEqual(
            finalize_outputs(["account john at sign example underscore corp hash sign vip parameter q=hello"]),
            ["account john@example_corp#vip parameter q=hello"],
        )
        self.assertEqual(
            finalize_outputs(["password A plus sign B minus sign C asterisk D percent sign code A ampersand B"]),
            ["password A+B-C*D% code A&B"],
        )
        self.assertEqual(
            finalize_outputs(["verified check mark failed cross mark status pending"]),
            ["verified✓failed×status pending"],
        )
        self.assertEqual(
            finalize_outputs(["name tab character John new line notes blank line done"]),
            ["name\tJohn\nnotes\n\ndone"],
        )
        self.assertEqual(
            finalize_outputs(["bullet point check ID new line bullet point confirm phone"]),
            ["- check ID\n- confirm phone"],
        )
        self.assertEqual(
            finalize_outputs(
                ["heading one meeting notes new line heading level two action items new line bullet point confirm phone"],
            ),
            ["# meeting notes\n## action items\n- confirm phone"],
        )
        self.assertEqual(
            finalize_outputs(["number one confirm ID new line number two confirm phone"]),
            ["1. confirm ID\n2. confirm phone"],
        )
        self.assertEqual(
            finalize_outputs(["bold start urgent case bold end new line code start status_code code end"]),
            ["**urgent case**\n`status_code`"],
        )
        self.assertEqual(
            finalize_outputs(["template open brace name: John close brace tag left angle bracket vip right angle bracket"]),
            ["template{name: John}tag<vip>"],
        )
        self.assertEqual(
            finalize_outputs(["windows C: backslash Users backslash test regex A pipe B tilde tmp"]),
            ["windows C:\\Users\\test regex A|B~tmp"],
        )


if __name__ == "__main__":
    unittest.main()
