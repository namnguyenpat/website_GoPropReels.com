
import os
import json

base_dir = r"d:\Dropbox\@Code _offical\New_skills\website_GoPropReels.com_new"
coupons_dir = os.path.join(base_dir, "src", "content", "coupons")
public_dir = os.path.join(base_dir, "public")

missing_logos = []
checked_logos = set()

for filename in os.listdir(coupons_dir):
    if filename.endswith(".json"):
        with open(os.path.join(coupons_dir, filename), "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                logo_path = data.get("firm_logo")
                firm_name = data.get("firm_name")
                
                if logo_path and logo_path not in checked_logos:
                    checked_logos.add(logo_path)
                    # Normalize path (remove leading slash)
                    actual_path = os.path.join(public_dir, logo_path.lstrip("/"))
                    if not os.path.exists(actual_path):
                        missing_logos.append({
                            "firm_name": firm_name,
                            "logo_path": logo_path
                        })
            except Exception as e:
                print(f"Error reading {filename}: {e}")

if missing_logos:
    print("MISSING_LOGOS_START")
    for item in missing_logos:
        print(f"{item['firm_name']}|{item['logo_path']}")
    print("MISSING_LOGOS_END")
else:
    print("NO_MISSING_LOGOS")
