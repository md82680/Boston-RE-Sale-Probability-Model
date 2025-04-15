# Boston Real Estate Sale Probability Dataset

## Overview
This dataset contains synthesized information about residential properties in Boston, along with calculated probabilities of sale. The data simulates real estate market dynamics with a focus on factors that might influence a property's likelihood of selling.

## Data Generation
This dataset was synthetically generated to demonstrate machine learning techniques for real estate market analysis. The sale probability was calculated using a formula that incorporates various property characteristics, with specific emphasis on:

- Years of ownership (with a U-shaped relationship where both newer purchases and long-term ownerships have higher probabilities)
- Property liens (negative impact)
- Financial factors
- Market conditions

## Features

| Feature | Description | Type | Units/Format |
|---------|-------------|------|--------------|
| `years_owned` | Number of years the current owner has owned the property | Integer | Years |
| `property_value` | Estimated market value of the property | Integer | US Dollars ($) |
| `square_feet` | Total interior living area | Integer | Square Feet |
| `bedrooms` | Number of bedrooms | Integer | Count |
| `bathrooms` | Number of bathrooms (including half baths) | Float | Count (0.5 = half bath) |
| `property_age` | Age of the property | Integer | Years |
| `neighborhood` | Boston neighborhood where property is located | Categorical | - |
| `distance_to_t` | Distance to nearest MBTA station (T stop) | Float | Miles |
| `school_rating` | Rating of local schools | Float | 1-10 scale (10 being best) |
| `property_tax` | Annual property tax | Integer | US Dollars ($) |
| `has_liens` | Whether property has liens | Binary | 0 (No) or 1 (Yes) |
| `lien_amount` | Total amount of liens on property | Integer | US Dollars ($) |
| `mortgage_rate` | Current mortgage interest rate | Float | Percentage (%) |
| `income_to_mortgage_ratio` | Ratio of estimated income to mortgage payment | Float | Ratio |
| `market_inventory_months` | Current inventory of homes expressed in months of supply | Float | Months |
| `avg_days_on_market` | Average days on market for homes in the area | Integer | Days |
| `last_transaction_date` | Date of last property purchase | Date | YYYY-MM-DD |
| `sale_probability` | Calculated probability of sale within next period | Float | 0-1 (where 1 = 100%) |

## Target Variable
- `sale_probability`: The probability that a property will sell in the upcoming period, expressed as a value between 0 and 1.

## Statistical Information
- Number of records: 1,000
- Range of sale probabilities: Approximately 0.01 to 0.99
- Mean sale probability: Typically around 0.40-0.45

## Formula Used for Sale Probability
The sale probability was calculated using: 

## Neighborhoods
The dataset includes properties from 17 Boston neighborhoods, including Back Bay, Beacon Hill, North End, South End, Fenway, Allston, Brighton, Jamaica Plain, Roxbury, Dorchester, South Boston, East Boston, Charlestown, West Roxbury, Hyde Park, Mattapan, and Roslindale.

## Usage Notes
- Due to the synthetic nature of this dataset, it should be used for educational and demonstration purposes only
- The sale probability calculation, while based on reasonable assumptions about real estate dynamics, is simplified for educational purposes
- The relationships embedded in the data include both linear and non-linear effects
