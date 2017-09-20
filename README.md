# Predicting Used Car Prices in San Francisco Bay Area

## Description
I implemented linear regression, Lasso, Random Forest and Gradient Boosting regression to predict used car prices in San Francisco bay area using data scraped from TrueCar.com.

## Result
I find that used car prices can be predicted fairly well given enough data points. The prices not only vary for different car models and features, but also vary across selling locations.

My final model is a gradient boosting regression model that achieves R-squared score of 0.912.

![Predicted Prices Versus True Prices](/raw/predicted_value_check.png?raw=true)

## Recommendations
* Recommendations For Used Car Buyers
    * Go to more dealer locations in your area to get better deals
* Recommendations for Used Car Sellers:
    * Be aware of different price implications of car features
        * For example, premium wheel feature may add little value to your used car price
        * Avoid models and colors that depreciate fast

# Licenses
See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
