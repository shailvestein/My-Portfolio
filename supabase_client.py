from supabase import create_client, Client
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANNON_KEY = os.getenv('SUPABASE_ANNON_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANNON_KEY)
admin = {
  'username': 'shailvestein',
  'password': generate_password_hash(f"{os.getenv('ADMIN_PASSWORD')}")
}
try:
  response = supabase.table('users').select('*').eq('username', admin['username']).execute()
  if len(response.data) == 0:
    print('Creating admin user...')
    response = supabase.table('users').insert(admin).execute()
    print('Admin user created.')
except Exception as e:
  print(f'Connection failed.\nerror {e} occurred!')