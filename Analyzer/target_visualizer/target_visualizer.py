import argparse
from datetime import datetime
import pandas as pd 
import matplotlib.pyplot as plt

def parse_date(date):
    if isinstance(date, float) and pd.isna(date):
        return pd.NaT
    
    date = str(date)
    date = date.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
    try:
        return datetime.strptime(date, '%d %b %Y')
    except:
        return pd.NaT

def get_targeted_brand_from_sheet(file_name, start_date, end_date):
    df = pd.read_excel(file_name, engine='openpyxl')

    # Convert the 'Date' column to datetime
    df['Date (of Dataset)'] = pd.to_datetime(df['Date (of Dataset)'].apply(parse_date))

    # Filter the dataFrame to include only the specified date range
    start_date = datetime.strptime(start_date, '%d%m%y').strftime('%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%d%m%y').strftime('%Y-%m-%d')
    mask = (df['Date (of Dataset)'] >= start_date) & (df['Date (of Dataset)'] <= end_date)
    
    # Only include those targets that are deemed as phishing after VirusTotal validation (>4) and manually verified
    mask &= (df['Final Verdict '] == 'Yes')
    filtered_df = df.loc[mask]

    # Extract targeted Brandfrom the filtered DataFrame
    brands = filtered_df['Targeted Brand / Categories']

    # Count the occurrences of each brand/category
    brand_counts = brands.value_counts()

    return brand_counts


def generate_frequency_diagram(data_counts, start_date, end_date):
    # Set the figure size
    plt.figure(figsize=(20, 12))  

    # Create a bar chart
    plt.bar(data_counts.index, data_counts.values)

    # Rotate the x-axis labels to show them vertically
    plt.xticks(rotation=90)

    # Set the x-axis & y-axis label 
    plt.xlabel('Targeted Brand')  
    plt.ylabel('Frequency')

    # Set the title of the chart
    plt.title(f'Targeted Brands for week {start_date} to {end_date}')
    
    # Adjust the layout to fit everything nicely
    plt.tight_layout()

    # Save the diagram
    output_file = f"target_{start_date}_to_{end_date}.png"
    plt.savefig(output_file)
    plt.close()

def generate_percentage_diagram(data_counts, start_date, end_date):
    # Calculate the percentages
    total_count = data_counts.sum()
    percentages = (data_counts / total_count) * 100

    # Set the figure size
    plt.figure(figsize=(20, 12))  

    # Create a bar chart
    plt.bar(percentages.index, percentages.values)

    # Rotate the x-axis labels to show them vertically
    plt.xticks(rotation=90)
    #plt.yticks(range(0, 101, 20))

    # Set the x-axis & y-axis label 
    plt.xlabel('Targeted Brand')  
    plt.ylabel('%')

    # Set the title of the chart
    plt.title(f'Targeted Brands for week {start_date} to {end_date}')

    # Include the total count 
    plt.text(x=0.5, y=0.95, s=f"Total Count: {total_count}", 
             ha='center', va='top', transform=plt.gca().transAxes)
    
    # Adjust the layout to fit everything nicely
    plt.tight_layout()

    # Save the diagram
    output_file = f"target_percentage_{start_date}_to_{end_date}.png"
    plt.savefig(output_file)
    plt.close()


def generate_empirical_cdf_diagram(data_counts, start_date, end_date):
    # Convert the series to a DataFrame
    df = data_counts.reset_index()
    df.columns = ['Brand', 'Count']

    # Sort the DataFrame by count
    df = df.sort_values(by='Count', ascending=False)

    # Calculate the cumulative sum of the counts
    df['Cumulative'] = df['Count'].cumsum()
    df['CDF'] = df['Cumulative'] / df['Cumulative'].max()

    # Plotting
    plt.figure(figsize=(20, 12))
    plt.step(df['Brand'], df['CDF'], where='post')

    # Rotate the x-axis labels to show them vertically
    plt.xticks(rotation=90)

    # Set the x-axis & y-axis label
    plt.xlabel('Targeted Brand')
    plt.ylabel('CDF')

    # Set the title of the chart
    plt.title(f'Targeted Brands for week {start_date} to {end_date}')

    # Adjust the layout to fit everything nicely
    plt.tight_layout()

    # Save the diagram
    output_file = f"target_cdf_{start_date}_to_{end_date}.png"
    plt.savefig(output_file)
    plt.close()


def target_visualizer(file_name, start_date, end_date):
    data_counts = get_targeted_brand_from_sheet(file_name, start_date, end_date)
    generate_frequency_diagram(data_counts, start_date, end_date)
    generate_percentage_diagram(data_counts, start_date, end_date)
    generate_empirical_cdf_diagram(data_counts, start_date, end_date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Supply the folder names")
    parser.add_argument("excel_file_path", help="Name of the excel file")
    parser.add_argument("start_date", help="Start Date")
    parser.add_argument("end_date", help="End Date")
    args = parser.parse_args()

    file_name = args.excel_file_path 
    start_date = args.start_date
    end_date = args.end_date

    target_visualizer(file_name, start_date, end_date)
