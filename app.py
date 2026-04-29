from flask import Flask, render_template, request, redirect, url_for
from supabase_client import get_supabase
import os

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('survey_form'))

@app.route('/survey', methods=['GET'])
def survey_form():
    try:
        supabase = get_supabase()
        response = supabase.table('plots').select('id, name').order('id').execute()
        plots = response.data
    except Exception:
        plots = []
    return render_template('survey.html', plots=plots)

@app.route('/survey/options', methods=['GET'])
def survey_options():
    opt_type = request.args.get('type')
    plot_id = request.args.get('plot_id')
    if opt_type == 'row':
        return render_template('partials/survey_options.html', type='row', rows=list(range(1, 16)), plot_id=plot_id)
    elif opt_type == 'col':
        return render_template('partials/survey_options.html', type='col', cols=list(range(1, 21)))
    return ""

@app.route('/survey/bulk', methods=['POST'])
def save_survey_bulk():
    try:
        supabase = get_supabase()
        data = request.form
        
        plot_id = data.get('plot_id')
        row_num = data.get('row_num')
        
        if not plot_id or not row_num:
            return "Missing Plot or Row", 400
            
        height_ft = data.get('height_ft')
        height_in = data.get('height_in')
        fertilizer_qty = data.get('fertilizer_qty')
        fertilizer_type = data.get('fertilizer_type')
        
        # Generate 60 entries
        entries = []
        for c in range(1, 21):
            for v in ['A', 'B', 'C']:
                plant_id = f"P{plot_id}-R{row_num}-C{c}-{v}"
                entries.append({
                    'plant_id': plant_id,
                    'height_ft': int(height_ft) if height_ft else None,
                    'height_in': int(height_in) if height_in else None,
                    'fertilizer_qty': float(fertilizer_qty) if fertilizer_qty else None,
                    'fertilizer_type': fertilizer_type if fertilizer_type else None
                })
        
        supabase.table('survey_entries').insert(entries).execute()
        return f"<div class='bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mt-4'>Success! Updated 60 plants in Plot {plot_id}, Row {row_num}.</div>"
    except Exception as e:
        return f"<div class='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4'>Error: {str(e)}</div>", 500

@app.route('/survey/single', methods=['POST'])
def save_survey_single():
    try:
        supabase = get_supabase()
        data = request.form
        
        plot_id = data.get('plot_id')
        row_num = data.get('row_num')
        col_num = data.get('col_num')
        vine_type = data.get('vine_type')
        
        if not all([plot_id, row_num, col_num, vine_type]):
            return "Missing plant identifiers", 400
            
        plant_id = f"P{plot_id}-R{row_num}-C{col_num}-{vine_type}"
        disease_tags = request.form.getlist('disease_tags')
        notes = data.get('notes')
        
        entry = {
            'plant_id': plant_id,
            'disease_tags': disease_tags,
            'notes': notes
        }
        
        supabase.table('survey_entries').insert(entry).execute()
        return f"<div class='bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mt-4'>Success! Note saved for Plant {plant_id}.</div>"
    except Exception as e:
        return f"<div class='bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mt-4'>Error: {str(e)}</div>", 500

@app.route('/plants', methods=['GET'])
def plants_browser():
    return render_template('browser.html')

@app.route('/plants/search', methods=['GET'])
def plants_search():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return "<p class='text-sm text-gray-500 text-center'>Start typing to search (at least 2 characters)...</p>"
    
    try:
        supabase = get_supabase()
        # Search plants by ID
        response = supabase.table('plants').select('*, survey_entries(*)').ilike('id', f'%{q}%').limit(10).execute()
        plants = response.data
        # Sort survey entries by date descending for each plant
        for p in plants:
            if p.get('survey_entries'):
                p['survey_entries'] = sorted(p['survey_entries'], key=lambda x: x.get('survey_date', ''), reverse=True)
                
        return render_template('partials/plant_results.html', plants=plants)
    except Exception as e:
        return f"<p class='text-red-500 text-sm'>Error: {str(e)}</p>"

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')

