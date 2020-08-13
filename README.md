# camels synthetic data
## Generating synthetic data for CAMELS, but can be done anywhere really, probably to analyze controlled nonstationarity.
## MetSim is borrowed from github.com/UW-Hydro
## The synthetic data will be used in both physically based hydrology models, and future projections of climate scenarios.
# Planned workflow
1. Generate a synthetic data (matching observed statistics) record of:
   * Daily minimum temperature
   * Daily macimum temperature
   * Precipitation
   * Wind speed

2. Use MetSim to produce:
   * SW Radiation
   * LW Ratiation
   * Humidity
   * Potential evapotranpiration

3. Compare the synthetic data to observed values from 1980 - 2014:
   * Match statistics
   * Match non-stationary trends

4. Generate ensemble of nonstationary conditions for future scenarios, similar to step 1.
5. Use MetSim to produce missing records for future scenarios, similar to step 2.
