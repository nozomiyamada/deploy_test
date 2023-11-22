from flask import Flask, request, render_template
from pythainlp import word_tokenize
from gensim.models import KeyedVectors
MODEL_THAIRATH = KeyedVectors.load_word2vec_format('static/thairath_wv.bin', unicode_errors='ignore', binary=True)

## instantiate flask app
app = Flask(__name__,
    static_folder='static',
    template_folder='templates'
    ) 

### tokenization page ###
@app.route('/', methods=['GET', 'POST'])
def page_tokenization():
	if request.method == 'GET':
		return render_template('tokenization.html') ## rendering "tokenization.html"
	elif request.method == 'POST':
		text = request.form['input_text'] ## get text from form
		delimiter = request.form['delimiter'] ## get delimiter | space -
		if delimiter in ['|', '-']:
			tokens = delimiter.join(word_tokenize(text))
		elif delimiter == ' ':
			tokens = ' '.join(word_tokenize(text, keep_whitespace=False))
		return render_template('tokenization.html', original_text=text, tokens=tokens) 
	
### word embedding page ###
@app.route("/wv", methods=['GET', 'POST'])
def page_wv():
	if request.method == 'GET':
		return render_template('wv.html', result=None)
	elif request.method == 'POST': ## if POST, return list of (word, cossim)  
		text = request.form['input_text'] ## get text from form
		try:
			result = MODEL_THAIRATH.most_similar(positive=text, topn=10) ## list of (word, cos_sim)
			result = [(word, round(cossim, 3)) for word, cossim in result]  ## rounding
		except:
			result = [['NOT FOUND', '']]
		return render_template('wv.html', original_text=text, wv_result=result) 

if __name__ == "__main__":
    # debug=True -> reload automatically when update app.py
    app.run(host="0.0.0.0", port=8000, debug=True)