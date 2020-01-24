"""Constants to be used in pazaak game"""

# playing until some player gets to 20 points
SCORE_GOAL = 20
# For blackjack strategy: "dealer draws to 16 stands on 17"
OPPONENT_STAND_THRESHOLD = 16
# 3 sets needed to win the game
WINNING_SETS = 3
# 4 cards on every player's hand
HAND_SIZE = 4

# ML settings
DATASET_FILE_NAME = 'resources/result.csv'
MODEL_FILE_NAME = 'resources/model.joblib'
GRAPHVIZ_FILE_NAME = 'resources/graph.dot'

# internal settings
# timeout after every turn, in seconds
SLEEP_TIME = 0
# After a set is won, wait for user input
REQUIRE_INPUT_AFTER_SET = False
