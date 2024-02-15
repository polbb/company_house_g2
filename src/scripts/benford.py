from database import get_ixbrl_data_from_dynamodb

import matplotlib.pyplot as plt

def benford(company_number):
        
    # Benford's Law application with frequencies in percentage
    ixbrl_data = get_ixbrl_data_from_dynamodb(company_number)
    first_digit_frequencies = {str(digit): 0 for digit in range(1, 10)}  # Initialize frequency dict for digits 1-9
    total_values = 0  # Initialize total values count for percentage calculation
    for key, value_list in ixbrl_data.items():
        for value in value_list:
            try:
                number = float(value.replace(',', ''))
                if number == 0:  # Discard values that are only zero
                    continue
                first_digit = str(number)[0]  # Extract the first digit
                if first_digit in first_digit_frequencies:
                    first_digit_frequencies[first_digit] += 1  # Increment frequency of the first digit
                    total_values += 1  # Increment total values count
            except ValueError:
                continue
    
    # Convert frequencies to percentages
    for digit, frequency in first_digit_frequencies.items():
        if total_values > 0:  # Prevent division by zero
            first_digit_frequencies[digit] = (frequency / total_values) * 100

    # Plotting the frequencies against Benford's Law expected distribution
    benford_distribution = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]  # Expected percentages
    fig, ax = plt.subplots()
    ax.bar(first_digit_frequencies.keys(), first_digit_frequencies.values(), label='Observed Frequencies', alpha=0.7)
    ax.plot(list(first_digit_frequencies.keys()), benford_distribution, color='red', label='Benford\'s Law Expected Distribution')
    ax.set_xlabel('First Digit')
    ax.set_ylabel('Frequency (%)')
    ax.set_title('Benford\'s Law Distribution')
    ax.legend()
    plt.show()
    
    return first_digit_frequencies