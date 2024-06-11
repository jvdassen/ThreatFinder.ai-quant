#!/usr/bin/env python
import numpy as np
import sys
import json
from scipy.stats import lognorm, poisson

def quantification (min_incidents, max_incidents, min_loss, max_loss, prob_confidence, loss_confidence):
  visualize = False

  # Calculate parameters for log-normal distribution of impacts
  loss_mean = np.log(min_loss) + (np.log(max_loss) - np.log(min_loss)) * loss_confidence
  loss_std = (np.log(max_loss) - np.log(min_loss)) * (1 - loss_confidence) / 2

  # Calculate parameters for Poisson distribution of probabilities
  prob_mean = min_incidents + (max_incidents - min_incidents) * prob_confidence

  # Perform Monte Carlo simulations
  num_simulations = 1 * 1000 * 1000
  losses = lognorm.rvs(loss_std, scale=np.exp(loss_mean), size=num_simulations)
  probabilities = poisson.rvs(prob_mean, size=num_simulations)
  exposures = losses * probabilities

  hist, bin_edges =np.histogram(exposures, bins=50, density=True)

  res = {
   "hist": hist.tolist(),
   "bin_edges": bin_edges.tolist()
  }

  # Calculate the bin centers
  bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

  # Calculate the probabilities (normalized histogram)
  probabilities = hist / np.sum(hist)

  # Calculate the expected value
  expected_value = np.sum(bin_centers * probabilities)

  #print("Expected Value:", expected_value)


  # Calculate statistics of expected exposures
  percentiles = np.arange(0.1, 1, 0.1)
  exposure_stats = np.percentile(exposures, percentiles * 100)

  #print("Expected Exposures:")
  for p, e in zip(percentiles, exposure_stats):
      res[str(int(p*100))]= f"{e:.2f}"
      if visualize:
        print(f"P({int(p*100)}): {e:.2f}")



  if visualize:
    import matplotlib.pyplot as plt
    # Display histogram
    plt.figure(figsize=(8, 6))
    plt.hist(exposures, bins=50, density=True, alpha=0.7)
    plt.xlabel("Exposure")
    plt.ylabel("Probability Density")
    plt.title("Histogram of Expected Exposures")
    plt.grid(True)
    plt.show()

  # Display loss exceedance curve
  sorted_exposures = np.sort(exposures)
  exceedance_probabilities = 1 - np.arange(1, len(exposures) + 1) / len(exposures)

  def downsample(data, factor):
      return data[::factor]

  if visualize:
    plt.figure(figsize=(8, 6))
    plt.plot(sorted_exposures, exceedance_probabilities)
    plt.xlabel("Exposure")
    plt.ylabel("Exceedance Probability")
    plt.title("Loss Exceedance Curve")
    plt.grid(True)
    plt.show()

  np.set_printoptions(threshold=sys.maxsize)
  # TODO Downsampling needed for ThreatFinder AI frontend
  #print('sorted_exposures')
  #print(",".join(map(str, downsample(np.round(sorted_exposures, 0), 500))))
  #print('exceedance_probabilities')
  #print(",".join(map(str, downsample(exceedance_probabilities, 500))))

  jsondump = json.dumps(res)
  return jsondump

if __name__ == '__main__':
  quantification(1, 5, 10000, 200000, 0.95, 0.95)
