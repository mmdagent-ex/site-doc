import re

def generate_response(str):
    if str == "こんにちは。":
        return "こんにちは。"
    return "わかりません。"

def main():
    while True:
        instr = input().strip()
        if not instr:
            break
        utterance = re.findall('^RECOG_EVENT_STOP\|(.*)$', instr)
        if utterance:
            print(utterance)
            outstr = generate_response(utterance[0])
            print(f"SYNTH_START|0|mei_voice_normal|{outstr}")

if __name__ == "__main__":
    main()
