import pandas as df
import matplotlib.pyplot as graph

# load the data 
file_name = "timestamp%2Caltitude_m%2Clatitude%2Clongitude%2Cbattery_vo.csv"
df = df.read_csv(file_name)
print("--- Initial Data Info ---")
df.info()

# clean it up
df_cleaned = df[(df['altitude_m'] < 1000) | (df['altitude_m'].isnull())].copy()
df_cleaned = df_cleaned[(df_cleaned['battery_voltage'] > 10.0) | (df_cleaned['battery_voltage'].isnull())]

# fill missing values
df_cleaned['altitude_m'] = df_cleaned['altitude_m'].interpolate()
df_cleaned['flight_mode'] = df_cleaned['flight_mode'].ffill()

# give arithmetic values of the cleaned data
print("\n--- Cleaned Data Statistical Summary ---")
print(df_cleaned.describe())

# time vs alt graph 
graph.figure(figsize=(10, 6))
graph.plot(df_cleaned['timestamp'], df_cleaned['altitude_m'], marker='o', linestyle='-', markersize=4)
graph.title('Cleaned Drone Altitude vs. Timestamp')
graph.xlabel('Timestamp (seconds)')
graph.ylabel('Altitude (meters)')
graph.grid(True)
graph.tight_layout()
graph.savefig("Alt vs Time.png")

# flight path graph 
graph.figure(figsize=(10, 8))
unique_modes = df_cleaned['flight_mode'].unique()
colors = graph.cm.jet([i/len(unique_modes) for i in range(len(unique_modes))])

for i, mode in enumerate(unique_modes):
    mode_data = df_cleaned[df_cleaned['flight_mode'] == mode]
    graph.scatter(mode_data['longitude'], mode_data['latitude'], 
                label=mode, 
                color=colors[i], 
                alpha=0.8)

graph.title('Drone Flight Path by Mode')
graph.xlabel('Longitude')
graph.ylabel('Latitude')
graph.legend(title='Flight Mode')
graph.grid(True)
graph.axis('equal')
graph.tight_layout()
graph.savefig("flightpathbymode.png")

print("\nData is clean and graphs are saved in the folder.")