import random

def generate_multiple_timetables(teachers, days, periods_per_day, num_timetables):
    timetables = [
        [[None for _ in range(periods_per_day)] for _ in range(len(days))]
        for _ in range(num_timetables)
    ]

    for t_index in range(num_timetables):
        for t in teachers:
            remaining = t["periods"]
            span = t.get("span", 1)

            attempts = 0
            while remaining > 0 and attempts < 500:
                attempts += 1
                d = random.randint(0, len(days) - 1)
                p = random.randint(0, periods_per_day - span)

                if any(timetables[t_index][d][pp] is not None for pp in range(p, p + span)):
                    continue

                timetables[t_index][d][p] = {
                    "text": f"{t['subject']} - {t['name']}",
                    "colspan": span
                }

                for pp in range(p + 1, p + span):
                    timetables[t_index][d][pp] = "SKIP"

                remaining -= span

    # Fill remaining slots (no empty cells)
    for table in timetables:
        fillers = [f"{t['subject']} - {t['name']}" for t in teachers]
        idx = 0
        for d in range(len(days)):
            for p in range(periods_per_day):
                if table[d][p] is None:
                    table[d][p] = fillers[idx % len(fillers)]
                    idx += 1

    return timetables
