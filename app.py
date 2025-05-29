from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.security import generate_password_hash, check_password_hash
from supabase_client import supabase

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    sections = {'project' : supabase.table('project').select('*').execute().data,
                'about' : supabase.table('about').select('*').execute().data,
                'contact' : supabase.table('contact').select('*').execute().data,
                'education' : supabase.table('education').select('*').order('id', desc=True).execute().data, # Education.query.order_by(Education.id.desc()).all(),
                'experience' : supabase.table('experience').select('*').order('id', desc=True).execute().data, # Experience.query.order_by(Experience.id.desc()).all(),
                'skill' : supabase.table('skill').select('*').order('id', desc=True).execute().data, # Skill.query.order_by(Skill.id.desc()).all()}
    }
    return render_template('home.html', sections=sections)


@app.route('/admin', methods=['GET', 'POST']) 
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(f"login page loaded!")
    if request.method == 'POST':
        print(f"login button clicked!")
        username = request.form['username']
        password = request.form['password']
        response = supabase.table('users').select('*').eq('username', username).execute()
        try:
            if response.data:
                user = response.data[0]
                if check_password_hash(user['password'], password):
                    session['username'] = username
                    session['admin'] = True
                    return redirect(url_for('admin'))
                else:
                    return render_template('login.html', error="Invalid password")
        except Exception as e:
            print(f"Error logging in: {e}")
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/add/<section>', methods=['GET', 'POST'])
def add(section):
    if request.method == 'POST':
        if section == 'project':
            title = request.form['project_title']
            description = request.form['project_description']
            from_date = request.form['from_date']  # e.g. '2023-01'
            to_date = request.form['to_date']      # e.g. '2023-12'
            accomplishments = request.form['accomplishments']
            new_project = {
                'title':title,
                'description':description,
                'from_date':from_date,
                'to_date':to_date,
                'accomplishments':accomplishments
            }
            try:
                supabase.table('project').insert(new_project).execute()
                print("Added project successfully!")
                return redirect(url_for('view', section='project'))
            except Exception as e:
                print(f"Error adding project: {e}")

        elif section == 'about':
            about_description = request.form['about_description']
            new_about = {'about':about_description}
            try:
                supabase.table('about').insert(new_about).execute()
                print("Added about successfully!")
                return redirect(url_for('view', section='about'))
            except Exception as e:
                print(f"Error adding about: {e}")

        elif section == 'skill':
            skill = request.form['skill']
            new_skill = {'skill':skill}
            try:
                supabase.table('skill').insert(new_skill).execute()
                print("Added skill successfully!")
                return redirect(url_for('view', section='skill'))
            except Exception as e:
                print(f"Error adding skill: {e}")

        elif section == 'education':
            degree = request.form['degree']
            university = request.form['university']
            field = request.form['field']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            percentage = float(request.form['percentage'])
            accomplishments = request.form['accomplishments']
            new_education = {
                'degree':degree,
                'university':university,
                'field':field,
                'from_date':from_date,
                'to_date':to_date,
                'percentage':percentage,
                'accomplishments':accomplishments
            }
            try:
                supabase.table('education').insert(new_education).execute()
                print("Added education successfully!")
                return redirect(url_for('view', section='education'))
            except Exception as e:
                print(f"Error adding education: {e}")

        elif section == 'experience':
            title = request.form['job_title']
            description = request.form['job_description']
            company = request.form['company_name']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            accomplishments = request.form['accomplishments']
            
            new_experience = {
                'title':title,
                'description':description,
                'company':company,
                'from_date':from_date,
                'to_date':to_date,
                'accomplishments':accomplishments
            }
            try:
                supabase.table('experience').insert(new_experience).execute()
                print("Added experience successfully!")
                return redirect(url_for('view', section='experience'))
            except Exception as e:
                print(f"Error adding experience: {e}")

        elif section == 'contact':
            phone = request.form['phone']
            email = request.form['email']
            new_contact = {'phone':phone, 'email':email}
            try:
                supabase.table('contact').insert(new_contact).execute()
                print("Added contact successfully!")
                return redirect(url_for('view', section='contact'))
            except Exception as e:
                print(f"Error adding contact: {e}")

    return render_template('add.html', section=section)


