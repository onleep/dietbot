from io import BytesIO

import matplotlib.pyplot as plt


async def progress(logged_water: list, logged_calories: list) -> bytes:
    dates = [list(entry.keys())[0] for entry in logged_calories]
    water = [list(entry.values())[0] for entry in logged_water]
    calories = [list(entry.values())[0] for entry in logged_calories]

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#242333')
    ax.set_facecolor('#242333')

    width = 0.5
    x = list(range(len(dates)))
    ax.bar([i + width - 0.9 for i in x], water, width=width, label='Вода')
    ax.bar([i - width for i in x], calories, width=width, label='Калории')
    ax.tick_params(axis='x', colors='white', labelsize=15)
    ax.tick_params(axis='y', colors='white', labelsize=15)

    ax.set_xticks([i - width + 0.05 for i in x])
    ax.set_xticklabels(dates)
    ax.legend()

    img_bytes = BytesIO()
    plt.savefig(img_bytes, dpi=200)
    plt.close(fig)
    img_bytes.seek(0)
    img = img_bytes.getvalue()
    return img
