# FarmDesk

A mobile-first, full-stack agricultural data entry application designed specifically for large-scale farm management. It tracks plant health, fertilizer usage, and disease distribution using a sleek dark-mode compatible UI and robust analytics.

## Tech Stack
- **Backend**: Python 3, Flask
- **Frontend**: HTMX, TailwindCSS, Plotly.js
- **Database**: Supabase (PostgreSQL)

## 🚀 Quick Setup (Local Development)

### 1. Database Setup
1. Create a free account at [Supabase](https://supabase.com/).
2. Start a new project and go to the **SQL Editor**.
3. Copy the contents of `schema.sql` and run it to create your tables.

### 2. Environment Variables
1. Clone this repository to your local machine.
2. Rename `.env.example` to `.env`.
3. Fill in your Supabase Project URL and Anon Key.
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key
```

### 3. Install & Initialize
Open your terminal in the project directory and run:

```bash
# Create a virtual environment (Optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize your farm with 30 plots and 27,000 plants
python seed.py
```

### 4. Run the App
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

## 📱 PWA Features
FarmDesk is a Progressive Web App (PWA). When accessed on a mobile device, you can use your browser's "Add to Home Screen" option to install it as a native-feeling app!

## 🌍 Deployment (Vercel)
This app is ready to deploy to Vercel instantly.
1. Create an account at [Vercel](https://vercel.com/) and link your GitHub.
2. Import this repository.
3. In the Vercel deployment settings, add your `SUPABASE_URL` and `SUPABASE_KEY` as Environment Variables.
4. Click **Deploy**. Vercel will automatically use the `vercel.json` configuration to serve the Flask app!
