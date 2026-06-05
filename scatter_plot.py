import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

data = {
    "income_group": ["하", "중하", "중", "중상", "상"],
    "drinking_drop": [6.0, 0.9, 5.0, 0.2, 1.2],
    "participation_drop": [6.967, 4.289, 4.324, 3.000, 2.405]
}

df = pd.DataFrame(data)

plt.figure(figsize=(8,6))

plt.scatter(
    df["drinking_drop"],
    df["participation_drop"]
)

for i in range(len(df)):
    plt.text(
        df["drinking_drop"][i],
        df["participation_drop"][i],
        df["income_group"][i]
    )

plt.xlabel("음주율 감소폭")
plt.ylabel("단체참여율 감소폭")
plt.title("음주율 감소폭과 단체참여 감소폭")

plt.grid(True)

plt.show()