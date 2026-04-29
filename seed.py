import os
from dotenv import load_dotenv
from supabase_client import get_supabase

load_dotenv()

def seed_db():
    supabase = get_supabase()
    
    print("Deleting existing data...")
    # This might fail if constraints are not cascading or tables are empty
    try:
        # Delete all plots (which cascades to plants)
        supabase.table('plots').delete().neq('id', 0).execute()
    except Exception as e:
        print("Delete error (safe to ignore if first run):", e)

    print("Generating 30 plots...")
    
    for p in range(1, 31):
        plot_name = f'Plot {p}'
        plot = supabase.table('plots').insert({'id': p, 'name': plot_name}).execute().data[0]
        
        print(f"Generating 900 plants for {plot_name}...")
        plants_data = []
        for r in range(1, 16):
            for c in range(1, 21):
                for v in ['A', 'B', 'C']:
                    plant_id = f"P{plot['id']}-R{r}-C{c}-{v}"
                    plants_data.append({
                        'id': plant_id,
                        'plot_id': plot['id'],
                        'row_num': r,
                        'col_num': c,
                        'vine_type': v
                    })
        
        # Insert 900 plants for this plot in one go
        supabase.table('plants').insert(plants_data).execute()
        
    print("Seed complete! 30 plots and 27,000 plants generated.")

if __name__ == '__main__':
    seed_db()
