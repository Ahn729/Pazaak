# Pazaak
#### A simple CLI implementation of KotOR's Blackjack-like minigame, including two machine learning model opponents

Computer strategies are included in the computer_strategies module. They include:
* A pretty stupid random strategy
* A blackjack-inspired (dealer draws to 16 stands on 17) strategy written by hand by me
* A strategy using a DecisionTree machine learning model 
* A strategy using a RandomForest machine learning model
 
Opponent strategy can be confiured in pazaak module, l. 16

To use the models, just use the model dumps found in the resources folder. Alternatively, you can use your favourite model to create your own by following the steps: 
1. Create a dataset with `create_dataset` from the `computer_learn` module. Play around with the random constant in `record_results`. Result dataset (default: `result.csv`) will be copied to resources folder.
2. Using the dataset, train the model with `train_model`. A model dump will be copied to the resources folder to be used by the `ml_trainee_strategy` function. 
3. You're all set up!

If you wish, you can play around with differnt models and evaluate their performance in the `train_and_evaluate` module. 
