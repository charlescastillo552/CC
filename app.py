from flask import app, jsonify, request

@app.route('/compute', methods=['POST'])
def compute_grades():
    try:
        # Get input from the user (Prelim and Total Grade)
        total = float(request.form['total'])
        prelim = float(request.form['prelim'])

        # Validate input ranges
        if total < 0 or total > 100 or prelim < 0 or prelim > 100:
            return jsonify({'error': 'Invalid grades. Both grades must be between 0 and 100.'})

        # Contribution of Prelim to the total grade (20% of Prelim Grade)
        prelim_contribution = prelim * 0.20

        # Remaining grade needed from Midterm and Finals (which account for 80% of the total)
        remaining_grade_needed = total - prelim_contribution

        # Check if it is possible to achieve the required total grade
        if remaining_grade_needed < 0 or remaining_grade_needed > 80:
            return jsonify({
                'error': 'It is not possible to achieve this total grade with the given Prelim grade.',
                'prelim_contribution': prelim_contribution
            })

        # Calculate required Midterm and Final grades
        required_midterm = (remaining_grade_needed / 0.80) * 0.30
        required_finals = (remaining_grade_needed / 0.80) * 0.50

        # Return the computed results
        return jsonify({
            'prelim': prelim,
            'total': total,
            'prelim_contribution': prelim_contribution,
            'required_midterm': required_midterm,
            'required_finals': required_finals,
            'chance_to_pass': required_midterm <= 100 and required_finals <= 100,
        })

    except ValueError:
        return jsonify({'error': 'Please enter valid numbers for Prelim and Total grades.'})


