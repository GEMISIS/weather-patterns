import json
import requests
import matplotlib.pyplot as plt

# Order storms by known wind speeds.
# Higher speed = more severe.
system_statuses = {
    'ET': 0,
    'DB': 0,
    'WV': 1,
    'LO': 2,
    'EX': 3,
    'SD': 4,
    'TD': 5,
    'SS': 6,
    'TS': 7,
    'HU': 8
}
url = "http://www.aoml.noaa.gov/hrd/hurdat/hurdat2.html"
image_size = (16, 10)
image_dpi = 500
output_dir = "tmp"

# Get our data first.
s = requests.get(url).content
content = s.decode('utf-8')
content = content.split("pre>")[1].lstrip()

# Now get it into a nicer format.
lines = content.split('\n')
data = []
i = -1
min_year = 1900
max_year = 1900
for line in lines:
    columns = line.split(",")
    if len(columns) == 4:
        # Header which we actually care about.
        alias = columns[0]
        name = columns[1].lstrip()
        year = int(columns[0][4:8])
        data.append({
            "alias": alias,
            "name": name,
            "year": year,
            "max_status": 0
        })
        max_year = max(max_year, year)
        i += 1
    elif len(columns) == 21:
        data[i]['max_status'] = max(data[i]['max_status'], system_statuses[columns[3].lstrip()])
        if columns[2].lstrip() == 'W':
            data[i]['avg_wind'] = int(columns[6].lstrip())

# Further refine the data for our graphs.
year_range = range(min_year, max_year)
years = []
storm_counts = []
storm_types = [] * 9
for i in range(0, 9):
    storm_types.append([])
for year in year_range:
    years.append(year)

    storm_count = 0
    storm_type = [0] * 9
    for ele in data:
        if (ele["year"] == year):
            storm_count += 1
            storm_type[ele['max_status']] += 1
    storm_counts.append(storm_count)
    for i in range(0, 9):
        storm_types[i].append(storm_type[i])

# General storm count
def generate_storm_count_results():
    plt.figure(1, figsize=image_size, dpi=image_dpi)
    plt.title("Total Number of Storms ({0} - {1})".format(min_year, max_year))
    plt.plot(years, storm_counts)
    plt.xlabel("Years ({0} - {1})".format(min_year, max_year))
    plt.ylabel("Number of Storms")
    plt.savefig('{0}/total_number_storms.png'.format(output_dir))
    plt.clf()

# Bar graph of storm types.
def generate_storm_type_count_results():
    plt.figure(1, figsize=image_size, dpi=image_dpi)
    plots = []
    ind = year_range
    for i in range(0, 9):
        plots.append(plt.bar(ind, storm_types[i])[0])
    plt.title("Storm Type Counts ({0} - {1})".format(min_year, max_year))
    plt.xlabel("Years ({0} - {1})".format(min_year, max_year))
    plt.ylabel("Storm Type Count")
    plt.legend(plots,
        [
            'Disturbance',
            'Tropical Wave',
            'Low',
            'Extratropical cyclone',
            'Subtropical Cyclone (< 34 knots)',
            'Tropical Cyclone (< 34 knots)',
            'Subtropical Cyclone (>= 34 knots)',
            'Tropical Cyclone (34-63 knots)',
            'Hurricane'
        ]
    )
    plt.savefig('{0}/storm_type_counts.png'.format(output_dir))
    plt.clf()


###########################################
#######                             #######
####### The actual lambda function. #######
#######                             #######
###########################################
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Todo: Handle properly')
    }
