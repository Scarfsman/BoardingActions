from flask import Flask, render_template, request, jsonify
import BoardingActions
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    selected_Units = BoardingActions.getSelected()
    options = BoardingActions.detats
    selected = '0'
    tables = []
    return render_template('index.html', 
                           options=options, 
                           selected=selected, 
                           tables=tables, 
                           selected_Units = selected_Units)

@app.route('/get-tables', methods=['POST'])
def get_tables():
    selected = request.form.get('detachment')
    headers, dataTable, tables_html = BoardingActions.getTables(int(selected))
    selected_Units = zip(['Test'], [pd.DataFrame(columns=[['Unit Name'], ['Quantity'], ['Points']])])
    # Zip headers and tables into a single iterable
    tables = list(zip(headers, tables_html))
    
    # Render only the tables portion
    return render_template('tables_partial.html', tables=tables)

@app.route('/clear-selected', methods=['POST'])
def clear_tables():
    BoardingActions.clear_selections()
    return render_template('table.html', table_html = BoardingActions.getSelected())

@app.route('/update-selected', methods=['POST'])
def update_selected():
    unit_ID = request.form.get('unit_id')
    action = request.form.get('action')
    newCount, selected_Units = BoardingActions.update_selections(unit_ID, action)
    return jsonify({'newCount': int(newCount),
                    'table_html': selected_Units})
    #return render_template('table.html', table_html = selected_Units) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)