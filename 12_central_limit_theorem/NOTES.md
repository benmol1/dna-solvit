# The Central Limit Theorem — Notes (WIP)

**Status:** Part 1 (exponential) done. Part 2 (Cauchy, running mean) and Part 3 (explanation) still to do.

## The statement

The distribution of the sample mean tends to normal as the sample size n grows. More precisely, for a population with mean μ and finite variance σ²:

- the mean of the sample means is **μ**
- their standard deviation (the *standard error*) is **σ/√n**
- their shape approaches a normal as n grows

The rationale for *why* the bell shape appears is still an open question for me.

## Part 1: Exponential(1)

Population: mean μ = 1, σ = 1, skewness 2.

Parameter gotcha: the exponential has **rate** λ (events per unit time), but `rng.exponential` takes the **scale** β = 1/λ. With λ = 1 they coincide, so the bug hides. The code passes `1 / rate`.

10,000 sample means per n:

| n | mean | std | 1/√n | skew | 2/√n |
|---|---|---|---|---|---|
| 2 | 0.993 | 0.704 | 0.707 | | |
| 5 | 1.000 | 0.450 | 0.447 | | |
| 30 | 1.000 | 0.186 | 0.183 | | |

(Skew columns were added after this run. Rerun `solution.py` to fill them in.)

The n=30 std of 0.186 against 1/√30 = 0.183 confirms the spread check.

### Leftover skew

At n=30 the histogram is still visibly right-skewed: the peak sits left of the normal's peak and the tail is longer on the right. The skewness of the mean of n iid draws is the population skewness divided by √n, so for Exp(1) it is **2/√n** (about 0.37 at n=30). Skewness fades slowly, which is why the folklore "n=30" is a rough guide only.

### Noise in the estimate

The gap between empirical and predicted skew is sampling noise. Mean absolute gap at n=5, averaged over 20 seeds:

| reps | mean gap |
|---|---|
| 10,000 | 0.0326 |
| 100,000 | 0.0075 |
| 1,000,000 | 0.0021 |

Each 10× in reps shrinks the gap 3.6–4.3×, against the predicted √10 ≈ 3.16×. That matches the 1/√reps scaling, with slightly faster shrinkage. Skewness depends on the third moment, so a few tail values make it a noisy statistic.

## Code notes

- `sampling_dist(n, ax, ...)` draws the means, plots the histogram plus the normal overlay N(μ, σ/√n), and returns the means.
- The x-range for the overlay follows the data (`means.min()` to `means.max()`).
- The figure is saved to `exponential_clt.png` next to the script, not shown interactively.
- Format `.3g` means 3 significant figures; `.3f` means 3 decimal places.

## Next

- Repeat with `rng.standard_cauchy` for n = 2, 5, 30. Prediction to test: the histograms will *not* narrow, because Cauchy tails fall like 1/x².
- Running mean of a single stream of 1,000,000 Cauchy draws.
- Explain what breaks the theorem (no finite mean or variance) and why the mean of n Cauchy draws is itself standard Cauchy.
- Extension: lognormal σ=1.5, QQ-plot to find the n at which the sampling distribution looks Gaussian.
