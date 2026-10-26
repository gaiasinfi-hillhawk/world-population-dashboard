import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="World Population Dashboard",
    page_icon="🌍",
    layout="wide"
)

df = pd.read_csv("world_population.csv")

st.title("🌍 World Population Dashboard")
st.write("Explore population data from countries and territories around the world.")

# Dataset overview
st.subheader("Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Countries and Territories", len(df))

with col2:
    st.metric("Data Columns", len(df.columns))

# Filter countries by continent
st.subheader("Explore a Country")

continents = ["All Continents"] + sorted(df["Continent"].unique().tolist())

selected_continent = st.selectbox(
    "Filter by continent",
    continents
)

if selected_continent == "All Continents":
    filtered_df = df
else:
    filtered_df = df[df["Continent"] == selected_continent]


country_search = st.text_input(
    "Search for a country",
    placeholder="Type a country name, e.g. India"
)

available_countries = sorted(
    filtered_df["Country/Territory"].tolist()
)

if country_search:
    matching_countries = [
        name for name in available_countries
        if country_search.lower() in name.lower()
    ]
else:
    matching_countries = available_countries

if matching_countries:
    country = st.selectbox(
        "Choose a country or territory",
        matching_countries
    )
else:
    st.warning("No matching country found. Try another name.")
    st.stop()


selected_country = df[
    df["Country/Territory"] == country
].iloc[0]

st.write(f"**Capital:** {selected_country['Capital']}")
st.write(f"**Continent:** {selected_country['Continent']}")

population = int(selected_country["2022 Population"])
st.metric("Population in 2022", f"{population:,}")

# Population comparison chart
years = ["1970", "1980", "1990", "2000", "2010", "2015", "2020", "2022"]
populations = [
    int(selected_country["1970 Population"]),
    int(selected_country["1980 Population"]),
    int(selected_country["1990 Population"]),
    int(selected_country["2000 Population"]),
    int(selected_country["2010 Population"]),
    int(selected_country["2015 Population"]),
    int(selected_country["2020 Population"]),
    int(selected_country["2022 Population"])
]

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(years, populations, marker="o")
ax.set_title(f"Population Trend: {country}")
ax.set_xlabel("Year")
ax.set_ylabel("Population")
ax.ticklabel_format(axis="y", style="plain")
ax.grid(alpha=0.3)

st.pyplot(fig)
plt.close(fig)
# Compare populations of multiple countries
st.subheader("Compare Countries")

comparison_countries = st.multiselect(
    "Choose countries to compare",
    sorted(df["Country/Territory"].tolist()),
    default=["India", "China", "United States"]
)

if comparison_countries:
    comparison_df = df[
        df["Country/Territory"].isin(comparison_countries)
    ]

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    ax2.bar(
        comparison_df["Country/Territory"],
        comparison_df["2022 Population"],
        color="skyblue",
        width=0.6
    )

    ax2.set_title("Population Comparison in 2022")
    ax2.set_xlabel("Country")
    ax2.set_ylabel("Population")
    ax2.set_ylim(0, comparison_df["2022 Population"].max() * 1.15)
    ax2.grid(axis="y", alpha=0.3)
    ax2.ticklabel_format(axis="y", style="plain")
    ax2.tick_params(axis="x", rotation=30)

    st.pyplot(fig2)
    plt.close(fig2)
# Population by continent
st.subheader("Population by Continent")

continent_population = df.groupby("Continent")["2022 Population"].sum()
continent_population = continent_population.sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(10, 5))

ax3.bar(
    continent_population.index,
    continent_population.values,
    color="lightgreen"
)

ax3.set_title("Total Population by Continent in 2022")
ax3.set_xlabel("Continent")
ax3.set_ylabel("Population")
ax3.ticklabel_format(axis="y", style="plain")
ax3.grid(axis="y", alpha=0.3)

st.pyplot(fig3)
plt.close(fig3)


# Population Statistics
st.subheader("Population Statistics")

stats_continent = st.selectbox(
    "Choose a continent for statistics",
    sorted(df["Continent"].unique().tolist())
)