@app.route('/view/<section>', methods=['GET'])
def view(section):
    if section == 'project':
        projects = supabase.table('project').select('*').order('id', desc=True).execute().data 
        return render_template('view.html', section=section, section_view=projects)
    elif section == 'skill':
        skills = supabase.table('skill').select('*').order('id', desc=True).execute().data 
        return render_template('view.html', section=section, section_view=skills)
    elif section == 'education':
        educations = supabase.table('education').select('*').order('id', desc=True).execute().data
        return render_template('view.html', section=section, section_view=educations)
    elif section == 'experience':
        experiences = supabase.table('experience').select('*').order('id', desc=True).execute().data 
        return render_template('view.html', section=section, section_view=experiences)
    elif section == 'about':
        abouts = supabase.table('about').select('*').order('id', desc=True).execute().data 
        return render_template('view.html', section=section, section_view=abouts)
    elif section == 'contact':
        contacts = supabase.table('contact').select('*').order('id', desc=True).execute().data 
        return render_template('view.html', section=section, section_view=contacts)
    else:
        return render_template('view.html', section=section)


@app.route('/edit/<section>/<id>', methods=['GET', 'POST'])
def edit(section, id):
    if section == 'skill':
        skill = supabase.table('skill').select('*').eq('id', id).execute().data[0]
        if request.method == 'POST' and section == 'skill':
            skill['skill'] = request.form['skill']
            supabase.table('skill').update(skill).eq('id', id).execute()
            print("Updated skill successfully!")
            return redirect(url_for('view', section='skill'))
        if skill:
          return render_template('edit.html', section=section, section_view=skill)
    elif section == 'project':
        project = supabase.table('project').select('*').eq('id', id).execute().data[0] 
        if request.method == 'POST' and section == 'project':
            project['title'] = request.form['title']
            project['from_date'] = request.form['from_date']
            project['to_date'] = request.form['to_date']
            project['description'] = request.form['description']
            project['accomplishments'] = request.form['accomplishments']
            supabase.table('project').update(project).eq('id', id).execute()
            print("Updated project successfully!")
            return redirect(url_for('view', section='project'))
        if project:
          return render_template('edit.html', section=section, section_view=project)
    elif section == 'education':
        education = supabase.table('education').select('*').eq('id', id).execute().data[0]
        if request.method == 'POST' and section == 'education':
            education['degree'] = request.form['degree']
            education['university'] = request.form['university']
            education['field'] = request.form['field']
            education['from_date'] = request.form['from_date']
            education['to_date'] = request.form['to_date']
            education['percentage'] = float(request.form['percentage'])
            supabase.table('education').update(education).eq('id', id).execute()
            return redirect(url_for('view', section='education'))
        if education:
          return render_template('edit.html', section=section, section_view=education)
    elif section == 'experience':
        experience = supabase.table('experience').select('*').eq('id', id).execute().data[0]
        if request.method == 'POST' and section == 'experience':
            experience['title'] = request.form['job_title']
            experience['description'] = request.form['job_description']
            experience['company'] = request.form['company_name']
            experience['from_date'] = request.form['from_date']
            experience['to_date'] = request.form['to_date']
            experience['accomplishments'] = request.form['accomplishments']
            supabase.table('experience').update(experience).eq('id', id).execute()
            return redirect(url_for('view', section='experience'))
        if experience:
          return render_template('edit.html', section=section, section_view=experience)
    elif section == 'about':
        about = supabase.table('about').select('*').eq('id', id).execute().data[0]
        if request.method == 'POST' and section == 'about':
            about['about'] = request.form['about']
            supabase.table('about').update(about).eq('id', id).execute()
            return redirect(url_for('view', section='about'))
        if about:
          return render_template('edit.html', section=section, section_view=about)
    elif section == 'contact':
        contact = supabase.table('contact').select('*').eq('id', id).execute().data[0]
        if request.method == 'POST' and section == 'contact':
            contact['phone'] = request.form['phone']
            contact['email'] = request.form['email']
            supabase.table('contact').update(contact).eq('id', id).execute()
            return redirect(url_for('view', section='contact'))
        if contact:
          return render_template('edit.html', section=section, section_view=contact)
    return render_template('admin.html')
        

@app.route('/delete/<section>/<id>', methods=['GET', 'POST'])
def delete(section, id):
    if section == 'skill':
        supabase.table('skill').delete().eq('id', id).execute()
        return redirect(url_for('view', section='skill'))
    elif section == 'project':
        supabase.table('project').delete().eq('id', id).execute()
        return redirect(url_for('view', section='project'))
    elif section == 'education':
        supabase.table('education').delete().eq('id', id).execute()
        return redirect(url_for('view', section='education'))
    elif section == 'experience':
        supabase.table('experience').delete().eq('id', id).execute()
        return redirect(url_for('view', section='experience'))
    elif section == 'about':
        supabase.table('about').delete().eq('id', id).execute()
        return redirect(url_for('view', section='about'))
    elif section == 'contact':
        supabase.table('contact').delete().eq('id', id).execute()
        return redirect(url_for('view', section='contact'))
    return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run()
