import os
import django
from django.utils import timezone
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from cars.models import Car, CarImage, InspectionReport

def seed_db():
    print("Starting database seeding...")
    
    # 1. Create Test User
    test_user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
    if created:
        test_user.set_password('password123')
        test_user.first_name = 'Pratik'
        test_user.last_name = 'Kanzariya'
        test_user.save()
        profile = test_user.profile
        profile.phone_number = '9876543210'
        profile.city = 'Ahmedabad'
        profile.save()
        print("Test user 'testuser' with password 'password123' created!")
    else:
        print("Test user 'testuser' already exists.")

    # 1.1 Create Admin User
    admin_user, created = User.objects.get_or_create(username='admin', email='admin@example.com')
    if created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.first_name = 'CarBazaar'
        admin_user.last_name = 'Admin'
        admin_user.save()
        profile = admin_user.profile
        profile.phone_number = '9999999999'
        profile.city = 'Ahmedabad'
        profile.save()
        print("Admin user 'admin' with password 'admin123' created!")
    else:
        print("Admin user 'admin' already exists.")

    # Clear old cars to prevent duplicates on rerun
    Car.objects.all().delete()
    print("Cleared existing car data.")

    # 2. Car data definitions
    cars_data = [
        {
            "brand": "Hyundai",
            "model": "i20",
            "variant": "Asta (O) 1.2",
            "year": 2021,
            "price": 680000.00,
            "km_driven": 32500,
            "fuel_type": "Petrol",
            "transmission": "Manual",
            "body_type": "Hatchback",
            "owner_count": 1,
            "registration_state": "GJ-01",
            "city": "Ahmedabad",
            "location_hub": "Spinny Hub, Vastrapur Lake",
            "image_url": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=600&q=80",
            "mileage": 20.35,
            "engine_displacement": 1197,
            "max_power": "81.86 bhp @ 6000 rpm",
            "torque": "114.7 Nm @ 4200 rpm",
            "seats": 5,
            "gallery": [
                "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=600&q=80",
                "https://images.unsplash.com/photo-1616422285623-13ff0162193c?auto=format&fit=crop&w=600&q=80",
                "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=600&q=80"
            ],
            "inspection": {
                "overall_rating": 4.5,
                "engine_rating": 4.6,
                "exterior_rating": 4.3,
                "interior_rating": 4.7,
                "suspension_rating": 4.5,
                "brakes_rating": 4.4,
                "notes": "Perfect engine condition. Small minor scratch on the left rear door, professionally touched up. Air conditioning is working excellently."
            }
        },
        {
            "brand": "Honda",
            "model": "City",
            "variant": "ZX i-VTEC",
            "year": 2019,
            "price": 920000.00,
            "km_driven": 48000,
            "fuel_type": "Petrol",
            "transmission": "Automatic",
            "body_type": "Sedan",
            "owner_count": 1,
            "registration_state": "MH-02",
            "city": "Mumbai",
            "location_hub": "Spinny Hub, Malad West",
            "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=600&q=80",
            "mileage": 18.00,
            "engine_displacement": 1497,
            "max_power": "117.6 bhp @ 6600 rpm",
            "torque": "145 Nm @ 4600 rpm",
            "seats": 5,
            "gallery": [
                "https://images.unsplash.com/photo-1542282088-fe8426682b8f?auto=format&fit=crop&w=600&q=80",
                "https://images.unsplash.com/photo-1525609004556-c46c7d6cf0a3?auto=format&fit=crop&w=600&q=80"
            ],
            "inspection": {
                "overall_rating": 4.7,
                "engine_rating": 4.8,
                "exterior_rating": 4.6,
                "interior_rating": 4.8,
                "suspension_rating": 4.7,
                "brakes_rating": 4.6,
                "notes": "Single hand driven, fully loaded variant with sunroof. Clean interiors, high quality leather seats. Engine is silent and extremely smooth."
            }
        },
        {
            "brand": "Maruti Suzuki",
            "model": "Swift",
            "variant": "VXI",
            "year": 2020,
            "price": 540000.00,
            "km_driven": 22000,
            "fuel_type": "Petrol",
            "transmission": "Manual",
            "body_type": "Hatchback",
            "owner_count": 2,
            "registration_state": "GJ-01",
            "city": "Ahmedabad",
            "location_hub": "Spinny Hub, Vastrapur Lake",
            "image_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=600&q=80",
            "mileage": 22.00,
            "engine_displacement": 1197,
            "max_power": "88.5 bhp @ 6000 rpm",
            "torque": "113 Nm @ 4400 rpm",
            "seats": 5,
            "gallery": [
                "https://images.unsplash.com/photo-1619767886558-efdc259cde1a?auto=format&fit=crop&w=600&q=80"
            ],
            "inspection": {
                "overall_rating": 4.2,
                "engine_rating": 4.5,
                "exterior_rating": 3.9,
                "interior_rating": 4.1,
                "suspension_rating": 4.2,
                "brakes_rating": 4.3,
                "notes": "Highly economical vehicle. Suspension and clutch are in great shape. Tyres are at 70% life remaining. Minor paint touchups on bumpers."
            }
        },
        {
            "brand": "Tata",
            "model": "Nexon",
            "variant": "XM 1.2",
            "year": 2022,
            "price": 810000.00,
            "km_driven": 15000,
            "fuel_type": "CNG",
            "transmission": "Manual",
            "body_type": "SUV",
            "owner_count": 1,
            "registration_state": "DL-3C",
            "city": "Delhi",
            "location_hub": "Spinny Hub, Connaught Place",
            "image_url": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&w=600&q=80",
            "mileage": 24.50,
            "engine_displacement": 1199,
            "max_power": "84.8 bhp @ 6000 rpm",
            "torque": "95 Nm @ 3500 rpm",
            "seats": 5,
            "gallery": [
                "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=600&q=80"
            ],
            "inspection": {
                "overall_rating": 4.6,
                "engine_rating": 4.7,
                "exterior_rating": 4.5,
                "interior_rating": 4.6,
                "suspension_rating": 4.7,
                "brakes_rating": 4.5,
                "notes": "Excellent choice for daily commute. Factory fitted CNG. Still under manufacturer warranty. Zero dent history."
            }
        },
        {
            "brand": "Hyundai",
            "model": "Creta",
            "variant": "SX (O) 1.5",
            "year": 2021,
            "price": 1480000.00,
            "km_driven": 28000,
            "fuel_type": "Diesel",
            "transmission": "Automatic",
            "body_type": "SUV",
            "owner_count": 1,
            "registration_state": "GJ-01",
            "city": "Ahmedabad",
            "location_hub": "Spinny Hub, Vastrapur Lake",
            "image_url": "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?auto=format&fit=crop&w=600&q=80",
            "mileage": 18.00,
            "engine_displacement": 1493,
            "max_power": "113.4 bhp @ 4000 rpm",
            "torque": "250 Nm @ 1500 rpm",
            "seats": 5,
            "gallery": [
                "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=600&q=80"
            ],
            "inspection": {
                "overall_rating": 4.8,
                "engine_rating": 4.9,
                "exterior_rating": 4.7,
                "interior_rating": 4.9,
                "suspension_rating": 4.8,
                "brakes_rating": 4.7,
                "notes": "Top end variant with panoramic sunroof, ventilated front seats, and Bose speakers. Driven with care, like-new showroom condition."
            }
        },
        {
            "brand": "Toyota",
            "model": "Fortuner",
            "variant": "2.8 4x2",
            "year": 2020,
            "price": 2950000.00,
            "km_driven": 60000,
            "fuel_type": "Diesel",
            "transmission": "Automatic",
            "body_type": "Luxury",
            "owner_count": 1,
            "registration_state": "KA-51",
            "city": "Bangalore",
            "location_hub": "Spinny Hub, Indiranagar",
            "image_url": "https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?auto=format&fit=crop&w=600&q=80",
            "mileage": 14.20,
            "engine_displacement": 2755,
            "max_power": "201.1 bhp @ 3400 rpm",
            "torque": "500 Nm @ 1600 rpm",
            "seats": 7,
            "gallery": [
                "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=600&q=80"
            ],
            "inspection": {
                "overall_rating": 4.7,
                "engine_rating": 4.9,
                "exterior_rating": 4.6,
                "interior_rating": 4.6,
                "suspension_rating": 4.8,
                "brakes_rating": 4.8,
                "notes": "Immaculate rugged design. Engine torque is powerful and automatic transmission shifts beautifully. Fully serviced at authorized Toyota service center."
            }
        },
        {
            "brand": "Tesla",
            "model": "Model 3",
            "variant": "Standard Range",
            "year": 2022,
            "price": 3500000.00,
            "km_driven": 12000,
            "fuel_type": "Electric",
            "transmission": "Automatic",
            "body_type": "Luxury",
            "owner_count": 1,
            "registration_state": "MH-01",
            "city": "Mumbai",
            "location_hub": "Spinny Hub, Malad West",
            "image_url": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=600&q=80",
            "mileage": 350.00, # Range in km
            "engine_displacement": None,
            "max_power": "283 bhp",
            "torque": "450 Nm",
            "seats": 5,
            "gallery": [
                "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=600&q=80"
            ],
            "inspection": {
                "overall_rating": 4.9,
                "engine_rating": 5.0, # Motor/Battery
                "exterior_rating": 4.8,
                "interior_rating": 4.9,
                "suspension_rating": 4.8,
                "brakes_rating": 4.9,
                "notes": "Electric motor and battery health at 98%. Autonomous autopilot features active. Ultra premium minimalistic interior."
            }
        }
    ]

    # 3. Insert data
    for car_info in cars_data:
        gallery = car_info.pop('gallery')
        insp_info = car_info.pop('inspection')
        
        # Create Car
        car = Car.objects.create(**car_info)
        print(f"Created Car: {car}")
        
        # Create Gallery Images
        for g_url in gallery:
            CarImage.objects.create(car=car, image_url=g_url)
            
        # Create Inspection Report
        InspectionReport.objects.create(
            car=car,
            overall_rating=insp_info['overall_rating'],
            engine_rating=insp_info['engine_rating'],
            exterior_rating=insp_info['exterior_rating'],
            interior_rating=insp_info['interior_rating'],
            suspension_rating=insp_info['suspension_rating'],
            brakes_rating=insp_info['brakes_rating'],
            inspector_notes=insp_info['notes']
        )
        print(f"  Added inspection report & {len(gallery)} gallery images.")
        
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_db()
