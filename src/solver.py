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

        self.bonus_count = {
            bonus: self.solver.addIntegral() for bonus in self.bonus_data
        }

    def construct_constraints(self):
        self.max_air()
        self.max_ground()
        self.pet_bonuses()
        self.total_bonuses()

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

            self.solver.addConstr(
                self.bonus_count[bonus]
                == sum(
                    self.pets[pet_id]
                    for pet_id in self.pet_data.keys()
                    if bonus in self.pet_data[pet_id]["bonuses"]
                )
            )

    def total_bonuses(self):
        self.solver.addConstr(sum(self.bonuses.values()) == 21)

    def construct_objective(self):
        self.solver.maximize(
            self.bonus_count["Class Exp Earned"]
            + self.bonus_count["Protein"]
            + self.bonus_count["Residue Created"]
        )

    # def construct_objective(self):
    #     self.solver.maximize(
    #         10000 * sum(self.bonuses.values())
    #         + 100
    #         * sum(
    #             len(self.pet_data[pet_id]["bonuses"]) * self.pets[pet_id]
    #             for pet_id in self.pet_data.keys()
    #         )
    #         + sum(self.bonus_count.values())
    #         + 20 * self.bonus_count["Protein"]
    #     )

    def solve_model(self, relative_gap=0.007):
        self.solver.setOptionValue("min_rel_gap", relative_gap)
        self.solver.solve()

    def _solution_string(self):
        pet_assignments = self.get_pet_id_used()

        pet_string = "\n".join(
            [f"{pet_id}: {self.pet_data[pet_id]['name']}" for pet_id in pet_assignments]
        )

        bonuses_used = ["Used:"]
        used = self.get_bonuses_used()
        for bonus in used:
            bonuses_used.append(
                f"{bonus}: {self.solver.variableValue(self.bonus_count[bonus]):.0f}"
            )
        bonus_string = "\n".join(bonuses_used)

        total_bonus_string = f"Number of bonuses: {len(bonuses_used) - 1}"

        missing_bonuses = ["Not Used:"]
        missing_bonuses.extend(self.get_bonuses_not_used())
        missing_bonuses_string = "\n".join(missing_bonuses)

        return "\n\n".join(
            [pet_string, bonus_string, missing_bonuses_string, total_bonus_string]
        )

    def get_pet_id_used(self):
        pet_assignments = []

        for pet_id in self.pet_data.keys():
            value = round(self.solver.variableValue(self.pets[pet_id]))

            if value:
                pet_assignments.append(pet_id)

        return pet_assignments

    def get_bonuses_used(self):
        pet_assignments = self.get_pet_id_used()

        bonuses = set()

        for pet_id in pet_assignments:
            bonuses.update(self.pet_data[pet_id]["bonuses"])

        return sorted(list(bonuses))

    def get_bonuses_not_used(self):
        all_bonuses = set(self.bonus_data)
        used_bonuses = self.get_bonuses_used()

        return sorted(list(all_bonuses.difference(used_bonuses)))

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
