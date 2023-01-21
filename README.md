# Reinforcement_Learning_#AI_-Apple_Basket_(stablebaselines_&_gym)

### Description
	This environment simulates an apple basket that collects falling apples by moving only horizontally.
	Field width and height, basket width and height, FPS, apples falling per second, gravity, and termination threshold variables 
	are fully adjustable from the top of the script.
    ### Action Space
    The action is a `ndarray` with shape `(1,)` which can take values `{0, 1, 2}` determines movement direction of the basket
    | Num | Action                       |
    |-----|------------------------------|
    | 0   | Move the basket to the left  |
    | 1   | hold the basket steady       |
    | 2   | Move the basket to the right |
    **Note**: The movement of the basket is not an accelerated movement, the position changes directly to the calculated place 
    corresponding to the basket speed.
    ### Observation Space
    The observation is a `ndarray` with shape `(3,)` with the values corresponding to the following positions:
    | Num | Observation                         | Min                 | Max               |
    |-----|-------------------------------------|---------------------|-------------------|
    | 0   | Basket Horizontall Position         | 0                   | Field Width       |
    | 1   | Closest Apple Horizontall Position  | 0                   | Field Width       |
    | 2   | Closest Apple Vertical Position     | 0                   | Field Height      |
    ### Rewards
    While a reward worth 1 is allocated for each apple caught, -1 value is lost in case of leaving the area.
    ### Starting State
    The horizontal position of the basket is set in the middle of the field and an apple is created in a random position.
    ### Episode End
    The episode ends if any one of the following occurs:
    1. Termination: Basket cannot catch the defined number of apples
    2. Termination: Basket leaves the area
    ### Additional Info
	Models trained in various steps are saved in the 'Saved Models' folder.
	The packages used in the environment can be installed by running the 'requirements.txt' file with the 'pip' command.
