# MINDMATE - Mental Wellness and Stress Management System

from datetime import datetime
import time

records = []
points = 0
current_language = "E"

def t(en, hi):
    return en if current_language == "E" else hi

def choose_language():
    global current_language
    print("\n1. English")
    print("2. Hindi")
    choice = input("Choose Language / भाषा चुनें: ").strip()
    current_language = "H" if choice == "2" else "E"
    print(t("Language selected successfully.", "भाषा सफलतापूर्वक चुनी गई।"))

def line():
    print("=" * 62)

def pause():
    input(t("\nPress ENTER to continue...", "\nजारी रखने के लिए ENTER दबाएँ..."))

def get_num(msg, low, high):
    while True:
        try:
            n = float(input(msg))
            if low <= n <= high:
                return n
            print(t("Enter a value from", "मान दर्ज करें"), low, t("to", "से"), high)
        except ValueError:
            print(t("Please enter a number.", "कृपया सही संख्या दर्ज करें।"))

def get_int(msg, low, high):
    return int(get_num(msg, low, high))

def get_text(msg):
    while True:
        x = input(msg).strip()
        if x:
            return x
        print(t("Please enter something.", "कृपया कुछ दर्ज करें।"))

def latest(name):
    for r in reversed(records):
        if r["name"].lower() == name.lower():
            return r
    return None

def mood_check():
    print(t("\nMOOD CHECK", "\nमूड जाँच"))
    moods = ["Very low", "Low", "Okay", "Good", "Very good"]
    for i, mood in enumerate(moods, 1):
        print(i, mood)
    n = get_int(t("Choose: ", "चुनें: "), 1, 5)
    return moods[n - 1], n

def sleep_check():
    hours = get_num(t("Hours of sleep: ", "नींद के घंटे: "), 0, 24)
    print(t("Sleep quality: 1 Poor  2 Fair  3 Good  4 Very good  5 Excellent", "नींद की गुणवत्ता: 1 खराब  2 सामान्य  3 अच्छी  4 बहुत अच्छी  5 उत्कृष्ट"))
    quality = get_int(t("Choose: ", "चुनें: "), 1, 5)
    return hours, quality

def stress_questions():
    qs = [
        "How often have you felt unable to relax?",
        "How often have you felt under pressure?",
        "How often have you found it hard to focus?",
        "How often have you felt overwhelmed by tasks?",
        "How often have you worried about upcoming work?",
        "How often have things felt difficult to manage?"
    ]
    total = 0
    print(t("\nSTRESS CHECK", "\nतनाव जाँच"))
    print(t("1 = Never  2 = Sometimes  3 = Often  4 = Very often", "1 = कभी नहीं  2 = कभी-कभी  3 = अक्सर  4 = बहुत अक्सर"))
    for q in qs:
        print("\n" + t(q, {
        "How often have you felt unable to relax?":"आपने कितनी बार महसूस किया कि आप आराम नहीं कर पा रहे हैं?",
        "How often have you felt under pressure?":"आपने कितनी बार दबाव महसूस किया है?",
        "How often have you found it hard to focus?":"आपको कितनी बार ध्यान केंद्रित करने में कठिनाई हुई है?",
        "How often have you felt overwhelmed by tasks?":"आपने कितनी बार कामों से बहुत अधिक दबाव महसूस किया है?",
        "How often have you worried about upcoming work?":"आपने आने वाले काम को लेकर कितनी बार चिंता की है?",
        "How often have things felt difficult to manage?":"आपको कितनी बार लगा कि चीज़ों को संभालना कठिन है?"
    }[q]))
        total += get_int(t("Answer: ", "उत्तर: "), 1, 4)
    return total

def stress_level(score):
    if score <= 9:
        return "LOW", "😊"
    if score <= 16:
        return "MODERATE", "🌤️"
    if score <= 20:
        return "HIGH", "⚠️"
    return "VERY HIGH", "⚠️"

def wellness_score(mood, sleep_quality, hours, pressure, energy, focus, support, stress):
    score = mood * 3 + sleep_quality * 3
    if 7 <= hours <= 9:
        score += 10
    elif 6 <= hours <= 10:
        score += 7
    else:
        score += 3
    score += (6 - pressure) * 2
    score += energy * 2 + focus * 2 + support * 2
    score += max(0, 25 - stress)
    return min(100, max(0, score))

def wellness_status(score):
    if score >= 85:
        return "Excellent 🌟"
    if score >= 70:
        return "Good 😊"
    if score >= 55:
        return "Fair 🌱"
    if score >= 40:
        return "Needs attention 🟠"
    return "Needs more support 💙"