@app.route('/api/analytics', methods=['GET'])
def api_analytics():
    try:
        supabase = get_supabase()
        # Chart 1: Average height per plot
        # Fetch all surveys (paginating because Supabase defaults to 1000 records)
        all_surveys = []
        for i in range(15): # Fetch up to 15,000 records
            resp = supabase.table('survey_entries').select('survey_date, height_ft, height_in, plants(plot_id)').range(i*1000, (i+1)*1000 - 1).execute()
            all_surveys.extend(resp.data)
            if len(resp.data) < 1000:
                break
                
        plot_heights = {}
        plot_time_heights = {}
        farm_time_heights = {}
        
        for s in all_surveys:
            if s.get('height_ft') is not None and s.get('plants'):
                plot_id = f"Plot {s['plants']['plot_id']}"
                total_inches = (s['height_ft'] * 12) + (s['height_in'] or 0)
                
                # Aggregate for Chart 1
                if plot_id not in plot_heights:
                    plot_heights[plot_id] = []
                plot_heights[plot_id].append(total_inches)
                
                # Aggregate for Chart 3
                date_str = s.get('survey_date')
                if date_str:
                    month = date_str[:7] # Group by YYYY-MM
                    
                    if plot_id not in plot_time_heights:
                        plot_time_heights[plot_id] = {}
                    if month not in plot_time_heights[plot_id]:
                        plot_time_heights[plot_id][month] = []
                    plot_time_heights[plot_id][month].append(total_inches)
                    
                    if month not in farm_time_heights:
                        farm_time_heights[month] = []
                    farm_time_heights[month].append(total_inches)
        
        # Calculate averages for Chart 1
        avg_heights = {k: sum(v)/len(v)/12 for k, v in plot_heights.items()}
        sorted_plots = sorted(avg_heights.keys(), key=lambda x: int(x.split(' ')[1]) if len(x.split(' ')) > 1 else x)
        
        chart1 = {
            'x': sorted_plots,
            'y': [avg_heights[p] for p in sorted_plots],
            'type': 'bar',
            'marker': {'color': '#22c55e'}
        }
        
        # Chart 2: Disease Distribution (Pie Chart)
        disease_resp = supabase.table('survey_entries').select('disease_tags').execute()
        disease_counts = {}
        for row in disease_resp.data:
            tags = row.get('disease_tags')
            if tags:
                for tag in tags:
                    disease_counts[tag] = disease_counts.get(tag, 0) + 1
                    
        labels = list(disease_counts.keys())
        values = list(disease_counts.values())
        
        if not labels:
            labels = ['Healthy', 'Diseased']
            values = [100, 0]
            
        chart2 = [{
            'labels': labels,
            'values': values,
            'type': 'pie',
            'hole': 0.4,
            'marker': {'colors': ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']}
        }]
        
        # Chart 3: Plot Averages vs Farm-wide
        chart3 = []
        if farm_time_heights:
            months = sorted(farm_time_heights.keys())
            
            for plot_id in sorted_plots:
                if plot_id in plot_time_heights:
                    y_vals = []
                    for m in months:
                        if m in plot_time_heights[plot_id]:
                            vals = plot_time_heights[plot_id][m]
                            y_vals.append(sum(vals)/len(vals)/12)
                        else:
                            y_vals.append(None)
                    
                    chart3.append({
                        'x': months,
                        'y': y_vals,
                        'type': 'scatter',
                        'mode': 'lines+markers',
                        'name': plot_id
                    })
                    
            farm_y = [sum(farm_time_heights[m])/len(farm_time_heights[m])/12 for m in months]
            chart3.append({
                'x': months,
                'y': farm_y,
                'type': 'scatter',
                'mode': 'lines+markers',
                'name': 'Farm Avg',
                'line': {'color': '#111827', 'width': 3}
            })
        
        return {'chart1': chart1, 'chart2': chart2, 'chart3': chart3}
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
