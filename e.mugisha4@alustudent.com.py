class Assignment:
    def __init__(self, name, assignment_type, score, weight):
        self.name = name
        self.assignment_type = assignment_type  # "Formative" or "Summative"
        self.score = score
        self.weight = weight
        
    def weighted_score(self):
        """Calculate the weighted score of the assignment using the formula given."""
        return (self.score / 100) * self.weight


class Student:
    def __init__(self):
        self.assignments = []

    def add_assignment(self, assignment):
        """Add an assignment to the student's list."""
        self.assignments.append(assignment)

    def calculate_scores(self):
        """Calculate total scores for Formative and Summative assignments."""
        formative_total = 0
        summative_total = 0
        formative_weight = 0
        summative_weight = 0

        for assignment in self.assignments:
            if assignment.assignment_type == "Formative":
                formative_total += assignment.weighted_score()
                formative_weight += assignment.weight
            elif assignment.assignment_type == "Summative":
                summative_total += assignment.weighted_score()
                summative_weight += assignment.weight

        return formative_total, summative_total, formative_weight, summative_weight

    def check_progression(self, formative_total, summative_total):
        """Check if the student has passed or failed the course."""
        if formative_total >= 30 and summative_total >= 20:
            return "Passed"
        else:
            return "Failed"

    def check_resubmission(self):
        """Identify assignments eligible for resubmission."""
        resubmission_list = []
        for assignment in self.assignments:
            if assignment.assignment_type == "Formative" and assignment.score < 50:
                resubmission_list.append(assignment)
        return resubmission_list

    def generate_transcript(self, ascending=True):
        """Generate and display a transcript of assignments."""
        sorted_assignments = sorted(self.assignments, key=lambda x: x.score, reverse=not ascending)

        print(f"{'Assignment':<20} {'Type':<15} {'Score(%)':<12} {'Weight (%)':<12}")
        print("-" * 60)
        for assignment in sorted_assignments:
            print(f"{assignment.name:<20} {assignment.assignment_type:<15} {assignment.score:<12} {assignment.weight:<12}")


def main():
    student = Student()
    
    # Collect assignment details from the user
    while True:
        name = input("Enter assignment name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        assignment_type = input("Enter assignment type (Formative or Summative): ")
        score = float(input("Enter score (out of 100): "))
        weight = float(input("Enter weight (%): "))
        
        # Validate weights
        if assignment_type == "Formative" and weight + sum(a.weight for a in student.assignments if a.assignment_type == "Formative") > 60:
            print("Total weight for Formative assignments cannot exceed 60%. Please try again.")
            continue
        elif assignment_type == "Summative" and weight + sum(a.weight for a in student.assignments if a.assignment_type == "Summative") > 40:
            print("Total weight for Summative assignments cannot exceed 40%. Please try again.")
            continue
        
        student.add_assignment(Assignment(name, assignment_type, score, weight))

    # Calculate scores
    formative_total, summative_total, _, _ = student.calculate_scores()

    # Check progression
    result = student.check_progression(formative_total, summative_total)
    print(f"\nCourse Progression: {result}")

    # Check for resubmission
    resubmission_assignments = student.check_resubmission()
    if resubmission_assignments:
        print("You are eligible for resubmission for the following assignments:")
        for assignment in resubmission_assignments:
            print(f"- {assignment.name} (Score: {assignment.score}%)")

    # Generate transcript
    order = input("Would you like the transcript in ascending or descending order? (a/d): ")
    ascending = order.lower() == 'a'
    student.generate_transcript(ascending)

if __name__ == "__main__":
    main()