def rule_based_insight(r):
    issues = []
    if r["stress"] >= 17:
        issues.append("stress is currently high")
    if r["sleep"] < 7:
        issues.append("sleep is below 7 hours")
    if r["energy"] <= 2:
        issues.append("energy is low")
    if r["focus"] <= 2:
        issues.append("concentration is low")
    if r["support"] <= 2:
        issues.append("support feels limited")
    if not issues:
        return "Your current responses show a fairly balanced pattern. Keep your helpful routines going."
    return "Main areas to watch: " + ", ".join(issues) + "."

def assessment(name, age):
    global points
    line()
    print("COMPLETE WELLNESS ASSESSMENT")
    line()
    mood, mood_score = mood_check()
    hours, sleep_quality = sleep_check()
    pressure = get_int(t("Study/work pressure (1-5): ", "पढ़ाई/काम का दबाव (1-5): "), 1, 5)
    energy = get_int(t("Energy level (1-5): ", "ऊर्जा स्तर (1-5): "), 1, 5)
    focus = get_int(t("Concentration level (1-5): ", "एकाग्रता स्तर (1-5): "), 1, 5)
    support = get_int(t("Social support (1-5): ", "सामाजिक सहयोग (1-5): "), 1, 5)
    stress = stress_questions()
    level, icon = stress_level(stress)
    wellness = wellness_score(mood_score, sleep_quality, hours, pressure, energy, focus, support, stress)
    r = {
        "name": name, "age": age,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "mood": mood, "sleep": hours, "sleep_quality": sleep_quality,
        "pressure": pressure, "energy": energy, "focus": focus, "support": support,
        "stress": stress, "level": level, "icon": icon, "wellness": wellness
    }
    records.append(r)
    points += 20
    show_result(r)
    return r

def recommendations(r):
    print("\nPERSONALIZED SUGGESTIONS")
    if r["stress"] >= 17:
        print("• Break large tasks into smaller steps and talk to someone you trust if needed.")
    elif r["stress"] >= 10:
        print("• Take regular breaks and keep your daily workload manageable.")
    else:
        print("• Continue supportive routines and make time for rest.")
    if r["sleep"] < 7:
        print("• Protect enough time for regular sleep.")
    if r["pressure"] >= 4:
        print("• Prioritize urgent work instead of trying to finish everything together.")
    if r["energy"] <= 2:
        print("• Add short rest periods and simple daily self-care.")
    if r["focus"] <= 2:
        print("• Try short focused study sessions with breaks.")
    if r["support"] <= 2:
        print("• Consider connecting with a trusted friend, family member, teacher or counselor.")

def show_result(r):
    line()
    print(t("ASSESSMENT RESULT", "आकलन परिणाम"))
    line()
    print("Mood           :", r["mood"])
    print("Sleep          :", r["sleep"], "hours")
    print("Sleep quality  :", r["sleep_quality"], "/5")
    print("Pressure       :", r["pressure"], "/5")
    print("Energy         :", r["energy"], "/5")
    print("Concentration  :", r["focus"], "/5")
    print("Support        :", r["support"], "/5")
    print("Stress score   :", r["stress"], "/24")
    print("Stress level   :", r["level"], r["icon"])
    print("Wellness score :", r["wellness"], "/100")
    print("Status         :", wellness_status(r["wellness"]))
    print(t("\nRULE-BASED INSIGHT", "\nनियम-आधारित जानकारी"))
    print(rule_based_insight(r))
    recommendations(r)
    print("\nThis is an educational rule-based wellness model. The score is a project-defined indicator, not a clinical measure or diagnosis.")

def dashboard(name):
    r = latest(name)
    line()
    print(t("PERSONAL DASHBOARD", "व्यक्तिगत डैशबोर्ड"))
    line()
    if not r:
        print(t("Complete an assessment first.", "पहले एक आकलन पूरा करें।"))
        return
    total = sum(1 for x in records if x["name"].lower() == name.lower())
    print("Name          :", r["name"])
    print("Last check-in :", r["date"])
    print("Mood          :", r["mood"])
    print("Stress        :", r["stress"], "/24 -", r["level"])
    print("Wellness      :", r["wellness"], "/100")
    print("Status        :", wellness_status(r["wellness"]))
    print("Assessments   :", total)
    print("Points        :", points)
    print("\nRule-based insight :", rule_based_insight(r))

