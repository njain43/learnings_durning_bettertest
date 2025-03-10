from src.random_program.fix_repeating_groups import parse_fix_message

fixbuffer = "8=FIX.4.4|35=D|34=2|49=SENDER|56=TARGET|11=123456|"
fixbuffer += "453=2|448=ID1|447=D|452=1|448=ID2|447=D|452=2|10=128|"

fix_fields, repeating_groups = parse_fix_message(fixbuffer)

print("FIX Fields:", fix_fields)
print("Repeating Groups:", repeating_groups)


