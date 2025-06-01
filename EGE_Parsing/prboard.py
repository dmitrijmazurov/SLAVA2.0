import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Сначала сделаем все необходимые переменные,а потом уже приступим к рисовке графиков

@st.cache_data
def load_data():
    return pd.read_csv('slava2.0_pt.csv')

df = load_data()
df = df.dropna(subset=['subject', 'type'])

#Фильтр
all_subjects = sorted(df['subject'].unique())
selected_subjects = st.multiselect("Выберите предметы", all_subjects, default=all_subjects)
filtered_df = df[df['subject'].isin(selected_subjects)]

# Группируем
grouped = (filtered_df.groupby(['subject', 'type']).size().reset_index(name='count'))

pivot_df = grouped.pivot(index='subject', columns='type', values='count').fillna(0)
 
# Перевод 
subject_labels = {
    "bio": "Биология",
    "fr": "Французский",
    "inf": "Информатика",
    "math": "Мат (проф.)",
    "mathb": "Мат (баз.)",
    "phys": "Физика",
    "sp": "Испанский"
}
pivot_df.index = [subject_labels.get(x, x) for x in pivot_df.index]






# График
st.title("Количество вопросов по предмету и типу")

fig, ax = plt.subplots(figsize=(10, 4), facecolor='#d9d9d9')
ax.set_facecolor('white')

# Жёсткое сопоставление цветов к типам
type_color_map = {
    "аудирование": '#e5f0e5',
    "выбор ответа (один)": '#cccccc',
    "множественный выбор": '#7f7f7f',
    "неизвестно": '#4d4d4d',
    "открытый ответ": '#2d6b2d',
    "соответствие": '#cce5cc',
}

# Только те, которые есть в таблице, ибо была ошибка почему-то
present_types = list(pivot_df.columns)
custom_colors = [type_color_map.get(t, '#999999') for t in present_types]

# Жёсткий порядок колонок
pivot_df = pivot_df[present_types]

# Построение графика
pivot_df.plot(
    kind='bar',
    ax=ax,
    width=1,
    color=custom_colors,
    edgecolor='white'
)

# оси все дела
ax.set_title("Количество вопросов по предмету и типу", fontweight='bold', pad=10)
ax.set_ylabel("Кол-во", labelpad=10)
ax.set_xticklabels(pivot_df.index, rotation=0, ha='center', fontsize=10, wrap=True)
ax.grid(True, axis='y', linestyle='--', alpha=0.6)
ax.legend(title="Вид вопроса", loc='upper right', frameon=True, edgecolor='gray')

# выставим нижнюю границу, потому что не видно было
ax.set_ylim(bottom=50)
st.pyplot(fig)











# Другой график
st.markdown("---")
st.title("Общее количество заданий по каждому предмету")

# Подсчёт заданий по subject
subject_counts = filtered_df['subject'].value_counts().sort_values(ascending=False)


subject_counts.index = [subject_labels.get(subj, subj) for subj in subject_counts.index]

# Построение графика
fig2, ax2 = plt.subplots(figsize=(10, 4), facecolor='#d9d9d9')
ax2.set_facecolor('white')

subject_counts.plot(kind='bar', ax=ax2, color='#cce5cc', edgecolor='black')

ax2.set_title("Количество заданий по каждому предмету", fontweight='bold', pad=10)
ax2.set_ylabel("Кол-во")
ax2.set_xticklabels(subject_counts.index, rotation=0, ha='center', fontsize=10)
ax2.grid(True, axis='y', linestyle='--', alpha=0.6)
st.pyplot(fig2)







# Еще один график
st.markdown("---")
st.title("Количество заданий с прикреплёнными файлами по предметам")

df_comment = filtered_df.copy()

# Есть ссылка или нету
df_comment["Комментарий"] = df_comment["comment"].apply(
    lambda x: "Есть файл" if pd.notna(x) and str(x).startswith("http") else "Без файла"
)

#Группировка
grouped = (df_comment.groupby(["subject", "Комментарий"]).size().reset_index(name="count"))

comment_pivot = grouped.pivot(index="subject", columns="Комментарий", values="count").fillna(0)

# Перевод 
comment_pivot.index = [subject_labels.get(x, x) for x in comment_pivot.index]

# Сортировка колонок
cols = [col for col in comment_pivot.columns if col != "Без файла"] + ["Без файла"]
comment_pivot = comment_pivot[cols]

# Цвета
custom_colors = ["#2d6b2d", "#cccccc"]

# График
fig3, ax3 = plt.subplots(figsize=(10, 4), facecolor="#d9d9d9")
ax3.set_facecolor("white")

comment_pivot.plot(
    kind="bar",
    stacked=True,
    ax=ax3,
    width=0.6,
    color=custom_colors
)

ax3.set_title("Задания по предметам с файлами в комментариях", fontweight="bold", pad=10)
ax3.set_ylabel("Кол-во")
ax3.set_xticklabels(comment_pivot.index, rotation=0, ha="center", fontsize=10)
ax3.legend(title="Комментарий", frameon=True, edgecolor="gray", loc="upper right")
ax3.grid(True, axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig3)

