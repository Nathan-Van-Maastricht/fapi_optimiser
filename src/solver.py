import json

import highspy


class Model:
    def __init__(self, data, output_flag=False):
        self.solver = highspy.Highs()
        self.data = data

        self.solver.setOptionValue("output_flag", output_flag)
        self.solver.setOptionValue("log_to_console", output_flag)

    def build_model(self):
        self.define_variables()
        self.construct_constraints()
        self.construct_objective()

    def define_variables(self):
        self.pets = {pet_id: self.solver.addBinary() for pet_id in self.data.keys()}

    def construct_constraints(self):
        self.max_air()
        self.max_ground()
        self.pet_restrictions()

    def max_air(self):
        """
        Only three of the selected pets can be of type "air"
        """
        pass

    def max_ground(self):
        """
        Only three of the selected pets can be of type "gound"
        """
        pass

    def pet_restrictions(self):
        """
        If access to some pets has not been aquired yet, we can't use them
        """
        pass

    def construct_objective(self):
        pass

    def solve_model(self, relative_gap=0.007):
        self.solver.setOptionValue("min_rel_gap", relative_gap)
        self.solver.solve()

    def _solution_string(self):
        pass

    def print_solution(self):
        print(self._solution_string())

    def solution_to_file(self, filename):
        with open(filename, "w") as file:
            file.write(self._solution_string())


if __name__ == "__main__":
    with open("data/processed_data.json") as input_data:
        data = json.load(input_data)

    model = Model(data, True)
    model.build_model()
    model.solve_model()
