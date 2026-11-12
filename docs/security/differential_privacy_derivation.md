# Differentially Private Federated Averaging (DP-FedAvg) Derivation
**Author:** Soubhagya (`@Soubhagya981999`)

## 1. Local Gradient Perturbation
For client gradient update $\Delta w_i$:
$$\overline{\Delta w_i} = \frac{\Delta w_i}{\max\left(1, \frac{\|\Delta w_i\|_2}{S}\right)}$$

## 2. Gaussian Mechanism Noise Addition
$$\tilde{\Delta w} = \frac{1}{K} \left( \sum_{i=1}^K \overline{\Delta w_i} + \mathcal{N}\left(0, \sigma^2 S^2 \mathbf{I}\right) \right)$$
Guarantees $(\epsilon, \delta)$ differential privacy across federated rounds.
