# Pazaak
#### A simple CLI implementation of KotOR's Blackjack-like minigame

Computer strategies are included in the computer_strategies module. They include:
* A pretty stupid random strategy
* A blackjack-inspired (dealer draws to 16 stands on 17) strategy written by hand by me
* A strategy using a DecisionTree machine learning model 
 
Opponent strategy can be confiured in pazaak module, l. 16

To use the decision tree: 
1. Create a dataset with `create_dataset` from the `computer_learn` module, or use mine. Result dataset `result.csv` will be copied to resources folder.
2. Using the dataset, train the model with `train_model`. A model dump will be copied to the resources folder to be used by the `decision_tree_strategy` function (you can actually supply any regressor here). Again, feel free to use mine.
3. You're all set up!

If you wish, you can play around with differnt models and evaluate their performance in the `train_and_evaluate` module. 
