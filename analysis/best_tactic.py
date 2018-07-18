1, 5
2, 4
3, 3
4, 2
5, 1
6, 0

tactics = [
    (0, 6),
    (1, 5),
    (2, 4),
    (3, 3),
    (4, 2),
    (5, 1),
    (6, 0)
]


def get_good_day(tactic):
    inshore, outshore = tactic
    return sum([inshore * 3, outshore * 5])


def get_bad_day(tactic):
    inshore, outshore = tactic
    return sum([inshore * 5, outshore * -6])


def sort_tactics(ts):
    if len(ts) <= 1:
        return ts

    pivot = ts[0]["predicted"]

    lt, gt, eq = [], [], []

    for t in ts:
        value = t["predicted"]

        if value < pivot:
            lt.append(t)

        elif value > pivot:
            gt.append(t)

        else:
            eq.append(t)

    return sort_tactics(lt) + eq + sort_tactics(gt)


for i in range(len(tactics)):
    tactic = tactics[i]
    good_day, bad_day = get_good_day(tactic), get_bad_day(tactic)

    predicted_earning = sum(
        [
            (5/54) * (bad_day - 150),
            (5/18) * bad_day,
            (5/6) * bad_day,
            (205/54) * good_day
        ]
    )

    tactics[i] = {
        "predicted": predicted_earning,
        "profit": predicted_earning - 80,
        "tactic": tactic
    }

tactics = sort_tactics(tactics)[::-1]
best = tactics[0]

print("The best tactic is...")
print("Inshore: {}, Outshore: {}".format(best["tactic"][0], best["tactic"][1]))

print("")

print("This is the best tactic, becuase it leaves you with a profit of £{} at the end of the week.".format(
    round(best["profit"] * 100)/100))

print(len("This is the best tactic, becuase it leaves you with a profit of £{} at the end of the week.".format(
    round(best["profit"] * 100)/100)) * "=")

print("")

print("Runners Up:")
print(
    "2. ({}, {}) -> Profit: {}".format(tactics[1]["tactic"]
                                       [0], tactics[1]["tactic"][0], round(tactics[1]["profit"] * 100) / 100)
)
print("3. ({}, {}) -> Profit: {}".format(
    tactics[2]["tactic"][0], tactics[2]["tactic"][0], round(tactics[2]["profit"] * 100 / 100)))

print("4. ({}, {}) -> Profit: {}".format(
    tactics[3]["tactic"][0], tactics[3]["tactic"][0], round(tactics[3]["profit"] * 100) / 100))