def history(name):
    mine = [r for r in records if r["name"].lower() == name.lower()]
    line()
    print(t("WELLNESS HISTORY", "वेलनेस इतिहास"))
    line()
    if not mine:
        print(t("No previous assessments found.", "कोई पिछला आकलन नहीं मिला।"))
        return
    for i, r in enumerate(mine, 1):
        print(i, r["date"], "| Stress:", r["stress"], "| Wellness:", r["wellness"], "| Mood:", r["mood"])
    if len(mine) >= 2:
        old, new = mine[-2], mine[-1]
        print(t("\nLATEST PROGRESS", "\nनवीनतम प्रगति"))
        print("Stress  :", old["stress"], "->", new["stress"])
        print("Wellness:", old["wellness"], "->", new["wellness"])
        if new["wellness"] > old["wellness"]:
            print("🌟 Reported wellness has improved since the previous check-in.")
        elif new["wellness"] < old["wellness"]:
            print("📌 Reported wellness is lower than the previous check-in.")
        else:
            print("➡️ Reported wellness is unchanged.")

def toolkit():
    while True:
        line()
        print(t("WELLNESS TOOLKIT", "वेलनेस टूलकिट"))
        line()
        print(t("1. Breathing exercise", "1. साँस लेने का अभ्यास"))
        print(t("2. Grounding exercise", "2. ग्राउंडिंग अभ्यास"))
        print(t("3. Focus timer", "3. फोकस टाइमर"))
        print(t("4. Return", "4. वापस जाएँ"))
        c = get_int(t("Choose: ", "चुनें: "), 1, 4)
        if c == 1:
            print("\nBreathe in slowly..."); time.sleep(2)
            print("Hold gently..."); time.sleep(2)
            print("Breathe out slowly..."); time.sleep(3)
            print("Repeat if comfortable."); pause()
        elif c == 2:
            print("\nNotice 5 things you can see.")
            print("Notice 4 things you can hear.")
            print("Notice 3 things you can feel.")
            print("Notice 2 things you can smell.")
            print("Notice 1 thing you can taste or imagine tasting."); pause()
        elif c == 3:
            mins = get_int(t("Focus time in minutes (1-10): ", "फोकस समय मिनट में (1-10): "), 1, 10)
            print(t("Focus session started for", "फोकस सत्र शुरू हुआ"), mins, t("minute(s).", "मिनट के लिए।"))
            print(t("This is a simple practice timer, not a productivity measurement.", "यह केवल अभ्यास टाइमर है, उत्पादकता का माप नहीं।"))
            for left in range(mins, 0, -1):
                time.sleep(60)
                print(t("Minutes remaining:", "बचे हुए मिनट:"), left - 1)
            print(t("Focus session complete. Take a short break.", "फोकस सत्र पूरा हुआ। थोड़ा ब्रेक लें।")); pause()
        else:
            break

def goals():
    print("\nTODAY'S WELLNESS PLAN")
    print("1. Take regular study breaks")
    print("2. Drink water regularly")
    print("3. Keep a consistent sleep routine")
    print("4. Spend some time away from screens")
    print("5. Talk to someone you trust if you need support")
    pause()

def chatbot():
    line()
    print(t("MINDMATE CHATBOT", "MINDMATE चैटबॉट"))
    line()
    print(t("Ask about stress, sleep, study pressure, focus, mood or relaxation.", "तनाव, नींद, पढ़ाई का दबाव, एकाग्रता, मूड या आराम के बारे में पूछें।"))
    print(t("Type bye to return.", "वापस जाने के लिए bye लिखें।"))
    while True:
        msg = input(t("You: ", "आप: ")).lower().strip()
        if msg in ["bye", "exit", "quit"]:
            break
        if any(x in msg for x in ["stress", "pressure", "overwhelmed"]):
            print(t("MindMate: Try one small task at a time and take a short break.", "MindMate: एक समय में एक छोटा काम करें और थोड़ा ब्रेक लें।"))
        elif any(x in msg for x in ["sleep", "tired"]):
            print(t("MindMate: A regular sleep routine can support energy and concentration.", "MindMate: नियमित नींद की दिनचर्या ऊर्जा और एकाग्रता में मदद कर सकती है।"))
        elif any(x in msg for x in ["study", "exam", "focus", "concentration"]):
            print(t("MindMate: Try a short focused session followed by a break.", "MindMate: थोड़े समय का केंद्रित अध्ययन करें और फिर ब्रेक लें।"))
        elif any(x in msg for x in ["sad", "mood", "lonely"]):
            print(t("MindMate: Consider talking with someone you trust if you are having a difficult day.", "MindMate: यदि दिन कठिन लग रहा है तो किसी भरोसेमंद व्यक्ति से बात करने पर विचार करें।"))
        elif any(x in msg for x in ["relax", "calm"]):
            print(t("MindMate: The breathing and grounding exercises may help you pause.", "MindMate: साँस लेने और ग्राउंडिंग अभ्यास आपको थोड़ी देर रुकने में मदद कर सकते हैं।"))
        else:
            print(t("MindMate: I can help with stress, sleep, study pressure, focus, mood and relaxation.", "MindMate: मैं तनाव, नींद, पढ़ाई का दबाव, एकाग्रता, मूड और आराम से जुड़ी जानकारी दे सकता हूँ।"))

