from database import SessionDep, get_session, init_db
from models import Medspa, Services
from repositories.appoitments import AppointmentsRepository

appointments_repository = AppointmentsRepository()


def seed_database(db: SessionDep):
    # Create and commit medspas first
    medspas = [
        Medspa(
            name="Serenity Wellness Spa",
            address="123 Madison Avenue, New York, NY 10016",
            phone_number="212-555-0123",
            email_address="info@serenitywellness.com",
        ),
        Medspa(
            name="Pure Aesthetics MedSpa",
            address="456 Beverly Drive, Los Angeles, CA 90210",
            phone_number="310-555-0456",
            email_address="contact@pureaesthetics.com",
        ),
    ]

    db.add_all(medspas)
    db.commit()

    # Now create services with the committed medspa IDs
    services = [
        Services(
            name="Botox Treatment",
            description="Neuromodulator treatment to reduce fine lines and wrinkles",
            price=450,
            duration=30,
            medspa_id=medspas[0].id,
        ),
        Services(
            name="Juvederm Ultra XC",
            description="Dermal filler for lip enhancement and wrinkle treatment",
            price=750,
            duration=45,
            medspa_id=medspas[1].id,
        ),
        Services(
            name="VI Peel",
            description="Medical-grade chemical peel for skin rejuvenation",
            price=300,
            duration=60,
            medspa_id=medspas[0].id,
        ),
        Services(
            name="Hydrafacial",
            description="Advanced facial treatment for deep cleansing and hydration",
            price=200,
            duration=60,
            medspa_id=medspas[1].id,
        ),
        Services(
            name="Kybella",
            description="Injectable treatment for reducing double chin",
            price=800,
            duration=45,
            medspa_id=medspas[0].id,
        ),
        Services(
            name="Sculptra",
            description="Poly-L Lactic Acid treatment for facial volume restoration",
            price=900,
            duration=60,
            medspa_id=medspas[1].id,
        ),
        Services(
            name="PDO Thread Lift",
            description="Non-surgical face lift using PDO threads",
            price=1200,
            duration=90,
            medspa_id=medspas[0].id,
        ),
        Services(
            name="Vitamin B12 Injection",
            description="Energy boosting vitamin injection",
            price=75,
            duration=15,
            medspa_id=medspas[1].id,
        ),
        Services(
            name="NAD+ IV Therapy",
            description="Intravenous therapy for cellular health and anti-aging",
            price=350,
            duration=60,
            medspa_id=medspas[0].id,
        ),
        Services(
            name="Dermaplaning",
            description="Physical exfoliation treatment for smooth, glowing skin",
            price=150,
            duration=45,
            medspa_id=medspas[1].id,
        ),
    ]

    db.add_all(services)
    db.commit()


if __name__ == "__main__":
    # Initialize the database tables
    init_db()

    # Get a session using the session factory
    session = next(get_session())
    try:
        seed_database(session)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()
