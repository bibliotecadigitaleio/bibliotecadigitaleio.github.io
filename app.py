from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import datetime
from passver import PasswordVer

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Asistencia, Curso, Estudiante, Padre, Preceptor

@app.route('/',) #PAGINA DE INICIO
def usuario():
    return render_template('index.html')

@app.route('/menu') 
def bienvenida():
    return render_template('menu.html')

@app.route('/anpat') 
def anpat():
    return render_template('antpat.html')

@app.route('/biogca') 
def biogca():
    return render_template('biogca.html')

@app.route('/biogcb') 
def biogcb():
    return render_template('biogcb.html')

@app.route('/fecha')
def fecha():
    return render_template('fecha.html')

@app.route('/intodonto') 
def intodonto():
    return render_template('intodonto.html')

@app.route('/fundquima') 
def fundquima():
    return render_template('funquima.html')

@app.route('/fundquimb')
def fundquimb():
    return render_template('funquimb.html')

@app.route('/metod')
def metod():
    return render_template('metodologia.html')

@app.route('/consinformeprece',methods=["GET", "POST"])
def consinformeprece():
    if request.method == "POST":
        if request.form['cursoid']:
            asisaula=[]
            asisfis=[]
            inasisaulajus=[]
            inasisfisjus=[]
            inasisfisinjus=[]
            inasisaulainjus=[]
            inas=[]
            falta=0.0
            aula=0
            fis=0
            infisjus=0
            inaulajus=0
            infisinjus=0
            inaulainjus=0
            es=0
            cursos=Curso.query.filter_by(id=request.form['cursoid']).first()
            estudiantes=cursos.estudiante
            for i in range(len(estudiantes)):
                es+=1
                asis=estudiantes[i].asistencia_alum
                for b in range(len(estudiantes[i].asistencia_alum)):
                    if asis[b].codigoclase==1:
                        if asis[b].asistio == "s":
                            aula+=1
                        else:
                            if asis[b].justificacion != None:
                                falta+=1.0
                                inaulajus+=1
                            else:
                                falta+=1.0
                                inaulainjus+=1
                    else:
                        if asis[b].asistio == "s":
                            fis+=1
                        else:
                            if asis[b].justificacion != None:
                                falta+=0.5
                                infisjus+=1
                            else:
                                falta+=0.5
                                infisinjus+=1
                asisaula.append(aula)
                asisfis.append(fis)
                inasisaulajus.append(inaulajus)
                inasisfisjus.append(infisjus)
                inasisfisinjus.append(infisinjus)
                inasisaulainjus.append(inaulainjus)
                inas.append(falta)
                falta=0.0
                aula=0
                fis=0
                infisjus=0
                inaulajus=0
                infisinjus=0
                inaulainjus=0
            return render_template("consinformeprece.html", indice=es, est=cursos.estudiante, aulap=asisaula, fisp=asisfis, aulafj=inasisaulajus, fisfj=inasisfisjus, aulafi=inasisaulainjus, fisfi=inasisfisinjus, inasis=inas)
    else:
        return redirect(url_for('informeprece'))

@app.route("/asiscurso")
def curso():
    preceptor=Preceptor.query.filter_by(id=session["id"]).first()
    return render_template('curso.html', cursos=preceptor.cursos, r=range(len(preceptor.cursos)))

@app.route("/regasiscurso", methods=["GET", "POST"])
def regasis():
    if request.method == "POST":
        if request.form['cursoid']:
            curso=Curso.query.filter_by(id=request.form['cursoid']).first()
            session["asis"]=curso.id
            return render_template('regasis.html', estudiantes=curso.estudiante, r=range(len(curso.estudiante)))
    else:
        return redirect(url_for('asiscurso'))
    
@app.route('/asisreg', methods=['GET', 'POST'])
def asisreg():
    if request.method == "POST":
        curso=Curso.query.filter_by(id=session["asis"]).first()
        estudiantes=curso.estudiante
        for i in range(len(estudiantes)):
                codcl=request.form[f'tipo{i}']
                fech=request.form[f'fe{i}']
                asi=request.form[f'asis{i}']
                justi=request.form.get(f'justi{i}','')
                asistencia= Asistencia(fecha=fech,codigoclase=int(codcl),asistio=asi, justificacion=justi, idestudiante=estudiantes[i].id)
                db.session.add(asistencia)
        db.session.commit()
        flash('Asistencia cargada')
        return render_template('regasis.html', estudiantes=curso.estudiante, r=range(len(curso.estudiante)))
    else:
        return redirect(url_for('regasiscurso'))
    
if __name__ == '__main__': 
    app.run(debug = True)