def badges():
    line()
    print(t("WELLNESS BADGES", "वेलनेस बैज"))
    line()
    print("🏅 First Check-In     :", "Unlocked" if len(records) >= 1 else "Locked")
    print("🌱 Three Check-Ins    :", "Unlocked" if len(records) >= 3 else "Locked")
    print("⭐ 100 Wellness Points:", "Unlocked" if points >= 100 else "Locked")
    print("💙 Support Seeker     :", "Unlocked" if any(r["support"] <= 2 for r in records) else "Locked")
    print("📈 Progress Tracker   :", "Unlocked" if len(records) >= 2 else "Locked")
    pause()

def report(name):
    r = latest(name)
    line()
    print(t("COMPLETE WELLNESS REPORT", "पूर्ण वेलनेस रिपोर्ट"))
    line()
    if not r:
        print(t("Complete an assessment first.", "पहले एक आकलन पूरा करें।"))
        return
    print("Name          :", r["name"])
    print("Date          :", r["date"])
    print("Mood          :", r["mood"])
    print("Sleep         :", r["sleep"], "hours")
    print("Pressure      :", r["pressure"], "/5")
    print("Energy        :", r["energy"], "/5")
    print("Concentration :", r["focus"], "/5")
    print("Support       :", r["support"], "/5")
    print("Stress        :", r["stress"], "/24 -", r["level"])
    print("Wellness      :", r["wellness"], "/100")
    print("Status        :", wellness_status(r["wellness"]))
    print("\nRule-based insight :", rule_based_insight(r))
    recommendations(r)
    print("\nNote: Results are educational and not a diagnosis.")

def main():
    global points
    line()
    print("MINDMATE - MENTAL WELLNESS SYSTEM")
    line()
    print(t("Educational wellness and stress-management project.", "यह एक शैक्षणिक वेलनेस और तनाव-प्रबंधन प्रोजेक्ट है।"))
    print(t("It does not diagnose mental-health conditions.", "यह मानसिक स्वास्थ्य की बीमारी का निदान नहीं करता।"))
    choose_language()
    name = get_text(t("Enter your name: ", "अपना नाम दर्ज करें: "))
    age = get_int(t("Enter your age: ", "अपनी उम्र दर्ज करें: "), 5, 100)
    while True:
        line()
        print(t("Hello,", "नमस्ते,"), name)
        print(t("1. Complete Wellness Assessment", "1. पूर्ण वेलनेस आकलन"))
        print(t("2. Personal Dashboard", "2. व्यक्तिगत डैशबोर्ड"))
        print(t("3. Wellness History", "3. वेलनेस इतिहास"))
        print(t("4. Wellness Toolkit", "4. वेलनेस टूलकिट"))
        print(t("5. Today's Wellness Plan", "5. आज की वेलनेस योजना"))
        print(t("6. MindMate Chatbot", "6. MindMate चैटबॉट"))
        print(t("7. Personalized Suggestions", "7. व्यक्तिगत सुझाव"))
        print(t("8. Wellness Badges", "8. वेलनेस बैज"))
        print(t("9. Complete Report", "9. पूर्ण रिपोर्ट"))
        print(t("10. Change Language", "10. भाषा बदलें"))
        print(t("11. Exit", "11. बाहर निकलें"))
        c = get_int(t("Choose: ", "चुनें: "), 1, 11)
        if c == 1:
            assessment(name, age); pause()
        elif c == 2:
            dashboard(name); pause()
        elif c == 3:
            history(name); pause()
        elif c == 4:
            toolkit()
        elif c == 5:
            goals()
        elif c == 6:
            chatbot(); pause()
        elif c == 7:
            r = latest(name)
            if r:
                recommendations(r)
                print("\nRule-based insight:", rule_based_insight(r))
            else:
                print(t("Complete an assessment first.", "पहले एक आकलन पूरा करें।"))
            pause()
        elif c == 8:
            badges()
        elif c == 9:
            report(name); pause()
        elif c == 10:
            choose_language()
        else:
            print(t("\n🏃 MindMate is running away for a break! 😄", "\n🏃 MindMate थोड़ा ब्रेक लेने जा रहा है! 😄"))
            print(t("Take care of your mind, keep learning, and see you next time!", "अपने मन का ध्यान रखें, सीखते रहें और फिर मिलते हैं!"))
            print(t("Final points:", "अंतिम पॉइंट्स:"), points)
            break

if __name__ == "__main__":
    main()
