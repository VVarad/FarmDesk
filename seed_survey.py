import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase_client import get_supabase

load_dotenv()

def seed_surveys():
    supabase = get_supabase()
    
    print("Fetching plants...")
    # Get all plants from the first 4 plots (4 * 900 = 3600 plants)
    response = supabase.table('plants').select('id, plot_id').in_('plot_id', [1, 2, 3, 4]).execute()
    plants = response.data
    
    if not plants:
        print("No plants found. Run seed.py first.")
        return

    print("Generating survey entries...")
    entries = []
    
    # Generate data for the past 3 months
    base_date = datetime.now() - timedelta(days=90)
    
    for plant in plants:
        # Each plant gets 3 entries over 3 months
        for m in range(3):
            survey_date = (base_date + timedelta(days=m*30)).strftime('%Y-%m-%d')
            # Add variation so different plots have distinctly different average heights
            plot_num = int(plant['plot_id'])
            # Plot 1 starts small and grows slow, Plot 4 starts high and grows fast
            base_height = 10 + (plot_num * 6)
            growth_rate = 5 + (plot_num * 3)
            
            height_in_inches = base_height + (m * growth_rate) + random.randint(0, 5)
            
            entries.append({
                'plant_id': plant['id'],
                'height_ft': height_in_inches // 12,
                'height_in': height_in_inches % 12,
                'fertilizer_qty': round(random.uniform(0.5, 2.0), 1) if random.random() > 0.5 else None,
                'fertilizer_type': random.choice(['NPK', 'Urea', 'Compost']) if random.random() > 0.5 else None,
                'disease_tags': [random.choice(['Leaf Spot', 'Root Rot', 'Pests'])] if random.random() > 0.8 else [],
                'notes': 'Looking good' if random.random() > 0.5 else None,
                'survey_date': survey_date
            })

    print(f"Inserting {len(entries)} survey entries...")
    for i in range(0, len(entries), 100):
        supabase.table('survey_entries').insert(entries[i:i+100]).execute()
        
    print("Survey data seeded!")

if __name__ == '__main__':
    seed_surveys()
