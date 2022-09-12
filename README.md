# Decision Tree

## The decision tree is a supervised learning algorithm for classification or regression problems, and it can analyze nonlinear interactions between variables in a dataset. It looks very similar to a binary tree, and it's heavily revolved around recursion. Every leaf in tree should provide some essential information to determine the final solution. It's important not to overfit a tree by overcomplicating it and including any unnecessary leaves.

<img width="665" alt="Screen Shot 2022-09-11 at 7 12 32 PM" src="https://user-images.githubusercontent.com/102645083/189561966-3bb868c5-17fb-4ad3-b40e-98ba2a144220.png">

## The two most important concepts for the decision tree are entropies and information gains. An extropy measures how scrambled the values in a dataset column is, and we can think of it as measuring the variance. Inversely, information gain is the reduction in entropy by transforming a dataset, and we can think of it as spliting a dataset into two branches, and Information gain = the original entropy - the weighted entropies of each branch. These two are the main concepts used to determine what feature is the most effective during each recursive iteration.

## In this project's dataset, there are 24 samples, and each one is a list of five values, which are age, prescript, astigmatic, tear rate, and the 5th one being the label of the sample.
