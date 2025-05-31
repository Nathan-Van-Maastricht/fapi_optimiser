import json

import highspy


class Model:
    def __init__(self, pet_data, bonus_data, output_flag=False):
        self.solver = highspy.Highs()
        self.pet_data = pet_data
        self.bonus_data = bonus_data

        self.solver.setOptionValue("output_flag", output_flag)
        self.solver.setOptionValue("log_to_console", output_flag)

    def build_model(self):
        self.define_variables()
        self.construct_constraints()
        self.construct_objective()

    def define_variables(self):
        self.pets = {pet_id: self.solver.addBinary() for pet_id in self.pet_data.keys()}

        self.bonuses = {bonus: self.solver.addBinary() for bonus in self.bonus_data}

    def construct_constraints(self):
        self.max_air()
        self.max_ground()
        self.pet_bonuses()

    def max_air(self):
        """
        Only three of the selected pets can be of type "air"
        """
        self.solver.addConstr(
            sum(
                self.pets[pet_id]
                for pet_id in self.pet_data.keys()
                if self.pet_data[pet_id]["type"] == "Air"
            )
            <= 3
        )

    def max_ground(self):
        """
        Only three of the selected pets can be of type "gound"
        """
        self.solver.addConstr(
            sum(
                self.pets[pet_id]
                for pet_id in self.pet_data.keys()
                if self.pet_data[pet_id]["type"] == "Ground"
            )
            <= 3
        )

    def pet_bonuses(self):
        for pet_id in self.pet_data.keys():
            for bonus in self.pet_data[pet_id]["bonuses"]:
                self.solver.addConstr(self.pets[pet_id] <= self.bonuses[bonus])

        for bonus in self.bonus_data:
            self.solver.addConstr(
                self.bonuses[bonus]
                <= sum(
                    self.pets[pet_id]
                    for pet_id in self.pet_data.keys()
                    if bonus in self.pet_data[pet_id]["bonuses"]
                )
            )

    def construct_objective(self):
        self.solver.maximize(sum(self.bonuses.values()))

    def solve_model(self, relative_gap=0.007):
        self.solver.setOptionValue("min_rel_gap", relative_gap)
        self.solver.solve()

    def _solution_string(self):
        pet_assignments = []
        for pet_id in self.pet_data.keys():
            value = int(self.solver.variableValue(self.pets[pet_id]))

            if value:
                pet_assignments.append([pet_id, self.pet_data[pet_id]["name"]])

        return "\n".join([": ".join(assignment) for assignment in pet_assignments])

    def print_solution(self):
        print(self._solution_string())

    def solution_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(self._solution_string())

    def get_objective_value(self):
        return self.solver.getInfo().objective_function_value


if __name__ == "__main__":
    with open("data/user_data.json") as input_data:
        pet_data = json.load(input_data)

    with open("data/all_bonuses.json") as input_data:
        bonus_data = json.load(input_data)

    model = Model(pet_data, bonus_data, False)
    model.build_model()
    model.solve_model()
    model.print_solution()
    print(f"Objective value: {model.get_objective_value()}")
