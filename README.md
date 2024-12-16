## Unsupervised Novelty Detection using the Local Outlier Factor (LOF)

Novelty detection is commonly applied in scenarios where you have a set of "normal" data without any anomalies, and the objective is to identify "new" or "novel" data points that deviate from this normal model. It does not assume contamination in the training data, meaning it presumes the reference data used to learn the normal behavior is free of outliers. Novelty detection is useful in contexts where the notion of "novel" is relative to a known baseline of normal and is applied as new data comes in.

Note that this is different from outlier detection where the assumption is that the dataset you are working with is mostly clean but may contain some outliers.