continent_df = df[df["Continent"] == stats_continent]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Population",
        f"{continent_df['2022 Population'].mean():,.0f}"
    )

with col2:
    st.metric(
        "Highest Population",
        f"{continent_df['2022 Population'].max():,}"
    )

with col3:
    st.metric(
        "Lowest Population",
        f"{continent_df['2022 Population'].min():,}"
    )
# Top 10 Most Populous Countries
st.subheader("Top 10 Most Populous Countries in 2022")

top_10 = df.nlargest(10, "2022 Population").sort_values(
    "2022 Population",
    ascending=True
)

fig4, ax4 = plt.subplots(figsize=(10, 6))

ax4.barh(
    top_10["Country/Territory"],
    top_10["2022 Population"],
    color="cornflowerblue"
)

ax4.set_xlabel("Population")
ax4.set_ylabel("Country")
ax4.set_title("Top 10 Countries by Population")
ax4.ticklabel_format(axis="x", style="plain")
ax4.grid(axis="x", alpha=0.3)

st.pyplot(fig4)
plt.close(fig4)
# CRUD: Country Record Management
st.header("🗂️ Country Record Management")

st.write("Add, view, edit, or delete country records.")

crud_action = st.selectbox(
    "Choose an operation",
    ["View Records", "Add Record", "Update Record", "Delete Record"]
)

if crud_action == "View Records":
    st.dataframe(df, use_container_width=True)

elif crud_action == "Add Record":
    st.subheader("Add a New Country Record")

    new_country = st.text_input("Country/Territory Name")
    new_capital = st.text_input("Capital")
    new_continent = st.selectbox(
        "Continent",
        sorted(df["Continent"].unique().tolist())
    )
    new_population = st.number_input(
        "Population in 2022",
        min_value=0,
        step=1
    )

    if st.button("Add Country"):
        if not new_country.strip():
            st.error("Please enter a country name.")

        elif new_country in df["Country/Territory"].values:
            st.error("This country already exists.")

        else:
            new_record = {column: 0 for column in df.columns}
            new_record["Country/Territory"] = new_country.strip()
            new_record["Capital"] = new_capital.strip()
            new_record["Continent"] = new_continent
            new_record["2022 Population"] = new_population

            updated_df = pd.concat(
                [df, pd.DataFrame([new_record])],
                ignore_index=True
            )

            updated_df.to_csv("world_population.csv", index=False)
            st.success(f"{new_country} was added successfully!")
            st.rerun()
        
elif crud_action == "Update Record":
    st.subheader("Update a Country Record")

    country_to_update = st.selectbox(
        "Choose a country to update",
        sorted(df["Country/Territory"].tolist())
    )

    record = df[
        df["Country/Territory"] == country_to_update
    ].iloc[0]

    updated_capital = st.text_input(
        "Capital",
        value=str(record["Capital"])
    )

    updated_population = st.number_input(
        "Population in 2022",
        min_value=0,
        value=int(record["2022 Population"]),
        step=1
    )

    if st.button("Save Changes"):
        df.loc[
            df["Country/Territory"] == country_to_update,
            "Capital"
        ] = updated_capital.strip()

        df.loc[
            df["Country/Territory"] == country_to_update,
            "2022 Population"
        ] = updated_population

        df.to_csv("world_population.csv", index=False)

        st.success(f"{country_to_update} was updated successfully!")
        st.rerun()
elif crud_action == "Delete Record":
    st.subheader("Delete a Country Record")

    country_to_delete = st.selectbox(
        "Choose a country to delete",
        sorted(df["Country/Territory"].tolist())
    )

    st.warning(
        f"You are about to delete: {country_to_delete}"
    )

    confirm_delete = st.checkbox(
        "I confirm that I want to delete this record"
    )

    if st.button("Delete Country"):
        if confirm_delete:
            updated_df = df[
                df["Country/Territory"] != country_to_delete
            ]

            updated_df.to_csv("world_population.csv", index=False)

            st.success(
                f"{country_to_delete} was deleted successfully!"
            )
            st.rerun()
        else:
            st.error("Please confirm deletion first.")


