from supabase import create_client

url = "https://ltrrrknknhbzhsafgoiu.supabase.co"

key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx0cnJya25rbmhiemhzYWZnb2l1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg3ODc3MTEsImV4cCI6MjA5NDM2MzcxMX0.teazRAnf9ExYggvZx3ZTFR43ZaOGDoCcLs0ze7UrXQA"

# key = "sb_publishable_-_ptTGPrlYo5qY3W1sZekg_KzUhyEOc"


supabase = create_client(url, key)

data = supabase.table("profiles").select("*").limit(1).execute()
print
(data)
