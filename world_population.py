import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("world_population.csv")

# Select the top 10 most populated countries
top_10 = df.nlargest(10, "2022 Population").copy()

# Convert population into billions
top_10["Population (billions)"] = (
    top_10["2022 Population"] / 1_000_000_000
)

# Create the chart
plt.figure(figsize=(12, 6))
bars = plt.bar(
    top_10["Country/Territory"],
    top_10["Population (billions)"]
)

# Add titles and labels
plt.title("Top 10 Most Populated Countries (2022)")
plt.xlabel("Country")
plt.ylabel("Population (billions)")

# Display the population above each bar
plt.bar_label(bars, fmt="%.2f")

# Improve readability
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

# Save the chart
plt.savefig("top_10_population.png", dpi=300, bbox_inches="tight")
print("Professional chart saved successfully!")

plt.close()
# Stage 6: Find the 10 countries with the highest growth rates
top_growth = df.nlargest(10, "Growth Rate")

print("\nTop 10 Countries by Population Growth Rate")
print(
    top_growth[["Country/Territory", "Growth Rate"]]
    .to_string(index=False)
)
# Stage 6.2: Visualize the top 10 growth rates

top_growth = df.nlargest(10, "Growth Rate").copy()

# Convert growth-rate multipliers into percentages
top_growth["Growth Percentage"] = (
    top_growth["Growth Rate"] - 1
) * 100

plt.figure(figsize=(12, 6))

bars = plt.bar(
    top_growth["Country/Territory"],
    top_growth["Growth Percentage"]
)

plt.title("Top 10 Countries by Population Growth Rate")
plt.xlabel("Country")
plt.ylabel("Growth Rate (%)")
plt.bar_label(bars, fmt="%.2f%%")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "top_10_growth.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("Growth-rate chart saved successfully!")
# Stage 7: Compare population across continents

continent_population = (
    df.groupby("Continent")["2022 Population"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal Population by Continent (2022)")
print(continent_population.to_string())
# Stage 7.2: Visualize population by continent

plt.figure(figsize=(10, 6))

bars = plt.bar(
    continent_population.index,
    continent_population.values / 1_000_000_000
)

plt.title("Total Population by Continent (2022)")
plt.xlabel("Continent")
plt.ylabel("Population (billions)")
plt.bar_label(bars, fmt="%.2f")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "continent_population.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("Continent population chart saved successfully!")
# Stage 8: Analyse population density

top_density = df.nlargest(10, "Density (per km²)")

print("\nTop 10 Countries and Territories by Population Density")
print(
    top_density[["Country/Territory", "Density (per km²)"]]
    .to_string(index=False)
)
# Stage 8.2: Visualize population density

plt.figure(figsize=(12, 6))

bars = plt.bar(
    top_density["Country/Territory"],
    top_density["Density (per km²)"]
)

plt.title("Top 10 Countries and Territories by Population Density")
plt.xlabel("Country or Territory")
plt.ylabel("People per km²")

plt.bar_label(bars, fmt="%.0f")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "population_density.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
print("Population density chart saved successfully!")
# Stage 9: Analyse population change from 1970 to 2022

df["Population Change"] = (
    df["2022 Population"] - df["1970 Population"]
)

top_10_change = df.nlargest(10, "Population Change")

print("\nTop 10 Countries by Population Increase (1970–2022)")
print(
    top_10_change[
        ["Country/Territory", "1970 Population",
         "2022 Population", "Population Change"]
    ].to_string(index=False)
)# Stage 9.2: Visualize population change

plt.figure(figsize=(12, 6))

bars = plt.bar(
    top_10_change["Country/Territory"],
    top_10_change["Population Change"] / 1_000_000
)

plt.title("Top 10 Countries by Population Increase (1970–2022)")
plt.xlabel("Country")
plt.ylabel("Population Increase (Millions)")

plt.bar_label(bars, fmt="%.0f")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "population_change.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Population-change chart saved successfully!")
# Stage 10: Compare population in 1970 and 2022

top_10_2022 = df.nlargest(10, "2022 Population")

print("\nPopulation Comparison: 1970 vs 2022")

print(
    top_10_2022[
        ["Country/Territory", "1970 Population", "2022 Population"]
    ].to_string(index=False)
)
import numpy as np

countries = top_10_2022["Country/Territory"]
population_1970 = top_10_2022["1970 Population"] / 1_000_000
population_2022 = top_10_2022["2022 Population"] / 1_000_000

x = np.arange(len(countries))
width = 0.4

plt.figure(figsize=(14, 7))

plt.bar(x - width / 2, population_1970, width, label="1970")
plt.bar(x + width / 2, population_2022, width, label="2022")

plt.title("Population Comparison: 1970 vs 2022")
plt.xlabel("Country")
plt.ylabel("Population (Millions)")
plt.xticks(x, countries, rotation=45, ha="right")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(
    "population_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Population-comparison chart saved successfully!")
# Stage 11: Find the 10 least populous countries and territories

least_populated = df.nsmallest(10, "2022 Population")

print("\n10 Least Populous Countries and Territories (2022)")

print(
    least_populated[
        ["Country/Territory", "Continent", "2022 Population"]
    ].to_string(index=False)
)
