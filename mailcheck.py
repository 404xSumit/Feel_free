app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        contacts = [
            (request.form['contact1_name'], request.form['contact1_phone']),
            (request.form['contact2_name'], request.form['contact2_phone']),
            (request.form['contact3_name'], request.form['contact3_phone'])
        ]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, age, phone, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (name, age, phone, email, password))
        mysql.connection.commit()
        user_id = cur.lastrowid

        for contact in contacts:
            cur.execute("INSERT INTO emergency_contacts (user_id, contact_name, contact_phone) VALUES (%s, %s, %s)",
                        (user_id, contact[0], contact[1]))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
    return render_template('signup.html')