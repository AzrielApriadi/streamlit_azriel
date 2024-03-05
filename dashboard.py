import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st


sns.set(style='dark')

all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.header("Pilih Rentang Waktu")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date,
        value=[min_date, max_date]
    )


main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]


st.header('Bike Sharing Dashboard')

col1, col2, col3 = st.columns(3)
with col1:
    total_sewa = main_df['cnt'].sum()
    st.metric("Total Penyewa Sepeda", value=total_sewa)

with col2:
    total_sewa_tidak_terdaftar = main_df['casual'].sum()
    st.metric("Total Penyewa Tidak Terdaftar", value=total_sewa_tidak_terdaftar)

with col3:
    total_sewa_terdaftar = main_df['registered'].sum()
    st.metric("Total Penyewa Terdaftar", value=total_sewa_terdaftar)


total_casual = main_df['casual'].sum()
total_registered = main_df['registered'].sum()
total_penyewa = total_casual + total_registered

casual_percentage = (total_casual / total_penyewa) * 100
registered_percentage = (total_registered / total_penyewa) * 100

labels = ['Tidak Terdaftar', 'Terdaftar']
sizes = [casual_percentage, registered_percentage]
colors = sns.color_palette('Set2')
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax.axis('equal') 
plt.title('Persentase perbedaan penyewa casual (Tidak terdaftar) dan registered (Terdaftar)')
st.pyplot(fig)


st.subheader('Performa penyewaan sepeda pada tiap musim yang berbeda')

data_musim = main_df.groupby(by="season").agg({
    "cnt": "sum"})

sns.set_palette("Set2")

fig, ax = plt.subplots()
plt.bar(data_musim.index, data_musim['cnt'], color=sns.color_palette())
plt.xlabel('Season')
plt.title('Jumlah Penyewa Sepeda berdasarkan Musim dari 2011-2012')

for index, value in enumerate(data_musim['cnt']):
    plt.text(index, value + 5, str(value), ha='center', va='bottom')

st.pyplot(fig)

st.subheader('Performa penyewaan sepeda berdasarkan hari')

data_hari = main_df.groupby(by="weekday").agg({
    "cnt": "sum"})

data_hari = data_hari.sort_values(by='cnt', ascending=True)

sns.set_palette("Dark2")
fig, ax = plt.subplots()
plt.bar(data_hari.index, data_hari['cnt'], color=sns.color_palette())
plt.xlabel('Weekday')
plt.title('Jumlah Penyewa sepeda berdasarkan hari dalam satu minggu')

for index, value in enumerate(data_hari['cnt']):
    plt.text(index, value + 5, str(value), ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')

st.pyplot(fig)

st.subheader('Performa penyewaan sepeda berdasarkan kondisi cuaca')

data_cuaca = main_df.groupby(by="weathersit").agg({
    "cnt": "sum"})

data_cuaca = data_cuaca.sort_values(by='cnt', ascending=True)

sns.set_palette("Dark2")
fig, ax = plt.subplots()
plt.bar(data_cuaca.index, data_cuaca['cnt'], color=sns.color_palette())
plt.xlabel('Kondisi Cuaca')
plt.title('Jumlah Penyewa sepeda berdasarkan kondisi cuaca')

for index, value in enumerate(data_cuaca['cnt']):
    plt.text(index, value + 5, str(value), ha='center', va='bottom')

st.pyplot(fig)

st.subheader('Jam dengan jumlah penyewaan terbanyak dan paling sedikit')

data_jam = main_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(24, 6))
colors = ["#FF6347", "#9370DB", "#20B2AA", "#FFD700", "#008080"]

sns.barplot(x="cnt", y="hr", data=data_jam.head(24).sort_values(by="hr"), palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)

plt.suptitle("Jumlah Penyewaan sepeda berdasarkan jam", fontsize=20)

plt.show()
st.pyplot(fig)
