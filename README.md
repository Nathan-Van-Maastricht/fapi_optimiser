This repo contains an optimiser for the idle game Farmer Against Potatoes Idle.

# Outline

Within the game there are "pets" that you can equip to give a boost. I have found data for 104 different pets, with various bonuses. In total in this dataset there are 23 possible bonuses the pets can give, with some pets providing multiple bonuses. The pets are split into two types, "air" and "ground", with a maximum of three from each type being possible to select at once.

Given these restrictions, it seems a natural application for combinatorial optimisation algorithms. So the goal of this project is to use Mixed Integer Linear Programming (MILP) to allow more informed decision making in the selection of pets to equip.

# Model

The model is relatively simple, with only a small number of decision variables and constraints.

## Variables

There is a binary decision variable for each pet, $i$, of type $t$, with associated bonus set $B$, denoted $p_{i,t}^B$ and each bonus $b_j$.

## Constraints

There are three groups of constraints, of which two of the groups only contaian a single constraint.

### Maximum number of Air Pets

This constraint is to enforce that no more than three pets of type air are selected:

$$\sum_{i,t=\text{Air}}p_{i,t}^B\leq3.$$

### Maximum number of ground pets

Similar to the air constraint, this constraint restricts the number of pets that are of type ground that can be selected:

$$\sum_{i,t=\text{Ground}}p_{i,t}^B\leq3.$$

### Pet/Bonus relationship

This set of constraints is the most complex of the group, and is made of two types.

#### Pet $\Rightarrow$ Bonus

This constraint ensures that if a pet is selected, then every bonus that is associated with the pet is also selected:

$$p_{i,t}^B\leq b_j \text{ for all } b_j\in B.$$

#### Bonus $\Rightarrow$ Pet

This constraint ensures that if a bonus is selected, then at least one pet that has that as a bonus is also selected:

$$b_j\leq \sum_{b_j\in B}p_{i,t}^B.$$

## Objective function

Due to the decision to include variables for the bonus selection, this makes the objective function simple, we just want to maximise the number of bonuses selected:

$$\max\sum_j b_j.$$

## Extensions

One possible future extension is to give a set of bonuses that must be included in the bonuses selected. This is a relatively easy addition, but I have not had need for it up until this point.


# Data

The raw data (data/raw_data.json) was obtained from https://github.com/erik434/fapi-pets/tree/main.

As I suspect this data is incomplete (I suspect there are 140 pets in the current version of the game) this optimiser doesn't work quite as effectively as it could. I would happily incorporate any additional data available though.