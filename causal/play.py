import numpy as np

from dowhy import CausalModel
import dowhy.datasets 

if __name__ == '__main__':
  data = dowhy.datasets.linear_dataset(beta=10,
    num_common_causes=5,
    num_instruments = 2,
    num_effect_modifiers=1,
    num_samples=5000, 
    treatment_is_binary=True,
    stddev_treatment_noise=10,
    num_discrete_common_causes=1)
  
  df = data["df"]

  print(df.head())

  print(df.columns)

  model=CausalModel(
    data = df,
    treatment=data["treatment_name"],
    outcome=data["outcome_name"],
    graph=data["gml_graph"]
  )

  print(data['treatment_name'], data['outcome_name'])
  
  # model.view_model()

  identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
  print(identified_estimand)
  causal_estimate = model.estimate_effect(identified_estimand,
        method_name="backdoor.propensity_score_stratification")
  print(causal_estimate)
  refute_results = model.refute_estimate(identified_estimand, causal_estimate, method_name="random_common_cause")
  print(refute_results)
  