from flask import Flask, render_template, request, redirect, flash
from s3_handler import list_buckets, create_bucket, delete_bucket, list_ec2_instances, upload_file

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    buckets = list_buckets()
    instances = list_ec2_instances()
    return render_template('index.html', buckets=buckets, instances=instances)

@app.route('/create_bucket', methods=['POST'])
def create():
    bucket_name = request.form.get('bucket_name','').strip()
    if bucket_name:
        try:
            create_bucket(bucket_name)
            flash(f"Bucket créé : {bucket_name}")
        except Exception as e:
            flash(f"Erreur création bucket : {str(e)}")
    return redirect('/')

@app.route('/delete_bucket/<bucket_name>')
def delete(bucket_name):
    try:
        delete_bucket(bucket_name)
        flash(f"Bucket supprimé : {bucket_name}")
    except Exception as e:
        flash(f"Erreur suppression bucket : {str(e)}")
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    bucket_name = request.form.get('bucket_select')
    file = request.files.get('file')
    if bucket_name and file:
        try:
            url = upload_file(bucket_name, file, file.filename)
            flash(f"Fichier uploadé : {file.filename} - URL publique: {url}")
        except Exception as e:
            flash(f"Erreur upload fichier : {str(e)}")
    else:
        flash("Bucket ou fichier manquant")
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
